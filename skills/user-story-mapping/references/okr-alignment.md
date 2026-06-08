# OKR / strategic alignment

Connect each story (or at minimum, each slice) to a strategic outcome — typically an OKR or KR (Key Result). This surfaces two common misalignments:

1. **Orphan stories** — stories that don't ladder to any OKR. Either the OKR is missing or the story shouldn't be in scope.
2. **Orphan OKRs** — OKRs the company committed to that have no story coverage. Either the OKR is unrealistic or the team forgot to plan for it.

Both are red-flag findings worth surfacing.

## How to record alignment

If the user provides OKRs (or KRs), add an `okr` column to `backlog.csv`:

```csv
id,activity,task,story,slice,okr,okr_contribution
S001,Sign in,SSO,User signs in with company SSO,pi-1,KR-1.2,enables enterprise tier sales
S005,Issue refund,Submit,User submits a refund,pi-1,KR-2.1,reduces CS toil per ticket
S017,Dark mode toggle,UI,Dark mode toggle,r3,,does not ladder
```

The `okr_contribution` column is a one-line explanation of *how* the story moves the KR. Force this — "ladders to KR-1.2" with no reason is just decoration.

In `design.md`, add an **OKR alignment** section:

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

## When you don't have OKRs

If the user hasn't provided OKRs but talks about strategic goals informally ("we need to grow enterprise revenue"), draft 1-2 candidate OKRs and surface them as **proposed OKRs** in `design.md` with a "Confirm with leadership" note. Don't fabricate OKRs and treat them as gospel.

If the user explicitly has no OKR framework, skip this section entirely. Adding OKR-style structure to a team that doesn't use OKRs is bureaucratic noise.

## How OKRs change prioritization

When OKRs are present, two things happen to the prioritization step:

1. **WSJF/RICE scores get an OKR multiplier.** Stories that ladder to a committed KR get a +30% (or whatever the team decides) bonus to their Value/Impact score. Make this explicit in the reasoning column.
2. **The "ranked backlog" view gets a per-KR grouping** alongside the per-slice grouping. Both views are useful: per-slice tells you what ships; per-KR tells you how the KR is supported.

## Anti-patterns

- **Force-fitting every story to an OKR.** Some stories (security fixes, legal compliance, infra hygiene) legitimately don't ladder to a feature OKR. Tag them with a generic `OKR:HYGIENE` or leave blank — don't invent a ladder.
- **Per-story OKR theatrics.** If you find yourself writing "ladders to KR-X" with vague justification on every row, the OKRs are too broad. Push back to the user to sharpen the KRs.
- **OKR cascade overload.** Don't require story → KR → Objective → Theme → North Star chains. Story → KR is enough. The rest is overhead.
