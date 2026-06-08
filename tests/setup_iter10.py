#!/usr/bin/env python3
"""Generate iteration-10 workspace structure from evals.json."""
import json
from pathlib import Path

ROOT = Path(__file__).parent.parent
EVALS = json.loads((ROOT / "skills" / "user-story-mapping" / "evals" / "evals.json").read_text(encoding="utf-8"))
ITER = ROOT / "user-story-mapping-workspace" / "iteration-11"

for e in EVALS["evals"]:
    eval_dir = ITER / f"eval-{e['id']}-{e['name']}"
    (eval_dir / "with_skill" / "outputs").mkdir(parents=True, exist_ok=True)
    (eval_dir / "without_skill" / "outputs").mkdir(parents=True, exist_ok=True)
    meta = {
        "eval_id": e["id"],
        "eval_name": e["name"],
        "prompt": e["prompt"],
        "assertions": e.get("assertions", []),
    }
    (eval_dir / "eval_metadata.json").write_text(json.dumps(meta, indent=2), encoding="utf-8")

print(f"ready: {len(EVALS['evals'])} evals in {ITER}")
