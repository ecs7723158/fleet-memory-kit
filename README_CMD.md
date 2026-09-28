# fleet-memory-kit — CMD invoke cheat-sheet

**Root (MBP):** `~/Projects/fleet-memory-kit`  
**Repo:** https://github.com/ecs7723158/fleet-memory-kit  
**Memory store:** `~/Projects/fleet-memory-kit/memory`

## Demo

面試 / 現場 demo 一鍵跑（pytest + career/offer CLI search）：

```bash
cd ~/Projects/fleet-memory-kit && ./scripts/demo.sh
```

預期輸出形狀：

- `SUCCESS: pytest passed`
- JSON array（含 `career` / `offer` tags 的 entries）
- `SUCCESS: CLI demo completed`
- `SUCCESS: demo harness finished OK`
- path hints → `README.md` / `README_CMD.md` / portfolio one-pager

**Pitch one-liner:** local pytest + CI green；LICENSE MIT；no API key for core memory.

Portfolio one-pager（box）：`/home/box/knowledge/projects/career/portfolio-onepager-2026-09-29.md`

## Exact CLI path

```bash
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --root ~/Projects/fleet-memory-kit/memory
```

## Common CMD invocations

```bash
# help
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --help

# add
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --root ~/Projects/fleet-memory-kit/memory add \
  --title "short title" --body "markdown or plain body" --tag career --tag offer --source cmd

# list / search / get
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --root ~/Projects/fleet-memory-kit/memory list
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --root ~/Projects/fleet-memory-kit/memory search offer
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --root ~/Projects/fleet-memory-kit/memory get <id>
```

## Tests

```bash
cd ~/Projects/fleet-memory-kit && .venv/bin/pytest -q
# expected: 3 passed
```

If CLI missing: `cd ~/Projects/fleet-memory-kit && python3 -m venv .venv && .venv/bin/pip install -e '.[dev]'`
