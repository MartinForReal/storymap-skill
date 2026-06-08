# Refund Self-Service Portal — Design Doc

## The question this work answers

Can we eliminate engineering as the bottleneck for routine single-transaction
refunds by giving Customer Success a self-service path, without losing the
financial controls and audit trail that the current Jira-to-engineering
workflow provides?

## Outcome

In 6 months, the Customer Success (CS) team can resolve >90% of single-
transaction refund requests on their own, in under 5 minutes from receipt,
with a full audit log per refund. Engineering ticket volume from CS drops
from ~30/week to <3/week (only true edge cases). My team reclaims an
estimated 4–6 engineer-hours/week previously spent on refund tickets.

## Trigger

- CS leadership has verbally asked. ~30 refund Jiras/week against
  engineering, each pulling an engineer out of focused work.
- PI planning is **next Thursday** (~1 week away) and the **12-week PI
  starts in 3 weeks**, so the work needs to be scoped and prioritized now to
  be a committed PI 1 item.
- A 4-engineer + 1-PM team is the right size for a single-team internal
  tool; bigger ART involvement is not needed.

## Personas

### Customer Success Agent (primary)
- **Role:** Front-line CS rep handling customer-reported issues, including
  refund requests. Non-technical; uses a browser, a CS-tool (assumed
  Zendesk/Intercom-class), and Slack. Currently files Jiras to engineering
  for refunds.
- **Goal in this work:** Process a refund and close the customer's ticket
  in the same session, without filing or waiting on engineering.
- **Today they:** Copy the transaction ID and customer email out of the
  CS-tool, fill in a Jira template, drop a Slack ping in #eng-help, then
  wait hours (sometimes days) for an engineer to run a script. They post
  back to the customer once it's done.
- **Pain:** Customer waits. The engineer's context-switch annoys both
  parties. Mistakes (wrong txn ID) round-trip multiple times. No visibility
  into refund status mid-flight.

### CS Team Lead (secondary — approval/oversight)
- **Role:** Approves higher-risk refunds (above a threshold, repeat
  refunders, suspicious patterns) and reviews CS team activity.
- **Goal in this work:** Maintain oversight without being a per-refund
  bottleneck. Spot abuse or errors quickly.
- **Today they:** Has no real-time view. Hears about issues if the CS
  agent escalates or if finance flags something at month-end.
- **Pain:** Discovery of problems is too slow. No way to set per-agent or
  per-amount limits today; everything goes through eng anyway.

### Engineer-on-Refunds (current bottleneck, future fallback)
- **Role:** Whoever on my team picks up the Jira. Runs an internal CLI/script
  against the payments service to issue the refund.
- **Goal in this work:** Stop being involved in routine refunds. Stay
  involved only for true edge cases (multi-currency disputes, partial
  refunds on settled batches, chargeback overlaps).
- **Today they:** Drops focused work, validates the request, runs the
  refund script, replies in Jira. ~10–15 min per refund including context
  switch.
- **Pain:** Interruption tax. Same task 30x/week.

### Finance / Compliance (consumer of audit trail, not active user)
- **Role:** Owns the books. Already has a monthly reconciliation process
  against the payments processor.
- **Goal in this work:** Every refund issued via the new portal is
  logged with who/when/why/amount/txn ID, exportable for month-end.
- **Today they:** Reconciles against the payments processor's report;
  cross-references with engineering's refund script output when there is
  a discrepancy.
- **Pain:** Would object loudly if the new portal weakens the audit trail
  or creates an off-books refund path.

## User activities (the backbone)

The narrative flow, left-to-right, in CS-agent voice:

1. **Sign in & access the portal** — get authenticated, see the right
   scope of refunds for their role.
2. **Find the transaction** — locate the specific payment a customer is
   asking to be refunded.
3. **Review & decide** — see transaction context, refund eligibility,
   and any policy guardrails before deciding to refund.
4. **Issue the refund** — submit the refund, with optional approval step
   for higher-risk cases.
5. **Confirm & communicate** — get a clear confirmation, share status
   back to the customer, and have the action logged for audit.

See `storymap.md` for tasks and stories under each.

## Opportunities

| Activity | Opportunity |
|---|---|
| Sign in & access the portal | CS gets a dedicated tool instead of borrowing engineering's |
| Find the transaction | Lookup that matches CS's mental model (customer email + recent activity), not engineers' (txn ID only) |
| Review & decide | Guardrails (amount caps, duplicate-refund detection) catch most mistakes before they happen |
| Issue the refund | Refund completes in seconds, no human wait time, customer can be told "done" while still on the call/chat |
| Confirm & communicate | Built-in audit log = finance happy; built-in customer comms template = consistent messaging |

## Hypotheses

| # | Hypothesis | Validates in slice | Method |
|---|---|---|---|
| H1 | A simple lookup by customer email + transaction list is enough for CS to find the right transaction in >90% of cases (no need for advanced search at MVP) | pi-1 | Usability test with 2 CS agents on walking-skeleton; track lookup-success rate in pi-1 metrics |
| H2 | A single amount-based approval threshold (e.g., >$500 needs lead approval) covers >80% of risk cases — we don't need ML-based fraud scoring at MVP | pi-1 | Review of last 90 days of CS-filed refund Jiras to see distribution; agent feedback in pi-1 |
| H3 | CS agents will trust the portal enough to stop double-checking with engineering once it ships | pi-2 | Track residual eng-team refund ticket volume; target <5/week by end of pi-2 |
| H4 | Finance will accept the portal's audit log in lieu of the current engineering-script logs | pi-1 | Sign-off from finance on the audit-log schema before pi-1 ends; first month-end reconciliation runs clean |
| H5 | Refunds the portal can't handle (partial, multi-currency, batch-settled) are <10% of volume and can stay on the engineering escalation path | pi-1 | Same 90-day Jira review as H2 |

## Constraints

- **Hard deadlines:**
  - **PI planning next Thursday** — design.md, story map, and a credible PI 1
    commitment must exist by then.
  - **12-week PI starts in 3 weeks** — anything tagged `pi-1` must be
    deliverable by a team of 4 engineers + 1 PM in that window.
- **Platform / integrations:**
  - Must integrate with the existing payments service (assumed: a single
    internal payments API that already exposes a refund endpoint —
    confirm in week 1).
  - Must integrate with the company SSO (assumed: Okta or similar —
    confirm in week 1) — no separate login for an internal tool.
  - Audit log must be exportable in a format finance can already consume
    (CSV at minimum).
- **Team / skills:**
  - 4 engineers + 1 PM. Assumed mix of backend + frontend skills since
    the team has historically owned the payments-adjacent surface.
  - SAFe-lite: PI cadence, no full ART, no RTE. WSJF chosen because the
    org is used to it.
- **Compliance / regulatory (fintech):**
  - Refunds touch money movement — assume SOC 2 and PCI-DSS-relevant
    audit-trail requirements apply. Audit log is **not** optional.
  - Role-based access control is **not** optional — CS agents must not
    see refunds outside their authorized scope.

## Non-goals

Recording these prevents re-litigation during PI planning.

- **Partial refunds** in pi-1 (assume full-refund of a single transaction
  only; partial stays on engineering escalation path).
- **Multi-currency refund logic** in pi-1 (use the transaction's original
  currency; no FX conversion UI).
- **Refunding settled / batched payments** in pi-1 (the payments service
  may treat these differently — defer until we confirm).
- **Bulk refunds** (CSV upload, "refund all transactions from customer X")
  in pi-1 and pi-2 — out of scope unless evidence demands it.
- **Customer-facing self-service refunds.** This portal is for CS, not
  for end customers.
- **A custom in-portal customer comms channel.** CS already has their
  ticketing tool — we'll provide a copyable confirmation snippet, not a
  competing comms surface.
- **Fraud detection / ML scoring.** Out of scope for pi-1 and pi-2.
  Guardrails are rules-based.

## Assumptions (made for this design — confirm in week 1)

Because no live user is available, the following are explicitly assumptions
to validate before PI planning Thursday:

- **A1:** The payments service has a refund API the portal can call. If
  not, pi-1 scope grows substantially.
- **A2:** SSO exists and we can provision a `cs-agent` and `cs-lead`
  role/group.
- **A3:** Of ~30 refund Jiras/week, ≥80% are simple single-txn full
  refunds that fit the pi-1 happy path.
- **A4:** Finance is willing to accept the new audit log; they need to
  be looped in during week 1.
- **A5:** CS agents have laptops + Chrome/Edge (no mobile-first
  requirement for pi-1).
- **A6:** A web app served from the internal network (behind SSO) is
  acceptable; no separate desktop app needed.
- **A7:** "Customer Success folks" = ~5–15 agents company-wide. Used to
  size load: this is a low-RPS internal tool, not a customer-facing one.

## Open questions

These need answers before or during PI planning:

- What's the exact refund API contract on the payments service? Idempotency
  key? Async vs sync?
- Does finance need real-time audit-log feed, or is daily export enough?
- What's the approval threshold (dollar amount) for lead-approved refunds?
  CS leadership should set this, not engineering.
- Who owns the portal post-launch (my team? CS? a platform team)? Affects
  pi-3 staffing.
- Is there an existing audit-log infra to plug into, or do we own that
  schema and storage?

## Decisions log

| Date | Decision | Reasoning |
|---|---|---|
| 2026-06-08 | Slicing strategy: SAFe PI (pi-1, pi-2, pi-3) | User explicitly said "12-week PI starting in 3 weeks" and "PI planning next Thursday" — matches Strategy 2 in the skill's slicing reference |
| 2026-06-08 | Prioritization: WSJF | User explicitly said "Use WSJF since the org is used to it" |
| 2026-06-08 | Approval workflow is in scope for pi-1 (not deferred) | Fintech compliance + finance trust requires it from day 1; deferring breaks H4 |
| 2026-06-08 | Partial refunds, multi-currency, batched refunds explicitly out of pi-1 | Keep the walking skeleton honest; these are edge cases per H5 |
| 2026-06-08 | Single team, no ART, no RTE | Stated team composition (4 eng + 1 PM) doesn't warrant ART overhead |
