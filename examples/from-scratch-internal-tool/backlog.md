# Prioritized Backlog: Refund Self-Service Portal

> **Method:** WSJF (Cost of Delay / Job Size; modified Fibonacci 1, 2, 3, 5, 8, 13, 20)
> **Slicing:** SAFe PI — pi-1 (32 stories) / pi-2 (17 stories) / pi-3 (3 stories)

## Bottom line

**Start here:** the load-bearing PI-1 trio is S021 (single-click refund) + S008 (lookup) + S036 (audit logging) — they define whether PI 1 ships a usable product. WSJF also floats two tiny enablement items (S049 runbook, S050 training) to the very top; ship them, they lift adoption for near-zero cost.

See `backlog.csv` for the full table with `wsjf_value`, `wsjf_time`, `wsjf_risk`, `wsjf_size` columns and the per-row reasoning. The score column = `(value + time_criticality + risk_reduction) / job_size`. Scores are relative within this backlog only.

## Reading the rankings

Two patterns to be aware of before reading the top 10:

1. **Enablement work scores high.** S049 (one-page runbook) and S050 (one training session) ride the very top — not because they're the most valuable individually, but because they're tiny, lift the entire outcome (CS adoption + H3 validation), and have no value if delivered after pilot. This is a feature of WSJF, not a bug. Don't deprioritize "small + critical" work just because it isn't a code change.
2. **The functional core (S021 single-click refund + S008 lookup + S036 audit logging) cluster just below.** This is the load-bearing trio that defines whether pi-1 ships a usable product.

## Top 10 — what to actually start

| Rank | ID   | Story                                                                     | Slice | Score | Why                                                                                                  |
|-----:|------|---------------------------------------------------------------------------|-------|------:|------------------------------------------------------------------------------------------------------|
|    1 | S050 | In-person/Zoom training session with the CS team before pilot             | pi-1  | 11.00 | Highest-leverage enablement; one PM-day unlocks the whole adoption-curve hypothesis (H3)             |
|    2 | S049 | One-page CS runbook for the portal                                        | pi-1  |  9.00 | Same logic; pairs with S050. Both must land before pilot                                             |
|    3 | S021 | Single "Refund" button for an eligible transaction within my limit        | pi-1  |  8.20 | The core action — everything else exists to make this happen                                         |
|    4 | S008 | Search for a customer by email address                                    | pi-1  |  8.00 | Primary entry point for ≥80% of cases per H1                                                         |
|    5 | S032 | "Refund complete" confirmation screen with refund ID + timestamp          | pi-1  |  8.00 | Closes the loop; without it agents will double-check elsewhere                                       |
|    6 | S036 | System logs every refund attempt (who/when/txn/amount/reason/approval)    | pi-1  |  8.00 | Non-negotiable for fintech audit. Drives H4 (finance sign-off)                                       |
|    7 | S009 | See customer's recent transactions (last 90 days) listed newest-first     | pi-1  |  7.67 | Direct payoff of H1 — agents work the way they think                                                 |
|    8 | S023 | Confirm step ("Refund $X to <customer>?") before action is final          | pi-1  |  7.50 | Mistake-prevention is critical when refunds are real money. Tiny code cost                           |
|    9 | S001 | Sign in to portal via company SSO                                         | pi-1  |  7.00 | Foundational; nothing else ships without it                                                          |
|   10 | S016 | See prior refunds against this same transaction (if any)                  | pi-1  |  7.00 | Duplicate-refund prevention is the #1 finance risk of self-service                                   |

S018 (eligibility-gate UI) and S040 (SSO wiring) tie at 7.00 just below the cut — treat them as a tied #11/#12 and pull them in before any pi-2 work.

## Slice 1 — PI 1 (weeks 1–12 of the 12-week PI)

32 stories. Spans all five backbone activities (slice-coverage rule holds) plus the four cross-cutting themes' minimum-viable items. The full ranked list:

| ID   | Activity                                       | Story                                                                                       | Score | Why                                                                                          |
|------|------------------------------------------------|---------------------------------------------------------------------------------------------|------:|----------------------------------------------------------------------------------------------|
| S050 | Non-backbone: Onboarding & enablement          | In-person/Zoom CS training before pilot                                                     | 11.00 | Tiny cost, huge adoption return; validates H3                                                |
| S049 | Non-backbone: Onboarding & enablement          | One-page CS runbook                                                                         |  9.00 | Free outcome multiplier; one PM-day                                                          |
| S021 | Issue the refund                               | Single-click refund button (within limit)                                                   |  8.20 | The core action                                                                              |
| S008 | Find the transaction                           | Search customer by email                                                                    |  8.00 | Primary entry; validates H1                                                                  |
| S032 | Confirm & communicate                          | Refund-complete confirmation screen                                                         |  8.00 | Closes the loop                                                                              |
| S036 | Confirm & communicate                          | Audit log of every attempt (success + failure)                                              |  8.00 | Fintech non-negotiable; validates H4                                                         |
| S009 | Find the transaction                           | Customer's recent transactions listed newest-first                                          |  7.67 | Direct H1 payoff                                                                             |
| S023 | Issue the refund                               | Confirm step before submit                                                                  |  7.50 | Mistake prevention                                                                           |
| S001 | Sign in & access the portal                    | SSO sign-in                                                                                 |  7.00 | Foundational                                                                                 |
| S016 | Review & decide                                | Show prior refunds on same transaction                                                      |  7.00 | Duplicate-refund prevention                                                                  |
| S018 | Review & decide                                | Eligibility gate (eligible / not / needs approval)                                          |  7.00 | Heart of self-service trust; drives H2 + H4                                                  |
| S040 | Non-backbone: Compliance & security baseline   | Wire SSO with cs-agent / cs-lead roles in IdP                                               |  7.00 | Foundational, blocks every user story                                                        |
| S041 | Non-backbone: Compliance & security baseline   | Backend rejects unauthenticated refund actions                                              |  7.00 | Non-negotiable security control                                                              |
| S015 | Review & decide                                | Transaction-detail view (amount/date/method/status)                                         |  6.50 | Read endpoint + render; required to decide                                                   |
| S025 | Issue the refund                               | Submit refund-with-approval-request when over limit                                         |  6.00 | Makes "no-eng-needed" real for higher-value refunds                                          |
| S022 | Issue the refund                               | Reason code + free-text note before submit                                                  |  6.00 | Audit-required (H4)                                                                          |
| S042 | Non-backbone: Compliance & security baseline   | Append-only audit log on separate storage with retention                                    |  6.00 | SOC 2 / PCI-tone + H4 sign-off                                                               |
| S013 | Find the transaction                           | Clear "not found" message                                                                   |  5.00 | Cheap empty-state polish                                                                     |
| S027 | Issue the refund                               | Lead approves/denies with required reason                                                   |  5.00 | Audit-required                                                                               |
| S030 | Issue the refund                               | Human-readable payments-API error with "copy for eng" button                                |  5.00 | Without it, every API error becomes a Slack ping back to eng                                 |
| S033 | Confirm & communicate                          | Transaction row updates to "Refunded" immediately                                           |  5.00 | State-consistency basic                                                                      |
| S034 | Confirm & communicate                          | Copyable confirmation snippet for CS-tool reply                                             |  5.50 | Biggest time-save inside CS's own workflow                                                   |
| S037 | Confirm & communicate                          | CSV export of audit log for finance                                                         |  5.00 | First month-end reconciliation                                                               |
| S045 | Non-backbone: Reliability & observability      | Alert if refund-success rate drops or payments-API errors spike                             |  4.50 | Money-movement — quiet failures are worst                                                    |
| S004 | Sign in & access the portal                    | Lock CS Agent's landing page to refund actions only                                         |  4.50 | RBAC UI; cheap once roles exist                                                              |
| S012 | Find the transaction                           | Paste txn ID and jump straight there                                                        |  4.50 | Cheap; covers engineering-handoff flow                                                       |
| S019 | Review & decide                                | Reason text when not refundable via portal                                                  |  4.50 | Defines escalation back to eng                                                               |
| S044 | Non-backbone: Reliability & observability      | Structured logs + basic ops dashboard                                                       |  4.50 | Verify the 30→3 ticket-drop outcome                                                          |
| S002 | Sign in & access the portal                    | Auto sign-out on inactivity                                                                 |  4.50 | Compliance-mandated for money-movement tooling                                               |
| S005 | Sign in & access the portal                    | Lead "pending approvals" entry point                                                        |  4.33 | Required for approval workflow                                                               |
| S047 | Non-backbone: Tech foundations                 | Stand up portal repo, CI, deploy pipeline, non-prod env                                     |  4.20 | Blocks everything else if not done sprint 1                                                  |
| S026 | Issue the refund                               | Lead's pending-approvals list                                                               |  4.00 | Lead's primary surface; paired with S025/S027                                                |

### Sprint shape suggestion for PI 1

A 12-week PI at 2-week sprints = 6 sprints. With 4 engineers + 1 PM and the dependency chain (auth + tech foundations first, then read paths, then write/refund path, then audit + approval, then enablement):

- **Sprint 0 (week 0, before PI starts)** — confirm A1–A6 assumptions (payments API contract, SSO roles); finance/CS-leadership kickoff. Not part of the PI commitment.
- **Sprint 1 (PI weeks 1–2)** — S047 tech foundations; S001/S040 SSO; S041 backend auth gate; thin search endpoint stub.
- **Sprint 2 (PI weeks 3–4)** — S008/S009/S012 transaction lookup; S013 not-found; S015 transaction-detail view; S016 prior-refunds check.
- **Sprint 3 (PI weeks 5–6)** — S018/S019 eligibility gate; S021/S022/S023 single-click refund flow; S036/S042 audit logging end-to-end.
- **Sprint 4 (PI weeks 7–8)** — S025/S026/S027/S005 approval workflow; S030 payments-API error UX; S032/S033/S034 confirmation + comms.
- **Sprint 5 (PI weeks 9–10)** — S004 RBAC UI; S002 idle-timeout; S037 finance CSV export; S044/S045 logging + alerting; pilot dry-run with 1 CS agent on non-prod.
- **Sprint 6 (PI weeks 11–12)** — S049 runbook; S050 training session; pilot with full CS team; hardening; PI System Demo.

This is a starting point for PI planning Thursday, not a commitment — adjust during the planning session based on real story sizing with the team.

## Slice 2 — PI 2

17 stories. Differentiation, edge cases, and the items pi-1 surfaced as worth doing once we have data.

| ID   | Activity                                     | Story                                                                                  | Score |
|------|----------------------------------------------|----------------------------------------------------------------------------------------|------:|
| S024 | Issue the refund                             | Idempotent submit on double-click (likely promotable to pi-1 if payments API helps)    |  5.50 |
| S045 ↑ (already pi-1)                                                                                                                       |       |
| S010 | Find the transaction                         | Filter transaction list by date/amount                                                 |  4.00 |
| S028 | Issue the refund                             | Lead notification (email + in-portal) on new approval                                  |  4.00 |
| S039 | Confirm & communicate                        | Stable refund-ID matching payments-processor record                                    |  4.00 |
| S017 | Review & decide                              | Customer's refund history across all transactions                                      |  3.33 |
| S048 | Non-backbone: Tech foundations               | Automated end-to-end smoke test against sandbox payments                               |  3.00 |
| S029 | Issue the refund                             | Agent sees status of pending approval requests                                         |  3.00 |
| S031 | Issue the refund                             | Auto-retry transient payments-API failures                                             |  2.67 |
| S011 | Find the transaction                         | Search by customer ID / account ID                                                     |  2.67 |
| S043 | Non-backbone: Compliance & security baseline | Pen-test before scaling beyond pilot                                                   |  2.60 |
| S046 | Non-backbone: Reliability & observability    | Runbook: payments-service-down degrade to read-only                                    |  2.50 |
| S020 | Review & decide                              | Visible/explainable eligibility rules in UI                                            |  2.50 |
| S003 | Sign in & access the portal                  | SSO remembers me across browser sessions within day                                    |  2.50 |
| S038 | Confirm & communicate                        | Per-agent refund summary (last 30 days) for Lead                                       |  2.33 |
| S014 | Find the transaction                         | Near-miss search suggestions                                                           |  1.67 |
| S051 | Non-backbone: Onboarding & enablement        | In-app first-run tour                                                                  |  1.67 |
| S006 | Sign in & access the portal                  | Lead views provisioned-agents list with last-active time                               |  1.67 |

## Slice 3 — PI 3 (forecast, not commitment)

3 stories. Defer to PI 3 planning to confirm whether anything should pull forward.

| ID   | Story                                                                                  | Score |
|------|----------------------------------------------------------------------------------------|------:|
| S035 | Portal sends transactional refund-confirmation email to customer                       |  1.40 |
| S007 | Lead grants/revokes CS Agent refund capability from within portal                      |  1.20 |
| S052 | Recorded training video for CS onboarding                                              |  1.20 |

## What's not in any slice (non-goals — documented to prevent re-litigation)

Per `design.md` § Non-goals. Recorded here so they don't get raised in PI planning as "we forgot".

| ID    | Story                                                                  | Why not                                                              |
|-------|------------------------------------------------------------------------|----------------------------------------------------------------------|
| X001  | Partial refunds                                                        | Defer; stays on eng escalation path until evidence demands it        |
| X002  | Multi-currency refund logic with FX UI                                 | Use transaction's original currency only; defer FX                   |
| X003  | Refunding settled / batched payments                                   | Payments-service edge; eng-only until we confirm behavior            |
| X004  | Bulk refunds / CSV upload / "refund all from customer X"               | Out of scope for pi-1 + pi-2; raises abuse-control questions         |
| X005  | Customer-facing self-service refunds                                   | Wrong audience — this portal is for CS                               |
| X006  | Custom in-portal customer comms channel                                | CS already has a ticketing tool; we provide a snippet, not a surface |
| X007  | Fraud detection / ML scoring                                           | Rules-based guardrails only; ML is premature                         |

## Open prioritization questions (raise at PI planning Thursday)

- **A1 confirmation:** if the payments service doesn't already expose a refund API, S021 size jumps from 5 → 13 and pi-1 scope must contract (likely drop S025-S027 approval workflow to pi-2). This is the single biggest WSJF risk in the table.
- **Approval threshold ($):** CS leadership needs to set this before S018 can be built. Engineering can't pick the number.
- **Idempotency:** if the payments API enforces idempotency keys, S024 promotes to pi-1 at score ~7 (size drops from 2 → 1).
- **Audit-log infra:** if there's an existing append-only audit infra to plug into, S042 drops from size 3 → 1 and score lifts; otherwise, the size estimate may be optimistic.
- **Pilot scope:** how many CS agents in pilot? Affects whether S043 pen-test gates pi-2 → pi-3 transition or sits later.
