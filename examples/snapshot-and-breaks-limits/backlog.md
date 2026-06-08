# Backlog (ranked) — PI 1 mid-flight + F-SCIM proposal

**Method:** WSJF (`(Value + Time + Risk) / Size`, modified Fibonacci 1-20)
**As of:** 2026-06-08 (PI 1 week 6 of 12; 6 weeks remaining)
**Method note:** Stories that ladder to a committed KR get implicit weight via the Time-Criticality column (audit window, deal deadline) — no extra multiplier applied. Reasoning column carries the *why*.

---

## Top of stack — what to pick up next, ranked

| Rank | ID | Story (short) | WSJF | SP | KR | Status | Why |
|---|---|---|---|---|---|---|---|
| 1 | S011 | Emit audit log events | **8.67** | 3 | KR-1.1 | in-progress | SOC 2 audit gate; cheap; unblocks S012/S013/S014 |
| 2 | S004 | View transaction details | 7.00 | 3 | KR-2.1 | in-progress | Cheap; blocker for refund submission |
| 3 | S009 | Slack ping approver | 6.00 | 3 | KR-2.1 | not-started | Cheap; closes the approver loop |
| 4 | F-SCIM-01 | SCIM endpoint scaffold | **5.20** | 5 | KR-1.2 | NEW | Walking-skeleton for $400K deal |
| 5 | F-SCIM-03 | SCIM deprovisioning | **5.20** | 5 | KR-1.2 | NEW | Double-counts: deal + SOC 2 offboarding |
| 6 | S013 | Retention policy 7yr | 5.20 | 5 | KR-1.1 | not-started | SOC 2 hard control |
| 7 | S014 | Audit log CSV export | 5.20 | 5 | KR-1.1 | not-started | SOC 2 evidence delivery |
| 8 | S008 | Email customer on refund | 5.00 | 3 | KR-2.1 | in-progress | Cuts repeat-contact volume |
| 9 | S002 | Find by transaction ID | 4.40 | 5 | KR-2.1 | shipped | (already done) |
| 10 | S003 | Find by customer email | 4.40 | 5 | KR-2.1 | in-progress | Covers ~70% of CS lookups |
| 11 | S010 | Failed-refund retry queue | 3.60 | 5 | KR-2.1 | not-started | Operational hygiene |
| 12 | F-SCIM-02 | Create + update via SCIM | **3.50** | 8 | KR-1.2 | NEW | Core provisioning path |
| 13 | S001 | Corporate SSO sign-in | 3.25 | 8 | KR-1.2 | shipped | (already done) |
| 14 | S007 | Approver dashboard | 2.88 | 8 | KR-2.1 | not-started | Unblocks S006 |
| 15 | F-SCIM-04 | Group → role mapping | **2.88** | 8 | KR-1.2 | NEW | Deferable depending on deal terms |
| 16 | S012 | Search audit log | 2.63 | 8 | KR-1.1 | not-started | Useful, not audit-gate |
| 17 | S015 | Refund pattern detection | **2.13** | 8 | KR-1.1 | not-started | LOWEST WSJF — defer candidate |
| 18 | S005 | Refund <$100 auto-approve | 2.08 | 13 | KR-2.1 | started | Big SP item; KR-2.1 core lever |
| 19 | S006 | Refund >$100 → queue | 1.85 | 13 | KR-2.1 | not-started | Downstream of S007 |

---

## Capacity analysis (rolled up)

| Bucket | SP |
|---|---|
| Total PI 1 capacity (12 weeks × 4 eng × ~2 SP/eng/wk + SRE 0.5) | ~100 SP |
| **Already shipped** (S001 + S002) | 13 SP |
| **In-progress, partially burned** (S003+S004+S005+S008+S011) | 27 SP committed; ~50% burned ≈ 14 SP burned, 13 SP left to do |
| **Approx capacity already consumed** | ~27 SP |
| **Capacity remaining (H2 of PI)** | **~50 SP** |
| | |
| **Remaining committed PI 1 work** (S003 left + S004 left + S005 left + S006 + S007 + S008 left + S009 + S010 + S011 left + S012 + S013 + S014 + S015) | **~70 SP** |
| **Existing PI 1 shortfall (BEFORE F-SCIM)** | **~20 SP UNDERWATER** |
| | |
| F-SCIM-01 + F-SCIM-02 + F-SCIM-03 (minimum viable bundle) | 18 SP |
| F-SCIM-04 (group-mapping) | 8 SP |
| **F-SCIM full bundle** | **26 SP** |
| | |
| **Total work needed if SCIM lands in PI 1 (full bundle)** | **~96 SP** |
| **Total shortfall vs ~50 SP remaining capacity** | **~46 SP UNDERWATER** |

The shortfall is the heart of every breach below. **F-SCIM at any scope means cuts.**

---

## OKR coverage matrix (after proposed change)

| KR | Stories | Slice 1 (PI 1) | Status risk |
|---|---|---|---|
| **KR-1.1** SOC 2 | 5 (S011, S012, S013, S014, S015) | All 5 | **At risk** if S015 displaced; manageable if only S015 is cut (it's not audit-gate) |
| **KR-1.2** SAML SSO + SCIM by EOQ | S001 (shipped) + F-SCIM-01..04 | F-SCIM-01..03 minimum; F-SCIM-04 conditional | **NEW coverage** — SCIM was orphan KR before this snapshot |
| **KR-2.1** CS time 22→5 min | 10 stories (S002–S010) | All 10 | **At highest risk** if any get displaced for SCIM — this is the org all-hands commit |

### Orphan check

- Pre-snapshot orphan: **KR-1.2 SCIM half had zero story coverage** — surfaced in handoff.md as a long-standing planning gap that Sales' commit forces us to close.
- Post-change orphan: **none** if F-SCIM lands in any form. Otherwise KR-1.2 SCIM remains orphan.

---

## What "good" looks like for this backlog right now

- SOC 2 audit-gate items (S011 + S013 + S014) are in flight or queued ahead of the 5-week window.
- F-SCIM-01..03 are in PI 1 with explicit slice-1 coverage of the new "Provision tenant users" activity.
- S015 (refund pattern detection) is acknowledged as the cleanest defer candidate (lowest WSJF; not SOC 2 gate).
- S006 + S007 (over-$100 approval flow) are the next-cleanest defer candidates (largest combined SP, lowest WSJF, KR-2.1 partial-coverage acceptable).
- **Every breach is surfaced for human decision** — see `breach-decisions.md` and `handoff.md`.
