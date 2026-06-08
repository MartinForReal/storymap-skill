# Iterative refinement and snapshots (Mode D)

User stories change over time. A story map written 3 months ago has stale priorities, outdated personas, finished work, and new constraints. Mode D is how this skill handles "extend / re-slice / add a feature" requests against an existing map — and crucially, how it **detects when a new request breaks the team's limits** rather than silently absorbing it.

## When this applies

- The user has an existing `storymap.md`, `backlog.csv`, or equivalent — produced by this skill, by another tool, or hand-written
- They want to:
  - Add a new feature
  - Re-slice (move work between PI/release boundaries)
  - Reprioritize after new data
  - Get a snapshot of current state ("where are we?")
  - Validate the plan against new constraints (team change, deadline change, OKR change)

If they have nothing prior, you're in Mode A/B/C, not D.

## The four-step Mode D process

### Step D.1 — Produce a snapshot

Before changing anything, capture **current state**. The snapshot is a focused subset of `design.md` content (don't re-derive the whole thing) plus calculations:

```markdown
## Snapshot (as of YYYY-MM-DD)

### Slice composition
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
- Memory (Step 0.1)
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

If the user provides a `storymap.md` that contradicts `.user-story-mapping/state.json` (or MCP memory), the artifact wins — it's higher in the priority order than memory. Update memory to match the artifact after the run; don't silently apply memory hints that contradict the visible map.

## When prior artifacts contradict the user

If the prior `storymap.md` has Activity X but the user says "we removed X two weeks ago", the user wins. Mark X as REMOVED in the diff; archive the prior position. Don't keep X around because "the artifact says so".

## What NOT to do in Mode D

- **Don't quietly re-derive the backbone.** Mode D preserves the prior backbone unless explicitly told to re-derive. Silently changing the backbone destroys cross-PI traceability.
- **Don't absorb new work without checking limits.** "Sure, I added the 8 new stories to PI 1" is wrong if PI 1 is already at capacity. Always check; always surface.
- **Don't silently break the slice-1 rule.** If the new feature introduces a backbone activity with no slice-1 coverage, that's a decision the user must make. The default of "just add it as a 6th column" is wrong twice — it breaks the rule AND pollutes the backbone with cross-cutting drift.
- **Don't lose the decisions log.** The prior `design.md` decisions log carries forward. Append new decisions; never remove old ones (mark as superseded with date).
- **Don't pretend memory is current.** If memory is >90 days old and the repo has changed substantially, warn the user before applying.

## Cost ceiling for Mode D

Most Mode D invocations should cost **less than a full mode A/B/C run** because:
- Backbone is already known (skip most of Steps 1-2)
- Personas + design doc carry forward (small updates only)
- Most of the work is the snapshot + breach detection (cheap)

Target: 30-50% of the token cost of a full run. If you're approaching a full-run cost, you're probably re-deriving rather than refining — stop and revisit.

## Wiring with persistent memory

Mode D and `references/persistent-knowledge.md` are complementary:
- Memory holds *delta-state* across sessions (preferences, prior decisions, current PI)
- Mode D operates on *artifacts-as-input* in the current session

Both can be active. If both are present, the artifact's snapshot wins where they disagree. If memory is the only source of prior state and no artifact exists, treat the memory snapshot as the prior artifact and proceed.
