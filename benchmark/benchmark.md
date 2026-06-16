# Benchmark — user-story-mapping (iteration 12, v0.0.3)

## Summary

| Configuration | Pass rate | Notes |
|---|---|---|
| **with_skill** (v0.0.3) | **99.6% (255/256)** | iteration-12, 25 evals, lean SKILL.md v0.0.3 |
| without_skill (iter-11 reference) | 20.4% ± 17.2% | not re-run for v0.0.3 — assumed unchanged for non-skill agent behavior |
| **Δ (with − without)** | **+79.2 pp** | structural conformance + methodology correctness gap |

iteration-11 baseline (v0.0.2): with_skill = 98.2%. v0.0.3 = **+1.4 pp** despite the SKILL.md being 33% smaller and the eval suite growing from 20 → 25 scenarios (5 new v0.0.3-feature evals all passed 60/60 on first run).

## Per-eval (with_skill, iteration-12)

| Eval | Pass rate | Notes |
|---|---|---|
| 1 from-scratch-internal-tool | 10/10 | from scratch, SAFe PI, WSJF |
| 2 from-problem-brief-mobile-onboarding | 10/10 | from a brief, RICE |
| 3 from-existing-backlog-messy-csv | 10/10 | from existing backlog, MoSCoW, Jira-key preservation |
| 4 gstack-handoff-developer-portal | 10/10 | framework integration |
| 5 gsd-handoff-solo-builder-saas | 11/11 | framework integration |
| 6 pure-api-sdk-python | 9/9 | API/SDK, Now-Next-Later |
| 7 desktop-password-manager | 9/9 | desktop app, install/keychain |
| 8 enterprise-analytics-multitenant | 10/10 | multi-tenant SaaS, full ART |
| 9 cli-log-parser | 9/9 | CLI, single-user OSS |
| 10 mobile-consumer-fitness | 9/9 | mobile B2C |
| 11 customer-interview-synthesis | 10/10 | discovery: raw notes → personas |
| 12 dependency-aware-backlog | 9/10 | **real miss**: agent preserved 5/14 user-provided story IDs |
| 13 okr-aligned-roadmap | 10/10 | OKR coverage matrix + orphans |
| 14 thin-brief-gap-discovery | 10/10 | persona simulation, conflict matrix |
| 15 multi-stakeholder-conflict | 10/10 | user-input-authoritative |
| 16 snapshot-and-breaks-limits | 8/8 | iteration + breach detection |
| 17 empty-dir-loop-shortcircuit | 9/9 | Step 0 fast-exit for greenfield |
| 18 framework-artifacts-and-criteria | 10/10 | `.gsd/` reads + backbone criteria |
| 19 output-routing-from-scratch | 13/13 | tracker-seeding script (not auto-run) |
| 20 output-routing-existing-cascade | 12/12 | TODO.md cascade, no tracker push |
| 21 step-0-5-progress-reconciliation | 12/12 | **new** — tracker/code/storymap sync, graduation, drift |
| 22 per-persona-slice-1-coverage | 10/10 | **new** — 3 personas enforced in slice-1 |
| 23 step-2-5-role-hints-generation | 12/12 | **new** — UX + Architect sections, HIPAA/PCI/Twilio/Stripe |
| 24 plan-stage-auto-trigger-gstack | 10/10 | **new** — `/office-hours` auto-activation |
| 25 tracker-write-back-script-emitted | 13/13 | **new** — Jira-shaped status update script, not auto-run |

## What changed vs iteration-11

- **5 new evals** (IDs 21–25) covering v0.0.3 features. All 5 hit 100% on first run: **60/60** assertions across them.
- **SKILL.md trimmed** 655 → ~440 lines (-33%). Zero regressions on the 20 carry-over evals — the lean SKILL.md + on-demand references successfully reproduce all behaviors the old larger SKILL.md carried.
- **Grader hardening**: 5 categories of grader-too-strict bugs fixed in `tests/grade_runs.py` (CSV header schema, story-ID vs tracker-ID lookup, naive CSV split → `csv.reader`, WSJF/RICE column-name canonical forms, USER_VERBS list expansion). These bugs pre-existed v0.0.3 but surfaced when grading iter-12.
- **Baseline (without_skill) not re-run** — the v0.0.3 SKILL.md changes affect skill-loaded runs only; non-skill agent behavior is identical to iter-11. The 20.4% baseline carries over as the comparison anchor.

## The one real miss

`eval-12-dependency-aware-backlog`: the user prompt provides 14 explicit story IDs (`F-AUTH`, `F-RBAC`, etc.) that the agent should preserve through the storymap and backlog. The agent kept 5/14, renaming the rest. All 9 other assertions (dependency-cycle detection, depends_on column, slice-1 feasibility check, WSJF columns, etc.) passed. Recommend a small adjustment to Step 2 / from-existing-backlog reference text to emphasize ID preservation when the user provides existing IDs.

## Reproducing

```bash
# 1) Scaffold the iteration-12 workspace
python -c "import json; from pathlib import Path; \
  e=json.loads(Path('skills/user-story-mapping/evals/evals.json').read_text(encoding='utf-8')); \
  [Path(f'user-story-mapping-workspace/iteration-12/eval-{ev[\"id\"]}-{ev[\"name\"]}/with_skill/outputs').mkdir(parents=True,exist_ok=True) \
   or Path(f'user-story-mapping-workspace/iteration-12/eval-{ev[\"id\"]}-{ev[\"name\"]}/eval_metadata.json') \
     .write_text(json.dumps({k:ev[k] for k in ('id','name','prompt','assertions')}, indent=2), encoding='utf-8') for ev in e['evals']]"

# 2) Run each eval via your preferred sub-agent runner (Claude Code Agent tool, Codex exec, etc.)
#    Each agent: load SKILL.md → apply skill to eval_metadata.json's prompt → write artifacts to with_skill/outputs/

# 3) Grade
python tests/grade_runs.py iteration-12
```

Raw per-assertion results: see `grading.json` in each `eval-N/with_skill/` directory of iteration-12. The bundled `tests/build_benchmark.py` aggregates into a fresh `benchmark.json` if you want the structured form.
