# OKR / strategic alignment

Tie every story (or at minimum every slice) to a Key Result, then run the coverage matrix in both directions: it surfaces **orphan stories** (work that ladders to no KR — either the KR is missing or the work is out of scope) and **orphan KRs** (committed Key Results with zero story coverage — either the KR is unrealistic or the team forgot to plan for it). Both are red-flag findings worth surfacing in `design.md`.

## When to use

Apply this when the user provides OKRs/KRs, or talks about strategic goals informally enough that candidate KRs can be drafted. **Skip it entirely** when the user explicitly has no OKR framework — bolting OKR structure onto a team that doesn't use OKRs is bureaucratic noise. This reference governs the `okr` ladder column in `backlog.csv`, the coverage matrix, and the two orphan checks; it does not own the source-tagging or priority rules it touches — those are linked below.

## How to record the ladder

When OKRs (or KRs) are provided, add two columns to `backlog.csv`: `okr` (the KR id this story ladders to) and `okr_contribution` (a one-line explanation of *how* the story moves that KR). Force the contribution — "ladders to KR-1.2" with no reason is decoration, not alignment.

```csv
id,activity,task,story,slice,okr,okr_contribution
S001,Sign in,SSO,User signs in with company SSO,pi-1,KR-1.2,enables enterprise tier sales
S005,Issue refund,Submit,User submits a refund,pi-1,KR-2.1,reduces CS toil per ticket
S017,Dark mode toggle,UI,Dark mode toggle,r3,,does not ladder
```

A blank `okr` cell is a legitimate signal, not an omission — it flags a candidate orphan story for the matrix below. Story ids stay `S001`-style in document order, exactly as the canonical `storymap.csv`/`backlog.csv` produce them; OKR work never renumbers them.

## The OKR alignment section in design.md

Record the stated OKRs, then the coverage matrix, then the two orphan lists. This is the payload that makes the alignment auditable:

```markdown
## OKR alignment

### Stated OKRs (from product brief)
- O1: Become viable for enterprise customers by EOY
  - KR-1.1: Land 3 enterprise contracts ≥$100K ARR
  - KR-1.2: SOC 2 Type II audit passed
- O2: Reduce operational burden on CS
  - KR-2.1: Cut CS time-per-refund-ticket from 22min → 5min
  - KR-2.2: 80% of refund cases self-served by EOY

### Coverage matrix
| KR | Story count | Slice 1 | Slice 2 | Notes |
|---|---|---|---|---|
| KR-1.1 | 8 | 3 | 5 | SSO + SCIM in slice 1 |
| KR-1.2 | 12 | 4 | 8 | Audit log + retention in slice 1; SOC 2 evidence in slice 2 |
| KR-2.1 | 14 | 10 | 4 | Bulk of refund-flow stories |
| KR-2.2 | 5 | 2 | 3 | Self-service path partial in slice 1 |

### Orphan stories (no OKR ladder)
- S017 Dark mode toggle — no KR ties; recommend cutting from this PI
- S089 Refactor search index to OpenSearch — tech-debt; should ladder to a Reliability KR if one exists

### Orphan OKRs (no story coverage)
- KR-1.1 "Land 3 enterprise contracts" has only enabling stories (SSO/SCIM/SOC 2) but no GTM-side stories — clarify with Sales whether their work is in scope here or separate
```

The matrix's per-slice columns (`Slice 1`, `Slice 2`, …) are how you catch a KR that is "covered" on paper but deferred entirely past the first release — story count alone hides that.

## Running the two orphan checks

- **Orphan stories** — walk the backlog; any row with a blank `okr` is a candidate. Decide per row: the KR is genuinely missing (add or propose it), or the story is out of scope (recommend cutting). Don't silently leave a blank cell unexplained.
- **Orphan KRs** — walk the stated KRs; any KR with zero rows pointing at it, or covered only by *enabling* stories with no user-facing path, is a planning gap. Surface it with a concrete "clarify with <owner>" note rather than fabricating coverage.

## When you don't have OKRs

If the user talks about strategic goals informally ("we need to grow enterprise revenue") but states no OKRs, draft 1-2 candidate OKRs and surface them as **proposed OKRs** in `design.md` with a "Confirm with leadership" note. Tag any drafted KR `[inferred]` per the source-tag vocabulary so its provenance is visible (see [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run)). Don't fabricate OKRs and present them as gospel.

If the user explicitly has no OKR framework, skip this reference.

## How OKRs change prioritization

When OKRs are present, two things happen during prioritization (the scoring math itself lives in [prioritization-frameworks.md](prioritization-frameworks.md)):

1. **WSJF/RICE scores get an OKR multiplier.** Stories that ladder to a committed KR get a +30% (or whatever the team decides) bonus to their Value/Impact score. Make the bonus explicit in the reasoning column.
2. **The ranked-backlog view gains a per-KR grouping** alongside the per-slice grouping. Both are useful: per-slice tells you what ships; per-KR tells you how each KR is supported. The slice-1 governing rule still binds the per-slice view — see [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run) (Rule 2) and the mechanics in [slicing-strategies.md](slicing-strategies.md).

## Anti-patterns

- **Force-fitting every story to an OKR.** Some stories (security fixes, legal compliance, infra hygiene) legitimately don't ladder to a feature OKR. Tag them `OKR:HYGIENE` or leave the cell blank — don't invent a ladder.
- **Per-story OKR theatrics.** If you're writing "ladders to KR-X" with vague justification on every row, the OKRs are too broad. Push back to the user to sharpen the KRs.
- **OKR cascade overload.** Don't require story → KR → Objective → Theme → North Star chains. Story → KR is enough; the rest is overhead.
- **Mapping the OKR id onto a tracker field unilaterally.** If the work item tracker already carries fix-versions, epics, or custom fields for strategy, align to that taxonomy read-only rather than minting a parallel one — see [`work-item-tracking.md`](work-item-tracking.md#align-to-the-existing-tracker-taxonomy).
