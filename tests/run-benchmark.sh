#!/usr/bin/env bash
# Convenience wrapper: run a full benchmark cycle end-to-end.
# Usage:
#   ./tests/run-benchmark.sh              # uses iteration-NEXT (auto-detect)
#   ./tests/run-benchmark.sh iteration-11 # explicit iteration name
#
# Steps:
#   1. Set up workspace dirs + eval_metadata.json files for all 18 evals
#   2. (Manual) Spawn the test runs — see comments below
#   3. Capture timing.json per run (you do this from your runner's output)
#   4. Grade all runs (assertions)
#   5. Build benchmark.json + benchmark.md
#   6. Build review.html (static viewer)
#
# This script automates steps 1, 4, 5, 6 — it doesn't run the agents themselves
# because that's host-specific (Claude Code Agent tool, OpenAI Codex, etc.).
# The test infra is host-agnostic.

set -euo pipefail
cd "$(dirname "$0")/.."

ITER="${1:-}"
if [[ -z "$ITER" ]]; then
  # Auto-detect next iteration number
  next=$(ls user-story-mapping-workspace/ 2>/dev/null | grep -oE 'iteration-[0-9]+' | sed 's/iteration-//' | sort -n | tail -1 || echo "0")
  ITER="iteration-$((next + 1))"
fi
WORKSPACE="user-story-mapping-workspace/$ITER"

echo "▶ Setting up workspace: $WORKSPACE"
mkdir -p "$WORKSPACE"

# Update setup_iter10.py to point at the chosen iteration, or use the simpler approach:
PYTHONUTF8=1 python -c "
import json
from pathlib import Path
evals = json.load(open('user-story-mapping/evals/evals.json', encoding='utf-8'))
for e in evals['evals']:
    d = Path('$WORKSPACE') / f\"eval-{e['id']}-{e['name']}\"
    (d / 'with_skill' / 'outputs').mkdir(parents=True, exist_ok=True)
    (d / 'without_skill' / 'outputs').mkdir(parents=True, exist_ok=True)
    meta = {'eval_id': e['id'], 'eval_name': e['name'], 'prompt': e['prompt'], 'assertions': e.get('assertions', [])}
    (d / 'eval_metadata.json').write_text(json.dumps(meta, indent=2), encoding='utf-8')
print(f'  Set up {len(evals[\"evals\"])} eval directories in $WORKSPACE')
"

cat <<EOF

▶ Step 2 — Spawn test runs (HOST-SPECIFIC, you do this part):

  For each eval-N-<name>/ directory in $WORKSPACE:
    • Spawn a with-skill agent with:
        - prompt = eval_metadata.json's "prompt" field
        - skill loaded from user-story-mapping/
        - output saved to with_skill/outputs/
    • Spawn a baseline agent with:
        - prompt = eval_metadata.json's "prompt" field
        - NO skill loaded
        - output saved to without_skill/outputs/

  Capture per-agent timing in timing.json:
    {"total_tokens": <int>, "duration_ms": <int>, "total_duration_seconds": <float>}

  For Claude Code: use the Agent tool with subagent_type=general-purpose.
  For other hosts: see your host's parallel-execution / subagent docs.

  Press Enter when all 36 runs (18 evals × 2 configs) are complete.
EOF
read -r

echo "▶ Grading runs..."
PYTHONUTF8=1 python tests/grade_runs.py "$ITER"

echo "▶ Building benchmark.json + benchmark.md..."
PYTHONUTF8=1 ITERATION_OVERRIDE="$ITER" python tests/build_benchmark.py

echo "▶ Building review.html..."
PYTHONUTF8=1 python tests/build_viewer.py

echo ""
echo "✓ Benchmark complete:"
echo "  $WORKSPACE/benchmark.md"
echo "  $WORKSPACE/benchmark.json"
echo "  $WORKSPACE/review.html  (open in browser)"
