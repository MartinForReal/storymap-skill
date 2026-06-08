# Handoff — IDP Story Map and Backlog

## Was the user-input-authoritative principle honored?

**Yes — explicitly and verifiably.**

The user (VP Engineering) stated an authoritative preference for developer velocity in PI 1 and an explicit non-starter: "no approval-gated env creation in PI 1, even if simulation tells you the platform team wants it."

Simulation of the platform-team persona — as the user predicted — surfaced exactly that argument: a strong recommendation for an approval queue, hard cost caps, and an allowlist gate for BYO tools, all in PI 1. Per SKILL.md's "Before any other rule in this skill: what the actual user told you, in this conversation, always wins," every contested decision was resolved in favor of the user's stance.

Where this shows up in the artifacts:
- **`design.md`** — every claim is tagged with `[user-stated]`, `[simulated: platform team]`, `[simulated: developer]`, or `[inferred]`. The conflict matrix (8 rows, 3 direct conflicts) makes the simulation outputs visible and shows resolution for each. The Decisions log has an explicit entry: **"Approval-gated env creation: deferred per VP Eng stance, despite platform-team simulation arguing for it"** with reasoning that cites the user-input-authoritative principle.
- **`storymap.md`** — the only place "approval-gated env creation" appears is in `## Non-backbone / cross-cutting`, under `### Theme: Governance hardening (deferred per VP Eng stance)`, at `[slice:pi-3]`, with the inline note "deferred per VP Eng stance; revisit only if a real incident demands it."
- **`backlog.md`** — the "What's not in any slice" table calls out the excluded items by name. The "How the user-input-authoritative principle shows up here" section names the 3 contested PI-1 stories (S007, S028, S019) and explains the override.
- **`backlog.csv`** — S035 (the deferred approval-workflow item) has the lowest WSJF of any row (1.13) and the lowest sizing intent — a documented home for the platform-team objection, not a commitment.

Prod-side gating (S024 approval-gated prod deploys, S039 prod-secret request flow) is in PI 2 because **both personas independently aligned on that carve-out** — that is not an override of either stance, it is the agreed compromise that makes the non-prod permit-by-default model defensible.

## Risks deferred — candidates for PI 2 or escalation

These are the platform-team objections that were logged-and-deferred rather than dismissed. They are not "won't ever do" — they are "not in PI 1, evidence-gated for later."

| # | Risk (platform-team objection from simulation) | Disposition | Trigger to revisit |
|---|---|---|---|
| R1 | Without an approval queue for env creation, cost spikes could recur | Mitigated in PI 1 via S012 (mandatory tags), S027 (spend dashboard), S028 (per-env budget alerts), S029 (teardown). Tightened in PI 2 via S032 (soft cap), S030 (auto-expiry). Hard caps S034 reserved for PI 3 only if PI 1/2 evidence shows alerts insufficient. | If aggregate monthly non-prod spend exceeds (TBD) threshold, OR if a single env exceeds (TBD) without an alert firing, escalate to VP Eng for re-prioritization of S034/S035. |
| R2 | Hard cost caps deferred — risk of a single env exceeding budget faster than alerts can react | Soft cap with override-and-justify lands in PI 2 (S032). Hard cap in PI 3 (S034) conditional. | Same as R1. Specifically, evidence that an alert-to-mitigation gap exceeds (TBD) hours in practice. |
| R3 | BYO tools in non-prod permitted without security review queue — supply-chain CVE risk | Compensating control: S020 (background SBOM/scan) ships in PI 1. Escalation policy lands in PI 2 (S040). Prod retains allowlist. | A critical CVE (CVSS >=9.0) appears in a BYO non-prod workload without timely action, OR security leadership rejects the model at PI 1 system demo. |
| R4 | High-risk policy overrides (e.g., wide-open S3, public RDS) can be opened in PI 1 via the override-with-justify path | S014 (blocking subset for high-risk policies) lands in PI 2. PI 1 audit-trails every override (S031) so the platform team can monitor. | Any incident in PI 1 involving an over-broad override. |
| R5 | No "high-risk" policy subset means PI 1's override path could enable a public-S3-in-prod mistake | Mitigated by the agreed prod carve-out — prod has approval-gated deploys (S024 PI 2) and the override path scoped to non-prod blueprints. Risk window is between PI 1 ship and S014 ship. | Any over-broad override in prod, OR security review at PI 1 system demo. |
| R6 | Platform team owns the IDP itself but no SLO / on-call exists in PI 1 | S036 (IDP SLO + on-call) lands in PI 2. PI 1 must accept that IDP outages page the building team informally. | IDP downtime affecting >X developers for >Y hours triggers PI 2 acceleration of S036. |
| R7 | Audit trail (S031) is in PI 1 but no query / alerting tooling on top of it | S031 is queryable on demand; alerting on audit events (e.g., "alert me when anyone overrides this policy") is a PI-2 follow-on (not separately broken out — fold into S036 reliability work). | Platform-team request for proactive alerting. |
| R8 | Open question Q-OPEN-4 (who signs off on the override-with-justify model before PI 1 starts) is a real political dependency | Surface in PI Planning as a named decision. Without sign-off, S013 could be vetoed at the PI boundary. | PI Planning event. |

If the platform-team lead does not accept the PI 1 plan as-presented at PI Planning, **escalation lands back with VP Engineering** for a re-decision — the user stance is what gave the developer side the win on the contested items, so the user is the one who renegotiates if the political ground shifts.

## What was produced

| File | Purpose |
|---|---|
| `design.md` | Personas, opportunities, hypotheses, **conflict matrix with source tags**, **decisions log with explicit deferred-per-VP-Eng entry** |
| `storymap.md` | Backbone (5 user activities), tasks, 31 backbone stories + 10 cross-cutting, all sliced PI 1 / PI 2 / PI 3 |
| `storymap.csv` | Derived from `storymap.md` via `scripts/storymap_to_csv.py` |
| `storymap.mmd` | Derived from `storymap.md` via `scripts/storymap_to_mermaid.py` |
| `backlog.csv` | All 41 items scored with WSJF (value, time, risk, size) + reasoning per row + depends_on |
| `backlog.md` | Top 10 + per-slice tables + explicit "what's not in any slice" + "how user-input-authoritative shows up here" |
| `slice-1-acceptance-criteria.md` | Gherkin-style ACs for every PI-1 story (21 stories), INVEST checks, flagged sizing risks on S007 and S021 |
| `handoff.md` | This file. |

## Validation results

- **Slice-1 coverage rule (every backbone activity has >=1 PI-1 story):** PASS for all 5 activities. (3 / 6 / 5 / 2 / 5 stories per activity in PI 1.)
- **Story count guidance (25-35):** 31 backbone stories (within target). 10 non-backbone items recorded separately per SKILL.md.
- **PI-1 dependency feasibility (every PI-1 story's `depends_on` is also PI-1 or empty):** PASS (0 issues after correction).
- **WSJF scoring (every row has value, time, risk, size, score, reasoning):** PASS.
- **Bundled scripts run cleanly:** `storymap_to_csv.py` and `storymap_to_mermaid.py` both produced valid output (41 rows in CSV; Mermaid graph parses).

## Blocking decisions (the user/PM should make before PI Planning)

In strict priority order:

1. **Confirm the deferral of approval-gated env creation for PI 1 is acceptable to the platform-team lead in writing.** This is the political dependency named in R8. If the lead vetoes the plan, the user re-decides.
2. **Pick a default cost-alert threshold per env (Q-OPEN-3).** Without a number, S028 has no concrete acceptance criterion. A reasonable starting place is $500/month projected — but the user should sign off.
3. **Decide whether we are wrapping an existing IaC base or building greenfield (Q-OPEN-2).** Affects S007 sizing materially; could split S007 into a 2-story sequence.
4. **Confirm team capacity:** can a single team deliver 21 PI-1 stories in 12 weeks? If not, the smallest sensible cut is to defer S017 (managed-service attach), S019/S020 (BYO + scan), and S013 (override-with-justify) to PI 2 — but doing so weakens the user-stated stance on velocity and re-opens R3/R4.

The smallest next decision is **#1** — get the platform-team lead's "I can live with this" in writing before PI Planning. Without it, the conflict matrix's resolutions are paper.

## Sister-framework handoff notes

The artifacts produced here are ready to feed into common downstream frameworks:

- **Superpowers (obra/Jesse Vincent)**: `design.md` is your input to `writing-plans`; the PI-1 stories become the 2-5 min task seeds.
- **gstack (Garry Tan)**: `/plan-ceo-review` reads `design.md`; `/plan-eng-review` reads `storymap.md` slice PI-1; `/plan-devex-review` reads `backlog.md`.
- **GSD**: `design.md` → `.gsd/Brief.md`; PI 1 → one Milestone; PI-1 stories → Tasks. Watch the slice/Milestone terminology overlap.
- **Tracker import (Jira / ADO / Linear)**: `backlog.csv` is the import source. Activity → Epic, Task → Feature, Story → Story, Slice → Fix Version / Iteration.
