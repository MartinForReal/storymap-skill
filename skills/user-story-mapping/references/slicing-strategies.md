# Slicing strategies

How to cut the story map into release-sized horizontal slices. Three options. Pick by context, not preference.

## The unbreakable rule

**The first slice must include at least one story from every backbone activity.**

This is what separates story mapping from "just a backlog with sections". A user must be able to traverse the entire backbone end-to-end after slice 1 ships, even if every step is minimal. If your first slice covers Activities 1, 2, 3 but not 4 and 5, you don't have a walking skeleton — you have a forearm.

Violations almost always come from one of:
- A backbone activity that's actually a system module in disguise (refactor it)
- A "we'll add that later" instinct kicking in (resist; thin slices reveal integration problems early)
- An activity that's genuinely optional (then it's not part of the backbone — move it)

## Strategy 1 — Patton classic (Walking Skeleton → MVP → R2 → R3)

Jeff Patton's original framing. Use for greenfield work where end-to-end validation is the priority.

| Slice | Purpose | Story count guidance |
|---|---|---|
| **Walking Skeleton** | Prove the architecture works end-to-end with the thinnest possible feature set. Often hardcoded values, no error handling, single happy path. | 1 story per activity |
| **MVP** | First slice you'd put in front of real users. Handles the main happy path with reasonable error states. | 2–4 per activity |
| **Release 2** | Differentiation — features that beat the competition or delight users. | Whatever fits |
| **Release 3+** | Long-tail polish, edge cases, secondary personas. | Open-ended |

Walking Skeleton is the slice that catches integration problems early. Don't skip it just because it feels embarrassingly small.

## Strategy 2 — SAFe Program Increments (PI 1 / PI 2 / PI 3)

For ARTs (Agile Release Trains) doing PI planning. A PI is typically 8–12 weeks across 4–6 sprints.

| Slice | Typical scope |
|---|---|
| **PI 1** | Walking-skeleton-equivalent + the highest-WSJF features. Targets a demoable end-to-end flow at the PI System Demo. |
| **PI 2** | Differentiation features + dependencies that PI 1 surfaced |
| **PI 3+** | Roadmap items beyond commitment horizon, treated as forecast |

Differences from Patton:
- PI slices are time-boxed; you fit work to time, not vice versa
- Each PI slice has a PI Objective sentence per team — record it in `design.md`
- Cross-team dependencies surface during PI planning; flag them in `storymap.md` with `[dep: <team>]`
- The Innovation & Planning iteration at the end of each PI is not part of slicing — leave it out

## Strategy 3 — Now / Next / Later

Roman Pichler / Janna Bastow style. Discovery-friendly. Best when commitment is risky and you want flexibility.

| Slice | Meaning |
|---|---|
| **Now** | Actively in progress or starting this sprint. High confidence. |
| **Next** | Validated as worth doing, will start within 1–2 sprints. Medium confidence. |
| **Later** | Recognized as needed eventually. Low confidence, may be re-prioritized. |
| **(Not on roadmap)** | Explicit non-goals. Record so they don't keep getting raised. |

The honesty of Now/Next/Later is that *Later* is a real bucket — not a polite "no". When stakeholders push to move things from Later to Now, the question is what trades down to Later in exchange.

## How to choose

| Context signal | Choose |
|---|---|
| Greenfield, single team, validating an idea | Patton |
| Existing ART, PI cadence in place, multi-team | SAFe PI |
| Discovery phase, exec asking "roadmap?", priorities will shift | Now/Next/Later |
| Reorganizing a chaotic backlog that has no slicing yet | Patton (start fresh) |
| User says "PI planning" anywhere in their request | SAFe PI |

When unsure, ask the user. Don't pick silently.

## Slice naming in the artifacts

Use the chosen strategy's labels consistently. Don't mix "MVP" and "PI 1" in the same map. The label appears as a column in `storymap.csv` and as a section header in `storymap.md`.

## Things that look like slices but aren't

- **Themes** ("performance", "accessibility", "tech debt") — these cut across slices, they don't replace them
- **Personas** ("admin features", "end-user features") — same; multiple personas appear in one slice
- **Tech layers** ("backend", "frontend") — the opposite of horizontal slicing; don't do it
- **Phases** ("design", "build", "test") — those are SDLC stages within a slice, not slices themselves

## Cross-cutting items vs. backbone activities

A common mistake: when a backlog contains items that don't fit a user activity (dark mode, localization, tech-debt refactors, infrastructure migrations, audit/compliance work), the temptation is to add a 6th column to the backbone called "Cross-cutting" or "Tech debt" or "Localization".

Don't. Adding a non-user column to the backbone breaks the narrative-flow property *and* breaks the "first slice covers every activity" rule (you can't write a user-facing slice-1 story for "tech debt").

Put cross-cutting work in a **separate section below the backbone** in `storymap.md`:

```markdown
## Activity: Find a property
...
## Activity: Make an offer
...

## Non-backbone / cross-cutting

### Theme: Tech debt
- [slice:pi-2] Migrate to OpenSearch
- [slice:pi-3] Retire legacy DB schema

### Theme: Localization
- [slice:pi-3] French (Quebec) translations
```

These still get prioritized in `backlog.csv` — record them with `activity = "Non-backbone: <theme>"` so they sort separately but aren't lost. The slice-coverage rule applies to backbone activities only.
