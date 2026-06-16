# Handoff — refinement run for Refund Portal PI 1 + F-SCIM proposal

**As of:** 2026-06-08 (PI 1 week 6 of 12)
**Run:** Refinement (the loop re-run against an existing, mid-flight PI plan)
**Status:** Provisional plan applied with default trade-offs. **Every commitment is conditional on user confirmation.**

## Bottom line

F-SCIM can fit at the minimum 18-SP bundle, but only by cutting ~29 SP of existing PI-1 commitments and re-baselining KR-2.1 with Marcus; even without SCIM, PI 1 is already ~20 SP underwater for the final 6 weeks. Six breaches were detected — each with 2–4 trade-off options in `breach-decisions.md`. Nothing is committed until you confirm.

---

## ⚠ READ FIRST — what changed and what gives

You asked: does $400K F-SCIM fit, and what gives?

**Short answer: it can fit at the minimum bundle (18 SP), but only by cutting ~29 SP of existing PI 1 commitments AND re-baselining KR-2.1 with Marcus.** Even without SCIM, PI 1 is already ~20 SP underwater for the final 6 weeks — that's the more uncomfortable surfacing this snapshot produced.

**Six breaches detected.** All are in `breach-decisions.md` with 2-4 trade-off options each.

| # | Breach | Default resolution | Conditional on |
|---|---|---|---|
| 1 | Capacity overrun (existing + SCIM = ~46 SP over) | Option E: cut S006+S007+S012+S015 (+ defer F-SCIM-04 to PI 2) | Capacity is truly ~50 SP; can't expand |
| 2 | New backbone activity "Provision tenant users" | Option A: ship F-SCIM-01+02+03 in PI 1 for full lifecycle slice-1 coverage | Deal commit holds |
| 3 | SOC 2 audit window vs SCIM deadline (both 5 weeks) | Option C: lock audit-gate items (S011+S013+S014); push S015 to PI 2 explicitly | Auditor accepts CSV export without search UI |
| 4 | F-SCIM had no story decomposition | Option B: spike F-SCIM-04 in week 7 to confirm sizing | Spike result determines F-SCIM-04 placement |
| 5 | Decisions-log "No AI auto-approve" check | NO conflict — F-SCIM is identity, not refund-approval logic | (Verified; no action) |
| 6 | KR-2.1 displacement (org all-hands commit) | Option A: re-baseline with Marcus — under-$100 ships; over-$100 slips to PI 2 | Marcus accepts re-baseline |

---

## Changes from prior snapshot (Step D.5 diff — the refinement's diff)

### ADDED
+ **New backbone activity: "Provision tenant users"** (Breach 2 — slice-1 coverage via F-SCIM-01+02)
+ **F-SCIM-01** "SCIM 2.0 endpoint scaffold + auth" — 5 SP, KR-1.2 — PI 1
+ **F-SCIM-02** "Create + update users via SCIM" — 8 SP, KR-1.2 — PI 1
+ **F-SCIM-03** "SCIM DELETE / disable" — 5 SP, KR-1.2 + KR-1.1 bonus — PI 1
+ **F-SCIM-04** "Group → role mapping" — 8 SP, KR-1.2 — **deferred or PI 2, gated on spike**
+ **Spike: F-SCIM-04 sizing** — 1 SP, week 7
+ Slice-1 ACs for F-SCIM-01 through F-SCIM-04 (`slice-1-acceptance-criteria.md`)

### MOVED (deferred to PI 2 or beyond — provisional, per default trade-offs)
~ S006 "Refund over $100 → queue" (13 SP, KR-2.1) — Breach 1 Option E + Breach 6 Option A
~ S007 "Approver dashboard" (8 SP, KR-2.1) — paired with S006
~ S010 "Failed-refund retry queue" (5 SP, KR-2.1) — operational hygiene, non-critical for the 22→5 min metric (kept in PI 1 per default; bumpable if needed)
~ S012 "Audit log search UI" (8 SP, KR-1.1) — Breach 3 Option C; auditor uses CSV export
~ S015 "Refund pattern detection" (8 SP, KR-1.1) — Breach 3 Option C; lowest WSJF in PI 1; not SOC 2 gate

### CUT
(none — every deferral is to PI 2, not killed)

### UNCHANGED
- Shipped: S001 (SSO), S002 (Find by ID)
- In progress: S003 (Find by email), S004 (View details), S005 (Submit refund <$100), S008 (Email customer), S011 (Emit audit events)
- Backbone activities 1-8 (Sign in / Find / Review / Submit / Approve / Notify / Audit / Detect anomalies)
- Decisions log: "No AI auto-approve on refunds" — verified, no conflict with F-SCIM (Breach 5)

### BREACHED LIMITS — DEFAULT RESOLUTIONS APPLIED (CONDITIONAL)
- **Breach 1 capacity:** Option E — defer S006+S007+S012+S015 + F-SCIM-04 → ~47 SP fits ~50 SP cap with thin margin
- **Breach 2 new activity:** Option A — F-SCIM-01+02+03 provide full create/update/delete lifecycle slice-1 coverage
- **Breach 3 SOC 2 vs SCIM:** Option C — S015 explicitly deferred; audit-gate items (S011+S013+S014) prioritized
- **Breach 4 decomposition:** Option B — 4-story decomposition proposed; F-SCIM-04 gated on 1 SP spike in week 7
- **Breach 5 decision conflict:** No conflict — auto-approve decision stands
- **Breach 6 KR-2.1:** Option A — re-baseline with Marcus; under-$100 ships, over-$100 slips

### OPEN AFTER CHANGE (need user input)
- **Does Sales' "before EOQ" mean GA, beta, or demoable in a sales call?** — sizes F-SCIM-04 in/out
- **Is the 50 SP capacity firm?** — opens/closes Options C (extension) and D (5th engineer)
- **Will Marcus accept KR-2.1 re-baseline?** — determines whether Option E holds or we need a different cut
- **Does the SOC 2 auditor accept CSV export without search UI?** — determines whether S012 can defer
- **Was the original PI 1 commit (96 SP into ~100 cap) realistic, or was it always going to slip?** — this snapshot shows ~20 SP shortfall even before SCIM; worth a retrospective conversation

---

## Snapshot (Step D.1) — for the record

### Slice composition (after default resolution)

| Slice | Stories | Backbone activities covered | Capacity used | Capacity remaining |
|---|---|---|---|---|
| PI 1 (final 6 weeks) | ~10 to land + 5 to finish in-flight | 8/9 (Provision tenant users newly added with slice-1 coverage; Detect anomalies deferred) | ~47 SP / ~50 cap remaining | ~3 SP thin margin |
| PI 2 (planned) | S006, S007, S012, S015, F-SCIM-04 (conditional) | All 9 carry forward | TBD | TBD |

### OKR coverage (after change)

| KR | Stories | Status |
|---|---|---|
| **KR-1.1** SOC 2 | S011 (in-flight) + S013 + S014 in PI 1; S012 + S015 deferred to PI 2 | Audit-gate items hold; auditor likely accepts |
| **KR-1.2** SAML + SCIM by EOQ | S001 shipped; F-SCIM-01+02+03 in PI 1 (minimum bundle) | Deal commit met at minimum scope |
| **KR-2.1** CS 22→5 min | S002 shipped; S003+S004+S005+S008 in flight; S009+S010 in PI 1; S006+S007 deferred PI 2 | **Re-baseline required** — under-$100 path lands, over-$100 slips |

### Open dependencies

- F-SCIM-01 → S001 (SSO shipped) ✓ feasible
- F-SCIM-02 → F-SCIM-01 (same slice) ✓ feasible
- F-SCIM-03 → F-SCIM-02 (same slice) ✓ feasible
- F-SCIM-04 → F-SCIM-02 (same slice if PI 1, OK if PI 2) ✓ feasible either way
- S011 (Emit audit) → S005 + S006 — note S006 is being deferred — does S011 need S006 specifically? **Likely soft, not hard** — verify with team; if hard, S011 may not be fully demoable without the over-$100 path
- S013 (Retention) → S011 ✓ same slice
- S014 (Export) → S011 ✓ same slice

### Known limits (carry from snapshot)

- Team: 4 engineers × ~2 SP/eng/week × 12 weeks + 0.5 SRE ≈ ~100 SP per PI
- Q3 SOC 2 audit window opens **2026-07-13** (5 weeks from snapshot) — KR-1.1 audit-gate items must complete by then
- Sales-committed F-SCIM deadline EOQ ≈ **2026-09-30** (16 weeks out, but practically the demo must be in the deal cycle ~5 weeks)
- "No AI auto-approve" decision (2026-04-12) — verified not violated by F-SCIM

---

## Smallest next decision

**Confirm Option E (or pick a different option from Breach 1).** Everything else cascades from this choice.

If Option E: proceed with the default plan above. Next operational steps:
1. Marcus 1:1 — re-baseline KR-2.1 (Breach 6)
2. SOC 2 auditor email — confirm CSV export is sufficient (Breach 3)
3. Sales loop-back — confirm "before EOQ" interpretation for F-SCIM-04 scoping (Breach 4)
4. Week 7: F-SCIM-04 spike + start F-SCIM-01 + finish in-flight S003/S004

If not Option E:
- Option C (extension) → engage leadership on release-date change
- Option D (5th engineer) → engage staffing/hiring within 1 week
- Or a hybrid — re-run Breach 1 trade-off with the desired constraints

---

## Files in this handoff

A tracker is the system of record here (your PI 1 tracker), so the skill does **not** emit the local data files — the ranked plan and its burn-down live in the tracker. Produced:

- `design.md` — personas, OKRs, decisions log, backbone identification, F-SCIM decomposition rationale
- `storymap.md` — the canonical map with the new "Provision tenant users" backbone activity + F-SCIM-01..04 stories
- `storymap.csv` — the flat items+status manifest (a deterministic projection of `storymap.md`, always produced as a checked-in snapshot regardless of where the dynamic plan lives)
- **`breach-decisions.md`** — full breach analysis with 2-4 trade-off options per breach
- `slice-1-acceptance-criteria.md` — Given/When/Then for the new F-SCIM stories only (existing PI 1 ACs assumed in your tracker)
- `tracker-status-update.sh` — **opt-in** write-back: creates F-SCIM-01..04 in the tracker with story-points + sprint and applies the approved cuts, setting the **burn-down fields** (points + sprint + status) so the tracker's native burn-down reflects the refined plan. Review before running.
- `handoff.md` — this file

> **No local `storymap.mmd` / `backlog.{md,csv}`** — a tracker is the system of record, so the ranked plan and the burn-down go into the tracker via `tracker-status-update.sh` rather than into local files. `design.md` + `storymap.md` + `storymap.csv` (the items+status manifest) are always produced.

---

## Process notes (for posterity)

- This refinement run did **not** re-derive the prior backbone (carried activities 1-8 forward from your PI 1 snapshot, added activity 9 for SCIM).
- Your existing tracker IDs (S001-S015) are preserved by the write-back; F-SCIM-* are created new in the tracker.
- No local `backlog.csv` / `backlog.md` / `storymap.mmd` is emitted — the tracker is the system of record, so the ranked plan and its burn-down fields (points + sprint + status) go into the tracker via `tracker-status-update.sh` (opt-in). `storymap.csv` is still produced as a checked-in items+status manifest.
- The ~20 SP pre-existing PI 1 shortfall (before SCIM) was uncovered by the snapshot math; it was not in your prompt. If this is news, the original PI 1 commit was likely over-subscribed at planning time — worth a separate retro conversation.
