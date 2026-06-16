# Integration with sibling skill frameworks and SAFe tooling

When a sister framework (Superpowers, gstack, GSD) hits its Plan stage, self-activate this skill there and produce the story map once — those frameworks' Plan-stage commands all consume the same inputs (design doc, slice-1 stories, role hints, test contract). This skill is otherwise standalone: none of the tools below are required, and when the user has none of them you just emit the canonical files.

## When to use

Read this file when a prompt carries a sister-framework Plan-stage signal, when you need the exact hand-off line to leave for one of those frameworks, or when you are writing artifacts for a GSD team and must navigate the "slice" terminology collision. For *whether* to push outputs to an issue tracker at all, see [output-routing.md](output-routing.md); for the per-tool import mechanics, see [work-item-tracking.md](work-item-tracking.md).

## Auto-activation cues — Plan-stage commands of sister frameworks

Before falling through to ad-hoc story drafting, detect whether a sister framework is at its Plan stage and self-activate this skill there. The story map + per-persona stories + role hints + test contract is what each of those frameworks' Plan-stage commands need as input — produce them once, here, and let the framework's own commands review and consume them.

| Framework | Plan-stage signal (any of these = activate this skill) | This skill produces what they consume |
|---|---|---|
| **Superpowers** | Just finished `brainstorming`; about to call `writing-plans` and the slice 1 stories aren't written yet | `storymap.md` slice 1 → input to `writing-plans` task decomposition |
| **gstack** | User invokes `/office-hours`, `/autoplan`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/plan-devex-review` | `design.md` → `/plan-ceo-review`; slice 1 → `/plan-eng-review`; persona narratives + `role-hints.md` → `/plan-design-review`; `backlog.md` → `/plan-devex-review` |
| **GSD** | User invokes `/gsd discuss`, `/gsd plan-milestone`; or is authoring `.gsd/Brief.md` / `.gsd/Roadmap.md` / a new `.gsd/Milestones/Mn/` directory | `design.md` → `.gsd/Brief.md`; slice 1 → `.gsd/Milestones/M1/`; `backlog.md` → `.gsd/Roadmap.md` |

When activated under a sister framework, skip framework-specific authoring of artifacts (don't write `.gsd/` files directly), but use that framework's vocabulary in your final hand-off line. See the per-framework notes below.

**Disambiguation rule.** If both this skill's triggers AND a sister-framework slash-command fire on the same prompt (e.g., the user types `/office-hours we need to plan our refund flow`), this skill runs *first* — produce the canonical artifacts — and the framework command runs against them. Don't try to satisfy both in one nested invocation.

## gstack (garrytan/gstack)

[gstack](https://github.com/garrytan/gstack) — Garry Tan (Y Combinator) — is a Claude Code slash-command pack that organizes work into a Think → Plan → Build → Review → Test → Ship → Reflect sprint. It exposes 23+ commands like `/office-hours`, `/autoplan`, `/plan-ceo-review`, `/plan-eng-review`, `/design-review`, `/review`, `/qa`, `/ship`, `/retro`.

This skill is the natural artifact-producer for gstack's **Plan** phase:

```
gstack /office-hours          ──→ user-story-mapping (the loop)
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
| `/plan-eng-review` | Reviews `storymap.md` slice 1 for engineering feasibility — also surfaces `role-hints.md`§Architect open questions |
| `/plan-design-review` | Reviews persona narratives, activity backbone, and `role-hints.md`§UX for UX coherence |
| `/plan-devex-review` | Reviews `backlog.md` for ranking sanity |
| `/ship`, `/canary` | Operate on built stories; this skill stops at the plan |
| `/retro`, `/learn` | Use `design.md` Hypotheses table as the "what did we believe" input to retro |

If gstack is active, after producing artifacts say: "Outputs are ready for `/plan-ceo-review` on `design.md`, `/plan-eng-review` on slice 1 of `storymap.md` + `role-hints.md`§Architect, and `/plan-design-review` on persona narratives + `role-hints.md`§UX." That makes the handoff explicit.

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

**Important terminology collision:** "slice" means different things in the two systems. In this skill, a slice is a horizontal cut across the backbone (e.g., MVP, R2, R3). In GSD, a "slice" is a sub-unit within a milestone — closer to an *activity* in our terms. When writing artifacts for a GSD-using team, use GSD's vocabulary in the final deliverable and add a one-line note in `design.md` explaining the mapping. Translate, never equate.

GSD workflow handoff:

```
This skill (the loop)
   ├── design.md             →   .gsd/Brief.md
   ├── storymap.md slice 1   →   .gsd/Milestones/M1/...
   ├── individual stories    →   GSD Tasks for /gsd execute-task
   └── backlog.md            →   .gsd/Roadmap.md
                                 ↓
                             GSD /gsd discuss → /gsd plan-milestone → /gsd auto
```

If GSD is active, after producing artifacts say something like: "Outputs map to GSD as: design.md → Brief; slice 1 of storymap.md → Milestone 1 (with 5 GSD slices = 5 backbone activities, ~15 GSD tasks); role-hints.md (UX + architect) sits alongside the Brief for the team to work through. Ready for `/gsd discuss` to confirm framing or `/gsd plan-milestone` to start the pipeline."

**Don't write directly to `.gsd/` from inside this skill** — GSD owns that directory and has its own state-machine expectations. Produce the canonical files and emit suggested import lines; let the user (or GSD's own commands) do the import.

## Superpowers (obra/superpowers)

[Superpowers](https://github.com/obra/superpowers) — Jesse Vincent / Prime Radiant — is an agentic skills framework organized into a 7-stage software-development workflow: `brainstorming` → `using-git-worktrees` → `writing-plans` → `subagent-driven-development` → `test-driven-development` → `requesting-code-review` → `finishing-a-development-branch`.

This skill slots between **`brainstorming`** and **`writing-plans`**:

```
brainstorming  →  user-story-mapping  →  writing-plans  →  rest of Superpowers
   (intent)        (sliced delivery        (2-5 min
                   plan + design doc)       tasks)
```

**Handoff in:** Superpowers' `brainstorming` produces a design doc clarifying intent. Use that doc as a problem-brief input to the loop.

**Handoff out:** The first slice of `storymap.md` becomes the input to `writing-plans`. Each story → 2-5 min tasks. `design.md` and `backlog.md` remain authoritative for scope decisions; `role-hints.md` rides alongside as a *head-start* for the designer and architect — resolve its open questions before `writing-plans` decomposes the work, but don't treat the hints themselves as scope-authoritative.

If Superpowers is active, mention this in your hand-off message: "Slice 1 is ready for `writing-plans`. design.md and backlog.md are authoritative for scope; role-hints.md (UX + architect) is a head-start — work through its open questions first."

## Jira / Azure DevOps / GitHub Issues / Linear / Trello / spreadsheets

For *whether* to push to a tracker at all, see [output-routing.md](output-routing.md) — for existing projects, the sister-framework state directories above are usually the right destination instead. For the full per-tool mapping and import mechanics, see [work-item-tracking.md](work-item-tracking.md). Short version: the CSV outputs are import sources — don't recreate stories by hand inside the tool.

## SAFe ART tooling (Jira Align, Targetprocess, Tempo)

These speak SAFe natively and have first-class WSJF support. Use the SAFe column mapping (Activity→Epic, Task→Feature, Story→Story) and let the tool calculate WSJF rather than pre-computing it.

## What NOT to do

- **Don't auto-invoke any sister-framework slash command** from inside this skill — they are user-facing commands the human runs when they want the review; this skill produces only the *inputs*.
- **Don't write directly into a framework's state directory** (`.gsd/` especially). Emit suggested import lines instead and let the user or the framework's own commands import.
- **Don't equate a GSD "slice" with this skill's slice** — they collide. Translate using the table above.
- **Don't push tooling integration the user hasn't mentioned.** Producing the canonical files for a human to read, edit, and act on is the supported and most common case.

## When the user has none of these

You produce the canonical files. They read them, edit them, decide what to do next. That's the supported case and probably the most common one. Don't push tooling integration if the user hasn't mentioned it.
