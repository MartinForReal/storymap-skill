# Dependency tracking between stories

Record story dependencies with `H:` / `S:` / `X:` in `depends_on`, then run cycle detection and the slice-1 feasibility check. These keep "first slice covers every backbone activity" from creating an unshippable slice — refund-flow before auth, dashboard before data ingestion. Dependencies make slicing **technically feasible**.

## When to use

Run after Step 3 once backbone and stories exist, before declaring any slice valid. Skip:

- **Empty-baseline / early-discovery runs** (no codebase, brand-new product): dependencies are speculative; don't force them. See [When dependencies don't matter](#when-dependencies-dont-matter).
- Runs where slice 1 is a single activity with no cross-story preconditions.

This file owns `depends_on` **mechanics**: tag grammar, `backlog.csv` column, cycle detection, slice-1 feasibility. Edge sources live elsewhere: cross-persona edges come from the [persona interaction map](persona-simulation-and-gap-filling.md#persona-interactions); slice-1 coverage lives in [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run) (mechanics in [slicing-strategies.md](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations)).

## What counts as a dependency

Use three explicit flavors:

| Type | Symbol | Meaning | Example |
|---|---|---|---|
| **Hard** | `H:` | Cannot start until predecessor ships | Refund flow `H:` Auth (can't refund anonymously) |
| **Soft** | `S:` | Better with predecessor, technically possible without | Search filters `S:` Search basic (filters work fine, just less useful) |
| **External** | `X:` | Depends on something outside the team's control | Plaid integration `X:` Plaid contract signed |

Hard blocks slicing. Soft/external inform sequencing but do not override slice coverage.

Cross-persona handoffs create hard edges: each precondition in the [persona interaction map](persona-simulation-and-gap-filling.md#persona-interactions) — one persona's story before another's — becomes an `H:` edge. That file produces the map; this file owns `depends_on`.

## How to record them

Add a `depends_on` column to `backlog.csv`:

```csv
id,activity,task,story,slice,depends_on
S001,Sign in,SSO,User signs in with company SSO,pi-1,
S005,Issue refund,Submit,User submits a refund,pi-1,"H:S001,H:S003"
S010,Bulk refund,Batch,Process 50 refunds in one go,pi-2,"H:S005,S:S007"
```

Format as comma-joined `<type>:<story-id>` values. Multiple dependencies are fine.

In `storymap.md`, add a **Dependencies** section after the backbone:

```markdown
## Dependencies

### Hard (blocks slicing)
- S005 (Submit refund) ← S001 (SSO), S003 (Find customer)
- S014 (Audit export) ← S005, S006

### External (outside team)
- S114 (Plaid income verify) ← Plaid contract signed (Sales: ETA 2026-Q3)

### Cycles detected
(if any — see below)
```

## Cycle detection

A dependency cycle (A `H:` B `H:` C `H:` A) is always a bug: merge two stories, or re-tag one dependency soft. **Surface cycles as red-flag findings** in `handoff.md`:

```markdown
## RED FLAG: Dependency cycle detected

S008 ← S012 ← S015 ← S008

This is structurally infeasible. Either:
1. Two of these stories are actually one (collapse them), or
2. One of the deps is soft, not hard (re-tag)

Recommended: re-examine S012 (Notification rules) — it depends on S015 (Settings UI)
but S015 only needs notification rules for one of its views.
```

Do NOT break the cycle silently by reordering. Make the user resolve it.

## Slice-1 feasibility check

After slicing, run this check before declaring the slice valid:

For each story `s` in slice 1:
- Get all `depends_on` of type `H:`
- For each dependency `d`: is `d` also in slice 1?
- If not: `s` is infeasible in slice 1 → either pull `d` forward or push `s` back

Surface failures clearly:

```markdown
## Slice-1 feasibility FAIL

S005 (Submit refund) is in slice 1 but depends on:
- S003 (Find customer) — in slice 2 ❌

Either:
- Pull S003 into slice 1, OR
- Push S005 to slice 2
```

This check is separate from the coverage rule it protects: slice 1 must include ≥1 story from every active backbone activity and never silently drop a persona. The rule lives in [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run), mechanics in [slicing-strategies.md](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations); this check ensures a coverage-valid slice is buildable.

## When dependencies don't matter

For early-discovery work — empty baseline, no codebase, brand-new product — dependencies are often speculative. Don't force them. Add a note in `design.md`:

```markdown
## Dependencies
This is early discovery; dependencies will firm up after the first technical
design pass. Initial slicing assumes no hard dependencies between user activities.
```

Then leave `depends_on` blank and skip cycle/feasibility checks. Re-run next loop pass once design firms up.

## Visualizing dependencies

`scripts/storymap_to_mermaid.py` can be extended to render dependency arrows (`A -.->|H:depends| B`) only when dependency count stays small (<20). At scale, use text; diagrams become unreadable. `storymap.mmd` only emits when no tracker is defined, so tracker-backed runs use text only.

## Edge cases

- **Dependency on a non-backbone item**: fine. Tag it like any other (`S:NB-T-001`).
- **Dependency on a future-slice story required for slice 1**: canonical *pulling forward* case. Pulling forward is usually cheaper than splitting the dependent story.
- **External dependency with no team owner**: flag in `handoff.md` as a **non-engineering risk** — PM/sales/legal must drive resolution.
