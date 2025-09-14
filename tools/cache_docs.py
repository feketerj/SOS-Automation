#!/usr/bin/env python3
"""
HigherGov document cache utility (optional, read-only by default).

Usage:
  python tools/cache_docs.py --status [--dir DIR]
  python tools/cache_docs.py --prune DAYS [--dir DIR] [--apply]
  python tools/cache_docs.py --clear [--dir DIR] --apply

Notes:
  - Defaults to the cache directory from config: pipeline.document_cache.dir (or cache/hg_docs)
  - Without --apply, prune/clear operate in dry-run mode and only print what would be removed.
"""

from __future__ import annotations

import argparse
from pathlib import Path
from datetime import datetime, timedelta


def resolve_cache_dir(cli_dir: str | None) -> Path:
    if cli_dir:
        return Path(cli_dir)
    # Try to read from centralized config
    try:
        from config.loader import get_config  # type: ignore
        cfg = get_config()
        d = cfg.get('pipeline.document_cache.dir')
        if d:
            return Path(d)
    except Exception:
        pass
    return Path('cache') / 'hg_docs'


def human_size(num: int) -> str:
    for unit in ['B','KB','MB','GB']:
        if num < 1024:
            return f"{num:.1f} {unit}"
        num /= 1024
    return f"{num:.1f} TB"


def status(cache_dir: Path) -> int:
    if not cache_dir.exists():
        print('Cache directory not found:', cache_dir)
        return 0
    files = list(cache_dir.glob('*.txt'))
    total = sum(f.stat().st_size for f in files)
    print('Cache dir:', cache_dir)
    print('Files   :', len(files))
    print('Size    :', human_size(total))
    # Show a few recent files
    if files:
        latest = sorted(files, key=lambda p: p.stat().st_mtime, reverse=True)[:5]
        print('Latest  :')
        for p in latest:
            dt = datetime.fromtimestamp(p.stat().st_mtime).strftime('%Y-%m-%d %H:%M')
            print('  ', dt, p.name, human_size(p.stat().st_size))
    return 0


def prune(cache_dir: Path, days: int, apply: bool) -> int:
    if not cache_dir.exists():
        print('Cache directory not found:', cache_dir)
        return 0
    cutoff = datetime.now() - timedelta(days=days)
    files = list(cache_dir.glob('*.txt'))
    victims = [p for p in files if datetime.fromtimestamp(p.stat().st_mtime) < cutoff]
    print(f'Prune candidates older than {days} day(s): {len(victims)}')
    total = sum(p.stat().st_size for p in victims)
    print('Total size:', human_size(total))
    if not victims:
        return 0
    if apply:
        removed = 0
        for p in victims:
            try:
                p.unlink()
                removed += 1
            except Exception as e:
                print('WARN: could not remove', p, e)
        print('Removed:', removed)
    else:
        print('Dry run (use --apply to delete)')
        for p in victims[:10]:
            print('  ', p.name)
        if len(victims) > 10:
            print('  ...')
    return 0


def clear(cache_dir: Path, apply: bool) -> int:
    if not cache_dir.exists():
        print('Cache directory not found:', cache_dir)
        return 0
    files = list(cache_dir.glob('*.txt'))
    print('Files to clear:', len(files))
    if not files:
        return 0
    if apply:
        removed = 0
        for p in files:
            try:
                p.unlink()
                removed += 1
            except Exception as e:
                print('WARN: could not remove', p, e)
        print('Removed:', removed)
    else:
        print('Dry run (use --apply to delete)')
        for p in files[:10]:
            print('  ', p.name)
        if len(files) > 10:
            print('  ...')
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description='HigherGov document cache utility')
    ap.add_argument('--dir', help='Cache directory (optional)')
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument('--status', action='store_true', help='Show cache status')
    g.add_argument('--prune', type=int, metavar='DAYS', help='List/remove entries older than DAYS')
    g.add_argument('--clear', action='store_true', help='Clear all cache files')
    ap.add_argument('--apply', action='store_true', help='Apply deletions (default is dry-run)')
    args = ap.parse_args()

    cache_dir = resolve_cache_dir(args.dir)
    if args.status:
        return status(cache_dir)
    if args.prune is not None:
        return prune(cache_dir, args.prune, args.apply)
    if args.clear:
        return clear(cache_dir, args.apply)
    return 2


if __name__ == '__main__':
    raise SystemExit(main())

