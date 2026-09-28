from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from .store import MemoryStore


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="fleet-memory", description="Local fleet memory CLI")
    parser.add_argument(
        "--root",
        default=str(Path.cwd() / "memory"),
        help="memory root directory (default: ./memory)",
    )
    sub = parser.add_subparsers(dest="cmd", required=True)

    p_add = sub.add_parser("add", help="add a memory entry")
    p_add.add_argument("--title", required=True)
    p_add.add_argument("--body", required=True)
    p_add.add_argument("--tag", action="append", default=[])
    p_add.add_argument("--source", default="local")

    sub.add_parser("list", help="list entries")

    p_search = sub.add_parser("search", help="search entries")
    p_search.add_argument("query")
    p_search.add_argument("--limit", type=int, default=20)

    p_get = sub.add_parser("get", help="get one entry by id")
    p_get.add_argument("id")

    args = parser.parse_args(argv)
    store = MemoryStore(args.root)

    if args.cmd == "add":
        entry = store.add(args.title, args.body, tags=args.tag, source=args.source)
        print(json.dumps({"ok": True, "id": entry.id, "path": f"entries/{entry.id}.md"}, ensure_ascii=False))
        return 0
    if args.cmd == "list":
        print(json.dumps([e.__dict__ for e in store.list()], ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "search":
        hits = store.search(args.query, limit=args.limit)
        print(json.dumps([e.__dict__ for e in hits], ensure_ascii=False, indent=2))
        return 0
    if args.cmd == "get":
        entry = store.get(args.id)
        if not entry:
            print(json.dumps({"ok": False, "error": "not found"}, ensure_ascii=False), file=sys.stderr)
            return 1
        print(json.dumps(entry.__dict__, ensure_ascii=False, indent=2))
        return 0
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
