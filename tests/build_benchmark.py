#!/usr/bin/env python3
"""Aggregate per-iteration grading + timing into benchmark.json + a Markdown summary.

Reads from `user-story-mapping-workspace/<ITERATION>/eval-*/` and writes the aggregated
benchmark.json + benchmark.md back into the same iteration directory. Override the
target iteration via the ITERATION_OVERRIDE env var; defaults to iteration-12.
"""
from __future__ import annotations

import html
import json
import os
import statistics
from pathlib import Path

ROOT = Path(__file__).parent.parent
DEFAULT_ITERATION_NAME = os.environ.get("ITERATION_OVERRIDE", "iteration-12")
ITERATION = ROOT / "user-story-mapping-workspace" / DEFAULT_ITERATION_NAME
PREV_ITERATION = None
SKILL_NAME = "user-story-mapping"


def load_run(run_dir: Path) -> dict:
    grading_path = run_dir / "grading.json"
    timing_path = run_dir / "timing.json"
    grading = json.loads(grading_path.read_text(encoding="utf-8")) if grading_path.exists() else {"expectations": []}
    timing = json.loads(timing_path.read_text(encoding="utf-8")) if timing_path.exists() else {}
    passed = sum(1 for e in grading["expectations"] if e["passed"])
    total = len(grading["expectations"])
    return {
        "passed": passed,
        "total": total,
        "pass_rate": (passed / total) if total else 0.0,
        "duration_seconds": timing.get("total_duration_seconds", 0.0),
        "tokens": timing.get("total_tokens", 0),
        "expectations": grading["expectations"],
    }


def aggregate_config(runs: list[dict]) -> dict:
    pass_rates = [r["pass_rate"] for r in runs]
    durations = [r["duration_seconds"] for r in runs]
    tokens = [r["tokens"] for r in runs]
    return {
        "n": len(runs),
        "pass_rate_mean": statistics.mean(pass_rates) if pass_rates else 0,
        "pass_rate_stdev": statistics.stdev(pass_rates) if len(pass_rates) > 1 else 0,
        "duration_mean": statistics.mean(durations) if durations else 0,
        "duration_stdev": statistics.stdev(durations) if len(durations) > 1 else 0,
        "tokens_mean": statistics.mean(tokens) if tokens else 0,
        "tokens_stdev": statistics.stdev(tokens) if len(tokens) > 1 else 0,
    }


def main() -> int:
    eval_dirs = sorted(p for p in ITERATION.iterdir() if p.is_dir() and p.name.startswith("eval-"))

    per_eval = []
    with_skill_runs = []
    without_skill_runs = []
    for eval_dir in eval_dirs:
        meta = json.loads((eval_dir / "eval_metadata.json").read_text(encoding="utf-8"))
        with_run = load_run(eval_dir / "with_skill")
        without_run = load_run(eval_dir / "without_skill")
        with_skill_runs.append(with_run)
        without_skill_runs.append(without_run)
        per_eval.append({
            "eval_id": meta["eval_id"],
            "eval_name": meta["eval_name"],
            "prompt": meta["prompt"],
            "with_skill": with_run,
            "without_skill": without_run,
        })

    # Previous-iteration comparison
    prev_with = []
    prev_wo = []
    if PREV_ITERATION is not None and PREV_ITERATION.exists():
        for prev_dir in sorted(p for p in PREV_ITERATION.iterdir() if p.is_dir() and p.name.startswith("eval-")):
            prev_with.append(load_run(prev_dir / "with_skill"))
            prev_wo.append(load_run(prev_dir / "without_skill"))
    prev_agg = aggregate_config(prev_with) if prev_with else None

    benchmark = {
        "skill_name": SKILL_NAME,
        "iteration": int("".join(c for c in DEFAULT_ITERATION_NAME if c.isdigit()) or "12"),
        "configurations": {
            "with_skill": aggregate_config(with_skill_runs),
            "without_skill": aggregate_config(without_skill_runs),
        },
        "previous_iteration": None,
        "per_eval": per_eval,
        "delta": {
            "pass_rate": aggregate_config(with_skill_runs)["pass_rate_mean"] - aggregate_config(without_skill_runs)["pass_rate_mean"],
            "duration_seconds": aggregate_config(with_skill_runs)["duration_mean"] - aggregate_config(without_skill_runs)["duration_mean"],
            "tokens": aggregate_config(with_skill_runs)["tokens_mean"] - aggregate_config(without_skill_runs)["tokens_mean"],
        },
        "analyst_notes": [
            f"Iteration {DEFAULT_ITERATION_NAME[len('iteration-'):]} — auto-generated from per-eval grading.json + timing.json files. Re-run `tests/grade_runs.py {DEFAULT_ITERATION_NAME}` to refresh.",
            "Per-eval breakdown above shows assertion pass rates. With-skill should consistently beat baseline; the gap is what the skill is buying you.",
            "Without-skill runs may be skipped for refactor-only releases (where SKILL.md changes don't affect non-skill agent behavior); see the per-iteration README for the comparison strategy.",
        ],
    }

    (ITERATION / "benchmark.json").write_text(json.dumps(benchmark, indent=2), encoding="utf-8")

    # Markdown summary
    cfg_with = benchmark["configurations"]["with_skill"]
    cfg_wo = benchmark["configurations"]["without_skill"]
    md_lines = [
        f"# Benchmark — {SKILL_NAME} (iteration {benchmark['iteration']})",
        "",
        "## Summary",
        "",
        "| Configuration | Pass rate | Duration (s) | Tokens |",
        "|---|---|---|---|",
        f"| **with_skill** | {cfg_with['pass_rate_mean']*100:.1f}% ± {cfg_with['pass_rate_stdev']*100:.1f}% | {cfg_with['duration_mean']:.0f} ± {cfg_with['duration_stdev']:.0f} | {cfg_with['tokens_mean']:.0f} ± {cfg_with['tokens_stdev']:.0f} |",
        f"| without_skill | {cfg_wo['pass_rate_mean']*100:.1f}% ± {cfg_wo['pass_rate_stdev']*100:.1f}% | {cfg_wo['duration_mean']:.0f} ± {cfg_wo['duration_stdev']:.0f} | {cfg_wo['tokens_mean']:.0f} ± {cfg_wo['tokens_stdev']:.0f} |",
        f"| **Δ (with − without)** | **+{benchmark['delta']['pass_rate']*100:.1f}pp** | {benchmark['delta']['duration_seconds']:+.0f}s | {benchmark['delta']['tokens']:+.0f} |",
        "",
        "## Per-eval",
        "",
        "| Eval | with_skill | without_skill |",
        "|---|---|---|",
    ]
    for e in per_eval:
        md_lines.append(
            f"| {e['eval_name']} | {e['with_skill']['passed']}/{e['with_skill']['total']} ({e['with_skill']['duration_seconds']:.0f}s, {e['with_skill']['tokens']:,} tok) | {e['without_skill']['passed']}/{e['without_skill']['total']} ({e['without_skill']['duration_seconds']:.0f}s, {e['without_skill']['tokens']:,} tok) |"
        )
    md_lines.append("")
    md_lines.append("## Analyst notes")
    md_lines.append("")
    for note in benchmark["analyst_notes"]:
        md_lines.append(f"- {note}")
    (ITERATION / "benchmark.md").write_text("\n".join(md_lines) + "\n", encoding="utf-8")

    print(f"wrote {ITERATION / 'benchmark.json'}")
    print(f"wrote {ITERATION / 'benchmark.md'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
