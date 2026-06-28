# Slicing strategies

Cut the story map into horizontal, release-sized slices. Slice 1 must be demoable end-to-end; labels are secondary. Choose Patton, SAFe PI, or Now/Next/Later contextually. Rule 2: [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run); this file covers mechanics/violations.

## When to use

At Step 3, after backbone and per-persona stories exist, group into ordered releases. Also use for "PI planning", "roadmap", "MVP", "walking skeleton", or "what ships first". If a tracker is defined, use its fix-versions/releases (see [Slicing onto an existing tracker](#slicing-onto-an-existing-tracker)).

## The slice-1 rule — mechanics, why, and violations

**Slice 1 must include at least one story from every active backbone activity, and at least one story for every persona named in `design.md`.** (Rule statement and the never-silently-drop consequence: [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run).)

**End-to-end coverage is the point.** Slice 1 must let a user traverse the whole backbone, even minimally. That thin path is the *walking skeleton* and first E2E test contract: each activity is a swimlane; slice 1 proves the journey connects. If it covers Activities 1, 2, 3 but skips 4 and 5, the user cannot complete a journey, integration risk stays hidden, and the demo is incoherent.

**Persona coverage keeps it walkable for everyone.** Covering every activity for only one persona excludes secondary users. Every persona in `design.md` needs a slice-1 story. Zero candidates means re-slice (Step 3) or re-derive (Step 1), not omit.

**Violations almost always trace to one of these:**

| Symptom | Root cause | Fix |
|---|---|---|
| An activity has no plausible slice-1 story | System module disguised as activity (e.g. "Auth service", "Reporting engine") | Refactor the backbone — see [`backbone-criteria.md`](backbone-criteria.md) |
| "We'll add that step later" | Deferring an activity hides integration risk | Resist — a thin slice-1 story is cheaper than a late integration surprise |
| An activity genuinely has nothing worth shipping first | It isn't really part of the backbone | Move it out of the backbone; if it's not user-facing it's cross-cutting (below) |
| A persona has zero slice-1 stories | Stories were generated for the primary persona only | Re-run Step 2/Step 1 for that persona, then re-slice |

If re-slicing cannot satisfy the rule, fix upstream backbone or story generation; the slice is not the problem.

## Strategy 1 — Patton classic (Walking Skeleton → MVP → R2 → R3)

Jeff Patton's original framing. Use for greenfield end-to-end validation.

| Slice | Purpose | Story count guidance |
|---|---|---|
| **Walking Skeleton** | Prove architecture end-to-end with the thinnest set: hardcoded, no errors, single happy path. | 1 story per activity |
| **MVP** | First real-user slice; main happy path + reasonable errors. | 2–4 per activity |
| **Release 2** | Differentiation — competitive or delight features. | Whatever fits |
| **Release 3+** | Long-tail polish, edge cases, secondary personas. | Open-ended |

Walking Skeleton catches integration early. Don't skip it for feeling embarrassingly small — smallness is the feature.

## Strategy 2 — SAFe Program Increments (PI 1 / PI 2 / PI 3)

Use for ARTs (Agile Release Trains) doing PI planning. A PI is typically 8–12 weeks across 4–6 sprints.

| Slice | Typical scope |
|---|---|
| **PI 1** | Walking-skeleton-equivalent + the highest-WSJF features. Targets a demoable end-to-end flow at the PI System Demo. |
| **PI 2** | Differentiation features + dependencies that PI 1 surfaced |
| **PI 3+** | Roadmap items beyond commitment horizon, treated as forecast |

Differences from Patton:

- PI slices are time-boxed; fit work to time.
- Each PI slice has a PI Objective sentence per team — record it in `design.md`.
- Cross-team dependencies surface during PI planning; flag them in `storymap.md` with `[dep: <team>]`.
- Innovation & Planning at PI end is not part of slicing — leave it out.

## Strategy 3 — Now / Next / Later

Roman Pichler / Janna Bastow style. Use when commitment is risky and flexibility matters.

| Slice | Meaning |
|---|---|
| **Now** | Actively in progress or starting this sprint. High confidence. |
| **Next** | Validated as worth doing, will start within 1–2 sprints. Medium confidence. |
| **Later** | Recognized as needed eventually. Low confidence, may be re-prioritized. |
| **(Not on roadmap)** | Explicit non-goals. Record so they don't keep getting raised. |

*Later* is a real bucket, not polite "no". When Later moves to Now, ask what trades down. **Now** must cover every backbone activity and persona, or it isn't a walking skeleton.

## How to choose

| Context signal | Choose |
|---|---|
| Greenfield, single team, validating an idea | Patton |
| Existing ART, PI cadence in place, multi-team | SAFe PI |
| Discovery phase, exec asking "roadmap?", priorities will shift | Now/Next/Later |
| Reorganizing a chaotic backlog that has no slicing yet | Patton (start fresh) |
| User says "PI planning" anywhere in their request | SAFe PI |

When unsure, ask. Don't pick silently.

## Slicing onto an existing tracker

When a tracker is defined (test in [`output-routing.md`](output-routing.md#detecting-the-empty-baseline-no-tracker-defined)), don't mint slice labels. Reuse its fix-versions, releases, or sprints; read taxonomy in read-only. Full rules: [`work-item-tracking.md`](work-item-tracking.md#align-to-the-existing-tracker-taxonomy). The earliest fix-version still covers every backbone activity and persona.

## Slice naming in the artifacts

Use one label set; don't mix "MVP" and "PI 1". The label appears in `storymap.csv` `slice`, a `storymap.md` section header, and required `[slice:<id>]` story tag. With an issue tracker, it maps to **sprint/iteration** (burn-down time axis) — see [work-item-tracking.md § Enable the tracker burn-down](work-item-tracking.md#enable-the-tracker-burn-down).

## Cross-cutting work is not a slice and not a backbone activity

Cross-cutting work — tech debt, infrastructure, localization, theming, observability, compliance — is not a user activity, so it gets no slice and no 6th backbone column. Placement (`## Non-backbone / cross-cutting` + `### Theme:`, the "As a `<user>`…" test, exclusion from slice-1 coverage) is owned by [`backbone-criteria.md`](backbone-criteria.md#cross-cutting--non-backbone-work--the-full-rule). Slice coverage applies only to backbone activities.

## Anti-patterns — things that look like slices but aren't

- **Themes** ("performance", "accessibility", "tech debt") — cross slices; use `## Non-backbone / cross-cutting`, not slice labels.
- **Personas** ("admin features", "end-user features") — one slice can include multiple personas; never split by persona, and slice 1 contains *every* persona.
- **Tech layers** ("backend", "frontend") — opposite of horizontal slicing; all-backend ships nothing walkable.
- **SDLC phases** ("design", "build", "test") — stages *within* a slice, not slices.
- **Deferring a whole activity to slice 2** — common slice-1 violation. Thin the story; don't drop the activity.
