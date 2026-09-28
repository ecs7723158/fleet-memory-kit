import json
from pathlib import Path

import pytest

from fleet_memory.store import MemoryStore


def test_add_list_search_get(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path)
    e1 = store.add("HPA notes", "Kubernetes HPA scales on CPU", tags=["k8s", "memory"], source="unit")
    e2 = store.add("Prompt eval", "promptfoo smoke passed on hq-os", tags=["eval"], source="unit")

    assert e1.id
    assert (tmp_path / "entries" / f"{e1.id}.md").exists()
    assert "HPA notes" in (tmp_path / "INDEX.md").read_text(encoding="utf-8")

    listed = store.list()
    assert len(listed) == 2

    hits = store.search("kubernetes hpa")
    assert len(hits) == 1
    assert hits[0].id == e1.id

    got = store.get(e2.id)
    assert got is not None
    assert got.title == "Prompt eval"

    lines = [ln for ln in (tmp_path / "index.jsonl").read_text(encoding="utf-8").splitlines() if ln]
    assert len(lines) == 2
    assert json.loads(lines[0])["title"] == "HPA notes"


def test_add_requires_title_and_body(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path)
    with pytest.raises(ValueError):
        store.add("", "body")
    with pytest.raises(ValueError):
        store.add("title", "")


def test_duplicate_id_raises(tmp_path: Path) -> None:
    store = MemoryStore(tmp_path)
    store.add("a", "b", entry_id="fixedid")
    with pytest.raises(FileExistsError):
        store.add("c", "d", entry_id="fixedid")
