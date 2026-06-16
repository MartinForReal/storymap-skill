# Slicing strategies

Cut the story map into horizontal, release-sized slices so the first slice is demoable end-to-end — that single property is what makes the mechanics here matter more than which naming scheme you pick. Three strategies follow (Patton, SAFe PI, Now/Next/Later); choose by context, not preference. The governing statement of the slice-1 rule lives in [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run) (Rule 2); this file owns the how, the why, and the violation patterns.

## When to use

Reach for this at Step 3, after the backbone exists and per-persona stories are generated, when you need to group stories into ordered releases. Also use it when a request says "PI planning", "roadmap", "MVP", "walking skeleton", or "what ships first" — those phrases name a slicing strategy. If a tracker is defined, you slice onto its existing fix-versions/releases rather than inventing labels (see [Slicing onto an existing tracker](#slicing-onto-an-existing-tracker)).

## The slice-1 rule — mechanics, why, and violations

**Slice 1 must include at least one story from every active backbone activity, and at least one story for every persona named in `design.md`.** (Rule statement and the never-silently-drop consequence: [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run).)

**Why end-to-end coverage is the whole point.** This is what separates a story map from "just a backlog with sections." A user must be able to traverse the entire backbone after slice 1 ships, even if every step is minimal — that traversable thin path is the *walking skeleton*. It is also the team's first end-to-end test contract: each backbone activity is an E2E swimlane, and slice 1 is the set of scenarios that prove the whole journey connects. If slice 1 covers Activities 1, 2, 3 but skips 4 and 5, you don't have a walking skeleton — you have a forearm. The user can't complete a single real journey, integration problems stay hidden, and there's nothing coherent to demo.

**Why the persona half of the rule.** A slice that covers every activity but only one persona ships a skeleton no secondary user can walk. Every persona in `design.md` needs at least one slice-1 story so the demo is real for each of them; a persona with zero slice-1 candidates is a signal to re-slice (Step 3) or re-derive its stories (Step 1), never to quietly leave it out.

**Violations almost always trace to one of these:**

| Symptom | Root cause | Fix |
|---|---|---|
| An activity has no plausible slice-1 story | It's a system module in disguise (e.g. "Auth service", "Reporting engine"), not a user activity | Refactor the backbone — see [`backbone-criteria.md`](backbone-criteria.md) |
| "We'll add that step later" | A premature optimization instinct; deferring an activity hides the integration risk it carries | Resist — a thin slice-1 story is cheaper than a late integration surprise |
| An activity genuinely has nothing worth shipping first | It isn't really part of the backbone | Move it out of the backbone; if it's not user-facing it's cross-cutting (below) |
| A persona has zero slice-1 stories | Stories were generated for the primary persona only | Re-run Step 2/Step 1 for that persona, then re-slice |

When you can't satisfy the rule by re-slicing, the problem is upstream (backbone or story generation), not in the slice. Go fix it there.

## Strategy 1 — Patton classic (Walking Skeleton → MVP → R2 → R3)

Jeff Patton's original framing. Use for greenfield work where end-to-end validation is the priority.

| Slice | Purpose | Story count guidance |
|---|---|---|
| **Walking Skeleton** | Prove the architecture works end-to-end with the thinnest possible feature set. Often hardcoded values, no error handling, single happy path. | 1 story per activity |
| **MVP** | First slice you'd put in front of real users. Handles the main happy path with reasonable error states. | 2–4 per activity |
| **Release 2** | Differentiation — features that beat the competition or delight users. | Whatever fits |
| **Release 3+** | Long-tail polish, edge cases, secondary personas. | Open-ended |

Walking Skeleton is the slice that catches integration problems early. Don't skip it just because it feels embarrassingly small — that smallness is the feature.

## Strategy 2 — SAFe Program Increments (PI 1 / PI 2 / PI 3)

For ARTs (Agile Release Trains) doing PI planning. A PI is typically 8–12 weeks across 4–6 sprints.

| Slice | Typical scope |
|---|---|
| **PI 1** | Walking-skeleton-equivalent + the highest-WSJF features. Targets a demoable end-to-end flow at the PI System Demo. |
| **PI 2** | Differentiation features + dependencies that PI 1 surfaced |
| **PI 3+** | Roadmap items beyond commitment horizon, treated as forecast |

Differences from Patton:

- PI slices are time-boxed; you fit work to time, not vice versa.
- Each PI slice has a PI Objective sentence per team — record it in `design.md`.
- Cross-team dependencies surface during PI planning; flag them in `storymap.md` with `[dep: <team>]`.
- The Innovation & Planning iteration at the end of each PI is not part of slicing — leave it out.

## Strategy 3 — Now / Next / Later

Roman Pichler / Janna Bastow style. Discovery-friendly. Best when commitment is risky and you want flexibility.

| Slice | Meaning |
|---|---|
| **Now** | Actively in progress or starting this sprint. High confidence. |
| **Next** | Validated as worth doing, will start within 1–2 sprints. Medium confidence. |
| **Later** | Recognized as needed eventually. Low confidence, may be re-prioritized. |
| **(Not on roadmap)** | Explicit non-goals. Record so they don't keep getting raised. |

The honesty of Now/Next/Later is that *Later* is a real bucket — not a polite "no". When stakeholders push to move things from Later to Now, the question is what trades down to Later in exchange. Even here the slice-1 rule holds: **Now** must still cover every backbone activity and every persona, or it isn't a walking skeleton.

## How to choose

| Context signal | Choose |
|---|---|
| Greenfield, single team, validating an idea | Patton |
| Existing ART, PI cadence in place, multi-team | SAFe PI |
| Discovery phase, exec asking "roadmap?", priorities will shift | Now/Next/Later |
| Reorganizing a chaotic backlog that has no slicing yet | Patton (start fresh) |
| User says "PI planning" anywhere in their request | SAFe PI |

When unsure, ask the user. Don't pick silently.

## Slicing onto an existing tracker

When a tracker is defined (the operational test lives in [`output-routing.md`](output-routing.md#detecting-the-empty-baseline-no-tracker-defined)), don't mint fresh slice labels — slice onto the tracker's existing fix-versions, releases, or sprints so the map maps cleanly onto what the team already plans against. Read the taxonomy in read-only and reuse it; full rules for aligning to an existing tracker are in [`work-item-tracking.md`](work-item-tracking.md#align-to-the-existing-tracker-taxonomy). The slice-1 coverage rule is unchanged: the earliest fix-version still has to cover every backbone activity and every persona.

## Slice naming in the artifacts

Use the chosen strategy's labels consistently. Don't mix "MVP" and "PI 1" in the same map. The label appears as the `slice` column in `storymap.csv` and as a section header in `storymap.md`, and it's carried on each story bullet as a required `[slice:<id>]` tag. When an issue tracker is the system of record, the slice also maps to the tracker's **sprint/iteration** (the burn-down's time axis) — see [work-item-tracking.md § Enable the tracker burn-down](work-item-tracking.md#enable-the-tracker-burn-down).

## Cross-cutting work is not a slice and not a backbone activity

Cross-cutting work — tech debt, infrastructure, localization, theming, observability, compliance — doesn't fit a user activity, so it gets neither a slice of its own nor a 6th backbone column. Where it *does* go (the `## Non-backbone / cross-cutting` + `### Theme:` encoding, the "As a `<user>`…" test, and its exclusion from slice-1 coverage) is owned by [`backbone-criteria.md`](backbone-criteria.md#cross-cutting--non-backbone-work--the-full-rule); the slice-coverage rule above applies to backbone activities only.

## Anti-patterns — things that look like slices but aren't

- **Themes** ("performance", "accessibility", "tech debt") — these cut across slices, they don't replace them. They belong in the `## Non-backbone / cross-cutting` section, not as slice labels.
- **Personas** ("admin features", "end-user features") — multiple personas appear in one slice; never split a slice by persona (and per the slice-1 rule, slice 1 must contain *every* persona).
- **Tech layers** ("backend", "frontend") — the opposite of horizontal slicing. A slice that's all-backend ships nothing a user can walk.
- **SDLC phases** ("design", "build", "test") — those are stages *within* a slice, not slices themselves.
- **Deferring a whole activity to slice 2** — that's the most common slice-1 violation; it breaks end-to-end traversal. Thin the story, don't drop the activity.
