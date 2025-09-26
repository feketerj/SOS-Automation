#!/usr/bin/env python3
"""Streamlit control panel for the SOS pipeline."""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import List

import streamlit as st
import pandas as pd
import json

try:
    from config.loader import get_config  # type: ignore
except Exception:  # pragma: no cover
    get_config = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]
PYTHON = sys.executable


def _load_config() -> dict:
    if get_config is None:
        return {}
    try:
        return get_config()
    except Exception:
        return {}


def _endpoints_path(cfg: dict) -> Path:
    location = cfg.get("pipeline.endpoints_file") or "endpoints.txt"
    return (ROOT / location).resolve()


def _read_endpoints(path: Path) -> List[str]:
    # First try the specified file
    if path.exists():
        endpoints: List[str] = []
        for line in path.read_text(encoding="utf-8").splitlines():
            entry = line.strip()
            if entry and not entry.startswith('#'):
                endpoints.append(entry)
        if endpoints:
            return endpoints

    # If no endpoints.txt or it's empty, try demo endpoints for easy demos
    demo_path = ROOT / "demo_endpoints.txt"
    if demo_path.exists():
        demo_endpoints: List[str] = []
        for line in demo_path.read_text(encoding="utf-8").splitlines():
            entry = line.strip()
            if entry and not entry.startswith('#'):
                demo_endpoints.append(entry)
        return demo_endpoints

    return []


def _write_endpoints(path: Path, endpoints: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    unique = sorted(dict.fromkeys(endpoint.strip() for endpoint in endpoints if endpoint.strip()))
    path.write_text("\n".join(unique) + ("\n" if unique else ""), encoding="utf-8")


def _latest_output_dir(root: Path) -> Path | None:
    output_root = root / "SOS_Output"
    if not output_root.exists():
        return None
    candidates = []
    for month_dir in output_root.iterdir():
        if not month_dir.is_dir():
            continue
        for run_dir in month_dir.iterdir():
            if run_dir.is_dir():
                candidates.append(run_dir)
    if not candidates:
        return None
    return max(candidates, key=lambda p: p.stat().st_mtime)


def _run_pipeline(validate_smoke: bool, temp_endpoints: List[str] | None = None) -> tuple[int, str]:
    # If temp_endpoints provided, temporarily write them to endpoints.txt
    endpoints_file = ROOT / "endpoints.txt"

    if temp_endpoints:
        # Save current endpoints.txt content if exists
        backup_content = None
        if endpoints_file.exists():
            backup_content = endpoints_file.read_text()

        # Write temporary endpoints
        _write_endpoints(endpoints_file, temp_endpoints)

    cmd = [PYTHON, "tools/run_pipeline.py"]
    if validate_smoke:
        cmd.append("--validate-smoke")

    env = os.environ.copy()
    env.setdefault("PYTHONIOENCODING", "utf-8")

    result = subprocess.run(
        cmd,
        cwd=str(ROOT),
        env=env,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
    )

    # Restore original endpoints.txt if we modified it
    if temp_endpoints and backup_content is not None:
        endpoints_file.write_text(backup_content)

    return result.returncode, result.stdout


def main() -> None:
    st.set_page_config(page_title="SOS Pipeline", layout="wide")
    st.title("SOS Assessment Pipeline")
    st.write("Manage endpoints and run the entire pipeline from one screen.")

    cfg = _load_config()
    endpoints_file = _endpoints_path(cfg)

    # Initialize session state for endpoints if not exists
    if "session_endpoints" not in st.session_state:
        # Load from file initially but work with session state
        st.session_state["session_endpoints"] = _read_endpoints(endpoints_file)
        # Track if we're using demo endpoints
        st.session_state["using_demo"] = not endpoints_file.exists() or not _read_endpoints(endpoints_file)

    # Initialize session state for results
    if "session_results" not in st.session_state:
        st.session_state["session_results"] = None

    if "results_endpoints" not in st.session_state:
        st.session_state["results_endpoints"] = None

    # Use session endpoints instead of file
    endpoints = st.session_state["session_endpoints"]

    col1, col2 = st.columns([2, 1])
    with col1:
        st.subheader("Session Endpoints")
        if st.session_state.get("using_demo"):
            st.info("📋 **Demo Mode**: Using sample endpoints for demonstration. You can replace these with your actual search IDs.")
        else:
            st.caption("These endpoints are temporary and only for this session")
        if endpoints:
            st.write("Current HigherGov search IDs:")
            st.table({"#": list(range(1, len(endpoints) + 1)), "Search ID": endpoints})
        else:
            st.info("No endpoints defined yet. Add at least one search ID before running the pipeline.")

        # Simple text area for entering multiple endpoints
        st.write("### Add/Edit Endpoints")
        endpoint_text = st.text_area(
            "Enter search IDs (one per line):",
            value="\n".join(endpoints) if endpoints else "",
            height=150,
            help="Enter one HigherGov search ID per line. These are temporary for this session only."
        )

        col1_1, col1_2, col1_3 = st.columns(3)
        with col1_1:
            if st.button("Update Endpoints", type="primary"):
                # Parse the text area and update session endpoints
                new_endpoints = [line.strip() for line in endpoint_text.split("\n") if line.strip()]
                st.session_state["session_endpoints"] = new_endpoints
                # Clear results when endpoints change
                if st.session_state["results_endpoints"] != new_endpoints:
                    st.session_state["session_results"] = None
                    st.session_state["results_endpoints"] = None
                st.success(f"Updated to {len(new_endpoints)} endpoint(s)")
                st.rerun()

        with col1_2:
            if st.button("Clear All", type="secondary"):
                st.session_state["session_endpoints"] = []
                st.rerun()

        with col1_3:
            if st.button("Load from File"):
                # Reload from endpoints.txt
                st.session_state["session_endpoints"] = _read_endpoints(endpoints_file)
                st.info(f"Loaded {len(st.session_state['session_endpoints'])} endpoint(s) from file")
                st.rerun()

    with col2:
        st.subheader("Run Pipeline")
        validate_smoke = st.checkbox("Run preflight smoke tests", value=True)
        st.caption("Preflight runs the smoke + single batch checks before the full pipeline.")

        if "last_run_log" not in st.session_state:
            st.session_state["last_run_log"] = ""
            st.session_state["last_run_code"] = None
            st.session_state["last_run_time"] = None

        run_disabled = len(endpoints) == 0
        run_button = st.button("Run Pipeline", type="primary", disabled=run_disabled)

        if run_button:
            if run_disabled:
                st.warning("Add at least one endpoint before running the pipeline.")
            else:
                with st.spinner("Running pipeline. This may take several minutes..."):
                    # Pass session endpoints to the pipeline
                    code, output = _run_pipeline(validate_smoke, temp_endpoints=endpoints)
                st.session_state["last_run_log"] = output
                st.session_state["last_run_code"] = code
                st.session_state["last_run_time"] = datetime.now()
                # Mark that results are for current endpoints
                st.session_state["results_endpoints"] = endpoints.copy()
                # Trigger results refresh
                st.session_state["session_results"] = "pending"
                st.success("Pipeline run finished successfully." if code == 0 else "Pipeline run completed with errors.")

        if st.session_state["last_run_log"]:
            status = st.session_state["last_run_code"]
            timestamp = st.session_state["last_run_time"]
            log = st.session_state["last_run_log"]

            # Check for specific errors in the log
            if "AUTHENTICATION FAILED - HIGHERGOV API KEY IS INVALID OR EXPIRED" in log:
                st.error("⚠️ HIGHERGOV API KEY IS INVALID OR EXPIRED")
                st.error("The pipeline cannot fetch real opportunities. The API key needs to be updated.")
                st.info("Results shown are placeholder/test data only.")
            elif status == 0:
                st.success(f"Last run succeeded at {timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'unknown time'}.")
            else:
                st.error(f"Last run failed (exit code {status}) at {timestamp.strftime('%Y-%m-%d %H:%M:%S') if timestamp else 'unknown time'}.")

            st.download_button("Download Run Log", st.session_state["last_run_log"], file_name="pipeline_run.log")

    st.subheader("Assessment Results")

    # Add clear results button
    col_res1, col_res2 = st.columns([3, 1])
    with col_res2:
        if st.button("Clear Results", type="secondary"):
            st.session_state["session_results"] = None
            st.session_state["results_endpoints"] = None
            st.rerun()

    # Check if results match current endpoints
    if st.session_state["results_endpoints"] != endpoints:
        st.info("No results for current endpoints. Run the pipeline to see results.")
        return

    latest_dir = _latest_output_dir(ROOT)
    if latest_dir and st.session_state.get("session_results") is not None:
        st.write(f"Most recent output folder: `{latest_dir}`")

        # Look for assessment CSV file
        csv_files = list(latest_dir.glob("assessment.csv"))
        if csv_files:
            csv_file = csv_files[0]
            try:
                df = pd.read_csv(csv_file)

                # Display summary metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Total Assessments", len(df))
                with col2:
                    go_count = len(df[df['result'] == 'GO']) if 'result' in df.columns else 0
                    st.metric("GO", go_count)
                with col3:
                    no_go_count = len(df[df['result'] == 'NO-GO']) if 'result' in df.columns else 0
                    st.metric("NO-GO", no_go_count)
                with col4:
                    indeterminate_count = len(df[df['result'] == 'INDETERMINATE']) if 'result' in df.columns else 0
                    st.metric("INDETERMINATE", indeterminate_count)

                # Display the results table
                st.write("### Detailed Assessment Results")

                # Add filter options
                with st.expander("Filter Results"):
                    result_filter = st.multiselect("Filter by Result", options=['GO', 'NO-GO', 'INDETERMINATE'], default=None)
                    if result_filter and 'result' in df.columns:
                        df = df[df['result'].isin(result_filter)]

                # Show full details for each assessment
                for idx, row in df.iterrows():
                    with st.expander(f"{row.get('solicitation_title', 'Unknown Title')} - **{row.get('result', 'UNKNOWN')}**"):
                        col1, col2 = st.columns([1, 2])

                        with col1:
                            st.write("**Basic Info:**")
                            st.write(f"- ID: {row.get('solicitation_id', 'N/A')}")
                            st.write(f"- Agency: {row.get('agency', 'N/A')}")
                            st.write(f"- Result: **{row.get('result', 'N/A')}**")
                            st.write(f"- Pipeline Stage: {row.get('pipeline_stage', 'N/A')}")

                            # Show URLs
                            if row.get('sam_url') or row.get('hg_url'):
                                st.write("**Links:**")
                                if row.get('sam_url'):
                                    st.write(f"- [SAM.gov Link]({row['sam_url']})")
                                if row.get('hg_url'):
                                    st.write(f"- [HigherGov Link]({row['hg_url']})")

                        with col2:
                            st.write("**Decision Details:**")
                            if row.get('knock_out_reasons'):
                                st.write("**Knock-out Reasons:**")
                                if isinstance(row['knock_out_reasons'], list):
                                    for reason in row['knock_out_reasons']:
                                        st.write(f"  • {reason}")
                                else:
                                    st.write(f"  • {row['knock_out_reasons']}")

                            if row.get('rationale'):
                                st.write("**Rationale:**")
                                st.write(row['rationale'])

                            if row.get('exceptions'):
                                st.write("**Exceptions:**")
                                st.write(row['exceptions'])

                            if row.get('recommendation'):
                                st.write("**Recommendation:**")
                                st.write(row['recommendation'])

                        # Add full agent report section with copy button
                        if row.get('full_model_response') or row.get('detailed_analysis') or row.get('analysis_notes'):
                            st.write("---")
                            st.write("### 📋 Full Agent Report")

                            # Combine all available report fields
                            full_report = []

                            # Add title and basic info
                            full_report.append(f"ASSESSMENT REPORT")
                            full_report.append(f"=" * 50)
                            full_report.append(f"Title: {row.get('solicitation_title', 'N/A')}")
                            full_report.append(f"ID: {row.get('solicitation_id', 'N/A')}")
                            full_report.append(f"Agency: {row.get('agency', 'N/A')}")
                            full_report.append(f"Decision: {row.get('result', 'N/A')}")
                            full_report.append(f"=" * 50)
                            full_report.append("")

                            # Add the full analysis
                            if row.get('detailed_analysis'):
                                full_report.append("DETAILED ANALYSIS:")
                                full_report.append(row['detailed_analysis'])
                                full_report.append("")

                            if row.get('analysis_notes'):
                                full_report.append("ANALYSIS NOTES:")
                                full_report.append(row['analysis_notes'])
                                full_report.append("")

                            if row.get('full_model_response'):
                                full_report.append("FULL MODEL RESPONSE:")
                                full_report.append(row['full_model_response'])
                                full_report.append("")

                            if row.get('rationale'):
                                full_report.append("RATIONALE:")
                                full_report.append(row['rationale'])
                                full_report.append("")

                            if row.get('knock_out_reasons'):
                                full_report.append("KNOCK-OUT REASONS:")
                                if isinstance(row['knock_out_reasons'], list):
                                    for reason in row['knock_out_reasons']:
                                        full_report.append(f"  • {reason}")
                                else:
                                    full_report.append(f"  • {row['knock_out_reasons']}")
                                full_report.append("")

                            report_text = "\n".join(full_report)

                            # Display in a text area for easy copying
                            st.text_area(
                                "Full Report (click to select all, then Ctrl+C to copy):",
                                value=report_text,
                                height=300,
                                key=f"report_{idx}"
                            )

                            # Also add a copy button
                            st.code(report_text, language=None)

                # Download button for full CSV
                csv_data = df.to_csv(index=False)
                st.download_button(
                    label="Download Full Results CSV",
                    data=csv_data,
                    file_name="assessment_results.csv",
                    mime="text/csv"
                )

            except Exception as e:
                st.error(f"Error loading results: {str(e)}")
                # Fall back to listing files
                report_files = list(latest_dir.glob("*.md")) + list(latest_dir.glob("*.txt")) + list(latest_dir.glob("*.csv"))
                if report_files:
                    st.write("Available files:")
                    for file in sorted(report_files):
                        st.write(f"- `{file}`")
        else:
            # No CSV found, list available files
            report_files = list(latest_dir.glob("*.md")) + list(latest_dir.glob("*.txt")) + list(latest_dir.glob("*.csv")) + list(latest_dir.glob("*.json"))
            if report_files:
                st.write("Available files:")
                for file in sorted(report_files):
                    st.write(f"- `{file}`")

                # Try to load and display JSON if available
                json_files = list(latest_dir.glob("data.json"))
                if json_files:
                    try:
                        with open(json_files[0], 'r') as f:
                            data = json.load(f)

                        st.write("### Assessment Summary")
                        if isinstance(data, list):
                            st.write(f"Total assessments: {len(data)}")
                            # Convert to dataframe for display
                            df = pd.DataFrame(data)
                            if 'result' in df.columns:
                                result_counts = df['result'].value_counts()
                                col1, col2, col3 = st.columns(3)
                                with col1:
                                    st.metric("GO", result_counts.get('GO', 0))
                                with col2:
                                    st.metric("NO-GO", result_counts.get('NO-GO', 0))
                                with col3:
                                    st.metric("INDETERMINATE", result_counts.get('INDETERMINATE', 0))

                            # Display key columns
                            display_cols = ['solicitation_id', 'solicitation_title', 'result', 'agency']
                            available_cols = [col for col in display_cols if col in df.columns]
                            if available_cols:
                                st.dataframe(df[available_cols], width='stretch', height=400)
                    except Exception as e:
                        st.write(f"Could not parse JSON: {str(e)}")
            else:
                st.write("Folder created but no summary files found yet.")
    else:
        st.info("No pipeline outputs found yet. Run the pipeline to generate results.")

    st.caption("Run `python -m streamlit run ui_service/app.py` to launch this interface.")


if __name__ == "__main__":
    main()
