# Prioritization frameworks

Pick one method across the backlog: **WSJF** for SAFe / multi-team PI planning, **RICE** with reach-and-impact metrics, **MoSCoW** for thin-data triage. Mixed methods make scores non-comparable. `reasoning` matters more than score.

## When to use

Use at Step 4 (slice + prioritize), once backbone and per-persona stories need ordering. Default picker:

- **SAFe / multi-team / PI-driven** → WSJF
- **Product team with a metrics dashboard** → RICE
- **Discovery / new product / no data** → MoSCoW
- **Mixed signals** → MoSCoW first (cheap), then upgrade to WSJF or RICE next iteration once data exists

Ask first; use the rules above only without a preference. Related files: [dependency-tracking.md](dependency-tracking.md) for prerequisite-constrained rank; [okr-alignment.md](okr-alignment.md) for objective-linked scores.

**Where the scores land:** without an issue tracker, method columns go in `backlog.csv`. With a tracker system of record, **sizing** feeds story-points/estimate (burn-down work axis) instead of `backlog.csv` — see [work-item-tracking.md § Enable the tracker burn-down](work-item-tracking.md#enable-the-tracker-burn-down).

## WSJF — Weighted Shortest Job First

SAFe default: highest value per effort first.

**Formula:** `WSJF = Cost of Delay / Job Size`

**Cost of Delay** = User-Business Value + Time Criticality + Risk Reduction / Opportunity Enablement

Score components on modified Fibonacci: **1, 2, 3, 5, 8, 13, 20**. Score *relative to other items in the same backlog*; ratios matter, absolutes don't.

| Component | What it measures | High score (13–20) | Low score (1–2) |
|---|---|---|---|
| **User-Business Value** | Revenue, retention, satisfaction impact | Drives a major OKR | Marginal nice-to-have |
| **Time Criticality** | Does value decay if delayed? | Regulatory deadline, competitive window | Useful any time |
| **Risk Reduction / Opp Enablement** | Reduces uncertainty, unlocks future work | Removes a blocker for 5 other stories | Self-contained |
| **Job Size** | Relative effort | Multi-team, multi-PI | A few days |

**Worked example:**
- Story: "OAuth login for enterprise SSO"
- Value = 13 (unblocks enterprise tier sales)
- Time = 8 (two prospects asked this quarter)
- Risk/Opp = 5 (also unblocks SCIM provisioning later)
- Size = 8 (one team, one PI)
- WSJF = (13 + 8 + 5) / 8 = **3.25**

Against:
- Story: "Dark mode toggle"
- Value = 2, Time = 1, Risk/Opp = 1, Size = 2
- WSJF = (2 + 1 + 1) / 2 = **2.0**

OAuth wins; dark mode is positive but lower-leverage now.

## RICE — Reach × Impact × Confidence / Effort

Product-team standard for user-reach data and impact estimates.

**Formula:** `RICE = (Reach × Impact × Confidence) / Effort`

| Field | Unit | Typical range |
|---|---|---|
| **Reach** | Users / customers / events affected per quarter | 50 – 100,000+ |
| **Impact** | How much it moves the metric per affected user | 0.25 (minor) / 0.5 (low) / 1 (med) / 2 (high) / 3 (massive) |
| **Confidence** | How sure are we? | 50% / 80% / 100% — penalize wishful thinking |
| **Effort** | Person-months | 0.5 – 6+ |

**Worked example:**
- Story: "Inline error messages on the signup form"
- Reach = 8000 signups/quarter
- Impact = 0.5 (cuts ~10% drop-off, modest user-by-user effect)
- Confidence = 80% (A/B from a similar form last year)
- Effort = 1 person-month
- RICE = (8000 × 0.5 × 0.80) / 1 = **3200**

Rank matters more than the raw number.

If confidence is 100% across a 30-item backlog, push for 80% as the realistic default.

## MoSCoW — Must / Should / Could / Won't

Categorical triage for thin data.

| Bucket | Meaning | Typical share |
|---|---|---|
| **Must** | Slice fails without it. Non-negotiable for the release. | ~60% of effort, max |
| **Should** | High value, painful to skip, but slice still works without it | ~20% |
| **Could** | Desirable, included if capacity allows | ~20% |
| **Won't (this slice)** | Explicitly out of scope. Document so it's not re-litigated. | — |

Don't skip "Won't"; recording what's *out* prevents the same conversation in week 4.

**Worked example for Slice 1 (MVP) of a property-search app:**

| Story | Bucket | Reasoning |
|---|---|---|
| Browse listings by city | Must | Without this, no product |
| Filter by price | Must | Default user expectation |
| Save favorites | Should | Drives return visits, but Slice 2 OK |
| Map view of results | Could | Differentiator, but list view is sufficient |
| AI-suggested similar listings | Won't (Slice 1) | Validate basic flow first |
| Crypto payment | Won't (ever, probably) | Out of scope until evidence demands it |

## What to record in `backlog.csv`

For all methods, include:
`id, activity, task, story, persona, outcome, slice, method, score, reasoning`

Method-specific columns:
- WSJF: `wsjf_value, wsjf_time, wsjf_risk, wsjf_size`
- RICE: `rice_reach, rice_impact, rice_confidence, rice_effort`
- MoSCoW: `moscow` (one of: must, should, could, wont)

`reasoning` is mandatory. A score without it is unauditable in 3 months. One sentence per row, even "comparable to similar [other-story]".

## Anti-patterns

- **Mixing methods in one ranking.** A WSJF of 3.25 and a RICE of 3200 are not comparable. Pick one per backlog.
- **Scoring on an absolute scale.** WSJF/RICE are relative to *this* backlog. Re-anchor when items are added.
- **Confidence inflation.** If every RICE item is 100% confident, the team is fooling itself; 80% is the honest default.
- **Skipping the "Won't" column.** Recording out-of-scope work cheaply stops re-litigation.
- **A score with no reasoning.** Unauditable in three months. Every row gets one sentence, even "comparable to [other-story]".
