# fleet-memory-kit

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
