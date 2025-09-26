#!/usr/bin/env python3
"""
Endpoints manager: list, add, remove HigherGov search IDs.
Defaults to the pipeline endpoints file defined in config/settings.json.
"""

import argparse
from pathlib import Path
from typing import List

try:
    from config.loader import get_config  # type: ignore
except Exception:  # pragma: no cover
    get_config = None  # type: ignore

ROOT = Path(__file__).resolve().parents[1]


def _resolve_endpoints_path(explicit: str | None) -> Path:
    if explicit:
        return Path(explicit).expanduser().resolve()

    if get_config is not None:
        cfg = get_config()
        candidate = cfg.get("pipeline.endpoints_file")
        if candidate:
            return (ROOT / candidate).resolve()

    return (ROOT / "endpoints.txt").resolve()


def _read_endpoints(path: Path) -> List[str]:
    if not path.exists():
        return []
    endpoints: List[str] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        entry = line.strip()
        if not entry or entry.startswith('#'):
            continue
        endpoints.append(entry)
    return endpoints


def _write_endpoints(path: Path, endpoints: List[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    content = "\n".join(sorted(set(endpoints))) + "\n" if endpoints else ""
    path.write_text(content, encoding="utf-8")


def cmd_list(path: Path) -> None:
    endpoints = _read_endpoints(path)
    if not endpoints:
        print(f"No endpoints found in {path}.")
        return
    print(f"Endpoints in {path}:")
    for idx, entry in enumerate(endpoints, 1):
        print(f"  {idx:2d}. {entry}")


def cmd_add(path: Path, search_ids: List[str]) -> None:
    endpoints = _read_endpoints(path)
    original_len = len(endpoints)
    for sid in search_ids:
        sid = sid.strip()
        if sid and sid not in endpoints:
            endpoints.append(sid)
    if len(endpoints) == original_len:
        print("No new endpoints were added (duplicates or empty input).")
        return
    _write_endpoints(path, endpoints)
    print(f"Added {len(endpoints) - original_len} endpoint(s) to {path}.")


def cmd_remove(path: Path, search_ids: List[str]) -> None:
    endpoints = _read_endpoints(path)
    to_remove = set(sid.strip() for sid in search_ids if sid.strip())
    filtered = [sid for sid in endpoints if sid not in to_remove]
    removed = len(endpoints) - len(filtered)
    _write_endpoints(path, filtered)
    print(f"Removed {removed} endpoint(s) from {path}.")


def cmd_clear(path: Path) -> None:
    _write_endpoints(path, [])
    print(f"Cleared all endpoints in {path}.")


def interactive(path: Path) -> None:
    while True:
        print("\nEndpoint Manager")
        print("---------------")
        cmd_list(path)
        print("\nOptions:")
        print("  1) Add endpoint")
        print("  2) Remove endpoint")
        print("  3) Clear all")
        print("  4) Exit")

        choice = input("Select an option [1-4]: ").strip()
        if choice == '1':
            sid = input("Enter HigherGov search ID: ").strip()
            if sid:
                cmd_add(path, [sid])
        elif choice == '2':
            sid = input("Enter search ID to remove: ").strip()
            if sid:
                cmd_remove(path, [sid])
        elif choice == '3':
            confirm = input("Are you sure you want to clear all endpoints? (yes/no): ").strip().lower()
            if confirm in {"yes", "y"}:
                cmd_clear(path)
        elif choice == '4':
            print("Goodbye.")
            return
        else:
            print("Invalid option. Please choose 1-4.")


def main() -> int:
    parser = argparse.ArgumentParser(description="Manage HigherGov search IDs used by the pipeline.")
    parser.add_argument("--file", help="Path to endpoints file (defaults to config value or endpoints.txt).")
    sub = parser.add_subparsers(dest="command")

    sub.add_parser("list", help="List all endpoints.")

    add_parser = sub.add_parser("add", help="Add one or more endpoints.")
    add_parser.add_argument("search_ids", nargs="+", help="HigherGov search IDs to add.")

    remove_parser = sub.add_parser("remove", help="Remove one or more endpoints.")
    remove_parser.add_argument("search_ids", nargs="+", help="HigherGov search IDs to remove.")

    sub.add_parser("clear", help="Remove all endpoints.")

    args = parser.parse_args()
    path = _resolve_endpoints_path(args.file)

    if args.command == "list":
        cmd_list(path)
    elif args.command == "add":
        cmd_add(path, args.search_ids)
    elif args.command == "remove":
        cmd_remove(path, args.search_ids)
    elif args.command == "clear":
        cmd_clear(path)
    else:
        interactive(path)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
