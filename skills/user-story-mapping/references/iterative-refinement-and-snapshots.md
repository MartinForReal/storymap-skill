# Iterative refinement and snapshots (the loop on a non-empty baseline)

Use for non-empty baseline. Preserve prior backbone/design/status/decisions. Step 0.5 reconciles; the loop snapshots, computes change, and surfaces breaches. From-scratch = same loop with empty sources.

> **A non-empty baseline always runs Step 0.5 first.** Reconcile storymap ↔ tracker ↔ code per [`progress-reconciliation.md`](progress-reconciliation.md). Status changes (stories shipped, activities graduated, tracker drift) populate the snapshot; don't re-derive them here.

## When this applies

Baseline is non-empty when `storymap.md`, `backlog.csv`, or equivalent exists and user wants:

- Add feature
- Re-slice PI/release boundaries
- Reprioritize after new data
- Snapshot current state ("where are we?")
- Validate constraints (team change, deadline change, OKR change)
- Sync after execution (tracker status; cuts pushed back)

No prior artifact ⇒ skip.

## What "existing" and "desired" are (the diff)

② DIFF compares:

- **Existing** = reconciled reality. Authority: tracker = status, storymap = intent, code = evidence (a route with no test is evidence, not proof). Disagreements go to `handoff.md` `## Detected drift`, never silent merge. Step 0.5 owns reconciliation/conflicts/drift via [`progress-reconciliation.md`](progress-reconciliation.md). Empty sources ⇒ ∅. User overrides all.
- **Desired** = prior map amended/overridden by input, not "prior + new." Input can add, re-slice, reprioritize, or **pivot/remove**. Contradictions archive prior position; user wins (see [§ When prior artifacts contradict the user](#when-prior-artifacts-contradict-the-user)). Desired is hypothesis at ②, confirmed in interview, concretized in stories.
- **Diff = `desired − existing`** → ADDED / UNCHANGED / MOVED / CUT / DONE **+ surfaced conflicts**. Conflicts are decisions. At ② keep feature/activity granularity for scoping, interview, and breach checks; by `handoff.md`, make it per-story.

**Nothing to resolve ≠ nothing to generate.** No conflicts/gaps means fast confirm, then generate delta: ∅ existing ⇒ whole map; clean delta ⇒ update it; **∅ diff ⇒ snapshot only** (see [§ Snapshot without changes](#snapshot-without-changes)).

## The four-step refinement process

### Step D.1 — Produce a snapshot

Capture state: `design.md` subset + calculations, not rederive.

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
- S-NEW (proposed) depends on S-AUTH (shipped) ✓
- S-X (PI 2) depends on S-Y (PI 3) ✗ INFEASIBLE — pull S-Y forward or push S-X back

### Known limits
- Team capacity: 4 engineers × 6 weeks = ~100 SP/PI
- App Store review: 10 days lead before client ship
- Compliance gate: SOC 2 opens 2026-09-01 (PI 1 must close KR-1.1)
```

Limits only: prior `design.md`, Step 0 memory signal (see [`persistent-knowledge.md`](persistent-knowledge.md)), user prompt, or `[user-stated]` facts. Unknown? Ask. **Don't assume generic capacity.**

### Step D.2 — Apply the requested change (provisionally)

Compute; don't commit.

```markdown
## Proposed change

Add feature: <name>
- New stories: S101 (8 SP), S102 (3 SP), S103 (5 SP), S104 (13 SP), S105 (5 SP) — 34 SP
- Target slice: PI 1 (per user request)
- New backbone activity: "Manage subscriptions" — absent from prior backbone
- New OKR coverage: KR-3.3 (usage-based billing)
- New dependencies: S101→S-AUTH (✓ shipped); S104→S105 (✓ both new, both PI 1)
```

### Step D.3 — Detect limit breaches

Breaches become decisions.

| Limit | Check | If breached |
|---|---|---|
| **Capacity** | SP after change ≤ slice capacity? | Show overage; offer cut N lowest-WSJF / push feature / expand capacity (more engineers, longer slice) |
| **Dependency feasibility** | every slice-1 hard dep also in slice 1? | List pairs; offer pull dep / push dependent / split dependent |
| **OKR coverage** | new story has KR ladder? owned OKRs covered? | Warn on orphan story or lost KR coverage |
| **Backbone integrity** | story activity in backbone? | New activity ⇒ warn re-slice required; demand slice-1 coverage |
| **Scope** | total stories ≤ ~50? slice-1 stories ≤ ~15? | Warn one PI too large; recommend split |
| **Cross-cutting drift** | "tech debt" / "infra" added as backbone activity? | Reject; move to Non-backbone section |
| **Stakeholder conflict** | new feature contradicts resolved `decisions.log` decision? | Surface contradiction; ask reversal confirmation |

### Step D.4 — Present trade-offs; do not silently absorb

If breached, get user decision:

```markdown
## ⚠ Change introduces breaches — your decision needed

### BREACH 1: PI 1 capacity overrun (+18 SP over)
PI 1: 92 SP → 110 SP vs. 100 SP cap (+5 stories).

Options:
A) Push S104 (13 SP, lowest WSJF in new set) to PI 2 → PI 1 lands at 97 SP ✓
B) Cut S023 + S041 (lowest WSJF in PI 1, 18 SP) → keep new feature in PI 1
C) Extend PI 1 by 1 week (~17 SP) → change release date
D) Add 5th engineer → staffing approval

Default: A (lowest political cost; preserves commitments)

### BREACH 2: KR-2.1 coverage lost
S027 (only KR-2.1 story) is implicitly displaced by the new feature.

Options:
A) Keep S027 in PI 1; KR-2.1 slips → sponsor re-baseline
B) Cut S027; KR-2.1 not attempted → leadership escalation

Default: A — committed KR; slip beats silent abandonment

### BREACH 3: new activity "Manage subscriptions" has no slice-1 coverage
New feature adds a 6th backbone activity; slice 1 has only S101.
S101 is "view subscription", not write. Demo needs one create/edit story.

Options:
A) Pull S104 (create subscription) into slice 1 — conflicts with BREACH 1
B) Defer new activity until PI 2 — keeps slice 1 tight
C) Accept partial slice-1 activity — violates the unbreakable rule, document why

Default: B (cleanest; preserves PI 1)

### Combined recommendation
Go with A (push S104) + A (keep S027, re-baseline KR-2.1) + B (defer new activity to PI 2). Net: PI 1 +21 SP; KR-2.1 slips one PI; new activity starts in PI 2.

CONFIRM before I update artifacts.
```

**Wait for user confirmation** before regenerating. In single-shot mode, document breach + recommendation in `handoff.md`, apply the default, and mark commitments conditional.

### Step D.5 — Generate the updated artifacts with a diff

After confirmation/defaults, update `design.md` / `storymap.md` / etc.; put this first in `handoff.md`:

```markdown
## Changes from prior snapshot

ADDED:
+ S101 "View subscription" (PI 1, KR-3.3)
+ S102 "Cancel subscription" (PI 1, KR-3.3)
+ S103 "Update payment method" (PI 1, KR-3.3)
+ S104 "Create subscription" (PI 2, KR-3.3) — BREACH 1 option A
+ S105 "Subscription history" (PI 2, KR-3.3)
+ New backbone activity: "Manage subscriptions" (PI 2 per BREACH 3 option B)

MOVED:
(none)

CUT:
(none)

UNCHANGED:
- Backbone 1-5 (Sign in / Find / Review / Submit / Audit)
- PI 1 commitments except +3 stories
- OKR ladders cover KR-1.2, 1.3, 2.1 (caveat), 2.2, 2.3

BREACHED LIMITS RESOLVED:
- Capacity: A (push S104 to PI 2) — PI 1 at 97 SP / 100 cap
- KR-2.1: A (kept S027, timeline re-baselined)
- New activity: B (deferred to PI 2 for clean slice-1)

OPEN AFTER CHANGE:
- KR-3.3 (usage-based billing meter) — PI 2; needs PI 1 spike
- Backbone re-introduction in PI 2 — design.md shows 6 activities
```

Diff makes shifts/trade-offs auditable.

## Snapshot without changes

Snapshot-only request ⇒ produce Step D.1; do not speculate or breach-check.

## When prior artifacts conflict with current memory

If `storymap.md` contradicts `.user-story-mapping/state.json` or MCP memory, artifact wins (see [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run)). Update memory; skip contradicted hints.

## When prior artifacts contradict the user

If prior `storymap.md` has Activity X but user says "we removed X two weeks ago", user wins. Mark X REMOVED; archive it; don't keep X because "the artifact says so."

## What NOT to do when refining

- **Don't quietly re-derive the backbone.** Preserve unless told otherwise; silent changes destroy cross-PI traceability.
- **Don't absorb new work without checking limits.** "Sure, I added the 8 new stories to PI 1" is wrong if PI 1 is at capacity. Check.
- **Don't silently break the slice-1 rule.** New backbone activity without slice-1 coverage is a user decision. "Just add it as a 6th column" breaks the rule and pollutes the backbone. Mechanics/violations live in [`slicing-strategies.md`](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations).
- **Don't lose the decisions log.** Carry prior `design.md` decisions forward. Append; never remove (mark superseded with date). Append-only: [`persistent-knowledge.md`](persistent-knowledge.md).
- **Don't pretend memory is current.** If memory is >90 days old and repo changed substantially, warn before applying it.

## Cost ceiling for refinement

Refinement costs **less than a full from-scratch run** because:
- Backbone known (skip most of Steps 1-2)
- Personas + design doc carry forward
- Snapshot + breach detection cheap

Target: 30-50% of full-run token cost. Near full-run cost means re-deriving; stop and revisit.

## Wiring with persistent memory

Refinement and [`persistent-knowledge.md`](persistent-knowledge.md) complement:
- Memory holds *delta-state* across sessions (preferences, prior decisions, current PI)
- Refinement uses current-session *artifacts-as-input*

If both exist, artifact wins conflicts. If memory is the only prior state, treat it as prior artifact.

## What each step does with prior context (per-stage)

Same loop; prior context controls carry-forward from code, tests, tracker, framework artifacts, `design.md`, memory, or all four. Empty sources mean "nothing to carry forward." **Rule: artifacts (current files) > memory > inferred. Re-derive only missing/contradicted data.**

| Stage | Existing project (code/tests/tracker/framework artifacts) | Memory / prior artifacts |
|---|---|---|
| **0** Context loop | Mine matching sources. `.gsd/` / prior `design.md` outrank redundant mining. | Load `state.json` / memory MCP. Tag `[memory: <date>]`; verify; contradicted ⇒ current wins. |
| **0.4** Gaps | Carry forward *resolved* decisions-log gaps; fill only new gaps. | Same — decisions log is gap memory. |
| **0.5** Reconcile progress | Build tracker + code + storymap status. Mark shipped `done`; detect graduated activities; surface drift. See [`progress-reconciliation.md`](progress-reconciliation.md). | Seed from prior `backlog.csv` `status`; re-pull tracker. Tracker overrides prior `status` on conflict. |
| **1** Backbone | Treat routes/handlers/test names as activity *candidates* — propose, don't impose. **Graduated activities (from Step 0.5) stay visible but are excluded from active slicing.** | Prior `design.md` `## Backbone criteria` is default. Re-derive only on user change. Preserve activities unless requested otherwise. |
| **2** Decompose | Use routes / components / handlers / endpoints as task candidates; reuse team naming. | Carry IDs. New ones use `max(prior_id) + 1` — don't renumber. |
| **3** Slice | Use tracker Fix Versions / Iteration Paths / Cycles as canonical slice names; don't invent. | Prior `design.md` slicing wins. Current PI (e.g., "PI 2026-Q3") comes from `active_pi`. |
| **4** Prioritize | Pull tracker WSJF/RICE fields as prior scores; re-score only new/changed stories. | Use memory method (WSJF / RICE / MoSCoW) if user silent. Reuse scores; annotate deltas. |
| **4a** ACs | Reference existing e2e / integration tests by file path; don't duplicate. | Preserve prior ACs verbatim for unchanged stories; regenerate only changed stories. |
| **4b** E2E contract | Let playwright / cypress / e2e suite inform it; reference scenarios by file path. State what *should* be covered. | Carry prior contract; update matrix only for added/removed activities. |
| **5** Generate derived | N/A — deterministic from storymap.md | N/A |
| **6** Hand off | Diff prior artifact (ADDED / MOVED / CUT / UNCHANGED). | If enabled, **write back** `.user-story-mapping/state.json` (or MCP memory). Never overwrite decisions log — append-only ([`persistent-knowledge.md`](persistent-knowledge.md)). |

### Three rules that apply at every stage

1. **Artifact > memory > inferred.** Current files beat stale memory; both beat inference. See [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run).
2. **Verify, don't trust.** Load memory, spot-check. If "CS rep" conflicts with pivoted README, override and update memory.
3. **Tag every fact.** Use shared source-tags for provenance — [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run).
