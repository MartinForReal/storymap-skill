---
name: user-story-mapping
description: Run user story mapping (Jeff Patton style) — turns a vague goal, brief, or messy backlog into a sliced delivery plan with per-persona user stories that act as the blueprint for the team's test playbook (acceptance criteria + E2E contract). Mines existing context first (README, code, tests, issue tracker via MCP) and reuses the tracker's own taxonomy. Produces a design doc, a story map (Markdown + CSV, plus Mermaid when no tracker is defined), a prioritized backlog (WSJF / RICE / MoSCoW), and optional role-hints for UX/UI + architect. Auto-activates when a sister framework enters its Plan stage — Superpowers between `brainstorming` and `writing-plans` / plan generation, gstack `/office-hours` / `/autoplan` / `/plan-*-review` including `/plan-dev-design-review`, or GSD `/gsd discuss` / `/gsd plan-milestone` / Brief / Roadmap authoring. Also activate when a design doc has been generated and the plan is being adjusted. Use when shaping work (discovery, MVP scoping, "what should we build first", PI planning, organizing a backlog, "stories per persona"). Skip for pure engineering — bug fixes, refactors, code review, deploy debugging.
license: MIT
compatibility: Requires Python 3.10+ for bundled scripts (storymap_to_csv.py, storymap_to_mermaid.py). No other system dependencies. Works across Claude Code, Claude.ai, and any Agent Skills v1 host (Cursor, Codex, Copilot, Gemini CLI, OpenCode, Goose, etc.).
metadata:
  author: MartinForReal
  version: "0.0.6"
  homepage: https://github.com/MartinForReal/storymap-skill
allowed-tools: Bash(python:*) Read Write Edit Glob Grep Agent Skill
---

# User Story Mapping

Turns a vague goal, brief, or messy backlog into a **sliced, prioritized delivery plan** of per-persona user stories — the team's **test playbook in skeletal form**: every backbone activity becomes an E2E swimlane, every slice-1 story ≥1 Gherkin scenario (Steps 4a/4b). Runs as **one re-entrant loop**.

This file is the answer-first spine — the routing-and-contract layer. Read it once at invocation; load a step's reference only on reaching that step; never pre-read a reference or read one twice.

## The loop

Each run discovers what exists, diffs it against the desired map, and **materializes the delta** in place. **From scratch is the same loop with empty data sources** — the diff is against nothing, so the delta is the whole map. No greenfield/brownfield branch; only the data differs, never the steps.

```
① DISCOVER → ② DIFF → ③ APPLY PREFERENCES → ④ SIMULATE → ⑤ INTERVIEW ──approved?──no──► back to ①
                                                                       │ yes
                                                                       ▼
                                          ⑥ BACKBONE → ⑦ GENERATE/UPDATE → ⑧ DERIVE + HAND OFF
```

**Loop ↔ Step** (table below): ①=Step 0, ②=Step 0/0.5, ③=Step 0 (saved prefs), ④=Step 0.3, ⑤=Step 0.4, ⑥=Step 1, ⑦=Steps 2–4b, ⑧=Steps 5–6.

1. **Discover** (Step 0) — scan data sources cheapest-first; the issue tracker (issues + taxonomy), `.user-story-mapping/state.json`, and any framework-owned `design.md` are first-class. The scan assembles the **existing** source.
2. **Diff** — **existing** (a *reconciled* snapshot, not a clean merge: tracker = status, code = evidence that can *contradict* → drift, storymap = intent, user overrides all) vs **desired** (the prior map *amended/overridden* by the user's new input — add / re-slice / **pivot-remove**). Classifies ADDED / UNCHANGED / MOVED / CUT / DONE **+ surfaced conflicts** — conflicts become decisions in `handoff.md`, never silently resolved. Empty existing ⇒ all new. Coarse here, per-story at handoff. Owner: [`iterative-refinement-and-snapshots.md`](references/iterative-refinement-and-snapshots.md).
3. **Apply preferences** — method, slicing, terminology, tracker field-mapping from `state.json`; the user's words this conversation override saved state.
4. **Simulate** (Step 0.3) — when there are personas to model, run one in-character subagent per persona (full roster to each) to surface **cross-persona interactions first** (handoffs / dependencies) plus conflicts and unfillable gaps → first-pass `## Persona interactions` map + conflict matrix in `design.md`. Conditional; trivial for a single specified persona.
5. **Interview until approved** (Step 0.4) — present the simulation findings + the diff, resolve *blocking* gaps/conflicts, loop to ① until the user approves. User wins over simulation; nothing to resolve ⇒ a fast confirm. No backbone work before approval.
6. **Backbone** (Step 1) — only after approval; carry a prior backbone forward, never silently re-derive.
7. **Generate / update** (Steps 2–4b) — **materialize the diff's delta**: per-persona stories, slices, prioritization, ACs, E2E. ∅ existing ⇒ author the whole map; a clean delta ⇒ update only it; **∅ diff ⇒ a snapshot, no regeneration**. Idempotent; reuse the tracker's taxonomy.
8. **Derive + hand off** (Steps 5–6) — **always** create-or-update `design.md` + `storymap.md` + `storymap.csv` (the flat items+status list, derived from `storymap.md`); if `design.md` came from gstack/Superpowers, preserve its framework-owned sections and append/update only the story-map addendum (bottom line, context trace, persona interactions, decisions). The ranked-backlog views (`backlog.md`, `backlog.csv`) and visualization (`storymap.mmd`) are **only when no tracker is defined**; when a tracker *is* defined the opt-in write-back sets burn-down fields (points + sprint + status) instead. Persist `state.json`; emit a diff-style `handoff.md`.

**"Tracker defined"** (gates the local renderings, `storymap.mmd`, and the burn-down write-back): true when a tracker MCP is connected for this work, the user points the skill at a specific tracker/project, or `state.json` already holds a `tracker` block. Operational test (and why a passing mention of a tool used elsewhere doesn't count): [`output-routing.md`](references/output-routing.md#detecting-the-empty-baseline-no-tracker-defined).

**Auto-trigger** when a sister framework enters its Plan stage — Superpowers (between `brainstorming` and `writing-plans`, or while generating a plan), gstack (`/office-hours`, `/autoplan`, `/plan-*-review`, including `/plan-dev-design-review`), GSD (`/gsd discuss`, `/gsd plan-milestone`, authoring `.gsd/Brief.md` / `Roadmap.md`), or when a design doc exists and the plan is being adjusted. Signal: "the user is shaping work, not coding it" — propose this skill rather than hand-drafting stories. Detail: [`framework-integration.md`](references/framework-integration.md).

## When to use

**Use** when the user is **shaping work**: a vague problem with no plan, an unnavigable backlog, MVP scoping, PI planning, "what should we build first", "stories per persona". **Skip** pure engineering — bug fixes, refactors, code review, deploy debugging, "explain this code."

## What it produces

- **Always:** `design.md` (created if absent; if supplied by gstack/Superpowers, augmented in place without clobbering framework-owned sections), `storymap.md` (the authored narrative — the source the parser/import reads), and `storymap.csv` (the **flat list of every item with its status** — id / activity / task / story / persona / outcome / slice / status / status_evidence; a deterministic projection of `storymap.md` via the bundled parser, a checked-in snapshot regardless of where the dynamic plan lives).
- **Only when no tracker is defined:** `storymap.mmd`, `backlog.md`, `backlog.csv` — the visualization and ranked-backlog views, redundant once a tracker is the system of record. (Canonical statement of the rule; the steps table and derived-file commands just reference it.)
- **When a tracker is defined:** instead of those files, the opt-in tracker write-back sets each item's **burn-down fields** — story-points/estimate + sprint/iteration + status — so the tracker's native burn-down works; the ranked "start here" essence moves into `handoff.md`. Mechanics: [`work-item-tracking.md`](references/work-item-tracking.md).
- **Optional:** `role-hints.md` (Step 2.5), `slice-1-acceptance-criteria.md` (4a), `e2e-test-contract.md` (4b), `tracker-status-update.<ext>` (Step 6 write-back), `handoff.md`.
- **State:** `.user-story-mapping/state.json` — saved preferences + the `tracker` config block (on by default; cross-session Memory MCP is an opt-in second backend — see [`persistent-knowledge.md`](references/persistent-knowledge.md)).

Templates and column schemas live in `assets/` — use them, don't hand-roll. The story-map → ACs → E2E-contract chain is deliberate: one test playbook at three levels of refinement, not a one-shot spec.

## Rules that govern every run

1. **User-input-authoritative.** What the actual user told you this conversation always wins; lower sources fill gaps, never override. Priority (high→low): (1) the user, (2) interview verbatim, (3) approved memory, (4) mined context, (5) simulated persona, (6) inference. **Tag every fact in `design.md`** with its source — `[user-stated]` `[interview: <name>]` `[memory: <date>]` `[code: <path>]` `[tracker: <id>]` `[skill: <name>]` `[simulated: <name>]` `[inferred]`. This priority order and tag vocabulary are defined here once; references cross-link, never re-list. *Wrong:* simulated-Compliance argues for RBAC, you add it over the user's explicit "no RBAC in PI 1." *Right:* log the objection as a future-slice risk; the user's stance ships.
2. **Slice 1 covers every backbone activity — and every persona.** The first slice includes ≥1 story from every *active* backbone activity (what makes a map a map, not a backlog) **and** ≥1 story per persona named in `design.md`. A gap means re-slice (Step 3) or re-derive (Step 1) — never a silent drop. Mechanics + violations: [`slicing-strategies.md`](references/slicing-strategies.md).
3. **Answer-first artifacts.** `design.md` / `backlog.md` / `handoff.md` each open with a `## Bottom line` — the answer, then the arguments, then the evidence (Pyramid Principle). Detail: [`answer-first-writing.md`](references/answer-first-writing.md).
4. **Cross-cutting work isn't backbone.** Tech debt, infra, localization, theming, observability, compliance go in a `## Non-backbone / cross-cutting` section — prioritized in `backlog.csv`, excluded from slice-1 coverage. The "can you write 'As a `<user>`…' tied to one backbone column?" test and the `### Theme:` encoding: [`backbone-criteria.md`](references/backbone-criteria.md).
5. **Guardrails — hitting one means stop and re-scope, not "try" to honor:** ≤50 stories total, slice-1 ≤15; backbone 5–7 activities (hard max 10); context loop ≤20 tool calls and <15% budget; ~200K total budget with an **80% turn-budget stop** (write what you have, defer the rest in `handoff.md`); skill-chaining ≤1 sister-framework + ≤3 domain-advisor per run; use the bundled scripts for derived files; Glob/Grep before Read; batch independent tool calls.

## Quick reference — route the ask to a reference

| If the user… | Load |
|---|---|
| Has only a verbal idea, no PRD/code/backlog | `discovery-questions.md` |
| Pastes raw interview notes / call transcripts | `customer-interview-synthesis.md` |
| Has a codebase + `.gsd/` or prior `design.md` | `context-collection.md` — mine first, don't re-ask |
| Says "extend my prior storymap" / "what changed since last PI" | `iterative-refinement-and-snapshots.md` |
| Has shipped stories, or a tracker that's drifted | `progress-reconciliation.md` (Step 0.5) |
| Has conflicting stakeholders, or ≥3 personas (simulate cross-persona interactions before the interview) | `persona-simulation-and-gap-filling.md` + `decomposition-and-stories.md` |
| Wants role hints (UX/architect) or flow advice | `role-hints-and-flow-advice.md` (Step 2.5) |
| Asks "what to build first" / names WSJF/RICE/MoSCoW | `slicing-strategies.md` + `prioritization-frameworks.md` |
| Has OKRs/KRs, or story dependencies | `okr-alignment.md` / `dependency-tracking.md` |
| Wants ACs / E2E scenarios | `acceptance-criteria.md` + `e2e-verification-and-contract.md` |
| Wants stories pushed somewhere | `output-routing.md`, then `work-item-tracking.md` |
| Working inside Superpowers / gstack / GSD | `framework-integration.md` |

## The steps

Load the reference when you reach the step. Budgets are % of the run; Steps 0.3 (simulate) and 0.5 (reconcile) are trivial/no-ops when there are no personas to model or no prior state.

| Step | Purpose | Output | Budget | Reference |
|---|---|---|---|---|
| **0** Discover | Hypothesis-driven mining of cheap→conditional sources; the scan IS the diff-baseline + tracker-defined determination | `## Context loop trace` + `## Contradictions flagged` in `design.md` | <15% | `context-collection.md` |
| **0.3** Simulate | One in-character subagent per persona (full roster); surface **cross-persona interactions** + conflicts + gaps; conditional (≥2 personas) | `## Persona interactions` + conflict matrix + gap inventory in `design.md` | 10-15% | `persona-simulation-and-gap-filling.md` |
| **0.4** Interview→approval | Present simulation findings + the diff; classify gaps; gate on blocking; **loop until approved** | gap resolutions + decisions log | 5-10% | `persona-simulation-and-gap-filling.md` |
| **0.5** Reconcile | Status map from tracker ⊕ code ⊕ prior storymap; graduations; drift; opt-in write-back | `## Implementation status` + `[status: …]` tags | 5-10% | `progress-reconciliation.md` |
| **1** Backbone | Left-to-right activities in user voice; six declared criteria; cross-cutting separate | `storymap.md` backbone | 5-10% | `backbone-criteria.md` |
| **2** Decompose | Tasks → per-persona stories; mandatory per-persona coverage; parallel `Agent` sweep when ≥3 personas; interaction map | `storymap.md` body | 15-20% | `decomposition-and-stories.md` |
| **2.5** Role hints | `role-hints.md` (UX + architect) + flow-advisor skill chaining | `role-hints.md` | 10-15% | `role-hints-and-flow-advice.md` |
| **3** Slice | Patton / PI / Now-Next-Later; **slice 1 covers every backbone activity**; slice onto existing fix-versions when a tracker is defined | slice tags | 5% | `slicing-strategies.md` |
| **4** Prioritize | WSJF/RICE/MoSCoW + OKR linkage + dependency feasibility; reuse existing tracker score fields | `backlog.csv` + `backlog.md` (no tracker) · tracker points/iteration fields (tracker) | 15-20% | `prioritization-frameworks.md`, `okr-alignment.md`, `dependency-tracking.md` |
| **4a** ACs | Given/When/Then for slice-1 + INVEST | `slice-1-acceptance-criteria.md` | 10-15% | `acceptance-criteria.md` |
| **4b** E2E contract | Coverage matrix + E2E-HAPPY + per-activity scenarios — the test playbook | `e2e-test-contract.md` | 5-10% | `e2e-verification-and-contract.md` |
| **5** Derive | `storymap.csv` (always — the flat items+status list) + `storymap.mmd` (only when no tracker) via the bundled scripts | derived files | <2% | scripts in `scripts/` |
| **6** Hand off | Answer-first `handoff.md`; route items; persist `state.json`; opt-in write-back — sets tracker **burn-down fields** (points + sprint + status) when a tracker is defined | `handoff.md` (+ tracker write-back) | 5% | `output-routing.md`, `work-item-tracking.md`, `answer-first-writing.md`, `persistent-knowledge.md` |

**Glossary for first-use jargon in the table:** *Walking skeleton* — a slice that demos every backbone activity end-to-end, even if every step is minimal. *PI* — SAFe Program Increment, typically 8–12 weeks. *WSJF* — Weighted Shortest Job First (cost-of-delay ÷ job-size; SAFe default). *RICE* — Reach × Impact × Confidence ÷ Effort. *MoSCoW* — Must / Should / Could / Won't. *INVEST* — Independent / Negotiable / Valuable / Estimable / Small / Testable.

Derived-file commands (Step 5):
```bash
# Always — the flat items+status list (a deterministic projection of storymap.md):
python scripts/storymap_to_csv.py storymap.md > storymap.csv

# Only when no tracker is defined (with a tracker, push burn-down fields instead — see work-item-tracking.md):
python scripts/storymap_to_mermaid.py storymap.md > storymap.mmd
```

## A good run

Backbone reads aloud as a coherent user story · slice 1 is demoable end-to-end · every story has a persona + outcome · priorities carry *reasoning*, not just numbers · `design.md` states the question being answered and every fact is source-tagged · narrative artifacts are answer-first.

**Avoid:** system-shaped backbones (Login / Database / API), one giant slice called "MVP", skipping `design.md`, letting simulated personas override the user, hand-writing CSV/Mermaid when the scripts exist, generating 80+ stories then running out of turns.

## References (load on demand, don't pre-read)

| File | When to read |
|---|---|
| `discovery-questions.md` | Sparse/empty input — drive discovery via batched questions |
| `customer-interview-synthesis.md` | Raw interview notes / call transcripts in the input |
| `context-collection.md` | Step 0 — what to mine from each source; the diff-baseline determination |
| `persona-simulation-and-gap-filling.md` | Step 0.3/0.4 — pre-interview persona simulation (cross-persona interactions + conflicts) + the gap gate |
| `persistent-knowledge.md` | Step 0 / Step 6 — memory + the saved `tracker` config across runs |
| `iterative-refinement-and-snapshots.md` | The diff (existing vs desired) + the loop on a non-empty baseline — extend, breach-detect, per-stage matrix |
| `progress-reconciliation.md` | Step 0.5 — storymap ↔ tracker status ↔ code sync |
| `backbone-criteria.md` | Step 1 — six-criteria options, cross-cutting rule, anti-patterns |
| `decomposition-and-stories.md` | Step 2 — tasks → per-persona stories, coverage, parallel sweep, interactions |
| `role-hints-and-flow-advice.md` | Step 2.5 — UX/architect hints, flow-advisor chaining |
| `slicing-strategies.md` | Step 3 — Patton vs PI vs Now/Next/Later; the slice-1 unbreakable rule |
| `prioritization-frameworks.md` | Step 4 — WSJF/RICE/MoSCoW rubrics |
| `dependency-tracking.md` | Step 4 — depends_on, cycle detection, cross-persona handoffs |
| `okr-alignment.md` | Step 4 — OKR column, coverage matrix |
| `acceptance-criteria.md` | Step 4a — Given/When/Then + INVEST |
| `e2e-verification-and-contract.md` | Step 4b — backbone-as-E2E-contract |
| `output-routing.md` | Step 6 — diff-baseline / tracker-defined routing decision |
| `work-item-tracking.md` | Step 6 — per-tool import, aligning to an existing tracker's taxonomy, enabling the tracker burn-down |
| `framework-integration.md` | Superpowers/gstack/GSD plan-stage auto-trigger + handoff |
| `answer-first-writing.md` | Writing design.md/backlog.md/handoff.md answer-first (Pyramid Principle) |
