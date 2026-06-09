# Benchmark — user-story-mapping (iteration 11)

## Summary

| Configuration | Pass rate | Duration (s) | Tokens |
|---|---|---|---|
| **with_skill** | 98.2% ± 4.1% | 554 ± 209 | 215947 ± 15730 |
| without_skill | 20.4% ± 17.2% | 236 ± 107 | 162905 ± 3773 |
| **Δ (with − without)** | **+77.8pp** | +319s | +53042 |

## Per-eval

| Eval | with_skill | without_skill |
|---|---|---|
| from-scratch-internal-tool | 10/10 (879s, 252,381 tok) | 0/10 (340s, 169,342 tok) |
| mobile-consumer-fitness | 8/9 (703s, 218,740 tok) | 0/9 (401s, 168,185 tok) |
| customer-interview-synthesis | 10/10 (758s, 234,828 tok) | 3/10 (317s, 162,537 tok) |
| dependency-aware-backlog | 10/10 (640s, 215,323 tok) | 3/10 (248s, 165,399 tok) |
| okr-aligned-roadmap | 10/10 (522s, 225,609 tok) | 2/10 (228s, 165,415 tok) |
| thin-brief-gap-discovery | 10/10 (362s, 212,052 tok) | 0/10 (191s, 163,335 tok) |
| multi-stakeholder-conflict | 10/10 (538s, 229,114 tok) | 3/10 (237s, 164,086 tok) |
| snapshot-and-breaks-limits | 8/8 (178s, 183,281 tok) | 6/8 (139s, 157,834 tok) |
| empty-dir-loop-shortcircuit | 8/9 (338s, 203,608 tok) | 2/9 (172s, 159,196 tok) |
| framework-artifacts-and-criteria | 10/10 (417s, 208,251 tok) | 3/10 (150s, 160,149 tok) |
| from-problem-brief-mobile-onboarding | 10/10 (456s, 211,674 tok) | 2/10 (204s, 164,202 tok) |
| from-existing-backlog-messy-csv | 10/10 (403s, 203,057 tok) | 2/10 (78s, 157,430 tok) |
| gstack-handoff-developer-portal | 10/10 (479s, 210,583 tok) | 1/10 (210s, 167,800 tok) |
| gsd-handoff-solo-builder-saas | 11/11 (567s, 207,812 tok) | 3/11 (92s, 158,266 tok) |
| pure-api-sdk-python | 9/9 (787s, 214,159 tok) | 1/9 (120s, 159,122 tok) |
| desktop-password-manager | 9/9 (292s, 198,419 tok) | 1/9 (324s, 164,133 tok) |
| enterprise-analytics-multitenant | 9/10 (893s, 232,166 tok) | 2/10 (460s, 165,962 tok) |
| cli-log-parser | 9/9 (768s, 225,986 tok) | 1/9 (334s, 159,897 tok) |

## Analyst notes

- Iteration 11 — full 18-eval benchmark against the v1.3.0 skill (now in claude-code plugin format). With-skill 171/174 (98.3%) vs baseline 35/174 (20.1%). 4.9x improvement, +0.6pp over iter-10.
- All 6 structural evals (modes A/B/C + 3 framework integrations) score 10/10+ with-skill (eval-5 GSD: 11/11).
- All 5 app-type evals (API, desktop, enterprise, CLI, mobile B2C) score 8-9/9. Baselines hit 0-2/9 — the skill's value is structural conformance the baseline can't replicate.
- 5 capability evals (interview synthesis, dependency tracking, OKR alignment, persona-sim, multi-stakeholder) all score 10/10 with-skill.
- 3 advanced behavior evals (Mode D snapshot+breaches, empty-dir loop short-circuit, framework artifacts + backbone criteria) score 8/8, 8/9, 10/10. The loop short-circuit eval (17) used 1 Bash call total — the rest of the budget went to ADHD persona simulation.
- Eval-16 (Mode D + breach detection) has the smallest with/baseline gap: 8/8 vs 6/8. Because the prompt explicitly demanded breach surfacing, even baseline did well. The skill's value lies in *consistent* breach detection across less-structured prompts.
- Token usage: with-skill mean ~216K vs baseline ~163K (~33% more tokens for ~5x quality). Duration with-skill mean ~554s vs baseline ~236s.
- Three with-skill runs took small dings: eval-10 mobile (8/9 — 51 stories, +1 over the 50-story soft cap), eval-17 loop short-circuit (8/9 — Now/Next/Later signals partially matched), eval-8 enterprise (9/10 — single backbone-coverage check tripped). All within tolerance.
- Three baseline runs scored above their typical 0-2/N range: eval-11 (3/10 — verbatim quote preservation when the prompt has long quotes inline), eval-16 (6/8 — user explicitly demanded breach surfacing), eval-18 (3/10 — .gsd/ files were readable and the baseline read them). When prompts are explicit and inputs are structured, baselines do better; when prompts are sparse, baseline collapses (eval-1: 0/10, eval-10: 0/9, eval-14: 0/10).
- Plugin-format restructure (v1.3.0) preserved skill quality — iter-11 numbers are equal-to-better than iter-10's, confirming the move to skills/user-story-mapping/ + .claude-plugin/ marketplace.json did not regress behavior.

## Coverage updates since iter-11

The eval suite has grown from 18 → 20 scenarios. Two new evals exercise the explicit output-routing decision added in v0.0.2:

- **eval-19 — output-routing-from-scratch** — verifies the skill detects an empty/near-empty repo + no tracker mentioned + no framework state, generates a tracker import script for the from-scratch branch (does not auto-run it), references `.user-story-mapping/state.json` for Mode-D continuity, and does NOT designate `TODO.md` as the primary destination.
- **eval-20 — output-routing-existing-cascade** — verifies the skill detects an existing project (populated tracker mentioned + 800+ commits), routes to the keep-in-place cascade, writes slice-1 to `TODO.md` at the repo root, honors the user's explicit no-tracker constraint (no `gh issue create` / no bulk import), and names `TODO.md` in the handoff line.

Grader handlers live in [tests/grade_runs.py](../tests/grade_runs.py) as inline branches off `grade_run()` for `eval_id == 19` and `eval_id == 20`. Next benchmark iteration will pick up the 20-eval baseline.
