---
name: user-story-mapping
description: Run user story mapping (Jeff Patton style) to turn a goal, brief, or messy backlog into a sliced delivery plan. Produces a story map (markdown + Mermaid + CSV), a prioritized backlog (WSJF, MoSCoW, or RICE), and a design doc. Mines existing context first — README, code, tests, docs, Jira/ADO/GitHub via MCP — so backbones reflect real user journeys. Invoke when the user is shaping work rather than coding it — discovery, MVP scoping, what to build first, organizing a backlog, or PI planning. Triggers include "what should we build first", "MVP for X", "walking skeleton", "organize this backlog", "PI planning", "discovery for", "user journey", "scan our repo for missing work"; and sister-framework cues like Superpowers `brainstorming` / `writing-plans`, gstack `/office-hours` / `/plan-*`, or GSD Brief / Roadmap / Milestone / `/gsd discuss`. Use even when the user doesn't say "story mapping". Skip for pure engineering — bug fixes, refactors, code review, deploy debugging, doc updates.
license: MIT
compatibility: Requires Python 3.10+ for bundled scripts (storymap_to_csv.py, storymap_to_mermaid.py). No other system dependencies. Works across Claude Code, Claude.ai, and any Agent Skills-compliant agent (Cursor, Codex, Copilot, Gemini CLI, OpenCode, Goose, etc.).
metadata:
  author: MartinForReal
  version: "0.0.1"
  homepage: https://github.com/MartinForReal/storymap-skill
allowed-tools: Bash(python:*) Read Write Edit Glob Grep Agent Skill
---

# User Story Mapping

Turns vague intent into a sliced, prioritized plan that a SAFe/Scaled-Agile team can deliver against. Mode D (iterative refinement) re-opens an existing map to add/cut work and detect when a new feature breaks the team's limits.

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
| Has OKRs / KRs to align to | any | `okr-alignment.md` |
| Worries about story dependencies | any | `dependency-tracking.md` |
| Wants engineering-ready acceptance criteria | any | `acceptance-criteria.md` |
| Wants E2E test scenarios | any | `e2e-verification-and-contract.md` |
| Working inside Superpowers / gstack / GSD | any | `framework-integration.md` |
| Wants to push the result into Jira / ADO / Linear / etc. | any | `work-item-tracking.md` |

## Workflow at a glance

| Step | Purpose | Output | Budget |
|---|---|---|---|
| **0** Context loop | Hypothesis-driven mining of cheap-then-conditional sources (works for both from-scratch and existing project) | "Context loop trace" + "Contradictions flagged" in `design.md` | <15% (5-15 tool calls, hard cap 20) |
| **0.4** Fill gaps | Classify gaps (blocking/stage-local/deferrable); gate only on blocking; resolve others at the right time | Gap checklist + conflict matrix | 15-20% |
| **1** Backbone | Left-to-right user activities in user voice; cross-cutting work in separate section | `storymap.md` backbone | 5-10% |
| **2** Decompose | Tasks under activities; stories under tasks | `storymap.md` body | 10-15% |
| **3** Slice | Walking-skeleton/PI/Now-Next-Later; first slice covers every backbone activity | Slice tags on stories | 5% |
| **4** Prioritize | WSJF/RICE/MoSCoW + OKR linkage + dependency feasibility check | `backlog.csv` + `backlog.md` | 15-20% |
| **4a** ACs | Given/When/Then for slice-1 stories + INVEST check | `slice-1-acceptance-criteria.md` | 10-15% |
| **4b** E2E contract | Backbone-as-contract: coverage matrix, E2E-HAPPY happy path, per-activity scenarios | `e2e-test-contract.md` | 5-10% |
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
8. **One framework-skill invocation per run** (Skill chaining cost ceiling). If you want to chain to more than one other installed skill, the discovery is too unscoped — push back to the user to narrow first.
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
2. **Story map** (three formats) — `storymap.md` (readable), `storymap.mmd` (Mermaid graph), `storymap.csv` (Jira/ADO importable).
3. **Prioritized backlog** — `backlog.csv` (full scoring) + `backlog.md` (one-page summary). Method = WSJF (SAFe default) / RICE / MoSCoW.

Optional 4th: `slice-1-acceptance-criteria.md` (Given/When/Then) for engineering handoff.
Optional 5th: `handoff.md` (what's done, what's open, smallest next decision).

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
| **1** Backbone | Mined routes/handlers/test names become activity *candidates* — propose, don't impose. Existing system shape is one input among several. | If prior `design.md` has a `## Backbone criteria` section, **default to those criteria** (only re-derive if user says to change them). Same for backbone activities — preserve unless user requests re-derivation. |
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

### Step 0 — Context collection loop (works for both from-scratch and existing-project)

Context collection is NOT a linear pipeline of "always run 0.1, then 0.2, then 0.3, then 0.4". That wastes turns on empty sources (greenfield) and over-investigates when one signal already answers the question. **Use a loop: cheap signal → form hypothesis → pick the next source based on hypothesis → repeat → exit on stable hypothesis or budget ceiling.**

#### Loop algorithm

```
hypothesis = "unknown"
turns_used = 0

loop until hypothesis is stable (no change for 2 iterations) OR turns_used > 15% of budget:
    1. Pick the cheapest source that would best refine the current hypothesis
    2. Mine it (one tool call, narrow scope)
    3. Update hypothesis based on signal (or absence of signal)
    4. Surface contradictions immediately
    5. turns_used += 1
```

#### Starter signals (always try these first, in this order)

| Signal | Cost | What it tells you |
|---|---|---|
| Working directory listing (`ls`) | free | Codebase exists? Empty dir? What languages? |
| User's prompt re-read | free | Highest-priority source — re-anchor on what user actually said |
| `.user-story-mapping/state.json` or memory MCP | free | Prior runs to extend (Mode D signal) |
| `README.md` (if present) | cheap | One-line product description — often gives the outcome statement directly |
| Interview notes in the prompt | already in context | Switch to synthesis (`customer-interview-synthesis.md`) |

After these 5 cheap signals, you should already know:
- **From-scratch** vs **existing-project** (working dir empty / no code → from-scratch)
- **Mode A vs B vs C vs D** (no prior artifact → A; brief in prompt → B; backlog input → C; storymap.md exists → D)
- **Tech stack hint** (manifest files present → existing codebase)

#### Branch-conditional sources (only mine if hypothesis warrants)

| Source | Mine when hypothesis includes... |
|---|---|
| `package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` | Existing codebase. Confirms tech stack, app type. |
| `Dockerfile`, `k8s/`, CI configs | Existing codebase. Reveals deploy topology. |
| `src/routes/`, `pages/`, `controllers/` (route grep) | Web/API/mobile codebase. Routes = user-activity candidates. |
| Test names (`grep -r "test(\|describe(\|it(" tests/`) | Test suite present. Test names = golden paths. |
| `docs/`, `ARCHITECTURE.md`, `docs/adr/` | Docs present. ADRs reveal constraints, decisions log. |
| `git log --oneline -50` | Git repo present. Reveals what's actually getting built right now. |
| Tracker MCP (Jira/ADO/GitHub) | User mentioned tracker OR Mode C. |
| Analytics/runtime MCPs (Sentry/Datadog/Mixpanel) | User mentioned production/runtime concern. |
| **Framework artifacts** — `.gsd/Brief.md`, `.gsd/Roadmap.md`, `.gsd/Decisions/`, `.gsd/task-summaries/` | If `.gsd/` directory exists — GSD users have rich pre-staged intent here |
| **Framework artifacts** — Superpowers `brainstorming/` design docs, `plans/` directory | If working in a Superpowers project — `brainstorming` stage output is gold |
| **Framework artifacts** — gstack `/plan-*-review` outputs, `/office-hours` notes if saved | If gstack is active and prior review outputs are on disk |
| **Prior `design.md` / `storymap.md` / `backlog.md`** | If they exist anywhere in the working tree — this is Mode D and they're authoritative for backbone criteria + decisions log |

**Mine framework artifacts BEFORE asking the user.** Framework state directories often contain everything the user would tell you, in cleaner form. `.gsd/Brief.md` is literally a Brief — read it before re-asking for the brief. Prior `design.md` from a previous run carries forward the backbone criteria, persona definitions, and decisions log — read it before re-deriving.

**Other installed skills can be context sources too.** If a skill like `code-explorer`, `db-schema-analyzer`, `customer-interview-summarizer`, or a sister-framework command (e.g., gstack's `/office-hours`) has already done — or can quickly do — work that would otherwise be your mining burden, invoke it via the `Skill` tool rather than re-deriving by hand. Budget one invocation per loop run; tag output as `[skill: <name>]`. Detail: `references/context-collection.md`.

The posture is: **know everything that's already written down — including what other skills can quickly tell you — before asking the user a single question.** Then ask only what's genuinely missing.

#### Exit conditions

Stop the loop and proceed to Step 0.4 (gap-filling) when ANY of:
- Hypothesis has been stable for 2 iterations (you keep confirming what you already knew)
- Budget ceiling hit (≥15% of total turns)
- User has explicitly said "we have enough, proceed"
- Working dir is empty AND no interview notes provided (skip to persona simulation or ask user)
- Strong "from-scratch" signal AND no codebase → don't mine code/tests/ADRs; pivot to Step 0.4 (persona sim or ask user)
- Strong "existing-project" signal but a single source (e.g., README) already gave the outcome → don't keep digging for redundant signal

#### What this gets right

- **From-scratch verbal idea**: Loop exits after 2-3 turns (listing + README check + prompt re-read = "no codebase, no prior artifact, just an idea"). Skips code/test/ADR mining entirely. Pivots to Step 0.4.
- **Mature existing project**: Loop iterates through README → manifests → routes → tests → ADRs → commits → tracker, refining hypothesis at each step. Stops when hypothesis stabilizes (e.g., "this is a B2B SaaS web app on Rails with 4 active feature branches" — no need to mine further).
- **Mixed signal**: README says "we're a mobile app" but `Cargo.toml` says Rust + Tauri → contradiction surfaced; user asked to clarify; only ONE side gets pursued.
- **Mode D with tracker MCP**: existing storymap.md + Jira MCP → load both, reconcile, surface deltas. Skips full code mining.

#### Surface findings in design.md

```markdown
## Context loop trace
- (1) `ls` → working dir has 47 files including `src/`, `tests/`, `docs/adr/` — existing project
- (2) `README.md` → product is "TimeSink, a B2B time-tracking SaaS for design agencies"
- (3) `package.json` → Next.js + Prisma + Postgres, dependency count 84 — mature web stack
- (4) `src/routes/` → 12 routes; backbone candidates: auth, projects, time-entries, invoices, settings
- (5) Test names (61 e2e) → golden paths: create-project, log-time, generate-invoice
- (6) `docs/adr/0017` (most recent) → "Replace Stripe Invoicing API with Paddle" (2026-04, Accepted)
- (7) Jira MCP → 23 open issues, top label "paddle-migration" (8 issues — confirms ADR-0017 is active work)
- Hypothesis: STABLE after iteration 7. Proceeding to Step 0.4.

## Contradictions flagged
- README says "Stripe-powered invoicing" — outdated per ADR-0017 (Paddle migration). Likely safe; ADR is recent. Confirm with user.
```

The trace itself is documentation — a reviewer can see exactly what evidence drove which conclusion.

#### Cost ceiling and override

Target: 5-15 tool calls for context collection on a typical project. Hard cap: 20 tool calls. If you're approaching the cap and the hypothesis still isn't stable, the project is genuinely complex — write your current best understanding to design.md, flag the residual ambiguity, and proceed.

If the user explicitly says "skip context — just build the map" or "I have a brief, work from this only", honor it. Skip Step 0 entirely; treat the prompt as the complete input. (Tag everything in design.md as `[user-stated]` or `[inferred]` only.)

Detailed source-by-source guidance (what each file/MCP gives you, how to mine cheaply): `references/context-collection.md`.

Two sub-flavors of Step 0 that often happen *inside* the loop above (not as separate sequential steps):

- **Persistent memory** — if `.user-story-mapping/state.json` exists OR the user signals "extend the prior map", read prior state as one of the cheap starter signals. Treat memory as *hints*, not gospel — verify against current state. Off by default. See `references/persistent-knowledge.md`.
- **Customer interview synthesis** — if the user provides interview transcripts/notes, extract personas (with verbatim quotes), activities, problems, hypotheses (with vote counts), non-goals. Cluster across customers. See `references/customer-interview-synthesis.md`.

### Step 0.4 — Fill remaining gaps; gate planning on completeness

After Step 0 (context loop + any memory/interview synthesis folded in) you usually still have unanswered questions. **Not every gap needs to block planning** — classify before deciding what to do.

#### Gap criticality classification

| Class | Definition | When to resolve | Example |
|---|---|---|---|
| **Blocking** | Would change the backbone, the slicing strategy, or violate the user-input-authoritative principle if left unresolved | **At Step 0.4** (gate planning) | "Two stakeholders want incompatible flows — which one wins?"; "Is this single-persona or multi-persona?" |
| **Stage-local** | Affects one downstream stage's output but not the backbone or other stages | **At the stage's entry** (mini-resolution, just-in-time) | "Don't know the WSJF size of S027" (affects Step 4 only); "Don't know what regex S015 should match" (affects Step 4a only) |
| **Deferrable** | Would refine output but not change it; the missing info is precision, not direction | **In `handoff.md`** as open questions | "Don't know exact pricing tier — assumed $10 for RICE calc"; "Don't know exact Salesforce field name — referenced as 'opportunity ID'" |

The gate at Step 0.4 applies **only to blocking gaps**. Stage-local and deferrable gaps move forward with the workflow.

#### Resolving each class

For **blocking** gaps:
1. **Ask the user** — always the first choice. List specific gaps as a checklist; ask in batches.
2. **Simulate personas** — when asking would mean 20 questions and you have enough background to role-play credibly, spawn one subagent per persona briefed with everything known. Each answers in-character. Aggregate; build a conflict matrix.

**Do not proceed to Step 1 until either:**
- All blocking conflicts are resolved (user has decided or explicitly punted), AND
- Blocking gaps simulation couldn't fill are documented as open questions OR the user has said "proceed with these gaps"

**The user always wins** over simulation. Log simulated objections as future-slice risks, not as overrides.

In single-shot/automated mode: still simulate, still build the conflict matrix, document unresolved items as "blocking decisions" in `handoff.md`, proceed with strongest defensible interpretation, tag conditional commitments with gap-ids. See `references/persona-simulation-and-gap-filling.md`.

For **stage-local** gaps:
- Note them in `design.md` under a `## Stage-local gaps to resolve` checklist
- When entering each subsequent stage, do a quick re-scan: do I have what I need for THIS stage?
- If a stage-local gap blocks the stage, run a mini Step 0.4 *scoped to that stage* — ask only what that stage needs, simulate only the relevant persona, mine only the relevant source
- Resolve, then continue forward. Don't rewind earlier stages.
- Tag resolved gaps with their source (`[user-stated]`, `[simulated]`, etc.) the same way blocking gaps are tagged

For **deferrable** gaps:
- Note them in `design.md` under `## Open questions (deferrable)`
- Apply a reasonable default; tag the field with `[inferred — see open question Q-XX]`
- Surface in `handoff.md` so the user can validate or correct after the run
- Never silently apply a default without disclosure

#### Mid-stage discovery

If a NEW gap surfaces mid-stage (e.g., during Step 2 decomposition you realize persona X has needs you don't know about):

1. **Classify it** (blocking / stage-local / deferrable) — re-use the table above
2. If **blocking** and would invalidate an earlier stage's decision: stop, surface to the user (or in single-shot, to `handoff.md`), and either pause for user input or proceed with a clearly-flagged conditional commitment
3. If **stage-local** and addressable now: resolve in-place (ask / simulate / mine), continue
4. If **deferrable**: note it, apply a default, continue

Never silently absorb a discovered gap. The cost of disclosure is one line in `design.md`; the cost of a buried assumption is "why did we build that?" three months later.

#### Late-stage escalation

If at Step 4 (prioritization) or Step 4a (ACs) a gap emerges that *would have changed* a Step 1 (backbone) or Step 3 (slicing) decision had it been known upfront:

1. **Don't silently rewrite** Steps 1-3 — that loses the audit trail
2. Surface in `handoff.md` under a `## Late-discovered gaps` section: what the gap is, what stage's output it would have changed, what the current output assumed
3. Recommend either (a) accept the current output with the caveat documented, or (b) re-run from the affected stage with the new info
4. User decides

#### Why classify

Without classification, Step 0.4 becomes a giant gate that either:
- Blocks too eagerly (every minor missing detail stops the workflow → user frustration, slow output)
- Is silently bypassed (agents proceed with "I'll figure it out as I go" → buried assumptions surface in retro)

Classification keeps the gate tight on what actually matters (the backbone + slicing + user-authoritative violations) while letting the rest resolve at the right time and cost.

### Step 1 — Establish the backbone

A backbone can be generated under different criteria, and the criteria choice changes the backbone shape. **Pick the criteria explicitly, confirm with the user, and record them in `design.md` so future runs reproduce the same backbone.**

#### Six criteria to declare (default in **bold**)

| Criterion | Options | Why it matters |
|---|---|---|
| **Frame** | **Activity flow** / Jobs-to-be-done / System interaction / Customer journey | Activity flow = Patton classic; JTBD = "when [situation] I want to [motivation] so I can [outcome]"; system interaction reads like API/touchpoints — pick one and stick with it |
| **Persona perspective** | **Primary user** (one specified by user) / Multiple parallel personas (admin + end-user) / Aggregate across personas | When personas diverge (admin vs end-user), single-perspective is cleaner; parallel risks doubling the backbone |
| **Time horizon** | **Single end-to-end session** / Day-in-the-life / Lifecycle (signup → power user → churn) | Affects how many activities. Session: 4-6. Day-in-life: 6-10. Lifecycle: 8-15. |
| **Granularity** | **5-7 activities** / 3-5 (high-level) / 8-12 (detailed) | Story-mapping convention is 5-7. Fewer is harder to slice; more is hard to read. |
| **Scope** | **Happy path only** / Happy path + error recovery / Full surface (incl. edge cases) | Happy path is the right default; recovery paths usually become slice-2/3 stories |
| **Aggregation** | **Single role per activity** / Multiple roles per activity (collaboration arrows) | Single-role is cleaner; multi-role only when handoffs ARE the activity |

#### Workflow

1. **Propose criteria** based on context loop findings and user prompt
2. **Confirm with the user** in a single message: "Proposing backbone with these criteria: [list]. Confirm or override?"
3. **Record the confirmed criteria** in `design.md` under a `## Backbone criteria` section
4. **Generate the backbone** using those criteria
5. In **Mode D** (refinement) and re-runs: read the prior criteria from `design.md` and use the same ones unless the user explicitly says to change them — this keeps the backbone reproducible

When the user is silent (single-shot / automated mode), apply defaults and explicitly state "Applied defaults: [list]. Override by re-running with criteria= ..." in `design.md`. Never silently choose without disclosure.

#### Why this matters

Without explicit criteria, two runs of the skill on the same prompt may produce different backbones — one agent picks "activity flow", another picks "jobs-to-be-done", another picks "lifecycle". The downstream slicing and prioritization differ. Recording the criteria makes the backbone:
- **Reproducible** — same prompt + same criteria + same context = same backbone
- **Reviewable** — a stakeholder can see *why* this backbone shape was chosen
- **Refinable** — Mode D extension uses the same criteria so additions are consistent

#### Backbone rules (apply regardless of criteria)

Backbone activities written in user voice, present tense, active.

Good: `Sign up`, `Find a property`, `Schedule a viewing`, `Make an offer`
Bad: `User onboarding flow`, `Search functionality`, `Booking module`, `Offer submission API`

System language (modules, APIs, services) leaks implementation thinking into a discovery artifact and breaks the slicing logic later.

**CRITICAL: Cross-cutting work doesn't belong in the backbone.** Tech debt, infrastructure, localization, theming, observability, compliance — give them their own `## Non-backbone / cross-cutting` section *below* the activity backbone, with `### Theme:` headers. They still get prioritized in `backlog.csv` (with `activity = "Non-backbone: <theme>"`) but are excluded from the slice-1 coverage check.

**❌ Wrong:** 6 backbone columns where #6 is "Tech debt" — breaks the slice-1 coverage rule (no user-facing story to put under it).
**✅ Right:** 5 user-activity columns + a `## Non-backbone / Tech debt` section below. Backbone stays a narrative.

Rule of thumb: if you can't write "As a `<user>`, I want to..." that ties to a single backbone column, the item is cross-cutting.

### Step 2 — Decompose into tasks, then stories

Tasks = the user's smaller steps within an activity. Stories = deliverable increments under tasks.

Standard form: **As a `<persona>`, I want to `<action>`, so that `<outcome>`**. Skip when it's noise ("Display loading spinner" doesn't need persona dressing).

If you find yourself writing >7 stories under one task, the task is probably two tasks. Split.

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

## Pushing the artifacts into a tracker

CSV outputs are the import source — don't recreate stories by hand inside the tool.

- **Jira / ADO / Jira Align / Targetprocess**: Activity → Epic, Task → Feature, Story → Story, Slice → Fix Version / Iteration
- **GitHub Issues + Projects v2**: labels for activity/slice/persona, Project custom fields for score, `gh` CLI for bulk creation
- **Linear**: Project per Activity, Cycle per Slice, native CSV importer
- **Trello / Notion / Airtable / spreadsheet**: import the CSV as-is

**Don't auto-create issues without asking** — generate the import command or script, then let the user run it. Detail: `references/work-item-tracking.md`.

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
├── storymap.md                        # human-readable hierarchical map
├── storymap.mmd                       # Mermaid graph (auto-generated)
├── storymap.csv                       # flat table for Jira/ADO/Excel import (auto-generated)
├── backlog.md                         # ranked summary with reasoning
├── backlog.csv                        # full backlog with WSJF/RICE/MoSCoW scores, depends_on, okr columns
├── slice-1-acceptance-criteria.md     # Given/When/Then for slice 1 (optional)
├── e2e-test-contract.md               # Backbone-as-contract E2E scenarios (optional)
└── handoff.md                         # what's done, what's open, next decision (optional)
```

Templates and column schemas live in `assets/`. Use them.

## References (load on demand, don't pre-read)

| File | When to read |
|---|---|
| `discovery-questions.md` | Mode A — driving discovery via batched questions |
| `customer-interview-synthesis.md` | Mode B with raw interview notes |
| `context-collection.md` | Step 0.3 — depth on what to mine from each source |
| `persona-simulation-and-gap-filling.md` | Step 0.4 — protocol for persona-sim subagents |
| `persistent-knowledge.md` | Step 0.1 — memory across sessions |
| `iterative-refinement-and-snapshots.md` | Mode D — extend existing map, detect limit breach |
| `slicing-strategies.md` | Step 3 — picking Patton vs PI vs Now/Next/Later |
| `prioritization-frameworks.md` | Step 4 — WSJF/RICE/MoSCoW scoring rubrics |
| `dependency-tracking.md` | Step 4 — depends_on column, cycle detection |
| `okr-alignment.md` | Step 4 — OKR column, coverage matrix |
| `acceptance-criteria.md` | Step 4a — Given/When/Then generation |
| `e2e-verification-and-contract.md` | Step 4b — backbone-as-E2E-contract |
| `framework-integration.md` | Step 6 — Superpowers/gstack/GSD/Jira/ADO/GitHub handoff |
| `work-item-tracking.md` | Step 6 — per-tool import details |
