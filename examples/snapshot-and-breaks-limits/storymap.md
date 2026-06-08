# Story Map: Refund Portal — PI 1 (mid-flight) + proposed F-SCIM

> **Outcome:** Ship the refund portal MVP to cut CS time-per-ticket 22min→5min (KR-2.1), pass SOC 2 Type II (KR-1.1), and now possibly land SCIM provisioning (KR-1.2) for the $400K enterprise deal.
> **Personas:** CS agent, CS lead (Marcus), Approver, Enterprise IT admin (NEW), SOC 2 auditor (external)
> **Slicing strategy:** PI (Program Increment) — preserving prior PI 1 commitments; F-SCIM added provisionally per Mode D protocol

## Activity: Sign in

### Task: Authenticate via corporate SSO

- [slice:pi-1] [persona:CS agent] As a CS agent, I want to sign in with my company SSO, so that I don't manage another password [shipped]

## Activity: Find transaction

### Task: Look up by identifier

- [slice:pi-1] [persona:CS agent] As a CS agent, I want to find a transaction by ID, so that I can resolve a customer ticket fast [shipped]

### Task: Look up by customer

- [slice:pi-1] [persona:CS agent] As a CS agent, I want to find transactions by customer email, so that I can find the right charge when the customer doesn't have an ID [in-progress]

## Activity: Review transaction

### Task: Inspect details before action

- [slice:pi-1] [persona:CS agent] As a CS agent, I want to view full transaction details, so that I can confirm I'm refunding the right charge [in-progress]

## Activity: Submit refund

### Task: Issue refund within auto-approve threshold

- [slice:pi-1] [persona:CS agent] As a CS agent, I want to submit refunds under $100 with rule-based auto-approve, so that small refunds clear instantly without a queue [started]

### Task: Issue refund above threshold

- [slice:pi-1] [persona:CS agent] As a CS agent, I want to submit refunds over $100 into the approval queue, so that supervisors can sanity-check before money moves [not-started]

## Activity: Approve refund

### Task: Supervisor review

- [slice:pi-1] [persona:Approver] As a refund approver, I want a dashboard of pending refunds, so that I can clear the queue without hunting for individual cases [not-started]

## Activity: Notify stakeholders

### Task: Notify customer

- [slice:pi-1] [persona:Customer] As a customer, I want an email when my refund is approved, so that I know the money is on the way [in-progress]

### Task: Notify approver

- [slice:pi-1] [persona:Approver] As an approver, I want a Slack ping when a refund needs my review, so that I don't miss queued items [not-started]

### Task: Handle failed refunds

- [slice:pi-1] As a CS agent, I want failed refunds to retry automatically, so that intermittent payment-provider blips don't become support escalations [not-started]

## Activity: Audit / compliance

### Task: Emit audit events

- [slice:pi-1] [persona:SOC 2 auditor] Emit audit log events for every refund action, so that auditors can reconstruct decisions [in-progress]

### Task: Search audit log

- [slice:pi-1] [persona:Compliance] As a compliance reviewer, I want to search the audit log by case/user/date, so that I can answer auditor questions without engineering [not-started]

### Task: Retention policy

- [slice:pi-1] Enforce SOC 2 audit log retention policy (7 years), so that the audit trail is admissible [not-started]

### Task: Export evidence

- [slice:pi-1] [persona:Compliance] As a compliance officer, I want to export the audit log to CSV, so that I can hand evidence to the auditor [not-started]

## Activity: Detect anomalies

### Task: Pattern detection on refunds

- [slice:pi-1] As a security engineer, I want suspicious refund clusters to fire an alert, so that we catch internal fraud or compromised accounts early [not-started]

## Activity: Provision tenant users

> **NEW BACKBONE ACTIVITY — added provisionally for F-SCIM.** Surfaced as Breach #2 in handoff.md.

### Task: Establish SCIM 2.0 endpoint surface

- [slice:pi-1-scim] [persona:Enterprise IT admin] As an enterprise IT admin, I want a SCIM 2.0 endpoint scaffolded with auth, so that my IdP can discover the provisioning API

### Task: Provision users

- [slice:pi-1-scim] [persona:Enterprise IT admin] As an enterprise IT admin, I want to create and update users via SCIM, so that new hires get refund-portal access automatically

### Task: Deprovision users

- [slice:pi-1-scim] [persona:Enterprise IT admin] As an enterprise IT admin, I want SCIM DELETE to disable access immediately, so that offboarded employees lose portal access (also closes a SOC 2 control)

### Task: Group-to-role mapping

- [slice:deferred-or-pi-1-scim] [persona:Enterprise IT admin] As an enterprise IT admin, I want my IdP group memberships to map to refund-portal roles, so that I don't manually re-assign permissions per user

<!--
Slice tags:
- pi-1            = original PI 1 commitment (shipped, in-progress, or not-started)
- pi-1-scim       = F-SCIM additions, provisionally in PI 1 per Mode D defaults
- deferred-or-pi-1-scim = F-SCIM-04 — keep in PI 1 only if "before EOQ" means full GA; else defer to PI 2

Status tags ([shipped], [in-progress], [started], [not-started]) are informational
and were carried in from the user-supplied PI 1 snapshot.
-->
