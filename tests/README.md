# Test infrastructure

This directory contains the eval grading + benchmarking scripts used to validate the `user-story-mapping` skill across the 20 scenarios in `../user-story-mapping/evals/evals.json`.

## What's here

- **`grade_runs.py`** — Reads workspace test outputs, evaluates assertion checks per eval, writes `grading.json` into each run directory
- **`build_benchmark.py`** — Aggregates grading.json + timing.json across runs into `benchmark.json` and `benchmark.md` for a given iteration
- **`build_viewer.py`** — Generates a standalone HTML viewer with all outputs side-by-side + benchmark tab + per-eval feedback textbox

## How to run a test cycle

1. **Spawn test runs.** For each eval, launch two agents (one with-skill, one baseline) in parallel:
   ```
   # Pseudocode for the workflow — implement using your preferred subagent runner
   for eval in evals.json:
     run_with_skill(eval, save_to=workspace/iteration-N/eval-<id>/with_skill/outputs/)
     run_baseline(eval, save_to=workspace/iteration-N/eval-<id>/without_skill/outputs/)
   ```

2. **Capture timing** as each run completes (token count + duration) into `timing.json` in each run dir.

3. **Grade.** From the project root:
   ```bash
   python tests/grade_runs.py iteration-N
   ```
   Writes `grading.json` into each `with_skill/` and `without_skill/` directory.

4. **Build benchmark.**
   ```bash
   python tests/build_benchmark.py
   ```
   Writes `benchmark.json` + `benchmark.md` to the iteration directory.

5. **Build viewer.**
   ```bash
   python tests/build_viewer.py
   ```
   Writes `review.html` to the iteration directory. Open in a browser; review outputs + leave feedback per eval; click "Submit All Reviews" to download `feedback.json`.

## Expected results

With-skill should score ≥90% across all 18 evals. Baseline typically scores 15-25%. The big discriminators:

- Structural conformance — baseline rarely produces the canonical 6-file output
- Methodology correctness — baseline rarely uses the canonical CSV header / Mermaid format
- Capability-specific behaviors — baseline misses persona conflict surfacing, dependency cycle detection, OKR coverage gaps, Mode D breach detection, etc.

## Skill-creator dependency

The original test runs used Anthropic's [skill-creator](https://github.com/anthropics/skills) plugin. The description-optimization loop (`run_loop.py`) in that plugin uses `select.select()` on subprocess pipes which is Linux/Mac only — it doesn't work on Windows.

For Windows, run the description optimization on Linux/Mac/WSL, or tune the description manually using the assertions in `../user-story-mapping/evals/evals.json` as the trigger eval set.

## Workspace structure expected by these scripts

```
user-story-mapping-workspace/
└── iteration-N/
    ├── eval-1-<name>/
    │   ├── eval_metadata.json          # { eval_id, eval_name, prompt, assertions }
    │   ├── with_skill/
    │   │   ├── outputs/                # the artifacts the agent produced
    │   │   ├── timing.json             # { total_tokens, duration_ms, total_duration_seconds }
    │   │   └── grading.json            # written by grade_runs.py
    │   └── without_skill/
    │       ├── outputs/
    │       ├── timing.json
    │       └── grading.json
    ├── eval-2-<name>/
    │   └── ...
    ├── benchmark.json                  # written by build_benchmark.py
    ├── benchmark.md
    └── review.html                     # written by build_viewer.py
```

The workspace itself is `.gitignore`'d — per-iteration test outputs are not committed. Regenerate locally with your preferred subagent runner.
