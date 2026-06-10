---
name: user-story-mapping
description: Run user story mapping (Jeff Patton style) — turns a vague goal, brief, or messy backlog into a sliced delivery plan with per-persona user stories that act as the blueprint for the team's test playbook (acceptance criteria + E2E contract). Mines existing context first (README, code, tests, tracker via MCP). Produces design doc, story map (Markdown + Mermaid + CSV), prioritized backlog (WSJF / RICE / MoSCoW), and optional role-hints for UX/UI + architect. Auto-activates when a sister framework enters its Plan stage — Superpowers between `brainstorming` and `writing-plans`, gstack `/office-hours` / `/autoplan` / `/plan-*-review`, or GSD `/gsd discuss` / `/gsd plan-milestone` / Brief / Roadmap authoring. Use when shaping work (discovery, MVP scoping, "what should we build first", PI planning, organizing a backlog, "stories per persona"). Skip for pure engineering — bug fixes, refactors, code review, deploy debugging.
license: MIT
compatibility: Requires Python 3.10+ for bundled scripts (storymap_to_csv.py, storymap_to_mermaid.py). No other system dependencies. Works across Claude Code, Claude.ai, and any Agent Skills v1 host (Cursor, Codex, Copilot, Gemini CLI, OpenCode, Goose, etc.).
metadata:
  author: MartinForReal
  version: "0.0.3"
  homepage: https://github.com/MartinForReal/storymap-skill
allowed-tools: Bash(python:*) Read Write Edit Glob Grep Agent Skill
---

# User Story Mapping

Turns vague intent into a sliced, prioritized plan that a SAFe/Scaled-Agile team can deliver against. Mode D (iterative refinement) re-opens an existing map to add/cut work and detect when a new feature breaks the team's limits.

**Auto-trigger in sister-framework Plan stages.** When the host environment shows you're at a Plan-phase command in Superpowers / gstack / GSD, this skill should self-activate before user stories are written by hand:
- **Superpowers** — between `brainstorming` (intent locked) and `writing-plans` (tasks not yet written)
- **gstack** — at `/office-hours`, `/autoplan`, or any `/plan-*-review` command
- **GSD** — at `/gsd discuss`, `/gsd plan-milestone`, or whenever the user is authoring `.gsd/Brief.md` / `.gsd/Roadmap.md` / a new `.gsd/Milestones/Mn/` directory

The signal is "the user is shaping work, not coding it." If you see those cues, propose this skill explicitly rather than falling through to ad-hoc story drafting. Detail: `references/framework-integration.md`.

**Stories here are a blueprint, not the final spec.** Per-persona stories produced by this skill are the input that downstream stages refine into:
1. **Gherkin acceptance criteria** for slice-1 stories (`slice-1-acceptance-criteria.md`, Step 4a)
2. **E2E test contract** scenarios derived from the backbone (`e2e-test-contract.md`, Step 4b)
3. **Engineering tasks** (Superpowers `writing-plans`, gstack `/autoplan`, GSD Tasks)

Treat the user-story map as **the test playbook in skeletal form** — every backbone activity becomes an E2E swimlane, every slice-1 story becomes ≥1 Gherkin scenario. The story map and the test playbook share the same backbone surface; they diverge only on detail level.

## Quick reference

Map the user's ask to the right step + reference to load:

| If the user... | Mode | Most relevant reference |
|---|---|---|
| Has only a verbal idea, no PRD/code/backlog | A | `discovery-questions.md` |
| Pastes a PRD, brief, or customer letter | B | `customer-interview-synthesis.md` (if raw interview notes) |
| Pastes a CSV/Jira/ADO/GitHub backlog | C | n/a — cluster items by inferred activity |
| Says "extend my prior storymap" / "what changed since last PI" | D | `iterative-refinement-and-snapshots.md` |
| Has a codebase + `.gsd/` or prior `design.md` | any | `context-collection.md` — mine first, don't re-ask |
| Hands you raw interview notes / call transcripts | any | `customer-interview-synthesis.md` |
| Asks "what should we build first" / "find the MVP" | any | `slicing-strategies.md` for the slice; `prioritization-frameworks.md` for the rank |
| Names WSJF / RICE / MoSCoW explicitly | any | `prioritization-frameworks.md` |
| Has stakeholders with conflicting interests | any | `persona-simulation-and-gap-filling.md` |
| Has multiple personas (admin + end-user + ops) | any | `persona-simulation-and-gap-filling.md` for sim; Step 2 below for **per-persona story sweep with parallel agents** |
| Wants role hints for UX/UI designer or architect | any | `role-hints-and-flow-advice.md` (new — Step 2.5) |
| Wants flow advice from another installed skill (auth flow, payment flow, onboarding flow, etc.) | any | `role-hints-and-flow-advice.md` — Skill-chaining section |
| Has an existing project where some stories are already shipped, or a tracker that's drifted since the last storymap | C / D | `progress-reconciliation.md` (new — Step 0.5) — bidirectional storymap ↔ tracker ↔ code-state sync |
| Treats stories as input to a test playbook | any | `acceptance-criteria.md` + `e2e-verification-and-contract.md` — backbone-as-contract |
| Has OKRs / KRs to align to | any | `okr-alignment.md` |
| Worries about story dependencies | any | `dependency-tracking.md` |
| Wants engineering-ready acceptance criteria | any | `acceptance-criteria.md` |
| Wants E2E test scenarios | any | `e2e-verification-and-contract.md` |
| Working inside Superpowers / gstack / GSD | any | `framework-integration.md` |
| Wants stories pushed somewhere (tracker, TODO.md, framework state, memory) | any | `output-routing.md` (decides from-scratch vs existing); then `work-item-tracking.md` for tracker mechanics |

## Workflow at a glance

| Step | Purpose | Output | Budget |
|---|---|---|---|
| **0** Context loop | Hypothesis-driven mining of cheap-then-conditional sources (works for both from-scratch and existing project) | "Context loop trace" + "Contradictions flagged" in `design.md` | <15% (5-15 tool calls, hard cap 20) |
| **0.4** Fill gaps | Classify gaps (blocking/stage-local/deferrable); gate only on blocking; resolve others at the right time | Gap checklist + conflict matrix | 15-20% |
| **0.5** Reconcile progress (existing project / Mode D) | Build status map from code evidence + tracker state + prior storymap; detect graduated activities; flag drift between storymap intent and tracker reality | `## Implementation status` table in `design.md` + status annotations on stories in `storymap.md` (`[status: done \| 2026-05-12]`, `[status: in-progress \| …]`) | 5-10% (skip entirely for from-scratch / no tracker / no prior storymap) |
| **1** Backbone | Left-to-right user activities in user voice; cross-cutting work in separate section | `storymap.md` backbone | 5-10% |
| **2** Decompose (per-persona sweep) | Tasks under activities; **for each persona, generate stories in parallel via the `Agent` tool** so every persona gets explicit coverage. Stories are blueprints — they will be refined into ACs/E2E later. | `storymap.md` body with per-persona stories | 15-20% |
| **2.5** Role hints + flow advice | Generate `role-hints.md` for UX/UI designer + architect; chain to other installed skills (e.g. `auth-flow-advisor`, `payment-integration-best-practices`, `accessibility-checker`) for advice on specific flows | `role-hints.md` + skill-advice notes folded into `design.md` | 10-15% |
| **3** Slice | Walking-skeleton/PI/Now-Next-Later; first slice covers every backbone activity | Slice tags on stories | 5% |
| **4** Prioritize | WSJF/RICE/MoSCoW + OKR linkage + dependency feasibility check | `backlog.csv` + `backlog.md` | 15-20% |
| **4a** ACs | Given/When/Then for slice-1 stories + INVEST check (refines the Step 2 stories into testable form) | `slice-1-acceptance-criteria.md` | 10-15% |
| **4b** E2E contract | Backbone-as-contract: coverage matrix, E2E-HAPPY happy path, per-activity scenarios — **the test playbook** | `e2e-test-contract.md` | 5-10% |
| **5** Generate derived | Run bundled scripts for `storymap.csv` + `storymap.mmd` | Two derived files | <2% |
| **6** Hand off | What was produced; what's still uncertain; smallest next decision | `handoff.md` | 5% |

Total token budget: target ~200K. Story count cap: ~50 total; slice-1 ≤ 15. If you exceed either, slow down — usually a signal the work needs splitting before mapping.

## Performance hard rules

Concrete limits that prevent the most common failure modes (running out of turns before completing the artifacts, redundant re-reading of references, runaway story generation):

1. **Story count cap.** Total stories ≤ 50; slice-1 ≤ 15. If you're heading past either, stop and either (a) split the work into multiple maps, (b) push later stories to a deferred list, or (c) escalate to the user with a "this is too big to plan as one PI" message. Generating 80+ stories then running out of turns before writing the backlog is the most common failure mode — cap proactively.
2. **Backbone activity cap.** 5-7 default; hard max 10. More than 7 means either the time horizon is too long, the granularity is too detailed, or the work is actually two products. Re-confirm Step 1 criteria before proceeding past 7.
3. **Read SKILL.md once** at invocation start. Load references **only** when you reach the step that needs them. Don't re-read the same reference twice in one run.
4. **Glob/Grep before Read.** Don't `Read` a file >500 lines without `offset` + `limit`. For directory exploration, `Glob` first to know what's there.
5. **Batch related tool calls.** Independent reads / greps / globs can go in one message. Don't serialize what can be parallel.
6. **Use bundled scripts** for `storymap.csv` + `storymap.mmd`. Hand-writing is slow, error-prone, and wastes turns.
7. **80% turn-budget stop.** If you've consumed 80% of your turn budget and the backlog isn't written yet, stop new generation, write what you have, and document the rest as deferred in `handoff.md`. Better a partial run with a clear "what's missing" than a truncated run with no audit trail.
8. **Skill-chaining cost ceiling.** *Sister-framework* invocations (gstack/Superpowers/GSD slash-commands) — **one per run**. *Domain-advisor* skills (auth-flow-advisor, payment-integration-best-practices, accessibility-checker, etc.) invoked at Step 2.5 — **up to 3 per run, one per flow**. If you'd want either limit higher, the discovery is too unscoped — push back to the user to narrow first.
9. **Context loop hard cap: 20 tool calls.** Same rule as cost ceiling above. If you hit it and hypothesis isn't stable, write your best understanding to `design.md`, flag the residual ambiguity, and proceed.
10. **Defer non-blocking gaps.** Per Step 0.4 classification: only blocking gaps gate planning. Stage-local resolves at the stage's entry; deferrable goes to `handoff.md` as open questions. Don't pre-flight everything.

These are not aspirational — they're guardrails. Hitting them is a signal to stop and re-scope, not a soft target to "try" to honor.

## The user-input-authoritative principle

**CRITICAL: What the actual user told you, in this conversation, always wins.** Lower-priority sources fill gaps but never override.

```
priority of sources (highest → lowest):
  1. The actual user in this conversation
  2. Verbatim from interview notes / call transcripts
  3. Persistent memory from prior sessions (only if user approved)
  4. Context mined from artifacts (README, code, tests, tracker)
  5. Simulated persona responses (Step 0.4)
  6. General-knowledge inference
```

Tag every fact in `design.md` with its source — `[user-stated]`, `[interview: Aisha]`, `[memory: 2026-04-23]`, `[code: src/routes/billing.ts]`, `[simulated: Marcus]`, `[inferred]`. When the user contradicts a lower source, update the cache to match.

**❌ Wrong:** Simulated-Compliance argues for RBAC; you add it to PI 1 over the user's explicit "no RBAC in PI 1."
**✅ Right:** Log Compliance's objection as a future-slice risk; user's stance ships.

## What this skill does

Three deliverables, always:

1. **Project design doc** (`design.md`) — personas, primary user activities, opportunities, hypotheses, the question this work answers.
2. **Story map** (three formats) — `storymap.md` (readable), `storymap.mmd` (Mermaid graph), `storymap.csv` (Jira/ADO importable). Stories are **per-persona** and intentionally a blueprint — they get refined in 4a/4b.
3. **Prioritized backlog** — `backlog.csv` (full scoring) + `backlog.md` (one-page summary). Method = WSJF (SAFe default) / RICE / MoSCoW.

Optional 4th: `role-hints.md` (UX/UI designer + architect head-start) from Step 2.5.
Optional 5th: `slice-1-acceptance-criteria.md` (Given/When/Then) for engineering handoff.
Optional 6th: `e2e-test-contract.md` — **the test playbook**, derived from the backbone + slice-1 ACs.
Optional 7th: `tracker-status-update.<ext>` — opt-in tracker write-back script from Step 6 (only when Step 0.5 ran and the user confirmed status changes).
Optional 8th: `handoff.md` (what's done, what's open, smallest next decision).

The story-map → ACs → E2E-contract chain is intentional: the skill produces a **test playbook in three levels of refinement**, not a one-shot spec. Per-persona stories from Step 2 are the seed; ACs in 4a pin down behavior; the E2E contract in 4b orchestrates the journey.

## When to choose this skill vs. just answering directly

Use when the user is **shaping work**, not coding it. Signals: vague problem with no plan, unnavigable backlog, MVP scoping, PI planning, "what should we build first".

Skip for: bug fixes, refactors, code review, deploy debugging, "explain this code" — those need engineering, not mapping.

## Invocation modes

Detect from the first user message; confirm in one sentence before proceeding.

| Mode | When | Behavior |
|---|---|---|
| **A** From scratch | No PRD, no brief, no backlog — verbal idea only | Drive discovery via batched questions (3-5 at a time). Propose backbone before drilling into stories. See `references/discovery-questions.md`. |
| **B** From a brief | PRD, problem statement, customer letter, interview notes | First response: restate outcome, list extracted personas + activities, flag gaps. Then proceed. If raw interview notes: `customer-interview-synthesis.md`. |
| **C** From existing backlog | CSV / Jira / ADO / GitHub issues to reorganize | Cluster items by inferred user activity; flag orphans; identify coverage gaps; re-slice. Prefer user's words over yours. |
| **D** Iterative refinement | Existing story map; extend, re-slice, add a feature, detect limit breach | Prior `storymap.md` is authoritative for backbone (unless user re-derives). Produce diff-style summary. Detect limit breaches and surface trade-offs. See `references/iterative-refinement-and-snapshots.md`. |

## Working with existing projects and prior runs (per-stage matrix)

When the project isn't from-scratch — there's an existing codebase, a prior `design.md`, persistent memory, an active tracker, or all four — every stage has specific behavior. **The rule: artifacts (current files) > memory > inferred. Re-derive only what's missing or contradicted.**

| Stage | If existing project (code/tests/tracker/framework artifacts) | If memory / prior artifacts |
|---|---|---|
| **0** Context loop | Mine the conditional sources that match the hypothesis. Framework artifacts (`.gsd/`, prior `design.md`) take precedence over redundant mining. | Load `state.json` / memory MCP as a starter signal. Tag loaded facts `[memory: <date>]`. Verify each against current state — if contradicted, current wins. |
| **0.4** Gaps | Gaps previously *resolved* in the decisions log carry forward — don't re-ask. Only newly-introduced gaps need filling. | Same — decisions log is the gap-resolution memory. |
| **0.5** Reconcile progress | Required step. Build status map from tracker + code surfaces + prior storymap. Mark shipped stories `done`; detect graduated activities; surface tracker drift. See `progress-reconciliation.md`. | Prior `backlog.csv` `status` column carries forward as the seed. Re-pull from tracker for live status; tracker overrides prior `status` value when they conflict. |
| **1** Backbone | Mined routes/handlers/test names become activity *candidates* — propose, don't impose. Existing system shape is one input among several. **Graduated activities (from Step 0.5) stay visible but are excluded from active slicing.** | If prior `design.md` has a `## Backbone criteria` section, **default to those criteria** (only re-derive if user says to change them). Same for backbone activities — preserve unless user requests re-derivation. |
| **2** Decompose | Existing routes / components / handlers / endpoints are pre-existing task candidates under their activity. Reuse the team's existing naming. | Prior task/story IDs carry forward. New tasks/stories get fresh IDs starting from `max(prior_id) + 1` — don't renumber. |
| **3** Slice | If the tracker has existing Fix Versions / Iteration Paths / Cycles, those are the canonical slice names — use them, don't invent. | Prior slicing strategy from `design.md` wins. Current PI name (e.g., "PI 2026-Q3") comes from memory's `active_pi`. |
| **4** Prioritize | If the tracker stores WSJF/RICE values already (custom fields), pull them as the prior scores. Re-score only stories the team changed or new ones. | Method preference (WSJF / RICE / MoSCoW) from memory wins if user is silent. Prior scores reused; deltas annotated. |
| **4a** ACs | Existing e2e / integration test names are candidate AC sources — reference them by file path. Don't duplicate. | Prior ACs preserved verbatim for unchanged stories. Re-generated only for changed stories. |
| **4b** E2E contract | Existing playwright / cypress / e2e suite informs the contract — reference scenarios by file path. The contract documents what *should* be covered, not re-writes what is. | Prior contract carries forward; coverage matrix updated only for added/removed activities. |
| **5** Generate derived | N/A — deterministic from storymap.md | N/A |
| **6** Hand off | Diff-style summary against the prior artifact (ADDED / MOVED / CUT / UNCHANGED). | If memory is enabled, **write back** updated state to `.user-story-mapping/state.json` (or MCP memory) and tell the user in one line what was saved. Never overwrite the decisions log — append-only. |

### Three rules that apply at every stage

1. **Artifact > memory > inferred.** Current files win over stale memory; both win over inference.
2. **Verify, don't trust.** Load memory; immediately spot-check against current state. If a remembered persona is "CS rep" but the README pivoted away, override and update memory.
3. **Tag every fact.** `[user-stated]`, `[interview: Aisha]`, `[memory: 2026-04-23]`, `[code: src/routes/billing.ts]`, `[tracker: PROJ-142]`, `[simulated: Marcus]`, `[inferred]`. Reviewers and Mode D need to know where each claim came from.

Detail: `references/persistent-knowledge.md` (memory lifecycle) and `references/iterative-refinement-and-snapshots.md` (Mode D protocol + diff format).

## Workflow

### Step 0 — Context collection loop

**Loop, don't pipeline.** Cheap signal → form hypothesis → pick the next source based on hypothesis → repeat → exit on stable hypothesis or budget ceiling. Wastes turns if you run sources in fixed order on greenfield, and over-investigates when one signal already gave the answer.

**Starter signals (always try first):** `ls`, prompt re-read, `.user-story-mapping/state.json` or memory MCP, `README.md`, interview notes already in the prompt. After these you should know: from-scratch vs existing-project, Mode A/B/C/D, tech-stack hint.

**Branch-conditional sources** (mine only if hypothesis warrants): manifests (`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod`), routes/handlers, test names, `docs/adr/`, `git log`, tracker MCP (Jira/ADO/GitHub/Linear), analytics MCPs, **framework artifacts** (`.gsd/`, Superpowers `brainstorming/`, gstack `/plan-*-review` outputs), prior `design.md` / `storymap.md` / `backlog.md`. Mine framework artifacts **before** asking the user — they often contain everything the user would say, in cleaner form.

**Other installed skills are context sources too.** If a skill like `code-explorer`, `db-schema-analyzer`, or a sister-framework command already knows what you'd otherwise discover, invoke it via the `Skill` tool. Budget one such invocation per loop run; tag output `[skill: <name>]`.

**Exit conditions:** hypothesis stable for 2 iterations · ≥15% of turn budget consumed · user says "proceed" · empty working dir + no interview notes · strong from-scratch signal + no codebase · single signal already gave the outcome.

**Surface findings in `design.md`** under `## Context loop trace` (numbered observations + final hypothesis) and `## Contradictions flagged` (sources that disagree). The trace is documentation — a reviewer sees what evidence drove which conclusion.

**Persistent memory** and **customer interview synthesis** ride inside the loop, not as separate steps — read [`persistent-knowledge.md`](references/persistent-knowledge.md) and [`customer-interview-synthesis.md`](references/customer-interview-synthesis.md) when those signals fire.

Detail: [`references/context-collection.md`](references/context-collection.md) — full loop algorithm, source-by-source guidance, worked traces, cost ceilings.

### Step 0.4 — Fill remaining gaps; gate planning on completeness

After Step 0 you usually still have unanswered questions. **Not every gap blocks planning** — classify before deciding.

| Class | Resolve when | Example |
|---|---|---|
| **Blocking** — would change the backbone, slicing strategy, or violate user-input-authoritative | **At Step 0.4** (gate planning) | "Two stakeholders want incompatible flows — which wins?"; "Single-persona or multi-persona?" |
| **Stage-local** — affects one downstream stage only | **At that stage's entry** (mini-resolution) | "Don't know S027's WSJF size" (Step 4 only); "Don't know S015's regex" (Step 4a only) |
| **Deferrable** — refines but doesn't change output | **In `handoff.md`** as an open question | "Don't know exact pricing tier — assumed $10 for RICE"; "Don't know exact Salesforce field name" |

**The gate at Step 0.4 applies only to blocking gaps.** Stage-local and deferrable gaps move forward; resolve them in place.

Blocking-gap resolution: **ask the user first**, then fall back to persona simulation when asking would mean 20 questions. Do not proceed to Step 1 until blocking conflicts are resolved (user decided or explicitly punted) and any unfillable gaps are documented as open questions. **User always wins over simulation** — log simulated objections as future-slice risks, not as overrides.

If a NEW gap surfaces mid-stage, classify and act on it the same way (`design.md` records the mini-resolution). Never silently absorb. If a gap emerges at Step 4/4a that *would have changed* Step 1 or Step 3, don't silently rewrite earlier stages — surface in `handoff.md` under `## Late-discovered gaps` for user decision.

Detail: [`references/persona-simulation-and-gap-filling.md`](references/persona-simulation-and-gap-filling.md) — full classification + resolution + persona-sim protocol + conflict matrix.

### Step 0.5 — Reconcile prior progress (existing-project / Mode D only)

**Skip entirely** for from-scratch runs (no codebase, no tracker, no prior storymap). Only run when ≥1 of:
- A prior `storymap.md` exists in this working tree
- A tracker (Jira/ADO/GitHub/Linear) was mined in Step 0 and contains issues that may correspond to backbone activities
- The codebase has shipped surfaces (deployed routes, merged PRs, passing test names) that map to plausible backbone activities

The goal is bidirectional sync — **storymap intent ↔ tracker authority for status ↔ code as evidence** — so the next slice doesn't re-commit work that's already shipped, and the team's tracker reflects the current storymap's view of cuts/deferrals.

Each story gets one of `done | in-progress | blocked | deferred | cut | unchanged` per the taxonomy + detection signals in [`progress-reconciliation.md`](references/progress-reconciliation.md#status-taxonomy). Authority rules in one line: **tracker wins for status, storymap wins for intent and slicing, code is evidence (not authority), user always wins over all three**.

Status lives as an annotation, not a separate file: in `storymap.md` append `[status: done | 2026-05-12]` to the story line; in `backlog.csv` add `status`, `status_evidence`, `status_date` columns (the bundled `storymap_to_csv.py` parses the tag and emits the first two automatically).

**Graduation.** When all stories under a backbone activity reach `done`, move the activity into a new `## Shipped foundation` section in `storymap.md` (visible for narrative continuity, excluded from active slicing) and note the graduation date in `design.md` under `## Activity status`. The slice-1 coverage rule applies only to *active* backbone activities.

**Drift surfacing.** Tracker issues with no matching backbone activity, or storymap stories with no tracker mapping, go under `## Detected drift` in `handoff.md` for user decision. Never silently absorb.

**Write-back (opt-in, never auto).** Storymap-authoritative status changes (user-confirmed cuts, re-slices, new tracked items) emit a `tracker-status-update.<ext>` script alongside Step 6 routing — the user reviews and runs it. Tracker → storymap status pulls don't need write-back.

Detail: [`references/progress-reconciliation.md`](references/progress-reconciliation.md) — full algorithm, conflict-resolution table, per-tracker write-back script templates (Jira/ADO/GitHub/Linear).

### Step 1 — Establish the backbone

A backbone can be generated under different criteria; the choice changes its shape. **Pick the criteria explicitly, confirm with the user, and record them in `design.md` under `## Backbone criteria` so future runs reproduce the same backbone.**

#### Six criteria to declare (default in **bold**)

| Criterion | Options |
|---|---|
| **Frame** | **Activity flow** / Jobs-to-be-done / System interaction / Customer journey |
| **Persona perspective** | **Primary user** / Multiple parallel personas / Aggregate across personas |
| **Time horizon** | **Single end-to-end session** / Day-in-the-life / Lifecycle |
| **Granularity** | **5-7 activities** / 3-5 (high-level) / 8-12 (detailed) |
| **Scope** | **Happy path only** / Happy path + error recovery / Full surface |
| **Aggregation** | **Single role per activity** / Multiple roles per activity |

In Mode D and re-runs, read the prior criteria from `design.md` and use the same ones unless the user explicitly says to change them. When the user is silent (single-shot), apply defaults and explicitly state "Applied defaults: [list]. Override by re-running with criteria= …" in `design.md` — never silently choose.

**Backbone rules** (apply regardless of criteria): user voice, present tense, active. Good: `Sign up`, `Find a property`, `Schedule a viewing`. Bad: `User onboarding flow`, `Search functionality`, `Booking module` — system language leaks implementation into a discovery artifact and breaks slicing.

**CRITICAL: Cross-cutting work doesn't belong in the backbone.** Tech debt, infrastructure, localization, theming, observability, compliance go in a `## Non-backbone / cross-cutting` section *below* the backbone with `### Theme:` headers. They're prioritized in `backlog.csv` (`activity = "Non-backbone: <theme>"`) but excluded from slice-1 coverage. Rule of thumb: if you can't write "As a `<user>`, I want to..." that ties to a single backbone column, it's cross-cutting.

Detail: [`references/backbone-criteria.md`](references/backbone-criteria.md) — what each criterion's options imply, why explicit criteria matter, common anti-patterns.

### Step 2 — Decompose into tasks, then per-persona stories

Tasks = the user's smaller steps within an activity. Stories = deliverable increments under tasks. Standard form: **As a `<persona>`, I want to `<action>`, so that `<outcome>`**. Skip the form when it's noise. If a task has >7 stories, it's probably two tasks — split.

**Per-persona coverage is mandatory.** Every persona named in `design.md` must appear as the `<persona>` in **at least one slice-1 story**. Without this, slice 1 silently optimizes for the loudest persona and the others' journeys never ship. A single backbone activity often produces multiple stories with different personas (e.g., "Sign in" → admin SSO setup, end-user sign-in, compliance role-claim verification). Stories with no persona (pure infra/cron) live in the cross-cutting section and don't count toward coverage.

If a persona has *zero* slice-1 candidates, that's a signal the slicing is wrong (re-run Step 3) or that persona shouldn't be in `design.md` (re-run Step 1) — not a silent drop.

**Parallelize via the `Agent` tool when persona count ≥3.** Spawn one subagent per persona, each receiving the backbone + that persona's verbatim quotes / pain points / constraints + the story-form template + an "in-character" instruction. Run them in parallel (one message, multiple `Agent` calls — no cross-dependency). Then merge, dedupe overlap (same activity from multiple personas often = same story with different framing — keep the most user-voiced version), and mark conflicts for the user. For ≤2 personas, inline generation is fine.

**Stories are a blueprint, not the final spec.** The form intentionally underspecifies — captures *intent*, not *behavior*. Behavior gets pinned down at Step 4a (Gherkin ACs) and Step 4b (E2E test contract). If you find yourself writing implementation detail in a story ("click a React button that calls `/api/v1/refunds` with idempotency key…"), stop. That belongs in ACs.

### Step 2.5 — Role hints + flow advice

After per-persona stories are drafted but before slicing, produce two outputs that make the storymap usable beyond developers:

1. **`role-hints.md`** — UX/UI designer + architect head-start derived from the backbone, cross-cutting section, and persona perspectives. UX section: persona snapshots, per-activity flow inventory, friction hotspots (where personas converge), open UX questions, accessibility/i18n hints. Architect section: cross-cutting work index, boundary candidates, hard constraints, risky integrations, open architecture questions. **Not a replacement for design or architecture work** — a head-start that names what each role should look at.

2. **Flow-advice skill chaining** — scan the backbone for well-known-pattern flows (auth, payment, onboarding, search, notifications, audit, accessibility, i18n, multi-tenancy). For each, check whether another installed skill (e.g., `auth-flow-advisor`, `payment-integration-best-practices`, `accessibility-checker`) can advise. If yes, invoke via the `Skill` tool with a tightly scoped question, tag the response in `design.md` as `[skill: <name> @ <date>]`, and fold into the relevant `role-hints.md` section. If no advisor is installed, list the flow under "Flows that would benefit from domain expertise" so the architect knows where to dig.

**Cap:** sister-framework chaining = 1/run (Performance hard rule 8); domain-advisor chaining = **up to 3/run, one per flow**. More than 3 means the backbone is too big — split.

Detail: [`references/role-hints-and-flow-advice.md`](references/role-hints-and-flow-advice.md) — `role-hints.md` templates, skill-discovery protocol, advisor invocation patterns, anti-patterns.

### Step 3 — Slice horizontally

| Strategy | Use when |
|---|---|
| Walking Skeleton → MVP → R2 → R3 (Patton) | Greenfield, validating end-to-end thin slice first |
| PI 1 / PI 2 / PI 3 (SAFe Program Increment) | Existing ART, PI planning, multi-team |
| Now / Next / Later | Discovery phase, low certainty, need flexible commitment |

Defaults: A→Patton; B→Patton or PI based on signal; C→PI; D→preserve existing strategy.

**CRITICAL: The first slice must include at least one story from every backbone activity.** That's what makes story mapping different from a backlog. Detail: `references/slicing-strategies.md`.

**❌ Wrong:** Slice 1 covers Activities 1, 2, 3 but not 4 and 5 — user can't demo the journey end-to-end.
**✅ Right:** Slice 1 has at least one (possibly minimal) story per backbone column.

### Step 4 — Prioritize, align, sequence

**Pick a method** (ask once; default WSJF for SAFe): WSJF (economic), RICE (metrics-driven), MoSCoW (data-thin triage). Detail: `references/prioritization-frameworks.md`.

**OKR alignment** — if user provides OKRs/KRs, add `okr` column to `backlog.csv`; surface orphan stories (no KR ladder) and orphan KRs (no story coverage). See `references/okr-alignment.md`.

**Dependencies** — when stories have hard dependencies, add `depends_on` column with `H:<id>` / `S:<id>` / `X:<id>` tags. Run slice-1 feasibility check: every hard dep of a slice-1 story must also be in slice 1. Surface cycles as red flags. See `references/dependency-tracking.md`.

### Step 4a — Generate acceptance criteria for slice 1

Given/When/Then for each slice-1 story (skip trivial ones like "rename button"). Cover happy path + 1-2 edge cases + 1 failure case. Run INVEST checklist; flag stories that fail. Save to `slice-1-acceptance-criteria.md`. Non-Gherkin teams get bulleted ACs with the same precision. See `references/acceptance-criteria.md`.

### Step 4b — Generate the E2E test contract (backbone-as-contract)

Backbone activities are a high-leverage source for end-to-end verification — every activity must be demonstrably reachable, and slice-1 ACs are already shaped like E2E scenarios. Generate `e2e-test-contract.md` containing:

- **Coverage matrix** — per backbone activity, which slice-1 stories cover it and how many E2E scenarios are required
- **One end-to-end happy-path scenario** that traverses every backbone activity in order (E2E-HAPPY) — this is the demoable journey + the slice-1 gate
- **Per-activity scenarios** mapped 1-to-1 with slice-1 ACs (reference by story ID, don't duplicate)
- **Dependency-aware sequencing** for the E2E suite itself

Default: produce `e2e-test-contract.md` whenever `slice-1-acceptance-criteria.md` is produced. Skip for solo / pre-PMF builders unless they ask. In Mode D, update the contract whenever a backbone activity is added or removed. See `references/e2e-verification-and-contract.md`.

### Step 5 — Generate derived artifacts

Write `design.md`, `storymap.md`, `backlog.md`, `backlog.csv` by hand. Then **always** run the bundled scripts for the derived two:

```bash
python scripts/storymap_to_csv.py storymap.md > storymap.csv
python scripts/storymap_to_mermaid.py storymap.md > storymap.mmd
```

Don't hand-write CSV/Mermaid. The scripts enforce the canonical format and save turns.

### Step 6 — Hand off

Tell the user what was produced, what's still uncertain, and what the smallest next decision is. Don't summarize the map back — they can read it. Surface what they need to decide.

**Route the items first.** Decide where the slice-1 stories physically land per the from-scratch vs existing rule in `references/output-routing.md`:

- **From-scratch project** (empty/near-empty repo, no tracker mentioned, no framework state) → generate a tracker import script via `work-item-tracking.md`. Don't auto-run it.
- **Existing project** → walk the persistence cascade (sister-framework state → plain `TODO.md` → Memory MCP) and write to the first that applies. Optionally also populate Claude Code's `TodoWrite` if the user is about to execute slice 1 in this session — `TodoWrite` is an orthogonal helper, not a persistence destination. Don't push to a populated tracker without explicit user opt-in.

**Status write-back (existing project + Step 0.5 ran).** If Step 0.5 produced status changes the user confirmed (cuts, re-slices, new tracked items) and the storymap considers authoritative for the tracker, also generate a *status-update script* alongside the slice-1 routing — separate file, separate user opt-in. Pull-only status changes (tracker → storymap) don't need write-back. See `progress-reconciliation.md` § "Write-back to the tracker".

End the handoff with a single line naming the destination(s) you wrote to, e.g. `"Slice 1 (12 stories) → .gsd/Roadmap.md + TODO.md; status updates for 4 closed-out-of-band stories → tracker-status-update.sh (review before running); run /gsd discuss next."`

If a sister framework is active (Superpowers / gstack / GSD), end with the explicit next command they should run. See `references/framework-integration.md`.

**Persist memory (if enabled).** When `.user-story-mapping/state.json` or MCP memory was used in this run, write the updated delta back at the end — preferences, current backbone criteria, active PI, persona-cache, decisions-log appendix. Never overwrite the decisions log; append only. Tell the user in one line what was saved: "Persisted to `.user-story-mapping/state.json`: backbone criteria, 4 personas, decisions D0017-D0019, active PI = 2026-Q3."

**Mode D diff.** If this run extended a prior artifact, lead `handoff.md` with a diff-style summary: ADDED / MOVED / CUT / UNCHANGED / BREACHES-RESOLVED. The diff is what makes refinement reviewable.

## Iterative refinement and limit-breach detection (Mode D)

When the user has an existing story map and wants to add work, re-slice, or extend:

1. **Read the prior artifact as authoritative** for backbone unless the user says otherwise
2. **Produce a snapshot** — current state of slices, capacity used, OKR coverage, open dependencies
3. **Apply the requested change** (add stories, re-slice, etc.)
4. **Detect limit breaches:**
   - **Capacity** — added stories exceed team capacity for the slice
   - **Dependencies** — new hard deps that aren't in the same slice
   - **OKR coverage** — new story doesn't ladder to a committed KR
   - **Scope** — change pushes total stories past the cap (~50)
   - **Slice-1 rule** — new activity introduced but no slice-1 coverage
5. **Surface the breach** — do not silently absorb. Offer trade-offs: cut other stories, push to next slice, expand capacity, defer.
6. **Output a diff-style summary** alongside the updated artifacts: what was added/removed/moved, which limits were breached, which trade-offs the user must approve.

Detailed protocol: `references/iterative-refinement-and-snapshots.md`.

## Where the artifacts land

Slice-1 stories need a home. **From-scratch (empty/near-empty repo, no tracker mentioned, no framework state) → seed an issue tracker via `references/work-item-tracking.md`.** **Existing project → walk the persistence cascade (sister-framework state → `TODO.md` → Memory MCP); optionally pair with `TodoWrite` if the user is coding now.** Don't push to a populated tracker without explicit opt-in. Full decision tree + the cascade walk: `references/output-routing.md`.

**Don't auto-create issues or auto-populate `TodoWrite` without asking** — generate the import command or script and tell the user what running it would do.

## Working with sister skill frameworks

This skill is the natural artifact-producer for the Plan phase of three popular Claude Code skill frameworks:

- **[Superpowers](https://github.com/obra/superpowers)** — slot between `brainstorming` and `writing-plans`
- **[gstack](https://github.com/garrytan/gstack)** — produce what `/plan-ceo-review`, `/plan-eng-review`, `/plan-devex-review` read
- **[GSD](https://getshitdone.help/solo-guide/why-gsd/)** — hand off to GSD's `/gsd discuss` → `/gsd plan-milestone` → `/gsd auto`; mind the slice/Slice terminology collision

When any is active, end with an explicit handoff line. Don't auto-invoke their commands. Don't write directly into framework state directories (`.gsd/`, etc.). See `references/framework-integration.md`.

## Quality bar + anti-patterns

A run is "good" when:
- Backbone reads as a coherent user narrative (read it aloud — does it sound like a story?)
- First slice covers every backbone activity (demoable end-to-end)
- Every story has a persona and an outcome (or is trivially small)
- Priorities have *reasoning* attached, not just numbers
- Design doc states the question being answered, not just features
- Every fact in `design.md` is source-tagged
- Token usage stays under ~200K; story count under ~50

Avoid:
- **System-shaped backbones** (Login, Database, API) — useless for slicing
- **Padding stories with persona dressing** when internal plumbing
- **One giant slice called "MVP"** with 80% of stories — slicing didn't happen
- **Skipping the design doc** because the user "just wants the map" — the doc is what makes the map auditable
- **Letting simulated persona input override the user**
- **Hand-writing CSV / Mermaid** when the scripts exist
- **Generating 80+ stories** and running out of turns — cap proactively per the perf hard rules

## File structure produced

```
<output-dir>/
├── design.md                          # personas, activities, opportunities, hypotheses, sources tagged
├── storymap.md                        # human-readable hierarchical map (per-persona stories)
├── storymap.mmd                       # Mermaid graph (auto-generated)
├── storymap.csv                       # flat table for Jira/ADO/Excel import (auto-generated)
├── role-hints.md                      # UX/UI designer + architect head-start (Step 2.5, optional)
├── backlog.md                         # ranked summary with reasoning
├── backlog.csv                        # full backlog with WSJF/RICE/MoSCoW scores, depends_on, okr columns
├── slice-1-acceptance-criteria.md     # Given/When/Then for slice 1 (Step 4a, refines per-persona stories)
├── e2e-test-contract.md               # the test playbook — backbone-as-contract E2E scenarios (Step 4b)
├── tracker-status-update.sh           # opt-in tracker write-back script (Step 6, only if Step 0.5 ran and user confirmed status changes)
└── handoff.md                         # what's done, what's open, next decision (optional)
```

Templates and column schemas live in `assets/`. Use them.

## References (load on demand, don't pre-read)

| File | When to read |
|---|---|
| `discovery-questions.md` | Mode A — driving discovery via batched questions |
| `customer-interview-synthesis.md` | Mode B with raw interview notes |
| `context-collection.md` | Step 0 — depth on what to mine from each source |
| `persona-simulation-and-gap-filling.md` | Step 0.4 — protocol for persona-sim subagents |
| `persistent-knowledge.md` | Step 0 — memory across sessions (Mode D starter signal) |
| `iterative-refinement-and-snapshots.md` | Mode D — extend existing map, detect limit breach |
| `progress-reconciliation.md` | Step 0.5 — bidirectional sync between storymap, tracker status, and code reality (existing-project / Mode D) |
| `backbone-criteria.md` | Step 1 — six-criteria options + anti-patterns |
| `role-hints-and-flow-advice.md` | Step 2.5 — UX/UI + architect hints, skill-chaining for flow advisors |
| `slicing-strategies.md` | Step 3 — picking Patton vs PI vs Now/Next/Later |
| `prioritization-frameworks.md` | Step 4 — WSJF/RICE/MoSCoW scoring rubrics |
| `dependency-tracking.md` | Step 4 — depends_on column, cycle detection |
| `okr-alignment.md` | Step 4 — OKR column, coverage matrix |
| `acceptance-criteria.md` | Step 4a — Given/When/Then generation (refines per-persona stories) |
| `e2e-verification-and-contract.md` | Step 4b — backbone-as-E2E-contract (the test playbook) |
| `framework-integration.md` | Step 6 — Superpowers/gstack/GSD plan-stage auto-trigger + Jira/ADO/GitHub handoff |
| `output-routing.md` | Step 6 — the from-scratch vs existing decision; cascade across tracker / framework state / TODO.md / Memory MCP / TodoWrite |
| `work-item-tracking.md` | Step 6 — per-tool import details (from-scratch branch) |
