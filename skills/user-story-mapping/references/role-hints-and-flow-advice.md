# Role hints (UX/UI designer, architect) and flow advice from sister skills

Step 2.5 produces `role-hints.md`: head-start notes for UX/UI, architecture, and skill advisors. It names first inspection points; not a design system or architecture decision record. Run after Step 2, before slicing.

## When to run Step 2.5

- **Always run** when ≥1 persona faces UI AND ≥1 backbone activity touches a boundary (third party, multi-tenant data, regulated data, async workflow).
- **Skip** when:
  - Pure infra / cron / cleanup with no UI (architect hints may help — produce just that half)
  - Solo founder pre-PMF 1-week experiments — overhead exceeds value
  - User says "skip the role hints, we have designer/architect already"

Unsure? Produce `role-hints.md`; ten lines/role beats zero.

## Inputs

Inputs:

1. `design.md` — personas (with verbatim quotes), context trace, hypotheses, non-goals
2. `storymap.md` backbone activities + per-persona stories (Step 2)
3. `## Non-backbone / cross-cutting` in `storymap.md` (architect themes)
4. Third-party integrations/platform constraints from context collection
5. Skill-chaining results (see [Flow-advisor skill chaining](#flow-advisor-skill-chaining)) — fold into role section

If missing, note: "(no cross-cutting themes recorded — confirm with user)".

## `role-hints.md` template

```markdown
# Role hints — <project name>

> Head-start notes from `design.md` and `storymap.md`. **Not a replacement for design or architecture work** — first inspection points.

## For the UX/UI designer

### Persona snapshots

| Persona | Day-to-day | Top pain point | Primary device / context | Source |
|---|---|---|---|---|
| Tenant Admin | Manages 5-15 sub-accounts | Onboarding takes 20+ min | Desktop, dual-monitor; rarely mobile | [interview: Aisha] |
| End User | Submits 10-30 transactions/day | Approval prompts interrupt | Desktop primary, mobile status checks | [interview: Marcus] |
| Compliance Officer | Audits weekly refund sample | Exports to Excel; audit search missing | Desktop only; screen-reader users | [interview: Priya] |

### Flow inventory (per backbone activity, persona-specific variants)

| Activity | Tenant Admin variant | End User variant | Compliance variant |
|---|---|---|---|
| 1. Sign in | SSO setup + sub-account assignment | One-tap SSO sign-in | SSO sign-in + role-claim verification |
| 2. Find transaction | (not in their flow) | Recent search / status filter | Bulk date + amount filter |
| 3. Submit refund | (not in their flow) | One-click within auto-approve limit | (read-only audit) |
| ... | ... | ... | ... |

### Friction hotspots

Start where personas converge or hand off; UI complexity grows there.

- **Activity 4 (Approver decision)** — Admin overrides; End User waits; Compliance audits. Same screen, different needs.
- **Activity 5 (Audit visibility)** — Compliance primary; End User checks outcome; Admin sees aggregate. Risk: three views vs. filter.

### Open UX questions (designer must call before slice 1)

- [ ] Approval queue UI — list, kanban, or inbox? Affects S006/S007.
- [ ] Audit search — global search, audit page, or main-list filter? Affects S008/S009.
- [ ] Refund-blocked — modal, disabled+tooltip, or both? Affects S005 edge cases.

### Accessibility / i18n / context hints

- Compliance screen-reader users — Activity 5 needs accessible names + keyboard navigation.
- End User uses mobile status checks (per [interview: Marcus]) — Activity 5 needs mobile read; Activity 3 desktop-only.
- No i18n for slice 1 (per [user-stated]: "US-only customers"). Add hooks; defer translation to slice 3+.

### Flow advice from external skills

(Empty if none; otherwise one section per advisor.)

#### Auth flow — from `auth-flow-advisor` skill [skill: auth-flow-advisor @ 2026-06-10]

> Activity 1 (Sign in) recommendations:
> - Use SSO PKCE for multi-tenant SaaS
> - Store sub-account assignment as claim, not lookup
> - Test stale-claim propagation within 5 min
>
> (Architect cross-references: see "Boundary candidates" below.)

## For the architect

### Cross-cutting work index

| Theme (from non-backbone section) | Activity it most touches | Likely cost / risk |
|---|---|---|
| Audit retention | Activity 5 (Audit visibility) | Storage = transaction volume × retention years; pick tier |
| Compliance webhook export | Activity 5 (Audit visibility) | Broken webhooks = failed audits/customer escalation |
| Observability | All | Per-tenant rate + per-activity SLO; default OpenTelemetry, not vendor lock-in |

### Boundary candidates (define contracts before slice 1)

Pin contracts before slice 1 for cross-system/team/store work.

- **Activity 1 (Sign in)** — SSO IdP; define JWT claims, issuer, rotation
- **Activity 3 (Submit refund)** — Payment processor (Stripe / Paddle); define idempotency key, retry policy, reconciliation event
- **Activity 5 (Audit visibility)** — Audit log writer; define event schema (refund_id, actor_id, amount, reason, timestamp, request_id) + retention

### Hard constraints

From `design.md` Hypotheses + context loop; non-negotiable inputs.

- Data residency: US slice 1; EU slice 3 — **don't pick a region-locked store**
- Latency: 500ms p95 sign-in (per [interview: Aisha]); 2s p95 audit search (per [interview: Priya])
- Framework: Next.js + Prisma + Postgres (per [code: package.json]) — integrate, don't greenfield
- Deploy: Vercel + Supabase Postgres (per [code: vercel.json + supabase/]) — async workers must fit

### Risky integrations

Third parties in backbone or `design.md`, one-line risk each.

- **Stripe / Paddle** (Activity 3) — webhooks; idempotent retry; 100 req/sec/account. Plan queueing + DLQ.
- **Auth0** (Activity 1) — token refresh; multi-tenant claim mapping needs rules.
- **SendGrid** (Activity 3 customer-email confirmation) — shared-IP deliverability degrades after 90 days. Dedicated IP at >50K emails/day, not before.

### Open architecture questions (architect must call before slice 1)

- [ ] Sync vs async refund pipeline — affects S005 cost/S008 latency. Lean async + status polling unless slice 1 <100 refunds/day.
- [ ] Audit log store — Postgres or time-series? Same-Postgres cheaper; migration hurts at >10M rows.
- [ ] Approval routing engine — codified rules vs. policy-as-data (e.g., OPA)? Codified faster for slice 1; policy-as-data scales past 5+ rule types.

### Flow advice from external skills

(Empty if none; otherwise one section per advisor.)

#### Payment flow — from `payment-integration-best-practices` skill [skill: payment-integration-best-practices @ 2026-06-10]

> Activity 3 (Submit refund) recommendations:
> - Use idempotency key (refund_id, attempt_number); same-key retries MUST return same result
> - Reconcile via `charge.refunded` webhook AND nightly last-7-days refund-status polling; webhooks miss ~0.1%
> - Test partial-refund + chargeback collision on same charge
>
> (UX: webhook lag creates stale Activity 5 state; designer should plan "pending" state.)
```

Adapt headings: drop Compliance column if no Compliance persona; drop "Risky integrations" if no third-party integration. Checklist, not quota.

## Flow-advisor skill chaining

Skill tool may expose domain experts for backbone flows. Use matches within the per-run cap.

### Discovery protocol

At Step 2.5:

1. **Re-read the available skills list** (host session-startup system messages; same list the orchestrator sees)
2. **Map backbone activities to candidate skill names** by keywords:
   - "sign in / sign up / SSO / OAuth / login" → `auth*`, `*identity*`, `*login*`, `*sso*`
   - "pay / refund / charge / invoice / billing / subscription" → `payment*`, `*billing*`, `*stripe*`, `*finance*`
   - "onboard / first-run / setup wizard" → `onboarding*`, `first-run*`
   - "search / find / filter / list" → `search*`, `*query*`
   - "notify / email / push / alert" → `notification*`, `email*`, `*messaging*`
   - "audit / compliance / log" → `audit*`, `compliance*`, `governance*`
   - "accessibility / a11y" theme → `accessibility*`, `a11y*`
   - "i18n / localization" theme → `i18n*`, `*localization*`, `*translation*`
   - "multi-tenancy" theme → `multitenant*`, `*tenant*`, `*saas*`
3. **Dedupe and rank by impact** — slice 1 = high, slice 2 = medium, later = skip. Stay within Step 2.5 advisor cap; see [SKILL.md → Rules that govern every run](../SKILL.md#rules-that-govern-every-run) Rule 5.
4. **Skip sister-framework slash-commands** — gstack `/plan-design-review`, Superpowers `brainstorming`, etc. are inbound user commands, not outbound advisors. (See [framework-integration.md](framework-integration.md).)

### Invocation pattern

Call `Skill` with tight question:

```
Skill: auth-flow-advisor
Args: |
  Context: Multi-tenant B2B SaaS refunds. Personas: Tenant Admin, End User, Compliance Officer.
  Backbone activity: "Sign in" — Auth0 SSO, sub-account claim, screen-reader Compliance users.
  Stories in slice 1:
    - S001: As a Tenant Admin, I want SSO setup so reps avoid per-user provisioning.
    - S002: As an End User, I want work-account sign-in so I don't manage another password.
    - S003: As a Compliance Officer, I want role claims checked every sign-in so audit access can't be silently revoked.

  Question: What should architect / UX bake into slice 1 for this auth flow?
```

Put advisor answer verbatim under "Flow advice from external skills"; usually UX and architect reference it.

Tag `[skill: <name> @ <date>]` in `design.md` for traceability.

### When the advisor says "I don't know" or asks for more context

If advisor asks questions:

1. **Pass through to the user** — Step 0.4 gaps
2. **Fold into open questions** — under "Open UX questions" or "Open architecture questions" in `role-hints.md`

Do not loop. One round/advisor; no actionable round 1 means human expertise, not more chaining.

### When no advisor skill exists for a flow

Document gap in `role-hints.md`:

```markdown
### Flows that would benefit from domain expertise (no advisor skill installed)

- Auth flow (Activity 1) — SSO + multi-tenant claim mapping. No installed advisor skill; architect should spend ~2 hours on OWASP ASVS L2 + Auth0's multi-tenant guide before slice 1.
- Payment flow (Activity 3) — Stripe refund integration. No installed advisor skill; pair architect with Stripe webhook experience at this scale.
```

Names outside expertise without pretending skill supplied it.

## Refining `role-hints.md` on a non-empty baseline (iteration)

On existing storymap:

1. **Read prior `role-hints.md`** if present — authoritative for persona snapshots/constraints not re-derived
2. **Diff new backbone vs. old** — added activities create flow rows + boundary candidates; removed activities are archived, not silently deleted
3. **Re-invoke advisor skills** only for *new* flows or changed advice (e.g., Stripe published a major API change). Don't re-invoke just because time passed.
4. **Append to decisions log** in `design.md` for resolved UX/architecture questions — append-only, never overwrite. Rule: [persistent-knowledge.md](persistent-knowledge.md).

## Anti-patterns

- **Don't author UX or architecture work here.** `role-hints.md` is a head-start; designers/architects own deliverables.
- **Don't fabricate persona snapshots.** If `design.md` lacks verbatim/interview source, write `[inferred]` and open-question it. Don't invent advice.
- **Don't invoke advisor skills "just in case".** Usually 1-2, never above Step 2.5 cap. Invoke only known-pattern surfaces (auth, payment, search, accessibility); calls cost turns/maintenance.
- **Don't let advisor output override user-stated decisions.** If user said "we don't need refund webhooks in slice 1" and advisor says "you absolutely need refund webhooks", user wins. Surface future-slice risk, not slice-1 override; see [SKILL.md → Rules that govern every run](../SKILL.md#rules-that-govern-every-run).
- **Don't generate `role-hints.md` after slice-1 ACs are written.** Step 2.5 informs commitments; delayed hints document decisions.
- **Don't duplicate `design.md` content.** Reference personas/activities by name; `design.md` is source of truth. Copy-paste creates maintenance debt.

## Cost ceiling

Step 2.5 should consume 10-15% of turn budget; most work restructures mined content. Skill-chaining adds 1-3 small-subagent-cost invocations.

If Step 2.5 exceeds 20%, you're authoring. Stop; document gaps as open questions.

## Where this fits in the framework integrations

- **Superpowers** — `brainstorming` clarifies intent; `role-hints.md` routes it to designer/architect work before `writing-plans` decomposes slice 1.
- **gstack** — `/plan-design-review` reviews UX coherence + persona narratives; `/plan-eng-review` reviews architect feasibility. Both are inbound; this skill supplies input.
- **GSD** — `role-hints.md` lives beside GSD Brief and informs Milestone planning. Reference in `.gsd/Brief.md` after import; never write `.gsd/`.

Per-framework handoff cues and GSD slice/Milestone collision live in [framework-integration.md](framework-integration.md). Step 6 handoff names `role-hints.md` if produced:

> "Slice 1 (12 stories) → .gsd/Roadmap.md + TODO.md. Designer should read role-hints.md§UX before slice-1 mocks; architect should read role-hints.md§Architect before slice-1 contracts. Run /gsd discuss next."
