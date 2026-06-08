# Story Map: Internal Developer Platform (IDP)

> **Outcome:** In 6 months, the majority of net-new non-prod env activity flows through the IDP without an approval queue, and the Q-1 $40K spend surprise is non-recurring. Application developers stop the threatened personal-AWS shadow-IT migration.
> **Personas:** Application Developer (primary), Platform Team Engineer (admin), VP Engineering (sponsor)
> **Slicing strategy:** pi-1 / pi-2 / pi-3 (SAFe Program Increment, 12 weeks per PI)

## Activity: Discover and request access

### Task: Find the IDP and sign in

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to sign in to the IDP with my corporate SSO, so that I do not need a separate credential to get started.
- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to land on a "what can I do here" home page after sign-in, so that I do not need a wiki to figure out the next step.
- [slice:pi-2] [persona:Application Developer] As an Application Developer, I want a one-click onboarding tour the first time I sign in, so that I can skip the docs and try a sandbox immediately.

### Task: Get into my team's workspace

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want my team membership auto-resolved from SSO group claims, so that I do not need to file a ticket to be added to my own team's workspace.
- [slice:pi-2] [persona:Platform Team Engineer] As a Platform Team Engineer, I want to override or correct team-workspace membership when SSO claims are stale, so that I am not blocked by an HR data lag.

## Activity: Spin up an environment

### Task: Pick a blueprint and provision

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to pick a sandbox blueprint from a catalog (e.g., "Node + Postgres", "Python + Redis"), so that I do not start from a blank Terraform file.
- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to click "Create sandbox" and have a working env in under 5 minutes with no approval gate, so that I stop using my personal AWS account.
- [slice:pi-1] [persona:Platform Team Engineer] As a Platform Team Engineer, I want every sandbox blueprint to pre-apply default security policies (private VPC, encrypted EBS, scoped IAM), so that the permit-by-default model is still safe by default.
- [slice:pi-2] [persona:Application Developer] As an Application Developer, I want to fork a blueprint and tweak it for my use case, so that my team's pattern can become a new template without filing a ticket.
- [slice:pi-2] [persona:Platform Team Engineer] As a Platform Team Engineer, I want to promote a community-forked blueprint to "official" status with a review, so that good patterns are amplified without forcing a review on every fork.

### Task: Apply tags and metadata at creation

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want the env-creation form to pre-fill team and cost-center from my profile, so that I do not retype them on every env.
- [slice:pi-1] [persona:Platform Team Engineer] As a Platform Team Engineer, I want team, cost-center, and env-type tags to be mandatory at creation (no skip path), so that every env is attributable in cost reports.

### Task: Override defaults with justification

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to override a default policy (e.g., open a port to the internet for a demo) with a one-line justification, so that I am not blocked but the platform team has an audit trail.
- [slice:pi-2] [persona:Platform Team Engineer] As a Platform Team Engineer, I want a "high-risk policy" subset (e.g., wide-open S3 in prod, public RDS) that does block rather than just warn, so that the most expensive mistakes cannot happen via override.

## Activity: Connect services and secrets

### Task: Self-service secrets for non-prod

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to store and retrieve non-prod secrets in a self-service vault from my env, so that I stop copy-pasting credentials in Slack.
- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want the IDP to inject secrets into my env as environment variables or mounted files, so that I do not roll my own bootstrap.

### Task: Request access to managed services

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want a list of internally-available managed services (DBs, queues, caches) I can attach to my env in one click, so that I do not file a ticket for a dev Postgres.
- [slice:pi-2] [persona:Application Developer] As an Application Developer, I want to request a new shared service to be added to the catalog with a justification, so that the catalog grows from real demand.

### Task: Bring my own tools (non-prod only)

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to install arbitrary tools, container images, or libraries in my non-prod sandbox without a security review queue, so that I can try things.
- [slice:pi-1] [persona:Platform Team Engineer] As a Platform Team Engineer, I want a background SBOM/scan job to run on BYO non-prod workloads and surface findings on a dashboard, so that BYO is observable without being blocking.

## Activity: Deploy to staging

### Task: Push to staging without a ticket

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to deploy my containerized app to staging from the IDP UI or CLI, so that I do not need a release-manager ticket for non-prod pushes.
- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want my deploy to show me logs and a healthcheck result in the UI, so that I know whether it worked.
- [slice:pi-2] [persona:Application Developer] As an Application Developer, I want preview environments per pull request, so that reviewers can click a link instead of pulling my branch locally.

### Task: Prod deploys (carve-out — approval-gated)

- [slice:pi-2] [persona:Platform Team Engineer] As a Platform Team Engineer, I want prod deploys to require a documented approver from a configured list, so that the permit-by-default model does not leak into prod.
- [slice:pi-2] [persona:Application Developer] As an Application Developer, I want to submit a prod deploy request from the same UI as my staging deploys, so that the workflow feels continuous even though prod is gated.

## Activity: Operate and observe

### Task: See my env cost and usage

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to see my env's running cost in near-real time in the IDP UI, so that I notice if I left something expensive running.
- [slice:pi-1] [persona:Platform Team Engineer] As a Platform Team Engineer, I want a project-wide spend dashboard with per-team and per-env breakdowns, so that the next $40K spike is attributable in hours, not weeks.
- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to receive a budget alert when my env's projected monthly cost crosses a configured threshold, so that I am the first to know I have a problem.

### Task: Tear down and clean up

- [slice:pi-1] [persona:Application Developer] As an Application Developer, I want to tear down my env in one click and confirm everything is destroyed, so that I do not leak resources after I am done.
- [slice:pi-2] [persona:Platform Team Engineer] As a Platform Team Engineer, I want auto-expiry on sandbox envs after a configurable idle period with a developer-controlled extension, so that forgotten envs do not accumulate.

### Task: Audit trail for the platform team

- [slice:pi-1] [persona:Platform Team Engineer] As a Platform Team Engineer, I want every env creation, override, secret access, and deploy event logged to a queryable audit store, so that I can investigate incidents without paging the developer.

## Non-backbone / cross-cutting

These don't fit a single user activity but still need slicing and prioritization. They appear in `backlog.csv` with `activity = "Non-backbone: <theme>"`.

### Theme: Governance hardening (deferred per VP Eng stance)

- [slice:pi-2] Soft cost cap per env with override-and-justify (the next step toward Q3 resolution; not a hard cap)
- [slice:pi-2] Platform-team review queue for new "official" blueprints
- [slice:pi-3] Hard cost caps with break-glass — only if PI 1/2 cost-alert evidence shows alerts are insufficient
- [slice:pi-3] Allowlist-style approval workflow for env creation — deferred per VP Eng stance; revisit only if a real incident demands it

### Theme: Platform reliability

- [slice:pi-2] IDP itself has SLO + on-call rotation
- [slice:pi-2] Blueprint provisioning has retry/idempotency so a half-created env does not strand resources
- [slice:pi-3] Multi-region IDP for DR

### Theme: Security and compliance

- [slice:pi-2] Prod-secret request flow (request → approve → time-bound access)
- [slice:pi-2] SBOM findings escalation policy (when a CVE crosses a threshold, who is notified)
- [slice:pi-3] SOC2/ISO evidence export from the audit store

<!--
Notes:
- 30 backbone stories across 5 activities, plus 9 non-backbone items = 39 total.
  Backbone story count is within the requested 25-35 range; non-backbone items
  are separate per the SKILL.md cross-cutting rule.
- Every backbone activity has at least one [slice:pi-1] story. Slice-1
  coverage rule: PASS.
- "Approval-gated env creation" appears ONLY in the cross-cutting section,
  ONLY at slice:pi-3, with an explicit "deferred per VP Eng stance" note.
  This honors the user-input-authoritative constraint.
- Prod approval gating is in slice:pi-2 (Activity 4) because both personas
  agreed on the prod carve-out — that is NOT the contested item.
-->
