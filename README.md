# fleet-memory-kit

[![pytest](https://img.shields.io/badge/tests-pytest-blue?logo=pytest)](https://github.com/ecs7723158/fleet-memory-kit)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/ecs7723158/fleet-memory-kit)
[![python](https://img.shields.io/badge/python-3.x-blue?logo=python)](https://github.com/ecs7723158/fleet-memory-kit)

## Demo (30s)

Copy-paste the CMD CLI path for a quick local search:

```bash
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --help
~/Projects/fleet-memory-kit/.venv/bin/fleet-memory --root ~/Projects/fleet-memory-kit/memory search offer
```

Local **markdown memory bank** for Oscar Kate's device fleet (WIN + MBP + Grok Bot box), with CLI, unit tests, and hooks aligned to common AI ops tools:

| Tool | Role | Stars (approx) | Status in this kit |
|------|------|----------------|--------------------|
| [mem0ai/mem0](https://github.com/mem0ai/mem0) | vector / long-term agent memory | 66k+ | documented optional next step (needs API key) |
| [langfuse/langfuse](https://github.com/langfuse/langfuse) | LLM observability | 35k+ | optional compose stub; prefer MBP **colima** |
| [promptfoo/promptfoo](https://github.com/promptfoo/promptfoo) | prompt eval | 25k+ | `prompts/smoke.yaml` stub; live eval already on WIN `hq-os` |

## Why local-first

- No API key required for core memory
- Files sync-friendly (`entries/*.md` + `INDEX.md` + `index.jsonl`)
- Same shape as CMD knowledge under `/home/box/knowledge`

## Install / test

```bash
cd fleet-memory-kit
python3 -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
fleet-memory --root ./memory add --title "demo" --body "hello" --tag fleet
fleet-memory --root ./memory search demo
```

## Fleet wiring

- **MBP**: primary git + colima host for this repo
- **WIN**: keep `promptfoo` evals in `hq-os`; mirror useful memories into this store
- **Box**: Crawl4AI knowledge stays at `/home/box/knowledge`; export notes here when promoting to versioned memory

## License

MIT
