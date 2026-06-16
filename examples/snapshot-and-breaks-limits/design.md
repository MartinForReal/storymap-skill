# Design Doc — Refund Portal — PI 1 mid-flight refinement

> **Outcome:** Determine whether SCIM 2.0 provisioning ($400K ARR deal commit) fits into the remaining 6 weeks of PI 1 without breaking SOC 2 audit readiness or the org-committed KR-2.1 (CS time-per-ticket cut).
> **Run:** Refinement of an existing map (the loop re-run against a mid-flight PI)
> **Snapshot taken:** 2026-06-08 (6 weeks into a 12-week PI; 6 weeks remaining)

## Bottom line

The $400K SCIM commit (~25 SP, 5-week deadline) does **not** cleanly fit the remaining 50 SP of PI 1 — and PI 1 was already ~20 SP underwater before SCIM entered. It can fit only at the minimum bundle, and only by cutting ~29 SP of existing work and re-baselining KR-2.1 with Marcus. Six breaches are surfaced with trade-off options; every resulting commitment is conditional on user confirmation.

---

## The question this work answers

Can we honor a Sales-driven SCIM commit (~25 SP, 5-week wall-clock deadline) inside the remaining 50 SP capacity of PI 1 without (a) missing the Q3 SOC 2 audit gate, (b) silently dropping KR-2.1 coverage we committed to the org, or (c) overrunning the team into burnout?

If yes — what gives.
If no — what's the cleanest cut, defer, or expansion to escalate.

---

## Personas

| Persona | Source | Notes |
|---|---|---|
| **Marcus** — CS Lead | [user-stated] (decisions log 2026-04-12) | Owns the "no AI auto-approve" call; KR-2.1 sponsor by inheritance |
| **CS agent** — primary refund operator | [inferred from KR-2.1 framing] | 22min→5min time-per-ticket is on their workflow |
| **Enterprise IT admin** — SCIM consumer | [user-stated: Sales deal] | New persona introduced by F-SCIM; manages tenant user provisioning |
| **SOC 2 auditor** — external, time-boxed | [user-stated: 5-week window] | Reads KR-1.1 audit log work in 5 weeks |
| **Eng team** — 4 engineers, 1 PM, 1 part-time SRE | [user-stated] | The only people who can move stories |

---

## OKR alignment (carried forward from prior PI plan)

### Committed OKRs

| KR | Description | Owner-committed at | Hard deadline |
|---|---|---|---|
| **KR-1.1** | SOC 2 audit log + retention + export | Prior PI commit | **Q3 SOC 2 audit window opens in 5 weeks** |
| **KR-1.2** | SAML SSO + SCIM available to all customers by end of Q3 | Prior PI commit; F-SCIM ladders here | End of Q3 (5 weeks) |
| **KR-2.1** | Cut CS time-per-refund-ticket from 22 min → 5 min | **Org all-hands commitment** | End of Q3 |

### Decisions log (carried forward; do not silently reverse)

| Date | Decision | Source |
|---|---|---|
| 2026-04-12 | **No AI auto-approve on refunds.** Marcus + CS leadership firm. | [user-stated decisions log] |
| PI planning (~8 weeks ago) | Auto-approve threshold = $100 (rule-based, not AI). See S005. | [user-stated PI 1 commit] |

### Decisions-log integrity check for F-SCIM (Breach #5 from prompt)

F-SCIM is **provisioning** (creating users + group membership via SCIM 2.0). It does not touch refund auto-approval. **No conflict with the "No AI auto-approve" decision.** Verified — documented for audit trail.

---

## Context sources mined

- [user-stated] PI 1 backlog: 15 stories, 96 SP, current status per story
- [user-stated] Capacity: ~100 SP / 12-week PI; ~50 SP remaining for H2
- [user-stated] Q3 SOC 2 audit window: 5 weeks out
- [user-stated] Sales commit: $400K ARR + 5-week deadline for SCIM
- [user-stated] Team shape: 4 eng + 1 PM + 0.5 SRE
- [user-stated] Decisions log entry on auto-approve
- [user-stated] The team's existing PI 1 tracker is the **system of record** — the PI 1 work and its acceptance criteria live there (carried forward, not re-derived)
- [inferred] Backbone activities — extracted from PI 1 story set (see storymap.md)

### Contradictions flagged

1. **Sales assumed SCIM was already in PI 1.** It is not. Sales' verbal commit and the team's PI plan are out of sync. Surface to leadership in handoff.md.
2. **KR-1.2 in OKRs says "SAML SSO + SCIM by end of Q3"** but PI 1 only contains SSO work (S001 shipped); SCIM was not decomposed. Either KR-1.2 was always going to slip OR SCIM was meant to come in PI 2. The Sales commit forces the decision now.

---

## Backbone (carried forward — DO NOT silently re-derive)

The PI 1 stories cluster into the following user activities. This is the backbone as of the current snapshot:

1. **Sign in** (KR-1.2 enablement)
2. **Find transaction** (KR-2.1 — CS agent locates the case)
3. **Review transaction** (KR-2.1 — agent reads details before action)
4. **Submit refund** (KR-2.1 — the actual action)
5. **Approve refund** (KR-2.1 — supervisor path)
6. **Notify stakeholders** (KR-2.1 — customer + approver loops)
7. **Audit / compliance** (KR-1.1 — SOC 2)
8. **Detect anomalies** (KR-1.1 — suspicious pattern alerting)

**F-SCIM adds a 9th backbone activity:** **Provision tenant users** (KR-1.2). This is a **new backbone activity** — it was not in prior backbone. Surfaced as Breach #2 in handoff.md.

---

## Non-goals (this PI)

- AI/ML refund auto-approval — explicitly out per decisions log
- Anything beyond rule-based auto-approve under $100
- Multi-tenant data partitioning beyond what SCIM directly requires
- Real-time refund anomaly response (S015 is detection + alert only)

---

## Open questions for the user (single-shot defaults applied; revisit when live)

These are flagged in handoff.md as "blocking decisions" the team must confirm:

1. **Capacity defense** — is the 50 SP/H2 capacity hard, or can it expand (5th eng, extended PI, weekend burn)?
2. **KR-2.1 displacement tolerance** — if KR-2.1 slips by ~2-3 weeks to fit SCIM, will the all-hands commit be re-baselined?
3. **SOC 2 work prioritization** — KR-1.1 stories (S008, S009, S013, S014, S015) total 29 SP — is the full set required, or can S015 (refund pattern detection, 8 SP) be deferred past the audit?
4. **F-SCIM decomposition** — proposed 4-story breakdown below; confirm before sequencing.
5. **Deal terms on SCIM** — does "before EOQ" mean GA, beta, or "demonstrable in a sales call"? Different scopes → different SP.

---

## Proposed F-SCIM decomposition (new — Breach #4 resolution)

Sales asked for ~25 SP across 3-4 stories. Proposed 4-story decomposition under new backbone activity **Provision tenant users**:

| ID | Story | SP | Persona | Notes |
|---|---|---|---|---|
| F-SCIM-01 | SCIM 2.0 endpoint scaffold (`/Users`, `/Groups` URLs, auth) | 5 | Enterprise IT admin | Backbone walking-skeleton; enables every other SCIM story |
| F-SCIM-02 | Create + update users via SCIM POST/PATCH | 8 | Enterprise IT admin | Core provisioning path |
| F-SCIM-03 | Deprovision / disable users via SCIM DELETE | 5 | Enterprise IT admin | Required for SOC 2 offboarding controls — also helps KR-1.1 |
| F-SCIM-04 | Group → role mapping (Okta/Azure AD test) | 8 | Enterprise IT admin | Required for "before EOQ" if customer is Okta — confirm in deal terms |
| | **Total** | **26 SP** | | Slightly over the ~25 SP estimate |

**Slice-1 coverage for new activity:** F-SCIM-01 + F-SCIM-02 give end-to-end "admin can create a user" — that satisfies the rule for the new backbone activity.

If "before EOQ" only requires "demonstrable in a sales call," F-SCIM-04 can defer → 18 SP. That's the smallest viable bundle.

---

## Anti-goals for this refinement pass

- Do **not** silently absorb F-SCIM by quietly slipping KR-2.1 stories.
- Do **not** re-derive the prior backbone — only add the new activity.
- Do **not** reverse the "no AI auto-approve" decision.
- Do **not** assume the team can add capacity without escalation.
