# Iterative refinement and snapshots (the loop on a non-empty baseline)

When the loop runs against an existing map — an extend / re-slice / reprioritize / "where are we?" request — it does **not** rebuild from zero and it does **not** silently absorb new work: it snapshots current state, computes the change provisionally, and surfaces any limit it would breach as a decision for the user. The same loop that runs from scratch runs here; the only difference is that the data sources hold a prior backbone, design doc, statuses, and decisions to carry forward instead of being empty.

> **A non-empty baseline always runs Step 0.5 first.** Before producing the snapshot below, reconcile prior storymap ↔ tracker ↔ code state per [`progress-reconciliation.md`](progress-reconciliation.md). Status changes since the prior run (stories shipped, activities graduated, tracker drift) populate the snapshot — they are not re-derived inside this refinement step.

## When this applies

The baseline is non-empty: the user already has a `storymap.md`, `backlog.csv`, or equivalent — produced by this skill, by another tool, or hand-written — and they want to:

- Add a new feature
- Re-slice (move work between PI/release boundaries)
- Reprioritize after new data
- Get a snapshot of current state ("where are we?")
- Validate the plan against new constraints (team change, deadline change, OKR change)
- Sync the storymap with reality after a sprint or two of execution (status pull from tracker; cuts pushed back)

If they have nothing prior, the baseline is empty — this refinement step doesn't apply; the loop runs on empty data sources instead (the "from scratch" case).

## What "existing" and "desired" are (the diff)

The loop's ② DIFF compares two things, and neither is a naive snapshot:

- **Existing** = a *reconciled* view of current reality. The sources carry **different authority** — tracker = status, storymap = intent, code = evidence (a route with no test is evidence, not proof) — and where they **disagree** the conflict is surfaced in `handoff.md` `## Detected drift`, never silently merged. Step 0.5 builds it; the reconciliation, conflict table, and drift detectors are owned by [`progress-reconciliation.md`](progress-reconciliation.md). Empty sources ⇒ existing is ∅ (from-scratch). The user overrides all sources.
- **Desired** = the prior map **amended/overridden by the user's new input** — *not* "prior + new." User input is top authority, so a new prompt can add, re-slice, reprioritize, or **pivot/remove**; where it contradicts the prior, the user wins and the prior position is **archived**, not retained (see [§ When prior artifacts contradict the user](#when-prior-artifacts-contradict-the-user)). Desired is a hypothesis at ②, confirmed at the interview, concretized when stories are generated.
- **Diff = `desired − existing`** → ADDED / UNCHANGED / MOVED / CUT / DONE **+ the surfaced conflicts** (decisions for the user, not auto-resolved). **Coarse at ②** (feature/activity level — scopes work, frames the interview, triggers the breach checks below), **per-story by `handoff.md`**.

**Nothing to resolve ≠ nothing to generate.** When the diff surfaces no conflicts/gaps the interview is a fast confirm and the generative steps still run on the delta: ∅ existing ⇒ author the whole map; a clean delta ⇒ update only it; **∅ diff ⇒ a snapshot, no regeneration** (see [§ Snapshot without changes](#snapshot-without-changes)).

## The four-step refinement process

### Step D.1 — Produce a snapshot

Before changing anything, capture **current state**. The snapshot is a focused subset of `design.md` content (don't re-derive the whole thing) plus calculations:

```markdown
## Snapshot (as of YYYY-MM-DD)

### Implementation status (sourced from Step 0.5 reconciliation)
| Activity | Total | Done | In-progress | Blocked | Deferred | Cut | Unchanged | Notes |
|---|---|---|---|---|---|---|---|---|
| 1. Sign in | 4 | 4 | 0 | 0 | 0 | 0 | 0 | **GRADUATED** |
| 2. Find transaction | 5 | 2 | 1 | 0 | 1 | 0 | 1 | |
| 3. Submit refund | 7 | 0 | 2 | 1 | 0 | 0 | 4 | |

### Slice composition (active backbone only — graduated activities excluded)
| Slice | Stories | Backbone activities covered | Capacity used | Capacity remaining |
|---|---|---|---|---|
| PI 1 | 18 | 5/5 ✓ | 92 SP / 100 cap | 8 SP |
| PI 2 | 14 | 4/5 (missing: Audit) | 70 SP / 100 cap | 30 SP |
| Backlog (no slice) | 23 | — | — | — |

### OKR coverage
| KR | Stories | Status |
|---|---|---|
| KR-1.2 SAML SSO | 4 (all PI 1) | committed |
| KR-2.1 anomaly detection | 0 | ORPHAN — at risk |

### Open dependencies
- S-EMRGY (PI 1) depends on S-RBAC (PI 1) ✓ feasible
- S-NEW (proposed) depends on S-AUTH (already shipped) ✓
- S-X (PI 2) depends on S-Y (PI 3) ✗ INFEASIBLE — pull S-Y forward or push S-X back

### Known limits
- Team capacity: 4 engineers × 6 weeks = ~100 SP per PI
- App Store review window: 10 days lead time before any client ship
- Compliance gate: SOC 2 audit window opens 2026-09-01 (PI 1 must close KR-1.1)
```

Don't fabricate the limits. Get them from:
- The prior `design.md` if it exists
- Memory loaded as a Step 0 starter signal (see [`persistent-knowledge.md`](persistent-knowledge.md))
- The user's prompt
- Tagged in `[user-stated]` if user provided in this conversation

If a limit is unknown, ask. **Don't assume a generic capacity number.**

### Step D.2 — Apply the requested change (provisionally)

Compute what the change would do, but **don't commit yet**:

```markdown
## Proposed change

Add feature: <name>
- New stories: S101 (8 SP), S102 (3 SP), S103 (5 SP), S104 (13 SP), S105 (5 SP) — total 34 SP
- Target slice: PI 1 (per user request)
- New backbone activity: "Manage subscriptions" — was not in prior backbone
- New OKR coverage: ladders to KR-3.3 (usage-based billing)
- New dependencies: S101 depends on S-AUTH (✓ shipped); S104 depends on S105 (✓ both new, both PI 1)
```

### Step D.3 — Detect limit breaches

Run each check. Surface any breach as a **decision the user must make**, not a problem to silently resolve.

| Limit | Check | If breached |
|---|---|---|
| **Capacity** | sum(SP of slice after change) ≤ slice capacity? | Show overage. Offer: cut N stories from existing slice (rank by lowest WSJF) / push new feature to next slice / expand capacity (more engineers, longer slice) |
| **Dependency feasibility** | every hard dep of every slice-1 story also in slice 1? | List infeasible pairs. Offer: pull dep forward / push dependent back / split the dependent |
| **OKR coverage** | new story has a KR ladder? OKRs we own still covered? | If new story is orphan: warn it's hard to defend. If existing KR loses coverage: warn the team committed to it. |
| **Backbone integrity** | new story's activity exists in backbone? | If new activity: warn it changes the backbone (re-slice required) and demand slice-1 coverage |
| **Scope** | total stories ≤ ~50? slice-1 stories ≤ ~15? | If exceeded: warn the work is too big to plan as one PI; recommend split |
| **Cross-cutting drift** | new "tech debt" or "infra" stories being added as a backbone activity? | Reject the placement; move to Non-backbone section |
| **Stakeholder conflict** | new feature contradicts a previously-resolved decision in `decisions.log`? | Surface the contradiction; ask user to confirm reversal |

### Step D.4 — Present trade-offs; do not silently absorb

If any breach was detected, the user must decide before you commit the change. Output:

```markdown
## ⚠ Change introduces breaches — your decision needed

### BREACH 1: PI 1 capacity overrun (+18 SP over)
Adding the 5 new stories pushes PI 1 from 92 SP to 110 SP against a 100 SP cap.

Options:
A) Push S104 (13 SP, lowest WSJF in the new set) to PI 2 → PI 1 lands at 97 SP ✓
B) Cut existing S023 + S041 (lowest WSJF in PI 1, total 18 SP) → keeps new feature in PI 1
C) Extend PI 1 by 1 week (add ~17 SP capacity) → requires release-date change
D) Add a 5th engineer → requires hiring/staffing approval

Default recommendation: A (lowest political cost, preserves existing commitments).

### BREACH 2: KR-2.1 coverage lost
S027 (the only story laddering to KR-2.1) is being implicitly displaced by the new feature.

Options:
A) Keep S027 in PI 1, accept KR-2.1 will slip → re-baseline with sponsor
B) Cut S027 and accept KR-2.1 isn't being attempted → escalate to leadership

Default recommendation: A — the KR was committed; better to slip than abandon silently.

### BREACH 3: new activity "Manage subscriptions" has no slice-1 coverage
Adding the new feature introduces a 6th backbone activity, but only S101 is in slice 1
under it — and S101 is the "view subscription" story, not a write path. End-to-end demo
of the new activity needs at least one create/edit story in slice 1.

Options:
A) Pull S104 (create subscription) into slice 1 — but this conflicts with BREACH 1
B) Defer the new activity entirely until PI 2 — keeps slice 1 tight
C) Accept that slice 1 has a partial new activity — violates the unbreakable rule, document why

Default recommendation: B (cleanest, preserves PI 1).

### Combined recommendation
Go with A (push S104) + A (keep S027, re-baseline KR-2.1) + B (defer new activity to PI 2).
Net change: PI 1 gains 21 SP of new feature work, KR-2.1 timeline slips one PI,
new activity is fully introduced in PI 2 instead of partially in PI 1.

CONFIRM before I commit this to the updated artifacts.
```

**Wait for user confirmation** before regenerating the artifacts. In single-shot mode where no live user exists, document the breach + recommended resolution in `handoff.md`, proceed with the default recommendation, and clearly mark every resulting commitment as conditional.

### Step D.5 — Generate the updated artifacts with a diff

After the user confirms (or in single-shot mode, after applying defaults), produce updated `design.md` / `storymap.md` / etc. **Include a diff-style summary** at the top of `handoff.md`:

```markdown
## Changes from prior snapshot

ADDED:
+ S101 "View subscription" (PI 1, ladder to KR-3.3)
+ S102 "Cancel subscription" (PI 1, ladder to KR-3.3)
+ S103 "Update payment method" (PI 1, ladder to KR-3.3)
+ S104 "Create subscription" (PI 2, ladder to KR-3.3) — pushed per BREACH 1 option A
+ S105 "Subscription history" (PI 2, ladder to KR-3.3)
+ New backbone activity: "Manage subscriptions" (introduced PI 2 per BREACH 3 option B)

MOVED:
(none)

CUT:
(none)

UNCHANGED:
- Backbone activities 1-5 (Sign in / Find / Review / Submit / Audit)
- All PI 1 commitments except the +3 new stories
- Prior OKR ladders (still cover KR-1.2, 1.3, 2.1 with caveat, 2.2, 2.3)

BREACHED LIMITS RESOLVED:
- Capacity: option A (push S104 to PI 2) — PI 1 at 97 SP / 100 cap
- KR-2.1: option A (kept S027, KR-2.1 timeline re-baselined)
- New activity: option B (deferred to PI 2 for clean slice-1)

OPEN AFTER CHANGE:
- KR-3.3 (usage-based billing meter) — committed for PI 2; needs spike in PI 1 to validate
- Backbone re-introduction in PI 2 — design.md updated to reflect 6 activities
```

The diff is what makes the change **reviewable** — a stakeholder can see exactly what shifted and audit the trade-offs.

## Snapshot without changes

If the user just asks "give me a snapshot" (no change request), produce only Step D.1. Don't speculate about changes; don't run breach detection on a hypothetical. The snapshot itself is the deliverable.

## When prior artifacts conflict with current memory

If the user provides a `storymap.md` that contradicts `.user-story-mapping/state.json` (or MCP memory), the artifact wins — it's higher in the priority order than memory (see [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run)). Update memory to match the artifact after the run; don't silently apply memory hints that contradict the visible map.

## When prior artifacts contradict the user

If the prior `storymap.md` has Activity X but the user says "we removed X two weeks ago", the user wins. Mark X as REMOVED in the diff; archive the prior position. Don't keep X around because "the artifact says so".

## What NOT to do when refining

- **Don't quietly re-derive the backbone.** Refinement preserves the prior backbone unless explicitly told to re-derive. Silently changing the backbone destroys cross-PI traceability.
- **Don't absorb new work without checking limits.** "Sure, I added the 8 new stories to PI 1" is wrong if PI 1 is already at capacity. Always check; always surface.
- **Don't silently break the slice-1 rule.** If the new feature introduces a backbone activity with no slice-1 coverage, that's a decision the user must make. The default of "just add it as a 6th column" is wrong twice — it breaks the rule AND pollutes the backbone with cross-cutting drift. The mechanics and violations of the slice-1 rule live in [`slicing-strategies.md`](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations).
- **Don't lose the decisions log.** The prior `design.md` decisions log carries forward. Append new decisions; never remove old ones (mark as superseded with date) — the append-only rule is owned by [`persistent-knowledge.md`](persistent-knowledge.md).
- **Don't pretend memory is current.** If memory is >90 days old and the repo has changed substantially, warn the user before applying.

## Cost ceiling for refinement

Most refinement runs should cost **less than a full from-scratch run** because:
- Backbone is already known (skip most of Steps 1-2)
- Personas + design doc carry forward (small updates only)
- Most of the work is the snapshot + breach detection (cheap)

Target: 30-50% of the token cost of a full run. If you're approaching a full-run cost, you're probably re-deriving rather than refining — stop and revisit.

## Wiring with persistent memory

Refinement and [`persistent-knowledge.md`](persistent-knowledge.md) are complementary:
- Memory holds *delta-state* across sessions (preferences, prior decisions, current PI)
- Refinement operates on *artifacts-as-input* in the current session

Both can be active. If both are present, the artifact's snapshot wins where they disagree. If memory is the only source of prior state and no artifact exists, treat the memory snapshot as the prior artifact and proceed.

## What each step does with prior context (per-stage)

It's the same loop every time; this table spells out what each step does with whatever prior context the data sources hold — an existing codebase, a prior `design.md`, persistent memory, an active tracker, or all four. With empty data sources, each row degenerates to "nothing to carry forward." **The rule: artifacts (current files) > memory > inferred. Re-derive only what's missing or contradicted.**

| Stage | If existing project (code/tests/tracker/framework artifacts) | If memory / prior artifacts |
|---|---|---|
| **0** Context loop | Mine the conditional sources that match the hypothesis. Framework artifacts (`.gsd/`, prior `design.md`) take precedence over redundant mining. | Load `state.json` / memory MCP as a starter signal. Tag loaded facts `[memory: <date>]`. Verify each against current state — if contradicted, current wins. |
| **0.4** Gaps | Gaps previously *resolved* in the decisions log carry forward — don't re-ask. Only newly-introduced gaps need filling. | Same — decisions log is the gap-resolution memory. |
| **0.5** Reconcile progress | Build status map from tracker + code surfaces + prior storymap. Mark shipped stories `done`; detect graduated activities; surface tracker drift. See [`progress-reconciliation.md`](progress-reconciliation.md). | Prior `backlog.csv` `status` column carries forward as the seed. Re-pull from tracker for live status; tracker overrides prior `status` value when they conflict. |
| **1** Backbone | Mined routes/handlers/test names become activity *candidates* — propose, don't impose. **Graduated activities (from Step 0.5) stay visible but are excluded from active slicing.** | If prior `design.md` has a `## Backbone criteria` section, **default to those criteria** (only re-derive if the user says to change them). Preserve backbone activities unless the user requests re-derivation. |
| **2** Decompose | Existing routes / components / handlers / endpoints are pre-existing task candidates under their activity. Reuse the team's existing naming. | Prior task/story IDs carry forward. New tasks/stories get fresh IDs from `max(prior_id) + 1` — don't renumber. |
| **3** Slice | If the tracker has existing Fix Versions / Iteration Paths / Cycles, those are the canonical slice names — use them, don't invent. | Prior slicing strategy from `design.md` wins. Current PI name (e.g., "PI 2026-Q3") comes from memory's `active_pi`. |
| **4** Prioritize | If the tracker stores WSJF/RICE values already (custom fields), pull them as the prior scores. Re-score only stories the team changed or new ones. | Method preference (WSJF / RICE / MoSCoW) from memory wins if the user is silent. Prior scores reused; deltas annotated. |
| **4a** ACs | Existing e2e / integration test names are candidate AC sources — reference them by file path. Don't duplicate. | Prior ACs preserved verbatim for unchanged stories. Re-generated only for changed stories. |
| **4b** E2E contract | Existing playwright / cypress / e2e suite informs the contract — reference scenarios by file path. The contract documents what *should* be covered, not re-writes what is. | Prior contract carries forward; coverage matrix updated only for added/removed activities. |
| **5** Generate derived | N/A — deterministic from storymap.md | N/A |
| **6** Hand off | Diff-style summary against the prior artifact (ADDED / MOVED / CUT / UNCHANGED). | If memory is enabled, **write back** updated state to `.user-story-mapping/state.json` (or MCP memory). Never overwrite the decisions log — append-only (see [`persistent-knowledge.md`](persistent-knowledge.md)). |

### Three rules that apply at every stage

1. **Artifact > memory > inferred.** Current files win over stale memory; both win over inference. This sits inside the user-input-authoritative priority order owned by [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run).
2. **Verify, don't trust.** Load memory; immediately spot-check against current state. If a remembered persona is "CS rep" but the README pivoted away, override and update memory.
3. **Tag every fact.** Use the shared source-tag vocabulary so reviewers and later loop runs know where each claim came from — defined in [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run).
