# Prioritized Backlog: Internal Developer Platform (IDP)

> **Method:** WSJF (per user request — SAFe context)
> **Slicing:** PI 1 / PI 2 / PI 3, 12-week PIs

See `backlog.csv` for the full table with all scoring columns.

## Top 10 (this slice — PI 1)

| Rank | ID | Story | Slice | Score | Why |
|---|---|---|---|---|---|
| 1 | S012 | Mandatory team / cost-center / env-type tags at creation | pi-1 | 7.00 | The foundational control that makes a future spend spike attributable in hours instead of weeks. Cheap. |
| 2 | S001 | Corporate SSO sign-in | pi-1 | 6.50 | Foundational — every other dev story depends on auth. |
| 3 | S008 | Safe-by-default blueprints (private VPC, encrypted EBS, scoped IAM) | pi-1 | 5.20 | Makes permit-by-default defensible to the platform team; if this slips, the carve-out collapses. |
| 4 | S027 | Project-wide spend dashboard with per-team / per-env breakdown | pi-1 | 4.43 | THE platform-team risk-reduction win for PI 1 — what they get in exchange for the deferred approval queue. |
| 5 | S028 | Per-env budget-threshold alerts | pi-1 | 4.40 | The user's chosen alternative to hard caps. Validates H1 directly. |
| 6 | S002 | "What can I do here" home page after sign-in | pi-1 | 4.33 | Adoption driver; without it, devs bounce back to the old workflow. |
| 7 | S006 | Sandbox blueprint catalog (Node+Postgres, Python+Redis, etc.) | pi-1 | 4.33 | Without it, sandbox creation is a Terraform homework assignment. |
| 8 | S004 | SSO-driven team-workspace auto-membership | pi-1 | 4.20 | Direct hit on the IT-bottleneck pattern the user is trying to escape. |
| 9 | S029 | One-click env teardown with destruction confirmation | pi-1 | 4.20 | Symmetric to spin-up; also the primary PI-1 cost-control lever. |
| 10 | S011 | Env-creation form pre-fills team / cost-center from dev profile | pi-1 | 4.00 | Resolves Q2 (mandatory tags without friction). |

## Slice 1 — PI 1 (12 weeks)

The walking-skeleton-equivalent for this work: a developer can sign in, spin up a sandbox in <5 min, attach a managed service, store a secret, deploy a containerized app to staging, see its cost, and tear it down — all without an approval ticket. Every backbone activity has at least one PI-1 story (5/5 PASS).

| ID | Activity | Story | WSJF | Why |
|---|---|---|---|---|
| S012 | Spin up | Mandatory tags at creation | 7.00 | Attribution foundation |
| S001 | Discover | SSO sign-in | 6.50 | Auth foundation |
| S008 | Spin up | Safe-by-default blueprints | 5.20 | Makes permit-by-default defensible |
| S027 | Operate | Project-wide spend dashboard | 4.43 | Platform-team PI-1 risk-reduction |
| S028 | Operate | Budget-threshold alerts | 4.40 | User's chosen cost-control mechanism |
| S002 | Discover | "What can I do here" home page | 4.33 | Adoption driver |
| S006 | Spin up | Blueprint catalog | 4.33 | Adoption foundation |
| S004 | Discover | Auto team-workspace membership | 4.20 | Direct kill of IT-ticket pattern |
| S029 | Operate | One-click teardown | 4.20 | Cost-control symmetry |
| S011 | Spin up | Pre-filled tag form | 4.00 | Resolves tag-friction conflict |
| S031 | Operate | Queryable audit store | 4.00 | Other half of "permit-by-default + auditing" |
| S007 | Spin up | Sub-5-min sandbox creation, no approval | 3.80 | THE headline PI-1 story; tests H1+H2 |
| S013 | Spin up | Policy override with one-line justification | 3.60 | Embodies "permit-by-default with auditing" |
| S015 | Connect | Self-service non-prod secrets vault | 3.50 | Kills credentials-in-Slack pattern |
| S026 | Operate | Per-env real-time cost in IDP UI | 3.40 | Tests H1 directly |
| S022 | Deploy | Inline deploy logs / healthcheck feedback | 3.20 | Prevents deploy black-box regression |
| S021 | Deploy | No-ticket staging deploy from UI / CLI | 3.13 | Closes sandbox→staging loop |
| S016 | Connect | Native secret injection (env vars / mounted files) | 3.00 | Pairs with S015 |
| S019 | Connect | BYO tools permitted in non-prod sandboxes | 3.00 | Resolves Q5 conflict (developer side wins per user) |
| S017 | Connect | One-click managed-service attach (DB, queue, cache) | 2.86 | Closes another ticket-flow loop |
| S020 | Connect | Background SBOM/scan for BYO non-prod workloads | 2.83 | Makes S019 acceptable to platform team |

21 stories in PI 1. Coherent end-to-end demo at PI-1 System Demo.

## Slice 2 — PI 2 (weeks 13-24)

PI 2 layers in: differentiation features for developers (preview envs per PR, blueprint forking), the agreed prod carve-out (approval-gated prod deploys, prod-secret request flow), and the first round of governance tightening that the platform team asked for in PI 1.

| ID | Activity | Story | WSJF | Why |
|---|---|---|---|---|
| S027b | (See S014) High-risk-policy blocking subset | (see below) | | |
| S027 | (Already PI-1; listed for context) | | | |
| S031 | (Already PI-1) | | | |
| S024 | Deploy | Approval-gated prod deploys | 3.40 | Both personas agree on prod carve-out |
| S030 | Operate | Sandbox auto-expiry with dev-controlled extension | 3.40 | Cost-control once leak pattern is visible |
| S037 | Cross-cutting (reliability) | Provisioning retry/idempotency | 3.40 | Reliability + cost (half-created envs leak silently) |
| S039 | Cross-cutting (security) | Prod-secret request flow | 3.40 | Pairs with S024 |
| S036 | Cross-cutting (reliability) | IDP SLO + on-call | 3.20 | IDP-itself outages become Sev-2 once devs depend on it |
| S032 | Cross-cutting (governance) | Soft cost cap per env with override-and-justify | 3.00 | Q3 tightening — first step toward hard caps without being one |
| S014 | Spin up | High-risk-policy blocking subset (S3 public in prod, etc.) | 2.86 | Tightens guardrails on the small set of "can't-undo" mistakes |
| S023 | Deploy | Per-PR preview environments | 2.86 | High delight; gated on stable PI 1 primitives |
| S040 | Cross-cutting (security) | SBOM findings escalation policy | 2.80 | Makes the S020 dashboard actionable |
| S003 | Discover | First-time onboarding tour | 2.67 | Polish |
| S025 | Deploy | Unified staging/prod deploy UX | 2.50 | Adoption hygiene |
| S009 | Spin up | Fork-and-tweak blueprints | 2.40 | Long-tail use case enablement |
| S033 | Cross-cutting (governance) | Platform-team review queue for "official" blueprints | 2.40 | Catalog quality control |
| S005 | Discover | Platform-team workspace-membership override | 2.33 | SSO-lag escape hatch |
| S010 | Spin up | Promote community blueprint to "official" status | 2.00 | Catalog quality control |
| S018 | Connect | Request-new-service flow | 1.83 | Demand-driven catalog growth |

16 stories in PI 2.

## Slice 3 — PI 3 (weeks 25-36)

PI 3 is forecast, not commitment. Reserved for items that depend on PI 1/2 evidence, plus the most-deferred governance items.

| ID | Activity | Story | WSJF | Why |
|---|---|---|---|---|
| S041 | Cross-cutting (security) | SOC2/ISO evidence export from audit store | 1.71 | Compliance lift; meaningful once audit data exists |
| S034 | Cross-cutting (governance) | Hard cost caps with break-glass | 1.67 | Conditional on PI 1/2 evidence showing alerts insufficient |
| S038 | Cross-cutting (reliability) | Multi-region IDP for DR | 1.38 | Premature until adoption proves IDP is critical-path |
| S035 | Cross-cutting (governance) | Allowlist-style approval workflow for env creation | 1.13 | **Deferred per VP Eng stance.** Listed at PI-3 only to give the platform-team objection a documented home — not a commitment. Revisit only if a real incident demands it. |

4 stories in PI 3 (all forecast / conditional).

## What's not in any slice

| ID | Story | Why not |
|---|---|---|
| (none) | Approval-gated env creation in PI 1 (specifically) | **Excluded by user-stated stance.** Platform-team simulation requested this; user explicitly said no for PI 1. Recorded at PI 3 (S035) as a conditional future-slice item, not committed. |
| (none) | Self-service prod env creation | Excluded — both personas align on the prod carve-out (Q6). Prod stays approval-gated. |
| (none) | Replace existing CI/CD systems | Out of scope to contain PI 1 effort. |
| (none) | BYO tools in prod without an allowlist | Excluded — both personas align on a stricter prod posture (Q5/Q6). Prod retains the allowlist. |
| (none) | Hard cost caps in PI 1 | Excluded by user stance (Q3 resolution). Soft cap in PI 2, hard cap conditional in PI 3 (S034). |

## Open prioritization questions

- **Q-OPEN-1: Existing tools to integrate with?** Affects PI 1 effort estimates for S006/S007/S021. If we are wrapping an existing IaC base, PI 1 sizing holds; if greenfield, S007's size may need to grow.
- **Q-OPEN-2: Platform-team headcount available?** Affects whether PI 1's 21 stories are realistic for a single team or need to be split across two teams.
- **Q-OPEN-3: Cost-alert default threshold per env?** Affects S028 acceptance criteria and the H1 success metric.
- **Q-OPEN-4: Who signs off on the override-with-justify model (S013) before PI 1 starts?** Political dependency — without a named owner, the platform team may block S013 at PI-planning.
- **Q-OPEN-5: Does an OKR framework exist?** No OKRs were provided, so the `okr` column in `backlog.csv` is empty. If OKRs exist, re-run with them attached.

## How the user-input-authoritative principle shows up here

The contested PI-1 items where developer-side preferences were ranked-in despite a platform-team simulation arguing against them:

- **S007** (sub-5-min sandbox, no approval gate) — in PI 1 per user stance. Platform-team simulation wanted approval queue (Q1). Overridden.
- **S028** (budget alerts, not hard caps) — in PI 1 per user stance. Platform-team simulation wanted hard caps (Q3). Overridden.
- **S019** (BYO tools in non-prod, no review queue) — in PI 1 per user stance. Platform-team simulation wanted hard no (Q5). Overridden.

In each case the platform-team objection is acknowledged with a compensating control (S012 mandatory tags, S027 spend dashboard, S031 audit store, S020 background SBOM scan) and a PI-2/PI-3 tightening path (S014, S032, S034, S035) — so the platform team is not abandoned, they are sequenced.
