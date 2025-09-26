from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
import threading
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path
from typing import Dict, IO, List, Optional


@dataclass
class RunRecord:
    run_id: str
    mode: str
    command: List[str]
    log_path: Path
    start_time: datetime
    process: Optional[subprocess.Popen] = field(default=None, repr=False)
    log_handle: Optional[IO[str]] = field(default=None, repr=False)
    status: str = "running"
    return_code: Optional[int] = None
    output_dir: Optional[Path] = None

    def to_status(self) -> Dict[str, object]:
        return {
            "run_id": self.run_id,
            "mode": self.mode,
            "status": self.status,
            "return_code": self.return_code,
            "log_path": str(self.log_path),
            "output_dir": str(self.output_dir) if self.output_dir else None,
            "started_at": self.start_time.isoformat(),
            "command": self.command,
        }


class RunManager:
    """Coordinates pipeline executions and exposes summary helpers."""

    def __init__(self, project_root: Path) -> None:
        self.project_root = project_root
        self.runs_dir = project_root / "ui_service" / "runs"
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        self._runs: Dict[str, RunRecord] = {}
        self._lock = threading.Lock()

    def list_runs(self) -> List[RunRecord]:
        with self._lock:
            return list(self._runs.values())

    def get(self, run_id: str) -> RunRecord:
        with self._lock:
            if run_id not in self._runs:
                raise KeyError(f"Unknown run_id: {run_id}")
            return self._runs[run_id]

    def start_run(self, endpoints_text: str, mode: str = "batch-agent") -> RunRecord:
        normalized_mode = mode if mode else "batch-agent"

        with self._lock:
            if any(rec.status == "running" for rec in self._runs.values()):
                raise RuntimeError("Another run is currently in progress. Please wait for it to finish before starting a new one.")

        endpoints = self._sanitize_endpoints(endpoints_text)
        if not endpoints:
            raise ValueError("No valid search IDs provided.")

        run_id = self._build_run_id(endpoints)
        run_dir = self.runs_dir / run_id
        run_dir.mkdir(parents=True, exist_ok=True)

        self._write_endpoints(endpoints, run_dir)

        log_path = run_dir / "pipeline.log"
        log_handle = open(log_path, "w", encoding="utf-8", buffering=1)

        command = [sys.executable, "RUN_FULL_PIPELINE.py", "--mode", normalized_mode]

        process = subprocess.Popen(
            command,
            cwd=str(self.project_root),
            stdout=log_handle,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
        )

        record = RunRecord(
            run_id=run_id,
            mode=normalized_mode,
            command=command,
            log_path=log_path,
            start_time=datetime.utcnow(),
            process=process,
            log_handle=log_handle,
        )

        with self._lock:
            self._runs[run_id] = record

        monitor_thread = threading.Thread(target=self._monitor_process, args=(run_id,), daemon=True)
        monitor_thread.start()

        return record

    def read_log(self, run_id: str, offset: int = 0, limit: int = 16_384) -> Dict[str, object]:
        record = self.get(run_id)
        log_path = record.log_path
        if not log_path.exists():
            return {"text": "", "offset": 0, "complete": record.status != "running"}

        with open(log_path, "r", encoding="utf-8", errors="replace") as handle:
            handle.seek(offset)
            chunk = handle.read(limit)
            new_offset = handle.tell()
        complete = record.status != "running" and record.return_code is not None and new_offset >= log_path.stat().st_size
        return {"text": chunk, "offset": new_offset, "complete": complete}

    def load_summary(
        self,
        run_id: str,
        decision_filter: Optional[str] = None,
        offset: int = 0,
        limit: Optional[int] = None,
    ) -> Dict[str, object]:
        record = self.get(run_id)
        output_dir = self._ensure_output_dir(record)
        if not output_dir:
            raise FileNotFoundError("Pipeline output directory not detected yet. Try again once the run completes.")

        data_json = output_dir / "data.json"
        if not data_json.exists():
            raise FileNotFoundError(f"Run output is missing data.json at {data_json}")

        data = json.loads(data_json.read_text(encoding="utf-8"))
        assessments = data.get("assessments", [])

        decision_normalized: Optional[str] = None
        if decision_filter:
            upper = decision_filter.upper()
            if upper in {"GO", "NO-GO", "INDETERMINATE"}:
                decision_normalized = upper

        if decision_normalized:
            filtered = [a for a in assessments if a.get("final_decision", "").upper() == decision_normalized]
        else:
            filtered = assessments

        total_count = len(filtered)
        if limit is not None and limit >= 0:
            slice_start = max(offset, 0)
            slice_end = slice_start + limit
            sliced = filtered[slice_start:slice_end]
        else:
            sliced = filtered
            slice_start = 0
            limit = len(sliced)

        files = self._collect_files(output_dir)
        full_report = self._read_optional(output_dir / "mistral_full_reports.md")

        return {
            "run_id": run_id,
            "status": record.status,
            "return_code": record.return_code,
            "output_dir": str(output_dir.relative_to(self.project_root)),
            "metadata": data.get("metadata", {}),
            "summary": data.get("summary", {}),
            "assessments": sliced,
            "assessments_total": total_count,
            "offset": slice_start,
            "limit": limit,
            "files": files,
            "full_report_markdown": full_report,
        }

    def _sanitize_endpoints(self, endpoints_text: str) -> List[str]:
        seen = set()
        result: List[str] = []
        for line in endpoints_text.splitlines():
            stripped = line.strip()
            if not stripped or stripped.startswith("#"):
                continue
            if stripped not in seen:
                seen.add(stripped)
                result.append(stripped)
        return result

    def _build_run_id(self, endpoints: List[str]) -> str:
        now = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        slug_source = endpoints[0] if endpoints else "run"
        slug = hashlib.sha256(slug_source.encode("utf-8")).hexdigest()[:6]
        return f"{now}_{slug}"

    def _write_endpoints(self, endpoints: List[str], run_dir: Path) -> None:
        content = "\n".join(endpoints) + "\n"
        (run_dir / "endpoints.txt").write_text(content, encoding="utf-8")
        target = self.project_root / "endpoints.txt"
        backup = run_dir / "endpoints.previous"
        if target.exists():
            backup.write_text(target.read_text(encoding="utf-8"), encoding="utf-8")
        target.write_text(content, encoding="utf-8")

    def _monitor_process(self, run_id: str) -> None:
        try:
            record = self.get(run_id)
        except KeyError:
            return

        proc = record.process
        if not proc:
            return

        return_code = proc.wait()
        if record.log_handle:
            record.log_handle.flush()
            record.log_handle.close()
            record.log_handle = None

        output_dir = self._detect_output_dir(record)
        status = "completed" if return_code == 0 else "failed"

        with self._lock:
            record.return_code = return_code
            record.status = status
            record.output_dir = output_dir

    def _detect_output_dir(self, record: RunRecord) -> Optional[Path]:
        log_path = record.log_path
        if log_path.exists():
            text = log_path.read_text(encoding="utf-8", errors="replace")
            for marker in ("Final results saved to:", "Output:"):
                if marker in text:
                    line = text.split(marker, 1)[1].strip().splitlines()[0]
                    candidate = line.strip()
                    path = (Path(candidate) if os.path.isabs(candidate) else (self.project_root / candidate)).resolve()
                    if path.exists():
                        return path
        return self._find_recent_output_dir(record.start_time)

    def _find_recent_output_dir(self, since: datetime) -> Optional[Path]:
        output_root = self.project_root / "SOS_Output"
        if not output_root.exists():
            return None
        newest: Optional[Path] = None
        newest_time: Optional[float] = None
        for run_dir in output_root.rglob("Run_*"):
            if not run_dir.is_dir():
                continue
            mtime = run_dir.stat().st_mtime
            if datetime.utcfromtimestamp(mtime) >= since:
                if newest_time is None or mtime > newest_time:
                    newest = run_dir
                    newest_time = mtime
        return newest

    def _ensure_output_dir(self, record: RunRecord) -> Optional[Path]:
        if record.output_dir and record.output_dir.exists():
            return record.output_dir
        detected = self._detect_output_dir(record)
        if detected and detected.exists():
            with self._lock:
                record.output_dir = detected
            return detected
        return None

    def _collect_files(self, output_dir: Path) -> List[Dict[str, str]]:
        files: List[Dict[str, str]] = []
        for name, label in [
            ("assessment.csv", "Assessment CSV"),
            ("report.md", "Summary Report"),
            ("mistral_full_reports.md", "Full Model Reports"),
            ("GO_opportunities.csv", "GO Opportunities CSV"),
            ("data.json", "Raw JSON"),
        ]:
            path = output_dir / name
            if path.exists():
                files.append({
                    "label": label,
                    "relative_path": str(path.relative_to(self.project_root)),
                    "size_bytes": path.stat().st_size,
                })
        return files

    def _read_optional(self, path: Path) -> Optional[str]:
        if path.exists():
            return path.read_text(encoding="utf-8", errors="replace")
        return None
