# Story Map: Refund Self-Service Portal

> **Outcome:** Customer Success can resolve a single-transaction refund in under 5 minutes, without filing an engineering ticket, with a complete audit trail.
> **Personas:** CS Agent, CS Team Lead, Engineer-on-Refunds (fallback), Finance (audit consumer)
> **Slicing strategy:** pi-1 / pi-2 / pi-3 (SAFe Program Increments, 12-week PI)

## Activity: Sign in & access the portal

### Task: Authenticate via company SSO

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to sign in to the portal using my company SSO, so that I don't need yet another password and IT keeps me in their identity system
- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to be auto-signed-out after a period of inactivity, so that an unattended laptop can't be used to issue refunds
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want SSO to remember me across browser sessions within the working day, so that I'm not re-authenticating every time I open the portal

### Task: Get the right access scope for my role

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to land on a page scoped to refund actions only, so that I can't accidentally wander into admin tooling
- [slice:pi-1] [persona:CS Team Lead] As a CS Team Lead, I want to see a "pending approvals" entry point in addition to issuing my own refunds, so that I know what's waiting on me
- [slice:pi-2] [persona:CS Team Lead] As a CS Team Lead, I want to view the list of CS Agents currently provisioned and their last-active time, so that I can spot stale or unused accounts during quarterly reviews
- [slice:pi-3] [persona:CS Team Lead] As a CS Team Lead, I want to grant/revoke a CS Agent's refund capability from within the portal, so that I don't have to file an IT ticket every time we onboard or offboard someone

## Activity: Find the transaction

### Task: Look up by customer

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to search for a customer by email address, so that I can start from how the customer identifies themselves to me
- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to see the customer's recent transactions (last 90 days) listed newest-first, so that I can pick the right one without knowing the transaction ID
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want to filter the transaction list by date range or amount, so that I can find the right one when the customer says "the $42 charge from a couple weeks ago"
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want to search by customer ID or account ID in addition to email, so that I can still find them when the customer reaches out from a different email

### Task: Look up by transaction ID directly

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to paste a transaction ID into a single search box and jump straight to that transaction, so that escalations that already have an ID don't need a multi-step lookup

### Task: Handle "no results"

- [slice:pi-1] As a CS Agent, I want a clear "not found" message when a customer email doesn't match anything, so that I don't waste time wondering whether the lookup is broken or the customer is wrong
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want suggestions when my search has a near-miss (typo, alternate email domain), so that I can recover from common input errors

## Activity: Review & decide

### Task: See the transaction in context

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to see transaction details (amount, date, customer, payment method last 4, original currency, current refund status), so that I have the facts I need to decide
- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to see prior refunds against this same transaction (if any), so that I don't accidentally issue a duplicate refund
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want to see this customer's refund history across all their transactions, so that I can spot a pattern (frequent refunder) before issuing another

### Task: Understand whether I'm allowed to refund this

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want the portal to tell me explicitly whether this transaction is refundable (eligible / not eligible / needs lead approval) before I try, so that I'm not surprised at the submit step
- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want a clear reason when a transaction is not refundable via the portal (e.g., "partial refund — escalate to engineering", "settled batch — escalate"), so that I know exactly what to do next
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want the eligibility rules and approval thresholds to be visible/explainable in the UI, so that I can answer a customer's "why" without guessing

## Activity: Issue the refund

### Task: Submit a refund within my limit

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to click a single "Refund" button for an eligible transaction within my limit, so that the common case is one click
- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to enter a short reason code + free-text note before submitting, so that finance and my Lead can understand why later
- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want a confirm step ("Refund $X to <customer>?") before the action is final, so that I can catch wrong-transaction mistakes before they happen
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want the submit action to be idempotent if I double-click, so that a flaky network doesn't cause a duplicate refund

### Task: Send a refund above my limit for approval

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want to submit a refund-with-approval-request when the amount is above my limit, so that I'm not blocked from handling the case at all
- [slice:pi-1] [persona:CS Team Lead] As a CS Team Lead, I want to see a list of pending refund approvals with all the context the agent provided, so that I can approve or deny in one screen
- [slice:pi-1] [persona:CS Team Lead] As a CS Team Lead, I want to approve or deny with a required short reason, so that there's a record of why
- [slice:pi-2] [persona:CS Team Lead] As a CS Team Lead, I want to be notified (email + in-portal) when a new approval is waiting, so that customers aren't waiting on me without my knowing
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want to see the status of my pending approval requests (waiting / approved / denied), so that I can update the customer without nagging my Lead

### Task: Handle failures from the payments service

- [slice:pi-1] As a CS Agent, I want a clear human-readable error message if the payments service rejects the refund (with a "copy details for engineering" button), so that I have a clean escalation path
- [slice:pi-2] [persona:CS Agent] As a CS Agent, I want the portal to auto-retry transient payments-service failures (with backoff) before showing me an error, so that I'm not bothered by blips

## Activity: Confirm & communicate

### Task: See that the refund actually happened

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want a clear "Refund complete" confirmation screen with the refund ID and timestamp, so that I know I can close the customer ticket
- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want the original transaction row to update to show "Refunded" immediately after, so that I'm not left guessing if I refresh

### Task: Communicate to the customer

- [slice:pi-1] [persona:CS Agent] As a CS Agent, I want a copyable confirmation snippet (refund amount, expected funds-availability window, refund ID) to paste into our CS-tool reply, so that customer messaging is consistent and complete
- [slice:pi-3] [persona:CS Agent] As a CS Agent, I want the portal to send a transactional refund-confirmation email to the customer on my behalf, so that I don't have to copy-paste anything

### Task: Leave a trail for finance and audit

- [slice:pi-1] As a system, log every refund attempt (success and failure) with: who, when, txn ID, amount, reason code, free-text note, approval chain
- [slice:pi-1] [persona:Finance] As a Finance analyst, I want to export the refund audit log as CSV for a given date range, so that I can reconcile against the payments processor at month-end
- [slice:pi-2] [persona:CS Team Lead] As a CS Team Lead, I want a per-agent refund summary (count, total amount, denied/approved breakdown) for the last 30 days, so that I can spot outliers in my team's behavior
- [slice:pi-2] [persona:Finance] As a Finance analyst, I want the audit-log export to include a stable refund-ID that matches the payments processor's record, so that reconciliation is unambiguous

# Non-backbone / cross-cutting

These don't fit a user activity but still need slicing and prioritization. The headings below are encoded as `## Activity: Non-backbone: <theme>` so that `storymap_to_csv.py` (which only recognizes `## Activity:` and `### Task:` headers) emits them with `activity = "Non-backbone: <theme>"` — matching the convention from the skill's slicing-strategies reference. They are excluded from the "every-activity-in-slice-1" check because they're not part of the user narrative.

## Activity: Non-backbone: Compliance & security baseline

### Task: Identity, access, and audit-trail integrity

- [slice:pi-1] Wire portal authentication to company SSO with `cs-agent` and `cs-lead` roles provisioned in the identity provider
- [slice:pi-1] All refund actions require an authenticated session; backend rejects anything else
- [slice:pi-1] Audit log is append-only and stored separately from the application DB (or on storage with retention/legal-hold)
- [slice:pi-2] Pen-test pass against the portal before scaling beyond pilot CS agents

## Activity: Non-backbone: Reliability & observability

### Task: Operability baseline

- [slice:pi-1] Structured logs + a basic dashboard: refund attempts/hour, success/failure ratio, latency
- [slice:pi-1] On-call alert if refund-success rate drops below threshold or payments-service errors spike
- [slice:pi-2] Runbook for "payments service is down" — portal degrades to read-only and tells CS to escalate

## Activity: Non-backbone: Tech foundations

### Task: Repo, CI, and environments

- [slice:pi-1] Stand up the portal repo, CI, deploy pipeline, and a non-prod environment that CS can dry-run against
- [slice:pi-2] Add an automated end-to-end smoke test that issues a refund against a sandbox payments account on every deploy

## Activity: Non-backbone: Onboarding & enablement

### Task: Get CS productive with the portal

- [slice:pi-1] Short written runbook for CS Agents (one page) — "how to issue a refund in the portal"
- [slice:pi-1] One in-person/Zoom training session with the CS team before pilot
- [slice:pi-2] In-app first-run tour for new CS Agents
- [slice:pi-3] Recorded training video that ships with CS team onboarding

<!--
Slice-1 coverage check (must hit every backbone activity):

  Activity 1 (Sign in & access)        -> S001, S002, S004, S005
  Activity 2 (Find the transaction)    -> S006, S007, S010, S011
  Activity 3 (Review & decide)         -> S013, S014, S016, S017
  Activity 4 (Issue the refund)        -> S019, S020, S021, S023, S024, S025, S027
  Activity 5 (Confirm & communicate)   -> S029, S030, S031, S033, S034

All five activities have pi-1 stories. End-to-end demoable at PI 1 System
Demo: SSO login -> lookup by email -> see eligibility -> issue refund (with
approval if over limit) -> confirm + copyable message -> audit log entry.
-->
