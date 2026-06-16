# Breach Decisions — F-SCIM proposal vs PI 1 mid-flight state

> **Step D.3 + D.4 output (the refinement's breach analysis).** Every breach below is a decision the user must make.
> Single-shot defaults are recommended **but conditional** — every commitment depends on the user accepting (or overriding) the default.

---

## Snapshot summary (carry from `design.md`)

- **6 weeks elapsed**, 6 weeks remaining in a 12-week PI
- 4 engineers + 1 PM + 0.5 SRE → ~50 SP capacity remaining
- 13 SP shipped; ~27 SP partially burned in flight; ~70 SP of committed work still to do
- **Existing PI 1 is already ~20 SP underwater** before F-SCIM is even considered
- Sales-committed F-SCIM is +18 to +26 SP on top
- SOC 2 audit window opens in 5 weeks; SCIM deadline is 5 weeks; both racing for the same final stretch

---

## BREACH 1 — Capacity overrun (already exists; SCIM makes it severe)

**Magnitude:**
- Without F-SCIM: ~70 SP work / ~50 SP capacity = **~20 SP over** (already breached, pre-existing)
- With F-SCIM minimum bundle (18 SP): ~88 SP / ~50 SP = **~38 SP over**
- With F-SCIM full bundle (26 SP): ~96 SP / ~50 SP = **~46 SP over**

**Note on the pre-existing breach:** The team was likely going to miss some PI 1 commitments even without SCIM. Mid-PI replanning is normal at week 6; this snapshot just makes the gap legible. Don't blame SCIM for all 46 SP — own that the original plan already required cuts.

**Trade-off options:**

| # | Option | Effect on PI 1 | Risk |
|---|---|---|---|
| **A** | Cut S015 (8 SP) + S006 (13 SP) + S007 (8 SP) + S012 (8 SP) = 37 SP cut; ship F-SCIM minimum (18 SP) | Land 50 SP remaining work + 18 SP SCIM = ~68 SP into ~50 cap → **still ~18 SP over** | Acceptable only if H2 capacity was underestimated OR S005/S008 don't actually need their full SP |
| **B** | Cut S006+S007+S015 (29 SP); ship F-SCIM minimum (18 SP); defer S005 second half to PI 2 | Lands ~50 SP work into ~50 cap; KR-2.1 partial — auto-approve <$100 ships, over-$100 path slips | KR-2.1 reduced scope; communicate to Marcus + CS leadership |
| **C** | Extend PI 1 by 2 weeks (adds ~17 SP capacity); cut only S015 (8 SP); ship F-SCIM full (26 SP) | Same release date slips 2 weeks; SOC 2 window still met if extension lands before audit | Release-date change — needs leadership approval; **2-week extension chews into the 5-week audit window** |
| **D** | Add a 5th engineer for the final 5 weeks (adds ~10 SP); cut S015 + S012 (16 SP); ship F-SCIM minimum (18 SP) | Lands ~52 SP into ~60 cap; KR-1.1 search-UI slips but audit-gate items hold | Requires hiring or borrowing an engineer in 1 week; onboarding cost real |
| **E** | Push F-SCIM-04 to PI 2 (saves 8 SP); cut S015 + S012 + S006 (29 SP); ship F-SCIM-01/02/03 | Lands ~50 SP; KR-2.1 over-$100 path slips; KR-1.1 search slips | Most balanced — accepts known pain in two KRs but neither dies |

**Default recommendation: Option E.**
Cuts the lowest-WSJF items (S015), the audit-gate-non-blocker (S012), and the most-expensive-lowest-WSJF refund story (S006). Lands SCIM at the minimum customer-defensible bundle. Both at-risk KRs (KR-1.1, KR-2.1) take a controlled, communicable hit; nothing dies silently.

---

## BREACH 2 — New backbone activity ("Provision tenant users") with conditional slice-1 coverage

**The breach:** F-SCIM introduces a 9th backbone activity that did not exist in the prior PI plan. The refinement rule: any new backbone activity needs slice-1 coverage that demos end-to-end.

**Coverage check:**
- F-SCIM-01 (endpoint scaffold) + F-SCIM-02 (create/update users) together give **end-to-end "IT admin creates a user via SCIM"** — that satisfies the rule.
- F-SCIM-03 (deprovision) closes the lifecycle.
- F-SCIM-04 (group-to-role) is polish — deferable.

**Trade-off options:**

| # | Option | Effect | Risk |
|---|---|---|---|
| **A** | Land F-SCIM-01 + 02 + 03 in PI 1 (slice-1 coverage = full lifecycle) | Activity is fully introduced; SOC 2 offboarding bonus from F-SCIM-03 | 18 SP capacity hit (see Breach 1) |
| **B** | Land only F-SCIM-01 in PI 1 (endpoint surface only); push 02/03/04 to PI 2 | Defers the actual customer value; Sales deal at risk because admin can't create users | $400K ARR deal lost or contract amended |
| **C** | Defer the entire new activity to PI 2; tell Sales the deal commit needs renegotiation | Cleanest PI 1; KR-1.2 SCIM stays orphan; deal at risk | Highest political cost; loses the deal or requires contract amendment |

**Default recommendation: Option A.**
The minimum customer-defensible bundle preserves the deal. Combined with Breach 1 Option E (defer F-SCIM-04), this is the lightest configuration that ships SCIM.

---

## BREACH 3 — SOC 2 audit window vs SCIM deadline (both 5 weeks)

**The collision:** Two hard-deadline efforts compete for the final 5 weeks of PI 1. SOC 2 fails the audit if KR-1.1 audit-gate items (S011 + S013 + S014) aren't done. Sales loses the deal if F-SCIM-01/02/03 aren't done.

**Items required for SOC 2 audit gate** (must be done by week 11):
- S011 Emit audit events (3 SP) — in-progress
- S013 Retention policy (5 SP) — not started
- S014 CSV export (5 SP) — not started
- **Sub-total: 13 SP, must land before audit**

**Items wanted for KR-1.1 but NOT audit-gate** (can slip past audit):
- S012 Search UI (8 SP) — useful for auditor turnaround but auditor can use raw export
- S015 Pattern detection (8 SP) — fraud detection, not SOC 2 control

**Items required for $400K deal** (must demo before EOQ):
- F-SCIM-01 (5 SP) + F-SCIM-02 (8 SP) + F-SCIM-03 (5 SP) = 18 SP minimum

**Combined audit + SCIM minimum: 13 + 18 = 31 SP** out of the 50 remaining.
**Plus committed in-progress completions** (S003, S004, S005 finish, S008 finish): ~15 SP.
**Sub-total of "must-land": ~46 SP** — fits within 50 SP capacity.

**Trade-off options:**

| # | Option | Effect | Risk |
|---|---|---|---|
| **A** | Lock the must-land 46 SP; everything else deferred or cut | Both deadlines met; cuts ~24 SP of remaining commitments | KR-2.1 over-$100 path (S006+S007+S009+S010) and S012+S015 all slip |
| **B** | Stagger: SOC 2 work front-loaded weeks 7-9 (13 SP); SCIM weeks 7-11 in parallel (18 SP) | Engineers split between tracks; coordination overhead | Context-switching cost ~15% effective capacity loss → may push back into Breach 1 |
| **C** | Run audit-gate-only on SOC 2 (S011 + S013 + S014); push S015 to PI 2 explicitly; everything else status quo | Same as A but framed as "S015 explicit defer" | Same as A |

**Default recommendation: Option C (which is essentially Option A reframed honestly).**
S015 is the lowest-WSJF item in PI 1 and is not an audit gate. Defer with sponsor.

---

## BREACH 4 — F-SCIM had no story decomposition

**The breach:** Sales' commit was for "~25 SP across 3-4 stories." No actual stories existed. Proposed decomposition is in the prompt response and the storymap.

**Proposed stories** (sized via comparable past work):

| ID | Story | SP | Confidence | Notes |
|---|---|---|---|---|
| F-SCIM-01 | SCIM 2.0 endpoint scaffold + auth | 5 | High | Library exists; scaffold is well-trodden |
| F-SCIM-02 | Create + update users via SCIM | 8 | Medium | Touches user table, role table, SCIM mapping |
| F-SCIM-03 | SCIM DELETE / disable | 5 | High | Mirrors create; uses same plumbing |
| F-SCIM-04 | Group → role mapping (Okta) | 8 | **Low** | IdP-specific gotchas; test against one IdP |

**Total: 26 SP** (vs Sales' ~25 SP estimate — close enough).

**Trade-off options:**

| # | Option | Effect | Risk |
|---|---|---|---|
| **A** | Accept the 4-story decomposition; let F-SCIM-04 be the slip candidate | Sales gets minimum-viable SCIM by EOQ | F-SCIM-04 confidence is "Low" — could blow up to 13 SP |
| **B** | Spike F-SCIM-04 in week 7 to confirm size (1 SP spike); commit after | Better confidence on what we're signing up for | Spike eats 1 SP from the 50; defensible |
| **C** | Tell Sales the commit needs to be 3 stories (skip F-SCIM-04 for now) | Cleaner scope; deal may need contract amendment ("group-mapping in next release") | Deal terms negotiation |

**Default recommendation: Option B (spike F-SCIM-04 in week 7).**
Cheap, sharpens the estimate, and the spike output informs whether F-SCIM-04 lands in PI 1 (Option A) or PI 2 (Option C).

---

## BREACH 5 — Decisions-log consistency check (No AI auto-approve)

**The check:** Does the Sales commit on F-SCIM contradict the 2026-04-12 decision "No AI auto-approve on refunds"?

**Verdict: NO conflict.** F-SCIM is identity provisioning (SCIM 2.0 user create/update/delete + group mapping). It has nothing to do with refund approval policy, auto-approve thresholds, or AI/ML on refunds. The decision stands.

**Action:** Documented here for audit trail. No revision needed.

---

## BREACH 6 — KR-2.1 displacement risk (org all-hands commit)

**The breach:** KR-2.1 (CS time 22→5 min) was committed to the org at the all-hands. The Option E default cuts S006 + S007 (over-$100 refund flow) — both are KR-2.1.

**Impact:** KR-2.1 still ships the auto-approve-under-$100 path (S005), the search paths (S002 shipped, S003), the review path (S004), the notify path (S008, S009), and retry (S010 — if kept). The **over-$100 path slips to PI 2**.

**Practical impact on KR-2.1 metric:**
- If ~60% of CS tickets are under $100, the metric still moves significantly (Marcus' rough number — verify with him).
- If most tickets are over $100, KR-2.1 movement is small and the org commit is at risk.

**Trade-off options:**

| # | Option | Effect | Risk |
|---|---|---|---|
| **A** | Accept S006/S007 slip; re-baseline KR-2.1 with sponsor (Marcus) explicitly — "we'll hit X min instead of 5 min this PI; over-$100 path lands PI 2" | Honest reframe; preserves SCIM deal and SOC 2 | Marcus may push back hard |
| **B** | Keep S006+S007 in PI 1; push F-SCIM-04 + F-SCIM-03 to PI 2 (loses SOC 2 offboarding bonus); lose the $400K deal or amend contract | KR-2.1 ships in full; deal at risk | Deal loss > KR-2.1 PR cost in most calculus, but business judgement |
| **C** | Keep S006+S007; do F-SCIM-01+02 only (deal demoable but not GA); negotiate deal phasing | Both partially met | Sales reaction unknown |

**Default recommendation: Option A — re-baseline KR-2.1 explicitly with Marcus.**
The "under $100" path is the higher-volume case in most refund-portal data. Re-baselining is honest; silently slipping is the actual breach to avoid.

---

## Combined default recommendation

```
PI 1 final 6 weeks lands:
  - In-flight completion: S003, S004, S005, S008, S011 (~15 SP remaining work)
  - SOC 2 audit gate: S013 + S014 (10 SP) + S011 finish
  - SCIM minimum bundle: F-SCIM-01 + F-SCIM-02 + F-SCIM-03 (18 SP)
  - Spike: F-SCIM-04 sizing (1 SP)
  - Cheap completion: S009 (3 SP, Slack ping approver)
  Total: ~47 SP — fits in ~50 SP capacity with thin margin

PI 1 explicit DEFERS (to PI 2 or beyond):
  - S006 Refund-over-limit (13 SP)            — KR-2.1 partial; re-baseline with Marcus
  - S007 Approver dashboard (8 SP)            — KR-2.1 partial; pairs with S006
  - S010 Failed-refund retry (5 SP)           — operational hygiene; non-critical
  - S012 Audit log search UI (8 SP)           — KR-1.1 non-gate; auditor uses CSV
  - S015 Refund pattern detection (8 SP)      — KR-1.1 non-gate; lowest WSJF
  - F-SCIM-04 Group → role mapping (8 SP)     — conditional on spike result + deal terms

Net OKR impact:
  - KR-1.1 SOC 2 — audit-gate items ship; S012 + S015 deferred to PI 2 ✓ (audit-safe)
  - KR-1.2 SAML+SCIM by EOQ — meets the deal commit at minimum bundle ✓
  - KR-2.1 CS 22→5 min — under-$100 path ships; over-$100 path slips; re-baseline required ⚠
```

**EVERY ITEM IN THE DEFAULT REQUIRES USER CONFIRMATION BEFORE COMMIT.**

The user should choose:
- Accept Option E (defer over-$100 refund path; re-baseline KR-2.1)?
- Or Option C with extension (slip the release date 2 weeks; eats SOC 2 buffer)?
- Or Option D with 5th engineer (requires staffing)?
- Or some hybrid?

---

## Recommended escalations (regardless of which option is picked)

1. **Sales ↔ Product alignment** — Sales sold SCIM without the team committing. Mid-flight insertion of a $400K deal commit is not sustainable; close the loop on how Sales commitments get sized before close.
2. **KR-2.1 re-baseline with Marcus** — even if the team picks an option that keeps S006/S007, the existing PI 1 ~20 SP shortfall (before SCIM) means something was always going to slip.
3. **SOC 2 audit logistics** — confirm the audit window is firm and what the auditor actually needs (raw export vs search UI vs retention proof).
4. **5th engineer feasibility** — fast-check whether Option D is even possible before ruling it out.

