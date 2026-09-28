#!/usr/bin/env bash
# Interview demo harness for fleet-memory-kit
# Runs pytest, then a short CLI search for career/offer tagged memories.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

echo "==> fleet-memory-kit demo"
echo "    root: $ROOT"

if [[ -f .venv/bin/activate ]]; then
  # shellcheck disable=SC1091
  source .venv/bin/activate
  echo "    venv:  .venv (activated)"
else
  echo "    venv:  not found (using system python/PATH)"
fi

echo
echo "==> pytest -q"
if ! pytest -q; then
  echo
  echo "FAIL: pytest failed — fix tests before demoing"
  exit 1
fi
echo "SUCCESS: pytest passed"

echo
echo "==> CLI demo: search career/offer memories"
CLI=""
if command -v fleet-memory >/dev/null 2>&1; then
  CLI="fleet-memory"
elif [[ -x .venv/bin/fleet-memory ]]; then
  CLI=".venv/bin/fleet-memory"
elif python -c "import fleet_memory.cli" 2>/dev/null; then
  CLI="python -m fleet_memory.cli"
else
  echo "FAIL: fleet-memory CLI not found. Install with: pip install -e '.[dev]'"
  exit 1
fi

MEMORY_ROOT="${ROOT}/memory"
echo "    entrypoint: $CLI"
echo "    memory:     $MEMORY_ROOT"
echo

# Prefer search for offer (hits career/offer tags); fall back to list
set +e
DEMO_OUT="$($CLI --root "$MEMORY_ROOT" search offer 2>&1)"
DEMO_RC=$?
set -e
if [[ $DEMO_RC -ne 0 ]]; then
  echo "WARN: search failed (rc=$DEMO_RC); falling back to list"
  DEMO_OUT="$($CLI --root "$MEMORY_ROOT" list)"
fi
echo "$DEMO_OUT"
echo
echo "SUCCESS: CLI demo completed"

echo
echo "==> Portfolio / interview hints"
echo "    README:         $ROOT/README.md"
echo "    CMD cheat-sheet:$ROOT/README_CMD.md"
echo "    Portfolio one-pager (box): /home/box/knowledge/projects/career/portfolio-onepager-2026-09-29.md"
echo "    Pitch: local markdown memory + pytest + GitHub Actions CI; LICENSE MIT."
echo
echo "SUCCESS: demo harness finished OK"
