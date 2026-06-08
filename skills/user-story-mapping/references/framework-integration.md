# Integration with sibling skill frameworks and SAFe tooling

This skill is standalone. None of the tools below are required. When they *are* in play, follow these patterns to fit cleanly.

## gstack (garrytan/gstack)

[gstack](https://github.com/garrytan/gstack) — Garry Tan (Y Combinator) — is a Claude Code slash-command pack that organizes work into a Think → Plan → Build → Review → Test → Ship → Reflect sprint. It exposes 23+ commands like `/office-hours`, `/autoplan`, `/plan-ceo-review`, `/plan-eng-review`, `/design-review`, `/review`, `/qa`, `/ship`, `/retro`.

This skill is the natural artifact-producer for gstack's **Plan** phase:

```
gstack /office-hours          ──→ user-story-mapping (Mode A or B)
gstack /autoplan                  ↳ produces design.md + storymap.md + backlog.md
gstack /plan-ceo-review       ──→ reviews design.md (the "why")
gstack /plan-eng-review       ──→ reviews storymap.md slice-1 (the "what to build first")
gstack /plan-design-review    ──→ reviews user activities + persona narratives
gstack /plan-devex-review     ──→ reviews backlog ranking
                                ↓
gstack /ship, /canary, /qa, /retro work the resulting slices
```

Practical mapping for the with-this-skill workflow inside gstack:

| gstack command | What it reads from this skill |
|---|---|
| `/office-hours` (refine an idea) | Feed it `design.md` — the personas, opportunities, and hypotheses sections give it concrete framing |
| `/autoplan` (turn a goal into work) | Skip if you've already produced `storymap.md` — point it at the first slice instead |
| `/plan-ceo-review` | Reviews `design.md` for outcome clarity and the question being answered |
| `/plan-eng-review` | Reviews `storymap.md` slice 1 for engineering feasibility |
| `/plan-design-review` | Reviews persona narratives and activity backbone for UX coherence |
| `/plan-devex-review` | Reviews `backlog.md` for ranking sanity |
| `/ship`, `/canary` | Operate on built stories; this skill stops at the plan |
| `/retro`, `/learn` | Use `design.md` Hypotheses table as the "what did we believe" input to retro |

If gstack is active, after producing artifacts say: "Outputs are ready for `/plan-ceo-review` on `design.md` and `/plan-eng-review` on slice 1 of `storymap.md`." That makes the handoff explicit.

**Don't auto-invoke gstack commands from inside this skill.** They are user-facing slash commands the human runs when they want the review. This skill produces the *inputs* those commands need.

## GSD — Get Shit Done (getshitdone.help)

[GSD](https://getshitdone.help/solo-guide/why-gsd/) is a context-engineering layer on top of Claude Code, aimed primarily at solo builders. It enforces a structured Research → Plan → Execute → Validate → Complete pipeline with a `.gsd/` project-state directory containing a Brief, Roadmap, Decisions, and task summaries.

The GSD hierarchy is **Milestone → Slice → Task**, which maps to this skill's outputs but at a different unit of scope. Be careful to translate, not equate:

| This skill | GSD term | Mapping note |
|---|---|---|
| The whole `storymap.md` | A multi-milestone **Roadmap** | The full backbone may span 2-3 GSD milestones |
| One **slice** (walking-skeleton / PI 1 / MVP / Now) | One GSD **Milestone** | A slice = a Milestone-sized unit of work |
| One **activity** within a slice | A GSD **Slice** (yes, the names collide) | A backbone activity, scoped to its share of the milestone |
| One **story** | A GSD **Task** | Atomic execution unit |
| `design.md` | The GSD **Brief** | Direct mapping — both are the "why and what" input doc |
| `backlog.md` | The GSD **Roadmap** | Add a per-row note like `[gsd-milestone: 1]` for clarity |

**Important terminology collision:** "Slice" means different things in the two systems. In this skill, a slice is a horizontal cut across the backbone (e.g., MVP, R2, R3). In GSD, a "slice" is a sub-unit within a milestone (i.e., an activity in our terms). When writing artifacts for a GSD-using team, use GSD's vocabulary in the final deliverable and add a one-line note in `design.md` explaining the mapping.

GSD workflow handoff:

```
This skill (Mode A or B)
   ├── design.md             →   .gsd/Brief.md
   ├── storymap.md slice 1   →   .gsd/Milestones/M1/...
   ├── individual stories    →   GSD Tasks for /gsd execute-task
   └── backlog.md            →   .gsd/Roadmap.md
                                 ↓
                             GSD /gsd discuss → /gsd plan-milestone → /gsd auto
```

If GSD is active, after producing artifacts say something like: "Outputs map to GSD as: design.md → Brief; slice 1 of storymap.md → Milestone 1 (with 5 GSD slices = 5 backbone activities, ~15 GSD tasks). Ready for `/gsd discuss` to confirm framing or `/gsd plan-milestone` to start the pipeline."

**Don't write directly to `.gsd/` from inside this skill** — GSD owns that directory and has its own state-machine expectations. Produce the canonical six files; let the user (or GSD's own commands) import them.

## Superpowers (obra/superpowers)

[Superpowers](https://github.com/obra/superpowers) — Jesse Vincent / Prime Radiant — is an agentic skills framework organized into a 7-stage software-development workflow: `brainstorming` → `using-git-worktrees` → `writing-plans` → `subagent-driven-development` → `test-driven-development` → `requesting-code-review` → `finishing-a-development-branch`.

This skill slots between **`brainstorming`** and **`writing-plans`**:

```
brainstorming  →  user-story-mapping  →  writing-plans  →  rest of Superpowers
   (intent)        (sliced delivery        (2-5 min
                   plan + design doc)       tasks)
```

**Handoff in:** Superpowers' `brainstorming` produces a design doc clarifying intent. Use that doc as Mode B input (from a problem brief).

**Handoff out:** The first slice of `storymap.md` becomes the input to `writing-plans`. Each story → 2-5 min tasks. `design.md` and `backlog.md` stay alongside as reference.

If Superpowers is active, mention this in your hand-off message: "Slice 1 is ready for writing-plans. design.md and backlog.md remain authoritative for scope decisions."

## Jira / Azure DevOps / GitHub Issues / Linear / Trello / spreadsheets

See `references/work-item-tracking.md` for the full per-tool mapping. Short version: the CSV outputs are import sources, don't recreate stories by hand inside the tool.

## SAFe ART tooling (Jira Align, Targetprocess, Tempo)

These speak SAFe natively and have first-class WSJF support. Use the SAFe column mapping (Activity→Epic, Task→Feature, Story→Story) and let the tool calculate WSJF rather than pre-computing.

## When the user has none of these

You produce six files. They read them, edit them, decide what to do next. That's the supported case and probably the most common one. Don't push tooling integration if the user hasn't mentioned it.
