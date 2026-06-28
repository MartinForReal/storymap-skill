# OKR / strategic alignment

Tie stories, or at least slices, to Key Results, then check both directions. **Orphan stories** have no KR (missing KR or out-of-scope work). **Orphan KRs** have no story coverage (unrealistic KR or forgotten plan). Surface both in `design.md`.

## When to use

Use this when the user provides OKRs/KRs, or goals clear enough to draft candidate KRs. **Skip it entirely** when the user explicitly has no OKR framework; forced OKRs are noise. This reference governs the `okr` column in `backlog.csv`, the matrix, and orphan checks; linked references own source-tagging and priority rules.

## How to record the ladder

With OKRs/KRs, add two `backlog.csv` columns: `okr` (KR id) and `okr_contribution` (how the story moves that KR). Require the latter: "ladders to KR-1.2" without a reason is decoration, not alignment.

```csv
id,activity,task,story,slice,okr,okr_contribution
S001,Sign in,SSO,User signs in with company SSO,pi-1,KR-1.2,enables enterprise tier sales
S005,Issue refund,Submit,User submits a refund,pi-1,KR-2.1,reduces CS toil per ticket
S017,Dark mode toggle,UI,Dark mode toggle,r3,,does not ladder
```

A blank `okr` cell is legitimate: a candidate orphan story. Story ids stay `S001`-style in document order, as canonical `storymap.csv`/`backlog.csv` produce them; OKR work never renumbers.

## The OKR alignment section in design.md

In `design.md`, record stated OKRs, the coverage matrix, then the two orphan lists:

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

Per-slice columns (`Slice 1`, `Slice 2`, …) catch KRs "covered" on paper but deferred past the first release; story count hides that.

## Running the two orphan checks

- **Orphan stories** — any blank `okr` row is a candidate. Decide whether the KR is missing (add/propose it) or the story is out of scope (recommend cutting). Don't leave blanks unexplained.
- **Orphan KRs** — any stated KR with zero rows, or only *enabling* stories with no user-facing path, is a planning gap. Add a concrete "clarify with <owner>" note; don't fabricate coverage.

## When you don't have OKRs

If the user gives informal goals ("we need to grow enterprise revenue") but no OKRs, draft 1-2 candidate OKRs as **proposed OKRs** in `design.md` with "Confirm with leadership". Tag drafted KRs `[inferred]` for provenance (see [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run)). Don't present them as gospel.

If the user explicitly has no OKR framework, skip this reference.

## How OKRs change prioritization

With OKRs, prioritization changes two ways (scoring math lives in [prioritization-frameworks.md](prioritization-frameworks.md)):

1. **WSJF/RICE scores get an OKR multiplier.** Stories laddering to a committed KR get a +30% (or team-chosen) Value/Impact bonus. Show it in the reasoning column.
2. **The ranked-backlog view gains a per-KR grouping** alongside per-slice grouping. Per-slice shows what ships; per-KR shows support. The slice-1 rule still binds per-slice — see [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run) (Rule 2) and [slicing-strategies.md](slicing-strategies.md).

## Anti-patterns

- **Force-fitting every story to an OKR.** Security fixes, legal compliance, and infra hygiene may not ladder to a feature OKR. Tag `OKR:HYGIENE` or leave blank — don't invent a ladder.
- **Per-story OKR theatrics.** If every row says "ladders to KR-X" vaguely, the OKRs are too broad. Push back to sharpen the KRs.
- **OKR cascade overload.** Don't require story → KR → Objective → Theme → North Star chains. Story → KR is enough; the rest is overhead.
- **Mapping the OKR id onto a tracker field unilaterally.** If the tracker already carries fix-versions, epics, or custom fields for strategy, align to that taxonomy read-only instead of minting a parallel one — see [`work-item-tracking.md`](work-item-tracking.md#align-to-the-existing-tracker-taxonomy).
