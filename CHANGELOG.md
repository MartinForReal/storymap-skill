# Changelog

All notable changes to **storymap-skill** are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is [SemVer](https://semver.org/).

## [Unreleased]

### Test infrastructure

- Removed unreachable dead code in `tests/grade_runs.py` (`grade_multi_stakeholder_conflict` had a stray duplicate of `grade_okr_alignment`'s body after its `return`).
- `tests/build_viewer.py` now renders the actual iteration name and eval count in `review.html` instead of hardcoded "iteration 5" / "3 test cases" strings.

## [0.0.6] — 2026-06-28 — compressed runtime docs and explicit plan-stage triggers

### Changed — runtime instruction compression

- Applied a compress-text + SkillOpt pass to `SKILL.md` and all 20 references: **36,088 → 27,430 words** (-24.0%) and **235,061 → 188,220 chars** (-19.9%) while preserving frontmatter, links/anchors, source tags, numeric hard rules, auto-trigger cues, and parser behavior.

### Changed — Plan-stage auto-activation cues

- Clarified Superpowers plan generation, gstack `/plan-dev-design-review` / any `/plan-*-review`, and design-doc plan-adjustment loops explicitly route through this skill.
- Defined `design.md` as a shared framework handoff: if gstack/Superpowers already produced it, this skill mines it as the brief and appends/updates story-map sections instead of overwriting framework-owned content.

## [0.0.5] — 2026-06-16 — items+status manifest always; mode-terminology fully purged

A small but real spec change on top of v0.0.4: every run produces a flat items+status list as a checked-in snapshot, regardless of whether an issue tracker is the system of record. And the legacy "Mode A/B/C/D" terminology is now gone from every working artifact (only [0.0.4] and earlier historical CHANGELOG blocks retain the term, as they describe what was true when those versions shipped).

### Changed — output contract: `storymap.csv` promoted to the always-tier

- **Always produced (was: 2 files in 0.0.4):** `design.md`, `storymap.md`, **`storymap.csv`**.
- **Only when no issue tracker is defined:** `storymap.mmd`, `backlog.md`, `backlog.csv`.
- **Tracker-defined (unchanged from 0.0.4):** opt-in write-back sets each item's burn-down fields (story-points + sprint/iteration + status); the ranked summary moves into `handoff.md`.

Rationale: `storymap.csv` is a *snapshot artifact* (a deterministic 9-column projection of `storymap.md`: id / activity / task / story / persona / outcome / slice / status / status_evidence), not a dynamic dashboard. The 0.0.4 reasoning ("the tracker has the list") under-rated its value as a checked-in items+status manifest, useful even when a tracker is the system of record. `storymap.mmd` and `backlog.{md,csv}` stay tracker-conditional — those *are* live views the tracker subsumes.

Owners updated: SKILL.md § What it produces; output-routing.md § What each branch produces; work-item-tracking.md § Enable the tracker burn-down (clarifies that `storymap.csv` stays alongside the tracker write-back).

### Changed — invocation-mode terminology fully removed

- **Every working artifact** is mode-free: `evals.json` category labels and prompts no longer say "Mode A/B/C/D" (categories are now "From scratch", "From a brief", "From existing backlog", "Iteration — limit-breach detection"); `tests/grade_runs.py` comments + assertion text use "iteration" instead of "Mode D"; `tests/README.md`, `benchmark/benchmark.md`, `examples/README.md` and the snapshot example's `handoff.md` are scrubbed.
- **SKILL.md** drops the defensive "there are no invocation modes" negation — with the term gone everywhere, the negation is no longer load-bearing.
- The 0.0.4 CHANGELOG entry (and older entries in this file) are historical and do reference the term — that's the point of a changelog.

### Test infrastructure

- `tests/grade_runs.py`: `REQUIRED_FILES_CANONICAL = ["design.md", "storymap.md", "storymap.csv"]` (was just the first two). `grade_csv_header` and `grade_first_slice_coverage` are non-tolerant again (`storymap.csv` is required). `grade_mermaid` and `grade_method_columns` stay tolerant-when-absent (`.mmd` and `backlog.csv` are still tracker-conditional).
- The 28-assertion regrade of the three `examples/` bundles continues to pass (snapshot example regenerated its `storymap.csv`).

### Migration notes

- **From 0.0.4:** if you were treating `storymap.csv` as no-tracker-only, you can stop. It's now always there. `storymap.mmd` / `backlog.md` / `backlog.csv` are unchanged from 0.0.4 (still no-tracker-only).
- **Eval / grader consumers:** if you grep eval prompts for "Mode A/B/C/D" you'll find nothing. The behavioral coverage is the same — the eval IDs (1, 2, 3, 16) are untouched.
- **Examples:** the tracker-defined `snapshot-and-breaks-limits` bundle now has `storymap.csv` (regenerated). The other two no-tracker examples are unchanged.

## [0.0.4] — 2026-06-15 — one re-entrant loop, tracker-aware (conditional local artifacts + native burn-down), pre-interview persona simulation, answer-first rewrite

Replaces the prior multi-entry-mode model with a single re-entrant loop, makes the brownfield path genuinely tracker-aware, gates the Mermaid artifact on tracker presence, teaches role simulation to model interactions between personas, and re-authors the whole skill answer-first (Pyramid Principle) with single-ownership de-duplication. No skill capability was removed — prior iteration/refinement behaviors are now loop defaults.

### Changed — invocation model: collapsed to one loop

- **A/B/C/D modes are gone.** `SKILL.md`'s `## Invocation modes` section is replaced by `## The loop`: **discover → diff (vs. existing artifacts/tracker/code) → apply saved preferences → simulate personas → interview until the user approves → backbone → generate/update idempotently → derive + hand off.** The **diff** subsumes the old from-scratch / existing split, and is now defined explicitly: existing = a *reconciled* snapshot (code-vs-tracker conflicts surface as drift, never silently merged), desired = the prior map *amended/overridden* by the user's new input (it can pivot/remove, not just add), and generation **materializes the delta** (∅ diff ⇒ a snapshot, no regeneration).
- **"From scratch" is not a separate flow** — it's the same loop running when the data sources happen to be empty (the diff is against nothing). Step 0.5 reconciliation is reframed as a **no-op** when there's no prior state, not a "skip branch."
- **Mode detection is now a data-source check, decided once.** The "detecting from-scratch" rule in [`output-routing.md`](skills/user-story-mapping/references/output-routing.md) becomes the canonical empty-baseline / "tracker defined" test, reused by the loop, Step 5, and routing — no more guessing a mode from the first message.

### Changed — answer-first structural rewrite (Pyramid Principle + single ownership)

- **The whole skill was re-authored from scratch answer-first.** `SKILL.md` is now a pure routing-and-contract spine (~130 lines): the loop is stated as the answer up top, detail lives only in references. Every reference opens with its conclusion before any procedure.
- **Single-ownership de-duplication.** Each shared rule now lives in exactly one owner and is cross-linked elsewhere (the repo's recurring SKILL.md↔reference drift): the user-input-authoritative priority order + source-tag vocabulary (SKILL.md Rule 1), the "tracker defined" operational test (`output-routing.md`), the cross-cutting/non-backbone rule (`backbone-criteria.md`), the slice-1 mechanics (`slicing-strategies.md`), the decisions-log append-only rule + `state.json` schema (`persistent-knowledge.md`), the persona-interaction protocol (`persona-simulation-and-gap-filling.md`), the tracker-taxonomy reuse (`work-item-tracking.md`), and the auto-trigger cues (`framework-integration.md`).
- All 18 prior references re-authored to use loop terminology consistently; `iterative-refinement-and-snapshots.md` reframed as "the loop on a non-empty baseline."

### Added — tracker-aware brownfield + cross-persona interactions

- **Tracker-taxonomy reuse.** When a tracker is defined, Step 0 pulls its existing taxonomy (epics, components, fix-versions/iterations/cycles, labels, custom fields) and Steps 2–4 reuse it instead of inventing categories; missing categories are *proposed, never auto-created*. New section in [`work-item-tracking.md`](skills/user-story-mapping/references/work-item-tracking.md) ("Align to the existing tracker taxonomy"); the pull is wired into `context-collection.md` §6.
- **Persisted tracker config.** A `tracker` block (type, project key, field `mapping`, taxonomy snapshot) is saved to `.user-story-mapping/state.json` by default and reloaded next run for consistency. New schema in [`persistent-knowledge.md`](skills/user-story-mapping/references/persistent-knowledge.md) §A.
- **Pre-interview persona simulation (cross-persona interactions first).** The loop now runs an explicit **SIMULATE stage (Step 0.3) before the interview** — one in-character subagent per persona surfaces cross-persona handoffs / dependencies / conflicts first, so the interview resolves what surfaced instead of interrogating. Subagents receive the **full persona roster**; aggregation produces a `## Persona interactions` map (in `design-doc-template.md`) that seeds cross-persona `H:` `depends_on` edges and slice-1 feasibility risks. Owned by `persona-simulation-and-gap-filling.md`; the map is refined against the real backbone at Step 2 (`decomposition-and-stories.md`) and lands as edges in `dependency-tracking.md`.
- **Two new references.** [`answer-first-writing.md`](skills/user-story-mapping/references/answer-first-writing.md) (Pyramid Principle for `design.md`/`backlog.md`/`handoff.md` — the `## Bottom line` opener) and [`decomposition-and-stories.md`](skills/user-story-mapping/references/decomposition-and-stories.md) (Step 2 — tasks → per-persona stories, parallel `Agent` sweep, interaction map). Reference count: **20**.
- **Answer-first artifacts.** `design.md`, `backlog.md`, and `handoff.md` now open with a `## Bottom line`; templates in `assets/` carry the opener (plus the `## Persona interactions` table in `design-doc-template.md`).
- **Agent instruction file** for repo contributors: `AGENTS.md` (the canonical guide for all coding agents — Claude Code, Codex, Gemini CLI, Copilot — per the AGENTS.md convention).

### Behavior changes

- **The local data artifacts are now tracker-conditional.** Only `design.md` + `storymap.md` are always produced; `storymap.csv`, `storymap.mmd`, `backlog.md`, and `backlog.csv` are generated **only when no issue tracker is defined**. When an issue tracker is the system of record, the opt-in write-back instead sets each item's native **burn-down fields** — story-points/estimate + sprint/iteration + status — so the tracker's own burn-down chart renders, and the ranked summary moves into `handoff.md`. Rationale: duplicating the plan locally goes stale when the team works in the tracker, and the burn-down belongs where the work is tracked. Owner: `work-item-tracking.md` § Enable the tracker burn-down.
- **Persistence of the tracker config is on by default** (it's project config/pointer, low-risk); Memory MCP write-back remains opt-in.

### Test infrastructure

- `tests/grade_runs.py`: `REQUIRED_FILES_CANONICAL` is now just `design.md` + `storymap.md`; the conditional-artifact graders (`grade_csv_header`, `grade_mermaid`, `grade_method_columns`, `grade_first_slice_coverage`) **pass when their file is absent** (acceptable when an issue tracker is the system of record) and validate when present. Most evals are no-tracker, so the files are present and still validated; coverage is unchanged.

### Migration notes

- **Consumers of the local files:** treat `storymap.csv`, `storymap.mmd`, `backlog.md`, `backlog.csv` as optional — all four are absent whenever an issue tracker is defined (the plan + burn-down live in the tracker). When present, `storymap.csv` is unchanged (still 9 columns since 0.0.3). `design.md` + `storymap.md` are always present.
- **`examples/*`** were aligned to the loop terminology and the answer-first openers; the tracker-defined snapshot example drops its local data files (`storymap.csv`, `storymap.mmd`, `backlog.md`, `backlog.csv`) and shows the burn-down write-back instead (a tracker is the system of record there).

## [0.0.3] — 2026-06-10 — plan-stage auto-trigger, per-persona stories, role hints, progress reconciliation, lean SKILL.md

A combined release covering four bodies of work that landed together: (1) **new workflow capabilities** — Step 0.5 progress reconciliation, Step 2.5 role hints, per-persona slice-1 enforcement, plan-stage auto-trigger, tracker write-back; (2) **structural refactor** — SKILL.md trimmed 655 → ~440 lines (-33%) with all duplicated content moved to references; (3) **5 new eval scenarios** covering the above behaviors (now 25 total); (4) **benchmark validation** at 99.6% with-skill pass rate on iteration-12 (255/256 assertions across 25 evals).

### Added — new capabilities

- **Plan-stage auto-activation** — `SKILL.md` description and new "Auto-activation cues" section in [`framework-integration.md`](skills/user-story-mapping/references/framework-integration.md) make it explicit the skill should self-activate when Superpowers / gstack / GSD enter their Plan stage (e.g., gstack `/office-hours`, GSD `/gsd discuss`, between Superpowers `brainstorming` and `writing-plans`).
- **Step 2 — per-persona story sweep** — every persona in `design.md` must appear as `<persona>` in ≥1 slice-1 story; for ≥3 personas, the skill spawns parallel `Agent` subagents (one per persona) to produce per-persona story sets.
- **Step 2.5 — role hints + flow advice** — new step generates `role-hints.md` with a UX/UI designer half (persona snapshots, flow inventory, friction hotspots, accessibility hints, open UX questions) and an architect half (cross-cutting work index, boundary candidates, hard constraints, risky integrations, open architecture questions).
- **Step 0.5 — progress reconciliation** — new step (existing-project / iteration only) that builds a status view from `prior storymap ⊕ tracker ⊕ code state`. Status taxonomy: `done | in-progress | blocked | deferred | cut | unchanged`. Detects orphan tracker issues, orphan storymap stories, and graduated backbone activities. Annotates `storymap.md` stories with `[status: …]` tags; appends `## Implementation status` and `## Activity status` sections to `design.md`.
- **Storymap → tracker write-back (opt-in)** — Step 6 now generates `tracker-status-update.<ext>` alongside slice-1 routing when Step 0.5 produced status changes the user confirmed. Per-tracker script templates for Jira / Azure DevOps / GitHub / Linear. Never auto-executed; user reviews and runs.
- **Skill chaining for flow advice** — Step 2.5 discovers and invokes installed domain-advisor skills (e.g., `auth-flow-advisor`, `payment-integration-best-practices`, `accessibility-checker`). Cap: 3 advisor invocations per run, separate from the existing 1-per-run cap on sister-framework slash-commands.
- **5 new eval scenarios** (IDs 21–25): `step-0-5-progress-reconciliation`, `per-persona-slice-1-coverage`, `step-2-5-role-hints-generation`, `plan-stage-auto-trigger-gstack`, `tracker-write-back-script-emitted`. Each with 6–13 assertions in `tests/grade_runs.py`. Total = 25 scenarios.
- New reference [`role-hints-and-flow-advice.md`](skills/user-story-mapping/references/role-hints-and-flow-advice.md) — Step 2.5 templates, skill-discovery protocol, advisor invocation patterns.
- New reference [`progress-reconciliation.md`](skills/user-story-mapping/references/progress-reconciliation.md) — Step 0.5 algorithm, status taxonomy, conflict-resolution table, per-tracker write-back script templates.
- New reference [`backbone-criteria.md`](skills/user-story-mapping/references/backbone-criteria.md) — absorbs the Step 1 explanatory prose, "why this matters", and common anti-patterns previously inlined in SKILL.md.

### Changed — structural refactor (lean SKILL.md)

The structural refactor was driven by a code review that flagged ~40% SKILL.md ↔ reference duplication. Three drift incidents in the same release cycle (caught manually) were symptoms. The fix: shrink SKILL.md to a routing-and-contract spine; expand the per-step references so they're self-contained.

- `SKILL.md` Step 0 body: 106 → 17 lines (loop algorithm, starter signals, branch-conditional sources, exit conditions, worked traces moved to `context-collection.md`)
- `SKILL.md` Step 0.4 body: 67 → 14 lines (gap classification table + resolution rules moved to `persona-simulation-and-gap-filling.md`)
- `SKILL.md` Step 1 body: 47 → 23 lines (workflow narrative + why-it-matters + per-criterion explanations moved to `backbone-criteria.md`; six-criteria table stays inline)
- `SKILL.md` Step 2 body: 37 → 14 lines (parallel-agent protocol prose compressed; per-persona enforcement rule stays inline)
- `SKILL.md` Step 2.5 body: 38 → 12 lines (`role-hints.md` template + skill-chaining protocol moved to `role-hints-and-flow-advice.md`)
- `SKILL.md` frontmatter `description`: 1768 → ~880 chars (drops the long trigger-keyword list and the per-command sister-framework enumeration; preserves the auto-activate signals + use-case framing)
- `SKILL.md` "What this skill does" lists `role-hints.md` as the optional 4th artifact and reframes the chain as "test playbook in three levels of refinement"
- `SKILL.md` Performance hard rule 8 distinguishes sister-framework chaining (1/run) from domain-advisor chaining (≤3/run)
- `SKILL.md` per-stage matrix gains a Step 0.5 row; existing-project and iteration runs now mandate reconciliation before backbone work
- `SKILL.md` References table at the end: added `backbone-criteria.md` row
- `framework-integration.md` per-framework hand-off lines reference `role-hints.md`§UX and `role-hints.md`§Architect where applicable; gstack `/plan-design-review` and `/plan-eng-review` mappings sharpened
- `iterative-refinement-and-snapshots.md` opens with "iteration runs always start with Step 0.5" and the snapshot template gains an Implementation-status table sourced from reconciliation
- `work-item-tracking.md` opening callout disambiguates seed-from-scratch (storymap is authoritative) vs reconciliation write-back (tracker authoritative for status, storymap for intent)
- [`persona-simulation-and-gap-filling.md`](skills/user-story-mapping/references/persona-simulation-and-gap-filling.md) gained a new opening section on gap criticality classification (blocking / stage-local / deferrable), resolution rules per class, mid-stage discovery, late-stage escalation
- [`context-collection.md`](skills/user-story-mapping/references/context-collection.md) gained "Surface findings in design.md" example (Context loop trace + Contradictions flagged), cost-ceiling and override sub-sections, "What this gets right" worked cases
- `plugin.json` keywords gain `personas`, `test-playbook`, `ux-hints`, `architect-hints`, `plan-stage`, `superpowers`, `gstack`, `gsd`

### Removed

- ~210 lines of duplicate content between SKILL.md and references (Step 0 algorithm, Step 0.4 gap classification, Step 1 explanatory prose, Step 2.5 role-hints template, Step 2 parallel-agent details — all live in references now)

### Behavior changes

- **Per-persona coverage is mandatory.** Slice 1 must include ≥1 story per persona named in `design.md`. A persona with zero candidate slice-1 stories is a forced re-check of Step 1 or Step 3, not a silent omission.
- **`role-hints.md` is generated by default** when ≥1 persona faces a UI surface AND ≥1 backbone activity touches a non-trivial system boundary. Skipped only for solo / pre-PMF / pure-infra cases.
- **Step 0.5 runs automatically for existing-project and iteration invocations.** Storymap stories matching closed tracker issues + shipped code are marked `done`; activities with all stories done graduate out of active slicing. Drift (orphan tracker items, status conflicts) gets surfaced in `handoff.md`, never silently absorbed.
- **Tracker write-back is opt-in and scripted.** Reading state is always safe; pushing storymap-driven status changes (cuts, re-slices) emits a runnable script that the user reviews before executing.
- **`storymap.csv` schema gained `status` + `status_evidence` columns** (9 columns total, was 7). The bundled `scripts/storymap_to_csv.py` parses `[status: <state> | <evidence>]` tags from storymap.md. The grader (`tests/grade_runs.py`) accepts both 7- and 9-column schemas for back-compat.

### Test infrastructure improvements

- `tests/grade_runs.py` gained 5 new dispatch branches (evals 21–25) + several robustness fixes discovered during iteration-12 grading: (1) CSV header check accepts both legacy 7-col and current 9-col schema; (2) eval-21/25 ID lookups use tracker IDs (PROJ-101..PROJ-112 / CMS-106..107) instead of skill-internal story IDs (which don't appear in storymap.md prose); (3) eval-22 CSV parsing switched from naïve `line.split(",")` to `csv.reader` (handles quoted commas in story column); (4) `grade_method_columns` for WSJF/RICE accepts both prefixed (`wsjf_value`/`rice_reach`) and canonical SAFe/RICE forms (`user_business_value` / `reach`); (5) USER_VERBS regex expanded with `mint`, `provision`, `grant`, `revoke`, `enable`, `disable`, `switch`, `fetch`, `push`, `pull`, `run`, `build`, `debug`, `profile`, `inspect`, `sync`, `reset`, `rotate`.

### Benchmark (iteration-12, all 25 evals)

| Configuration | Pass rate | vs iter-11 (v0.0.2) |
|---|---|---|
| **with_skill** (v0.0.3) | **99.6% (255/256)** | +1.3 pp |
| without_skill (carried over from iter-11) | 20.4% | — |
| **Δ** | **+79.2 pp** | — |

Only 1 real miss across 25 evals: `eval-12-dependency-aware-backlog` (9/10 — the agent preserved 5/14 of the user-provided story IDs instead of all 14; the other 13 assertions including dependency-cycle detection passed). All 5 new evals (21–25) hit 100% (60/60 assertions) on first run, confirming the new behaviors work end-to-end.

### Migration notes

- **CSV consumers** that depend on the legacy 7-column `storymap.csv` schema need to add two trailing columns (`status, status_evidence`) or ignore them. Both new columns are empty strings when no `[status:]` tag is present, preserving backward compatibility for from-scratch and pre-Step-0.5 runs.
- **Existing iteration-N baselines** in `user-story-mapping-workspace/` were generated against the old SKILL.md shape and the old eval set. The published iteration-12 baseline is the new reference. Earlier iterations are still valid for v0.0.2 regression checks; for v0.0.3 use iteration-12.

## [0.0.2] — 2026-06-09 — output-routing decision

Adds an explicit decision branch for *where* the generated items physically land, so the agent stops defaulting to "push to a tracker" on mature projects with curated backlogs.

### Added
- New reference [`skills/user-story-mapping/references/output-routing.md`](skills/user-story-mapping/references/output-routing.md) — the from-scratch vs existing detection rule + the three-destination persistence cascade (sister-framework state → `TODO.md` → Memory MCP) with `TodoWrite` as an orthogonal in-session execution helper.
- Two new evals (#19 `output-routing-from-scratch`, #20 `output-routing-existing-cascade`) in [`skills/user-story-mapping/evals/evals.json`](skills/user-story-mapping/evals/evals.json) with matching grader handlers in [`tests/grade_runs.py`](tests/grade_runs.py). Eval suite is now 20 scenarios (was 18).
- New `TODO.md` row schema (persona / score / depends-on / dated section header) for projects without sister-framework state.

### Changed
- `SKILL.md` Step 6 now leads with `Route the items first` instead of asking "where should this go?" at handoff — the from-scratch / existing decision is explicit.
- `SKILL.md` "Pushing the artifacts into a tracker" renamed to `Where the artifacts land`; the per-tracker mapping bullets remain authoritative in [`work-item-tracking.md`](skills/user-story-mapping/references/work-item-tracking.md).
- Callouts at the top of `work-item-tracking.md` and inside `framework-integration.md` flag the routing decision before readers jump to per-tool mechanics.
- README "What it does" gains an *Output routing* bullet.

### Behavior change
- **From-scratch (empty/near-empty repo, no tracker mentioned, no framework state)** → generates a tracker import script via `work-item-tracking.md`; writes a thin `.user-story-mapping/state.json` for iteration continuity; does not also populate `TODO.md` (the tracker is the system of record).
- **Existing project** → walks the persistence cascade (sister-framework state → `TODO.md` → Memory MCP); does not push to a populated tracker without explicit user opt-in. `TodoWrite` is opt-in pairing for when the user is about to execute slice 1.

## [0.0.1] — 2026-06-08 — initial public release

First public release. The skill was built and validated over 11 internal iterations before being shipped here as a single commit.

### Skill capabilities
- Conforms to the [Agent Skills v1 specification](https://agentskills.io/specification) — works in Claude Code and any compatible host (Cursor, Codex CLI, Goose, Letta, Roo, Kiro, OpenCode, ~30 others)
- Four invocation patterns: from-scratch / from-brief / from-backlog / iterative refinement
- Adaptive Step 0 context loop that mines: README, code, tests, ADRs, commit log, work-item trackers (Jira/ADO/GitHub/Linear via MCP), sister-framework state (`.gsd/`, `.superpowers/`), and prior `design.md` — before asking the user
- Customer-interview synthesis with verbatim-quote preservation
- Persona-simulation subagents that fill gaps and surface stakeholder conflicts (user-input-authoritative — simulated voices never override the actual user)
- Six-criterion backbone definition (frame / persona perspective / time horizon / granularity / scope / aggregation), user-confirmed and recorded for reproducibility across runs
- Three slicing strategies (Patton walking-skeleton/MVP/R2/R3, SAFe PI, Now/Next/Later)
- Three prioritization methods (WSJF / RICE / MoSCoW)
- Dependency tracking with cycle detection and slice-1 feasibility check
- OKR alignment with coverage matrix and orphan-KR / orphan-story surfacing
- Given/When/Then acceptance criteria + INVEST check for slice-1 stories
- Backbone-as-E2E-contract: coverage matrix + happy-path scenario + per-activity verification
- Iteration limit-breach detection (capacity / dependencies / OKR coverage / scope) — surfaces trade-offs rather than silently absorbing breaches
- Performance hard rules (50-story cap, slice-1 ≤ 15, 80% turn-budget stop) preventing truncation before backlog generation
- Opt-in persistent memory (`.user-story-mapping/state.json` or MCP memory server)
- Skill chaining — invokes other installed skills (code-explorer, db-analyzer, etc.) for context gathering

### Distribution
- **Claude Code plugin format** — repo is a self-contained marketplace via `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`. Install with:
  ```
  /plugin marketplace add martinforreal/storymap-skill
  /plugin install storymap-skill@storymap-skill
  ```
- **Raw `.skill` bundle** for non-Claude-Code hosts — built by CI on tag push and attached to each GitHub release; can also be built locally with `python scripts/build_skill_bundle.py`
- **Manual install** — copy `skills/user-story-mapping/` into the host's skills directory (e.g. `~/.claude/skills/`)

### Benchmark
- **with-skill: 171/174 (98.3%)** across 18 evaluation scenarios × 2 configurations
- **baseline (no skill): 35/174 (20.1%)**
- **Δ: +78.2 percentage points** (~4.9× quality improvement for ~33% more tokens)
- Mean duration: 554s with-skill vs 236s baseline
- Mean tokens: 215,947 with-skill vs 162,905 baseline
- Per-eval breakdown + analyst notes: [`benchmark/benchmark.md`](./benchmark/benchmark.md)
- Raw data: [`benchmark/benchmark.json`](./benchmark/benchmark.json)
- Regenerate locally: `bash tests/run-benchmark.sh`

### Eval coverage
- 6 structural evals — modes A/B/C × 3 framework integrations (Superpowers, gstack, GSD)
- 5 app-type evals — pure API/SDK, desktop, enterprise multi-tenant SaaS, CLI, mobile B2C
- 5 capability evals — customer interview synthesis, dependency tracking, OKR alignment, persona-simulation gap discovery, multi-stakeholder conflict
- 3 advanced behavior evals — iteration snapshot + breach detection, empty-dir loop short-circuit, framework-artifact mining + backbone criteria

### Repo layout
- `skills/user-story-mapping/` — the skill itself (SKILL.md + 14 references + 4 assets + 2 scripts + 18 evals)
- `.claude-plugin/` — Claude Code plugin manifest + marketplace
- `examples/` — sample outputs from 3 scenarios
- `tests/` — benchmark infrastructure (grader + benchmark builder + viewer builder + setup script)
- `benchmark/` — published benchmark.json + benchmark.md
- `scripts/build_skill_bundle.py` — builds the `.skill` bundle locally
- `.github/workflows/release.yml` — CI: builds and attaches `.skill` to each tagged release

[0.0.1]: https://github.com/MartinForReal/storymap-skill
