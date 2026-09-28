from __future__ import annotations

import json
import re
import uuid
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Iterable, List, Optional


def _utc_now() -> str:
    return datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


@dataclass
class MemoryEntry:
    id: str
    title: str
    body: str
    tags: List[str] = field(default_factory=list)
    created_at: str = field(default_factory=_utc_now)
    source: str = "local"

    def to_markdown(self) -> str:
        tags = ", ".join(self.tags) if self.tags else ""
        return (
            f"# {self.title}\n\n"
            f"- id: `{self.id}`\n"
            f"- created_at: `{self.created_at}`\n"
            f"- source: `{self.source}`\n"
            f"- tags: `{tags}`\n\n"
            f"{self.body.strip()}\n"
        )


class MemoryStore:
    """Filesystem memory bank: one markdown file per entry + INDEX.md + index.jsonl."""

    def __init__(self, root: Path | str) -> None:
        self.root = Path(root)
        self.entries_dir = self.root / "entries"
        self.index_md = self.root / "INDEX.md"
        self.index_jsonl = self.root / "index.jsonl"
        self.entries_dir.mkdir(parents=True, exist_ok=True)
        if not self.index_md.exists():
            self.index_md.write_text("# Memory INDEX\n\n", encoding="utf-8")
        if not self.index_jsonl.exists():
            self.index_jsonl.write_text("", encoding="utf-8")

    def add(
        self,
        title: str,
        body: str,
        tags: Optional[Iterable[str]] = None,
        source: str = "local",
        entry_id: Optional[str] = None,
    ) -> MemoryEntry:
        title = (title or "").strip()
        body = (body or "").strip()
        if not title:
            raise ValueError("title is required")
        if not body:
            raise ValueError("body is required")
        entry = MemoryEntry(
            id=entry_id or uuid.uuid4().hex[:12],
            title=title,
            body=body,
            tags=[t.strip() for t in (tags or []) if t and t.strip()],
            source=source,
        )
        path = self.entries_dir / f"{entry.id}.md"
        if path.exists():
            raise FileExistsError(f"entry already exists: {entry.id}")
        path.write_text(entry.to_markdown(), encoding="utf-8")
        with self.index_jsonl.open("a", encoding="utf-8") as fh:
            fh.write(json.dumps(asdict(entry), ensure_ascii=False) + "\n")
        with self.index_md.open("a", encoding="utf-8") as fh:
            tag_s = ", ".join(entry.tags) if entry.tags else "-"
            fh.write(
                f"- [{entry.created_at}] `{entry.id}` **{entry.title}** "
                f"(tags: {tag_s}) → `entries/{entry.id}.md`\n"
            )
        return entry

    def list(self) -> List[MemoryEntry]:
        out: List[MemoryEntry] = []
        if not self.index_jsonl.exists():
            return out
        for line in self.index_jsonl.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if not line:
                continue
            data = json.loads(line)
            out.append(MemoryEntry(**data))
        return out

    def get(self, entry_id: str) -> Optional[MemoryEntry]:
        for e in self.list():
            if e.id == entry_id:
                return e
        return None

    def search(self, query: str, limit: int = 20) -> List[MemoryEntry]:
        q = (query or "").strip().lower()
        if not q:
            return []
        tokens = [t for t in re.split(r"\s+", q) if t]
        scored: List[tuple[int, MemoryEntry]] = []
        for e in self.list():
            blob = " ".join([e.title, e.body, " ".join(e.tags), e.source]).lower()
            score = sum(1 for t in tokens if t in blob)
            if score:
                scored.append((score, e))
        scored.sort(key=lambda x: (-x[0], x[1].created_at), reverse=False)
        scored.sort(key=lambda x: (-x[0], x[1].created_at))
        return [e for _, e in scored[:limit]]
