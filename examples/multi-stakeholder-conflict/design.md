# Internal Developer Platform (IDP) — Design Doc

## The question this work answers

Can we ship a self-service IDP that closes the velocity gap for application developers while introducing *enough* governance to prevent another uncontrolled spend incident — without reintroducing the IT-bottleneck pattern developers are currently escaping into personal AWS accounts? [user-stated]

## Outcome

In 6 months: a measurable majority of non-prod sandbox environments are created via the IDP (target: 70%+ of net-new non-prod env activity) without an approval queue, AND the unbudgeted cloud-spend surprise from Q-1 is non-recurring (cost alerts in place, hard caps in PI 2). Developers stop the threatened shadow-IT migration to personal AWS. [user-stated, with success metrics inferred to make the outcome measurable]

## Trigger

- A $40K AWS spike in Q-1 has put governance on the executive radar [user-stated]
- Application developers are threatening to use personal AWS accounts, a shadow-IT failure mode that breaks every downstream control [user-stated]
- VP Engineering has chosen this PI to bet on developer velocity as the path back to platform-team relevance, rather than locking down [user-stated]

## Personas

### Application Developer (primary end-user)
- **Role:** Builds and ships product features; needs sandbox + staging + secrets + service access on demand. [user-stated]
- **Goal in this work:** Get a working sandbox in under 5 minutes with no approval gate; bring my own tools without a security review queue. [user-stated]
- **Today they:** Either wait days for IT tickets, or sidestep the org and spin things up in personal AWS accounts. [user-stated]
- **Pain:** IT bottleneck; perception that the platform team is an adversary rather than a service. [user-stated]
- **Verbatim flavor:** "Threatening to keep using personal AWS accounts." [user-stated]

### Platform Team Engineer (admin)
- **Role:** Owns the IDP, runs the cloud account, holds the security/cost/compliance pager. [user-stated]
- **Goal in this work:** Tight governance — approval workflows for env creation, mandatory tags, cost limits, security policies enforced. [user-stated]
- **Today they:** Operating under an "anyone can do anything" culture they consider broken. [user-stated]
- **Pain:** Took the heat for the $40K spike; expected to prevent the next one but currently lacks the controls to do so. [user-stated]

### VP Engineering (sponsor — also the actual user of this skill invocation)
- **Role:** Sponsor and decision-maker. [user-stated]
- **Goal in this work:** Defaults that favor "permit by default in non-prod with auditing" rather than "block by default with approval workflow". Restore velocity, then layer guardrails. [user-stated]
- **Constraint they imposed:** No approval-gated env creation in PI 1 — "a non-starter politically, even if simulation tells you the platform team wants it." [user-stated]

## User activities (the backbone)

The narrative flow, left-to-right, in app-developer voice:

1. **Discover and request access** — find the IDP, sign in, get into my team's workspace
2. **Spin up an environment** — provision a sandbox or non-prod env on demand
3. **Connect services and secrets** — wire up the databases, queues, APIs, and credentials my workload needs
4. **Deploy to staging** — push my build to a shared staging environment and validate
5. **Operate and observe** — see what my env is doing, what it costs, and tear it down when done

See `storymap.md` for tasks and stories under each.

## Opportunities

| Activity | Opportunity |
|---|---|
| Discover and request access | Devs stop filing tickets to onboard themselves; first sandbox up in <5 min from clicking the link |
| Spin up an environment | "Permit by default in non-prod" — no approval queue; pre-approved blueprint templates that just work |
| Connect services and secrets | Stop the copy-paste-credentials-to-Slack pattern; self-service vault with sane defaults |
| Deploy to staging | Push-button staging deploys that don't require a release-manager ticket |
| Operate and observe | Devs see their own cost in near-real time; audit trail exists for the platform team without blocking the dev |

## Context sources mined

- The user's prompt is the sole source of context for this invocation. No repository / README / commit log was provided; this is a pure Mode A from-scratch scoping. [user-stated context only]
- No interview notes, no persistent memory, no MCP integrations applied.

## Contradictions flagged

None at the artifact level (no other sources to contradict the prompt). The substantive contradiction is between the two stakeholder groups — captured in the conflict matrix below.

## Persona simulation: gaps surfaced

In single-shot mode, I role-played each persona in parallel using the rich context the user provided. The questions I asked each simulated persona:

1. **Should env creation be gated by an approval workflow in PI 1?**
2. **Are tags mandatory at creation, or audited after the fact?**
3. **Where should cost limits live — hard cap that blocks creation, soft cap that warns, or per-env budget alerts only?**
4. **Should security policies (network, IAM, image scanning) be enforced at creation, or surfaced as findings?**
5. **Can devs bring their own tools without a security review queue?**
6. **Is prod treated like non-prod under "permit by default", or carved out with stricter controls?**
7. **What's the rollback story if a dev breaks something? Self-service revert, or platform team intervenes?**
8. **Is secrets management self-service or admin-mediated?**

## Persona perspective matrix (conflict matrix)

| # | Question | Platform Team (sim) | Application Developer (sim) | Conflict? | Resolution (and source) |
|---|---|---|---|---|---|
| Q1 | Approval-gated env creation in PI 1 | "Yes — every non-prod env should go through a lightweight approval queue so we can review naming, tags, blueprint choice, and cost class before spend starts." [simulated: platform team] | "Absolutely not — that's the IT-bottleneck pattern we're escaping. Make it instant or we'll keep using personal AWS." [simulated: developer] | YES — direct conflict | **Developer side wins, BUT only because the user explicitly chose this.** [user-stated] overrides [simulated: platform team]. PI 1 ships permit-by-default env creation, no approval queue. Platform-team objection logged as a future-slice risk in handoff.md. |
| Q2 | Mandatory tags vs audited tags | "Mandatory at creation — without team/cost-center/env-type tags we cannot allocate the next $40K spike to anyone." [simulated: platform team] | "Mandatory is fine *if* the form is one-click defaults — don't make me type my team name on every env." [simulated: developer] | PARTIAL — both want tags, disagree on friction | Tags are mandatory at creation [simulated: platform team] but the form pre-fills team and cost-center from the dev's profile and offers a smart default for env-type [simulated: developer]. Devs can override, can't omit. Both sides accept. |
| Q3 | Cost limits in PI 1 | "Hard cap at the env level that blocks further provisioning when exceeded. Set conservatively." [simulated: platform team] | "Budget alerts are fine. Hard caps that block me mid-sprint are the same bottleneck wearing a different hat." [simulated: developer] | YES — direct conflict | Compromise consistent with [user-stated] "guardrails with permit-by-default": **PI 1 ships per-env budget alerts and a project-wide spend dashboard, no hard cap.** **PI 2 adds soft caps with override-and-justify; hard caps deferred to PI 3 or beyond pending evidence.** This honors the user's "permit by default in non-prod with auditing" stance. |
| Q4 | Security policy enforcement | "Policies enforced at the API/IaC layer — block creation of overly-permissive IAM, public S3, unencrypted volumes." [simulated: platform team] | "I want the policy to be a default in the blueprint, not a wall. If I'm experimenting with a public endpoint for a demo, don't block me." [simulated: developer] | PARTIAL — both want policies, disagree on enforcement strength | **PI 1: policies are pre-applied defaults in blueprints (you get a private VPC, encrypted EBS, scoped IAM by default) but devs can override with a recorded justification.** Audit trail captures the override. PI 2 introduces a "high-risk policy" subset that does block (e.g., wide-open S3 in prod). Consistent with [user-stated] "permit by default with auditing". |
| Q5 | BYO tools without security review | "Hard no — every new tool is an unaudited supply-chain risk." [simulated: platform team] | "Hard yes — security review queues are the reason I haven't shipped." [simulated: developer] | YES — direct conflict | **PI 1: BYO tools permitted in non-prod sandboxes only; an automated SBOM/scan runs in the background and surfaces findings without blocking. Prod still requires an allowlist.** This is a middle path consistent with [user-stated] "ability to bring their own tools without security review" for non-prod, and acknowledges the platform-team objection by carving out prod. The platform-team's "hard no" is overridden because [user-stated] preference explicitly permits BYO in non-prod. |
| Q6 | Prod vs non-prod | "Prod must be approval-gated and policy-locked regardless of what we do for non-prod." [simulated: platform team] | "Agreed — I don't need self-service prod. Just give me staging and below." [simulated: developer] | NO — both agree | Prod stays approval-gated and policy-locked. Non-prod is permit-by-default. This is the carve-out that makes the rest of the plan defensible. |
| Q7 | Rollback / break-glass | "Platform team intervenes — we own the cloud account." [simulated: platform team] | "Self-service tear-down and recreate. If I broke it, let me reset it." [simulated: developer] | PARTIAL | **Self-service for env-level operations (tear down, recreate, redeploy); platform-team intervention reserved for account-level or cross-tenant incidents.** Both sides accept. |
| Q8 | Secrets management | "Admin-mediated for prod secrets; tightly scoped for non-prod." [simulated: platform team] | "Self-service for non-prod, please. Prod via a request flow is fine." [simulated: developer] | NO — both align on the non-prod/prod split | Self-service secrets vault for non-prod; request flow for prod. PI 1 ships the non-prod self-service path; prod request flow lands in PI 2. |

**Arbitration summary:** Of 8 questions, 3 were direct conflicts. In all 3, the user-input-authoritative principle applied: the user's stated preference for developer velocity in PI 1 won. The platform team's objections are not discarded — they are logged in `handoff.md` as PI 2 candidates and risks to monitor.

## Hypotheses

| # | Hypothesis | Validates in slice | Method |
|---|---|---|---|
| H1 | Permit-by-default + per-env budget alerts is sufficient to prevent a repeat $40K-class spend spike. [user-stated stance, untested] | PI 1 demo + 8 weeks of cost telemetry | Track total non-prod spend and per-env outliers weekly; compare to Q-1 baseline |
| H2 | Sub-5-minute sandbox creation will stop the threatened personal-AWS shadow-IT migration. [user-stated outcome] | PI 1 | Survey dev cohort; measure personal-AWS shutdowns; count IDP-created envs |
| H3 | Mandatory pre-filled tags get >95% accurate coverage without a friction penalty. [inferred from compromise on Q2] | PI 1 | Audit tag completeness on a sample of PI 1 envs |
| H4 | Default-blueprint security policies (private VPC, encrypted EBS, scoped IAM) cover ~80% of non-prod use without manual override. [inferred from Q4 resolution] | PI 1 | Count override-and-justify events vs total provisioning events |
| H5 | A BYO-tools-with-background-scan model is acceptable to security leadership when scoped to non-prod. [simulated: platform team's objection means this is unproven] | PI 1 + security review at PI 1 system demo | Security sign-off review at end of PI 1 |

## Constraints

- **Hard deadlines:** None named. 12-week PI cadence (SAFe). [user-stated]
- **Platform / integrations:** AWS (implied by the $40K AWS spike). [user-stated, inferred to AWS as the cloud]
- **Team / skills:** Platform team exists; size and skill mix not stated. [inferred — gap]
- **Political:** No approval-gated env creation in PI 1, regardless of simulation outcome. [user-stated, hard constraint]

## Non-goals

- **PI 1 will not include an approval workflow for non-prod env creation.** [user-stated, explicit non-goal]
- **PI 1 will not include hard cost caps that block provisioning.** [resolved from Q3, consistent with user stance]
- **PI 1 will not include self-service prod env creation** — prod stays approval-gated. [from Q6, both personas align]
- **PI 1 will not include an allowlist gate for BYO tools in non-prod** — background scanning only. [resolved from Q5]
- **PI 1 will not replace existing CI/CD systems** — IDP integrates with whatever exists, doesn't rewrite. [inferred constraint to keep scope contained]

## Open questions

- **Q-OPEN-1: What existing tools should the IDP integrate with on day 1?** (Terraform / Crossplane / Backstage / a homegrown wrapper? — gap from the brief, [inferred])
- **Q-OPEN-2: Does the platform team have an existing IaC baseline we are wrapping, or are we building from scratch?** — affects PI 1 effort dramatically
- **Q-OPEN-3: What does "prod" mean operationally — single account, account-per-team, account-per-env?** — affects the prod approval flow in PI 2
- **Q-OPEN-4: Is there a single platform-team lead who can sign off on the carve-out in Q4 (override-with-justify) before PI 1 starts?** — political dependency
- **Q-OPEN-5: What is the cost-alert threshold per env?** — the $40K spike was the entire org; per-env reasonable defaults need a number

These are documented as blocking decisions in `handoff.md`.

## Decisions log

| Date | Decision | Reasoning |
|---|---|---|
| 2026-06-08 | Slicing: **SAFe PI cadence**, 12 weeks per PI | [user-stated] |
| 2026-06-08 | Prioritization: **WSJF** | [user-stated] |
| 2026-06-08 | **Approval-gated env creation: deferred per VP Eng stance, despite platform-team simulation arguing for it.** | The simulated platform-team persona argued strongly for an approval queue in PI 1 (see conflict matrix Q1). The user explicitly stated this is "a non-starter politically, even if simulation tells you the platform team wants it." Per the user-input-authoritative principle (SKILL.md "Before any other rule in this skill: what the actual user told you, in this conversation, always wins"), the user's stance overrides the simulated persona's preference. Platform-team objection logged in handoff.md as a PI 2 candidate and a risk to monitor. |
| 2026-06-08 | **PI 1 cost controls: alerts + dashboard only, no hard caps.** Soft caps in PI 2, hard caps deferred to PI 3+. | The simulated platform-team persona argued for hard caps in PI 1 (Q3). The user's "permit by default in non-prod with auditing" stance is incompatible with a hard cap that blocks provisioning. The compromise (alerts + dashboard in PI 1, soft cap in PI 2) gives the platform team visibility and a tightening path without breaking developer velocity in PI 1. |
| 2026-06-08 | **BYO tools permitted in non-prod sandboxes in PI 1; background SBOM/scan only, no allowlist gate.** | Direct conflict resolution (Q5). User-stated preference wins. Prod allowlist preserved as a future-slice item. |
| 2026-06-08 | **Tags mandatory at creation but pre-filled from dev profile + smart defaults.** | Compromise (Q2). Both personas accept. |
| 2026-06-08 | **Default security policies pre-applied in blueprints with override-with-justify audit trail.** | Compromise (Q4) — pre-applied defaults give 80%+ coverage without manual review; the override-and-justify model surfaces high-risk choices for audit without blocking. |
| 2026-06-08 | **Prod stays approval-gated; non-prod is permit-by-default.** | Both personas align (Q6); this is the carve-out that makes the rest of the plan defensible. |
| 2026-06-08 | **Walking-skeleton equivalent (PI 1 demo target):** A developer signs in, spins up a sandbox in <5 min, connects a secret, deploys a containerized app to staging, sees its cost in the dashboard, and tears it down — all without an approval ticket. | This is the end-to-end PI 1 narrative that drives slice-1 story selection. |
