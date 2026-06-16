# Dependency tracking between stories

Tag every blocking relationship between stories explicitly with `H:` / `S:` / `X:` in a `depends_on` column, then run two checks the rest of the workflow can't run for you: cycle detection and a slice-1 feasibility check. This is what keeps the "first slice covers every backbone activity" coverage rule from producing a slice the team literally cannot ship — refund-flow before auth, dashboard before data ingestion. Dependencies make the slicing recommendation **technically feasible**, not just narratively complete.

## When to use

Run dependency tracking once a backbone and stories exist (Step 3 onward), before declaring any slice valid. Two cases skip it:

- **Empty-baseline / early-discovery runs** (no codebase, brand-new product): dependencies are speculative — don't force them. See [When dependencies don't matter](#when-dependencies-dont-matter).
- Runs where slice 1 is a single activity with no cross-story preconditions.

This file owns the `depends_on` **mechanics** — the tag grammar, the `backlog.csv` column, cycle detection, and the slice-1 feasibility check. It does not own *where the edges come from*: the cross-persona ones are discovered in the [persona interaction map](persona-simulation-and-gap-filling.md#persona-interactions), and the slice-1 coverage rule those checks defend is governed in [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run) (mechanics in [slicing-strategies.md](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations)).

## What counts as a dependency

Three flavors. Tag each explicitly:

| Type | Symbol | Meaning | Example |
|---|---|---|---|
| **Hard** | `H:` | Cannot start until predecessor ships | Refund flow `H:` Auth (can't refund anonymously) |
| **Soft** | `S:` | Better with predecessor, technically possible without | Search filters `S:` Search basic (filters work fine, just less useful) |
| **External** | `X:` | Depends on something outside the team's control | Plaid integration `X:` Plaid contract signed |

Hard dependencies block slicing. Soft and external dependencies inform sequencing but don't override the slice-coverage rule.

A primary source of hard edges is cross-persona handoffs: every precondition in the [persona interaction map](persona-simulation-and-gap-filling.md#persona-interactions) — where one persona's story must exist before another's — lands here as an `H:` edge. The map is produced there; this file owns the `depends_on` mechanics it lands in.

## How to record them

Add a `depends_on` column to `backlog.csv`:

```csv
id,activity,task,story,slice,depends_on
S001,Sign in,SSO,User signs in with company SSO,pi-1,
S005,Issue refund,Submit,User submits a refund,pi-1,"H:S001,H:S003"
S010,Bulk refund,Batch,Process 50 refunds in one go,pi-2,"H:S005,S:S007"
```

The format is `<type>:<story-id>` joined by commas. Multiple dependencies are fine.

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

A dependency cycle (A `H:` B `H:` C `H:` A) is always a bug — either two of those stories are actually one story, or one of the deps is soft not hard. **Surface cycles as red-flag findings** in `handoff.md`:

```markdown
## RED FLAG: Dependency cycle detected

S008 ← S012 ← S015 ← S008

This is structurally infeasible. Either:
1. Two of these stories are actually one (collapse them), or
2. One of the deps is soft, not hard (re-tag)

Recommended: re-examine S012 (Notification rules) — it depends on S015 (Settings UI)
but S015 only needs notification rules for one of its views.
```

Do NOT silently break the cycle by reordering. Make the user resolve it.

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

This feasibility check is a distinct concern from the coverage rule it protects. The coverage rule (slice 1 must include ≥1 story from every active backbone activity, never silently drop a persona) is stated in [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run) and its mechanics in [slicing-strategies.md](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations); this check makes sure the slice that satisfies coverage is also buildable.

## When dependencies don't matter

For early-discovery work — the loop running on an empty baseline, no codebase, brand-new product — dependencies are often speculative. Don't force them in. Add a note in `design.md`:

```markdown
## Dependencies
This is early discovery; dependencies will firm up after the first technical
design pass. Initial slicing assumes no hard dependencies between user activities.
```

Then leave the `depends_on` column blank and skip the cycle/feasibility checks. Re-run them on the next pass of the loop, once the design firms up.

## Visualizing dependencies

`scripts/storymap_to_mermaid.py` can be extended to render dependencies as additional arrows in the Mermaid graph (`A -.->|H:depends| B`), but only if dependency count stays small (<20). At scale, the diagram becomes unreadable; use the textual Dependencies section instead. (Note `storymap.mmd` is only emitted when no tracker is defined; in a tracker-backed run the textual Dependencies section is the only rendering.)

## Edge cases

- **Dependency on a non-backbone item**: fine. Tag it like any other (`S:NB-T-001`).
- **Dependency on a story in a future slice that's a prerequisite for slice 1**: that's the canonical case for *pulling forward*. The cheaper option is usually pulling forward; the more expensive option is splitting the dependent story.
- **External dependency with no team owner**: flag in `handoff.md` as a **non-engineering risk** — needs PM/sales/legal to drive resolution.
