# Role hints (UX/UI designer, architect) and flow advice from sister skills

Step 2.5 produces `role-hints.md` — a head-start artifact that turns the story map from an engineer-ready backlog into something a UX/UI designer and an architect can also act on first, and that folds in domain expertise from other installed skills when one matches a backbone flow. It is a *starting point that names what each role should look at first*, never a design system or an architecture decision record — the designer and architect still own their deliverables. Run it after Step 2 (per-persona stories) and before slicing locks in commitments.

## When to run Step 2.5

- **Always run** when ≥1 persona faces a UI surface AND ≥1 backbone activity touches a non-trivial system boundary (third party, multi-tenant data, regulated data, async workflow). That covers most product work.
- **Skip** when:
  - Pure infra / cron / cleanup work with no UI (architect hints might still be useful — produce just that half)
  - Solo founder pre-PMF doing 1-week experiments — overhead exceeds value
  - User explicitly says "skip the role hints, we have a designer/architect already on this"

When in doubt, produce a minimal `role-hints.md` — even ten lines per role beats zero.

## Inputs

`role-hints.md` is derived, not authored. Inputs:

1. `design.md` — personas (with verbatim quotes), context loop trace, hypotheses, non-goals
2. `storymap.md` backbone activities + per-persona stories (Step 2 output)
3. `## Non-backbone / cross-cutting` section of `storymap.md` (themes for the architect)
4. Any third-party integrations or platform constraints surfaced during context collection
5. Skill-chaining results (see [Flow-advisor skill chaining](#flow-advisor-skill-chaining) below) — folded into the relevant role section

If any input is missing, note it explicitly in the corresponding section: "(no cross-cutting themes recorded — confirm with user)".

## `role-hints.md` template

```markdown
# Role hints — <project name>

> Head-start notes for the UX/UI designer and architect, derived from `design.md` and `storymap.md`. **Not a replacement for design or architecture work** — a starting point that names what each role should look at first.

## For the UX/UI designer

### Persona snapshots

| Persona | Day-to-day | Top pain point | Primary device / context | Source |
|---|---|---|---|---|
| Tenant Admin | Manages 5-15 active sub-accounts; rarely uses the product themselves | Onboarding new sub-account takes 20+ min today | Desktop, often dual-monitor; rarely mobile | [interview: Aisha] |
| End User | Submits 10-30 transactions/day in batches | Loses context when interrupted by approval prompts | Desktop primary, mobile for status checks | [interview: Marcus] |
| Compliance Officer | Audits a sample of refunds weekly | Has to export to Excel because there's no in-product audit search | Desktop only; screen reader for some users | [interview: Priya] |

### Flow inventory (per backbone activity, persona-specific variants)

| Activity | Tenant Admin variant | End User variant | Compliance variant |
|---|---|---|---|
| 1. Sign in | SSO setup + sub-account assignment | SSO sign-in (one-tap) | SSO sign-in + role-claim verification |
| 2. Find transaction | (not in their flow) | Search by recent / filter by status | Bulk filter by date range + amount range |
| 3. Submit refund | (not in their flow) | One-click within auto-approve limit | (read-only — they audit, not submit) |
| ... | ... | ... | ... |

### Friction hotspots

These are the activities where multiple personas converge or hand off. UI complexity grows fastest here — the designer should look at them first.

- **Activity 4 (Approver decision)** — Admin can override; End User waits; Compliance audits later. Three personas, same screen, different needs.
- **Activity 5 (Audit visibility)** — Compliance is the primary; End User checks "did my thing go through?"; Admin sees aggregate. Risk: building three views vs. one well-filtered view.

### Open UX questions (designer must call before slice 1)

- [ ] Approval queue UI — list view, kanban, or inbox? Affects S006/S007 layout.
- [ ] Audit search affordance — global search bar, dedicated audit page, or filter on the main list? Affects S008/S009.
- [ ] Refund-blocked state — modal explaining why, inline disabled button with tooltip, or both? Affects S005 edge cases.

### Accessibility / i18n / context hints

- Compliance persona includes screen-reader users — every interactive element on the audit screens (Activity 5) needs accessible names + keyboard navigation.
- End User persona uses mobile for status checks (per [interview: Marcus]) — Activity 5 needs mobile-friendly read view, even if Activity 3 (submit) stays desktop-only.
- No i18n required for slice 1 (per [user-stated]: "US-only customers"). Plan i18n hooks but defer translation to slice 3+.

### Flow advice from external skills

(Empty if no flow-advisor skills were invoked. Otherwise, one section per advisor.)

#### Auth flow — from `auth-flow-advisor` skill [skill: auth-flow-advisor @ 2026-06-10]

> Activity 1 (Sign in) recommendations:
> - Use SSO PKCE flow given multi-tenant SaaS context
> - Store sub-account assignment as a claim, not a separate table lookup, to avoid an extra hop per request
> - Test for stale-claim handling — admins changing sub-account assignments should propagate within 5 min
>
> (Architect cross-references: see "Boundary candidates" below.)

## For the architect

### Cross-cutting work index

| Theme (from non-backbone section) | Activity it most touches | Likely cost / risk |
|---|---|---|
| Audit retention | Activity 5 (Audit visibility) | Storage growth scales with transaction volume × retention years; pick storage tier early |
| Compliance webhook export | Activity 5 (Audit visibility) | Compliance team's downstream tools listen — broken webhooks = failed audits = customer escalation |
| Observability | All | Per-tenant request rate + per-activity SLO; default to OpenTelemetry, not vendor lock-in |

### Boundary candidates (define contracts before slice 1)

Activities that span multiple systems, teams, or data stores. These are where API / event / schema contracts must be pinned down before slice 1 starts coding.

- **Activity 1 (Sign in)** — SSO IdP boundary; needs JWT claim spec (which fields, who issues, how rotated)
- **Activity 3 (Submit refund)** — Payment processor boundary (Stripe / Paddle); needs idempotency key strategy + retry policy + reconciliation event spec
- **Activity 5 (Audit visibility)** — Audit log writer boundary; needs event schema (refund_id, actor_id, amount, reason, timestamp, request_id) + retention contract

### Hard constraints

From `design.md` Hypotheses + context loop. These are non-negotiable inputs to architecture choices.

- Data residency: US only for slice 1; EU customers in scope by slice 3 — **don't pick a region-locked store**
- Latency budget: 500ms p95 for sign-in (per [interview: Aisha]); 2s p95 for audit search (per [interview: Priya])
- Framework lock-in: existing app is Next.js + Prisma + Postgres (per [code: package.json]) — slice 1 must integrate, not greenfield
- Deploy topology: Vercel + Supabase Postgres (per [code: vercel.json + supabase/]) — async workers need to fit this stack

### Risky integrations

Third parties referenced anywhere in the backbone or `design.md`, with a one-line risk note.

- **Stripe / Paddle** (Activity 3) — webhook reliability; idempotency on retry; rate limits at 100 req/sec per account. Plan for queueing + DLQ.
- **Auth0** (Activity 1) — token-refresh edge cases; multi-tenant claim-mapping needs explicit rule definitions.
- **SendGrid** (Activity 3 customer-email confirmation) — 90-day deliverability degrades on shared IPs. Move to dedicated IP at >50K emails/day, not before.

### Open architecture questions (architect must call before slice 1)

- [ ] Sync vs async refund pipeline — affects S005 implementation cost and S008 audit-search latency. Lean async + status polling unless slice 1 is <100 refunds/day.
- [ ] Audit log store — same Postgres or dedicated time-series? Cheaper to start same-Postgres, painful to migrate at >10M rows.
- [ ] Approval routing engine — codified rules vs. policy-as-data (e.g., OPA)? Codified is faster for slice 1; policy-as-data scales better past 5+ rule types.

### Flow advice from external skills

(Empty if no flow-advisor skills were invoked. Otherwise, one section per advisor.)

#### Payment flow — from `payment-integration-best-practices` skill [skill: payment-integration-best-practices @ 2026-06-10]

> Activity 3 (Submit refund) recommendations:
> - Always use an idempotency key keyed on (refund_id, attempt_number); retries with same key MUST return same result
> - Reconciliation: subscribe to `charge.refunded` webhook AND poll the refund-status endpoint nightly for the last 7 days; webhooks miss ~0.1%
> - Test for partial-refund + chargeback collision — both can hit the same charge concurrently
>
> (UX cross-references: stale state in Activity 5 can come from webhook lag; designer should plan for "pending" state.)
```

Adapt the headings to the project — if there's no Compliance persona, drop that column. If there's no third-party integration, drop "Risky integrations". The structure is a checklist, not a quota.

## Flow-advisor skill chaining

The Skill tool may expose other installed skills. Some of them are domain experts on flows that appear in your backbone. Use them — within the per-run cap.

### Discovery protocol

At the entry to Step 2.5:

1. **Re-read the available skills list** (shown in the host's session-startup system messages — same list the orchestrator sees)
2. **Map backbone activities to candidate skill names** — heuristic match by description / keywords:
   - Activity has "sign in / sign up / SSO / OAuth / login" → look for `auth*`, `*identity*`, `*login*`, `*sso*` skills
   - Activity has "pay / refund / charge / invoice / billing / subscription" → look for `payment*`, `*billing*`, `*stripe*`, `*finance*` skills
   - Activity has "onboard / first-run / setup wizard" → look for `onboarding*`, `first-run*` skills
   - Activity has "search / find / filter / list" → look for `search*`, `*query*` skills
   - Activity has "notify / email / push / alert" → look for `notification*`, `email*`, `*messaging*` skills
   - Activity has "audit / compliance / log" → look for `audit*`, `compliance*`, `governance*` skills
   - Cross-cutting "accessibility / a11y" theme → look for `accessibility*`, `a11y*` skills
   - Cross-cutting "i18n / localization" theme → look for `i18n*`, `*localization*`, `*translation*` skills
   - Cross-cutting "multi-tenancy" theme → look for `multitenant*`, `*tenant*`, `*saas*` skills
3. **Dedupe and rank by impact** — which flows are in slice 1 (high), slice 2 (medium), later (skip)? Stay within the Step 2.5 advisor cap — see the skill-chaining caps in [SKILL.md → Rules that govern every run](../SKILL.md#rules-that-govern-every-run) (Rule 5).
4. **Skip sister-framework slash-commands** — gstack `/plan-design-review`, Superpowers `brainstorming`, etc. are user-facing commands, not advisors to invoke from within this skill. They are inbound integrations, not outbound. (See [framework-integration.md](framework-integration.md).)

### Invocation pattern

For each candidate skill, use the `Skill` tool with a tightly scoped question:

```
Skill: auth-flow-advisor
Args: |
  Context: Multi-tenant B2B SaaS for refund management. Personas: Tenant Admin, End User, Compliance Officer.
  Backbone activity: "Sign in" — SSO via Auth0, sub-account assignment as a claim, screen-reader users in Compliance.
  Stories in slice 1:
    - S001: As a Tenant Admin, I want to set up SSO once so my reps can sign in without per-user provisioning.
    - S002: As an End User, I want to sign in with my work account so I don't manage another password.
    - S003: As a Compliance Officer, I want my role claim verified at every sign-in so audit access can't be silently revoked.

  Question: What should we know about implementing this auth flow that an architect / UX designer should bake into slice 1?
```

The advisor's answer goes verbatim into `role-hints.md` under "Flow advice from external skills" within the relevant section (UX or architect — usually both reference each advisor's output).

Tag with `[skill: <name> @ <date>]` in `design.md` so reviewers can trace which content came from which advisor.

### When the advisor says "I don't know" or asks for more context

If the advisor responds with clarifying questions, you have two options:

1. **Pass through to the user** — surface the questions; treat them as additional gaps under Step 0.4
2. **Fold into open questions** — add the unanswered items under "Open UX questions" or "Open architecture questions" in `role-hints.md`

Don't loop on the advisor — one round per advisor is the budget. If round 1 didn't yield actionable advice, the flow probably needs human expertise, not skill chaining.

### When no advisor skill exists for a flow

Document it explicitly in `role-hints.md`:

```markdown
### Flows that would benefit from domain expertise (no advisor skill installed)

- Auth flow (Activity 1) — SSO + multi-tenant claim mapping. No installed advisor skill; recommend the architect spend ~2 hours reviewing OWASP ASVS L2 + Auth0's multi-tenant guide before slice 1.
- Payment flow (Activity 3) — Stripe refund integration. No installed advisor skill; recommend pairing the architect with someone who's shipped Stripe webhooks at this scale.
```

This is honest signal — it tells the user where outside expertise is needed, without pretending the skill provided it.

## Refining `role-hints.md` on a non-empty baseline (iteration)

When the loop runs on an existing storymap rather than from scratch:

1. **Read the prior `role-hints.md`** if it exists — it's authoritative for any persona snapshots and constraints that weren't re-derived
2. **Diff the new backbone vs. the old** — added activities → new flow inventory rows + new boundary candidates; removed activities → archive (don't silently delete) the related hints
3. **Re-invoke advisor skills** only for *new* flows or for flows where the advice has plausibly changed since the last run (e.g., if Stripe published a major API change). Don't re-invoke just because time passed.
4. **Append to the decisions log** in `design.md` for any UX or architecture question resolved since the prior run — append-only, never overwrite. The append-only decisions-log rule is owned by [persistent-knowledge.md](persistent-knowledge.md).

## Anti-patterns

- **Don't author UX or architecture work from inside this skill.** `role-hints.md` is a head-start with concrete pointers, not a design system or an architecture decision record. The designer and architect own the deliverables; this skill seeds them.
- **Don't fabricate persona snapshots.** If `design.md` doesn't have a verbatim or interview source for a persona's pain point, write `[inferred]` and surface it as an open question. Don't invent UX advice grounded in nothing.
- **Don't invoke advisor skills "just in case".** You should usually be at 1-2, never above the Step 2.5 cap. Each invocation costs turns and adds maintenance burden — only invoke when the flow actually has a known-pattern surface (auth, payment, search, accessibility).
- **Don't let advisor output override user-stated decisions.** If the user said "we don't need refund webhooks in slice 1" and the payment advisor says "you absolutely need refund webhooks", the user wins — surface the advisor's objection as a future-slice risk, not a slice-1 override. This follows the same user-input-authoritative priority order that governs persona simulation; see [SKILL.md → Rules that govern every run](../SKILL.md#rules-that-govern-every-run).
- **Don't generate `role-hints.md` after slice-1 ACs are written.** The point of Step 2.5 is that designer/architect questions surface *before* slicing locks in commitments. If you delay, you produce hints that document a decision instead of informing it.
- **Don't duplicate `design.md` content.** `role-hints.md` references personas and activities by name; the source of truth stays in `design.md`. If you're copy-pasting paragraphs across files, you're producing maintenance debt.

## Cost ceiling

Step 2.5 should consume 10-15% of the total turn budget — most of it is restructuring already-mined content into a role-readable format. Skill-chaining adds 1-3 extra invocations (each roughly the cost of a small subagent run).

If Step 2.5 is exceeding 20% of the budget, you're authoring instead of summarizing. Stop, write what you have, and document the gaps as open questions.

## Where this fits in the framework integrations

- **Superpowers** — `role-hints.md` is *not* the same as a `brainstorming` design doc; brainstorming clarifies intent (input to this skill), `role-hints.md` is downstream of intent. After this skill produces `role-hints.md`, the designer / architect work on it before `writing-plans` decomposes slice 1 into tasks.
- **gstack** — `/plan-design-review` reviews `role-hints.md` for UX coherence + persona narratives; `/plan-eng-review` reviews the `role-hints.md` architect section for engineering feasibility. Both are *inbound* commands the user runs; this skill produces the input.
- **GSD** — `role-hints.md` lives alongside the GSD Brief and informs Milestone planning. Reference it in `.gsd/Brief.md` (after the user imports), not write directly into `.gsd/`.

The per-framework handoff cues and the GSD slice/Milestone terminology collision are owned by [framework-integration.md](framework-integration.md). The handoff line at Step 6 should name `role-hints.md` if it was produced:

> "Slice 1 (12 stories) → .gsd/Roadmap.md + TODO.md. Designer should read role-hints.md§UX before slice-1 mocks; architect should read role-hints.md§Architect before slice-1 contracts. Run /gsd discuss next."
