# Handoff — Refund Self-Service Portal story map

## What's in the box

Six canonical files in this output directory, all consistent with each other:

| File                | What it is                                                                                       |
|---------------------|--------------------------------------------------------------------------------------------------|
| `design.md`         | Personas, outcome, hypotheses, constraints, **assumptions A1–A7** (highlighted; need confirming), decision log |
| `storymap.md`       | Backbone of 5 user activities + 4 cross-cutting themes; 52 stories tagged by PI slice            |
| `storymap.csv`      | Flat 52-row table; ready to import into Jira / ADO / Excel                                       |
| `storymap.mmd`      | Mermaid graph (paste into anything that renders Mermaid — GitHub, Notion, docs)                  |
| `backlog.md`        | One-page ranked summary with top-10, per-slice tables, suggested sprint shape for PI 1            |
| `backlog.csv`       | Full 52-story WSJF-scored backlog with `wsjf_value / wsjf_time / wsjf_risk / wsjf_size` columns  |

## Key facts (no live user — I made assumptions; please verify)

- **Mode:** Mode A (from scratch — no PRD, no brief, no backlog existed)
- **Slicing strategy:** SAFe PI (pi-1 / pi-2 / pi-3), driven by user's "12-week PI in 3 weeks" signal
- **Prioritization:** WSJF (modified Fibonacci 1, 2, 3, 5, 8, 13, 20), per user's explicit request
- **Story counts:** 32 pi-1 / 17 pi-2 / 3 pi-3 (52 total)
- **Slice-1 coverage rule:** all 5 backbone activities have ≥1 pi-1 story — verified
- **WSJF math:** every row reconciles `(value + time + risk) / size = score` — verified

## Things the user is NOT a live user — so I made these choices for them

Documented in `design.md` § Assumptions and § Decisions log:

1. Slicing = SAFe PI (matched user's PI cadence signal directly).
2. Prioritization = WSJF (user said so explicitly).
3. Approval workflow scoped into pi-1, not deferred (fintech + finance trust make this load-bearing for H4).
4. Partial refunds, multi-currency, batched payments explicitly out of pi-1 (keeps the walking skeleton honest).
5. Single team, no full ART, no RTE (4 eng + 1 PM team doesn't warrant the overhead).
6. Approval threshold ($) deliberately left unset — needs CS leadership to decide.

## What's still uncertain

These are real risks the rest of the plan rides on:

- **A1 — payments-API refund endpoint exists.** If not, pi-1 contracts significantly (drop S025–S027 approval workflow to pi-2). Single biggest WSJF risk in the table. **Confirm in week 1, before PI planning Thursday.**
- **A2 — SSO supports cs-agent and cs-lead roles.** If not, week-1 IT ticket; small impact.
- **A3 — ≥80% of current Jira refunds are simple single-txn full refunds.** Drives H2 + H5. Worth doing the 90-day Jira pull this week.
- **A4 — finance accepts the new audit log.** Drives H4. Loop finance in this week, before the audit-log schema is implementation-locked.
- **Approval-threshold dollar amount.** Engineering can't pick this. CS leadership needs to set it before S018 builds.

## Smallest next decision (this week, before PI planning Thursday)

**Confirm A1: does the payments service expose a refund API, and what's its contract (idempotency? sync/async? partial-refund support?).** This single fact changes whether the pi-1 scope above is achievable as drawn. Everything else is recoverable in PI planning; this is not.

Suggested 30-minute meeting: you + the engineer who most recently ran a refund through the existing payments-service script. Output: a one-paragraph note appended to `design.md` § Decisions log.

## What to do at PI planning Thursday

In rough order:

1. Walk CS leadership + your team through the **5 backbone activities** (`storymap.md`, top of file). The map is shaped around CS's narrative, not the system. They will recognize themselves.
2. Walk through the **PI 1 sprint shape** (`backlog.md` § Sprint shape suggestion). Treat the sprint breakdown as a strawman to react to, not a commitment.
3. Review the **assumptions block** in `design.md`. Get explicit confirm/deny on each.
4. Set the **approval threshold** with CS leadership.
5. Confirm the **5 hypotheses** are the right bets — especially H1 (email-first lookup) and H2 (single-threshold approvals).
6. Get **finance** to look at the audit-log schema before sprint 3.

## Push into your tracker

CSV import is the path — don't recreate stories by hand inside the tool.

- **Jira / ADO:** Activity → Epic, Task → Feature, Story → Story, slice → Fix Version / Iteration. Import `storymap.csv` directly; pull WSJF scores from `backlog.csv` into custom fields.
- **GitHub Projects:** labels for `activity:*`, `slice:*`, `persona:*`; bulk-create with `gh issue create` + the CSV.
- See `user-story-mapping/references/work-item-tracking.md` (in the skill) for per-tool gotchas.

## If you want to iterate on this

Use Mode D (iterative refinement) — re-invoke the skill with the existing `storymap.md` in scope and ask for the specific extension (e.g., "re-slice for PI 2 now that we have payments-API contract"). Don't sync the tracker back to the markdown; treat the story map as a discovery artifact and re-derive it when needed.

## Framework integration notes

The user didn't mention Superpowers, gstack, or GSD, so no handoff is wired. If your team uses one of those:

- **GSD:** `design.md` → `.gsd/Brief.md`; each PI slice → one GSD Milestone; individual stories → GSD Tasks.
- **gstack:** `design.md` is what `/plan-ceo-review` reads; pi-1 stories are what `/plan-eng-review` reads; `backlog.md` is what `/plan-devex-review` reads.
- **Superpowers:** this sits between `brainstorming` (output → this skill) and `writing-plans` (input ← pi-1 stories as 2–5 minute tasks).
