# Prioritization frameworks

Pick exactly one method and use it for the whole backlog: **WSJF** when the org runs SAFe / multi-team PI planning, **RICE** when you have reach-and-impact metrics, **MoSCoW** when data is thin and you need to triage fast. Mixing methods within one ranking is meaningless — the numbers stop being comparable. Whatever you choose, the `reasoning` column matters more than the score.

## When to use

Reach for this reference at Step 4 (slice + prioritize), once the backbone and per-persona stories exist and you need to order them. The default picker:

- **SAFe / multi-team / PI-driven** → WSJF
- **Product team with a metrics dashboard** → RICE
- **Discovery / new product / no data** → MoSCoW
- **Mixed signals** → MoSCoW first (cheap), then upgrade to WSJF or RICE next iteration once data exists

Ask the user which method they want; fall back to the rules above only if they have no preference. Two related concerns live in their own files: when an item's rank is constrained by what must ship before it, see [dependency-tracking.md](dependency-tracking.md) for feasibility ordering; when you want the score to reflect strategic alignment rather than raw effort math, link the item to an objective via [okr-alignment.md](okr-alignment.md).

**Where the scores land:** with no issue tracker, the method's columns go in `backlog.csv`; when an issue tracker is the system of record the **sizing** feeds the tracker's story-points/estimate field (the burn-down's work axis) instead of `backlog.csv` — see [work-item-tracking.md § Enable the tracker burn-down](work-item-tracking.md#enable-the-tracker-burn-down).

## WSJF — Weighted Shortest Job First

The SAFe default. Economic framing: deliver the highest-value-per-unit-of-effort work first.

**Formula:** `WSJF = Cost of Delay / Job Size`

**Cost of Delay** = User-Business Value + Time Criticality + Risk Reduction / Opportunity Enablement

Each component scored on a modified Fibonacci scale: **1, 2, 3, 5, 8, 13, 20**. Score *relative to other items in the same backlog* — absolute values don't matter, ratios do.

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

Compare against:
- Story: "Dark mode toggle"
- Value = 2, Time = 1, Risk/Opp = 1, Size = 2
- WSJF = (2 + 1 + 1) / 2 = **2.0**

OAuth wins. Note: dark mode has a positive WSJF — it's not bad work, it's just lower-leverage right now.

## RICE — Reach × Impact × Confidence / Effort

Product-team standard. Best when you have data on user reach and can estimate impact.

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

The number itself doesn't mean much. The *ranking* across the backlog is what matters.

When to be skeptical: if everyone's confidence is 100% across a 30-item backlog, the team is lying to itself. Push for 80% as the realistic default.

## MoSCoW — Must / Should / Could / Won't

Categorical, not numeric. Best when data is thin and you need to triage fast.

| Bucket | Meaning | Typical share |
|---|---|---|
| **Must** | Slice fails without it. Non-negotiable for the release. | ~60% of effort, max |
| **Should** | High value, painful to skip, but slice still works without it | ~20% |
| **Could** | Desirable, included if capacity allows | ~20% |
| **Won't (this slice)** | Explicitly out of scope. Document so it's not re-litigated. | — |

The "Won't" column is the one teams skip and shouldn't. Recording what's *out* prevents the same conversation in week 4.

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

For all methods, include columns:
`id, activity, task, story, persona, outcome, slice, method, score, reasoning`

Method-specific columns:
- WSJF: `wsjf_value, wsjf_time, wsjf_risk, wsjf_size`
- RICE: `rice_reach, rice_impact, rice_confidence, rice_effort`
- MoSCoW: `moscow` (one of: must, should, could, wont)

The `reasoning` column is the most important. A score with no reasoning is unauditable in 3 months. Force one sentence per row even if it's "comparable to similar [other-story]".

## Anti-patterns

- **Mixing methods in one ranking.** A WSJF of 3.25 and a RICE of 3200 are not comparable. Pick one per invocation and stick to it for the whole backlog.
- **Scoring on an absolute scale.** WSJF and RICE only mean anything relative to the rest of *this* backlog. Re-anchor when items are added.
- **Confidence inflation.** A backlog where every RICE item is 100% confident is self-deception; 80% is the honest default.
- **Skipping the "Won't" column.** Recording what's explicitly out of scope is the cheapest way to stop re-litigating it later.
- **A score with no reasoning.** Unauditable in three months. Every row gets one sentence, even if it's just "comparable to [other-story]".
