# Integration with sibling skill frameworks and SAFe tooling

When Superpowers, gstack, or GSD reaches Plan, self-activate and produce the story map once. This includes Superpowers plan generation, any gstack `/plan-*-review` (including `/plan-dev-design-review`), and cases where a design doc exists and the plan is being adjusted. If the framework already produced `design.md`, treat it as the brief and augment it; don't replace it. Their Plan commands consume the same inputs: design doc, slice-1 stories, role hints, test contract. Otherwise this skill is standalone; if no tool applies, emit canonical files.

## When to use

Read this for sister-framework Plan signals, exact hand-off lines, or GSD "slice" terminology. For tracker routing, see [output-routing.md](output-routing.md); for imports, see [work-item-tracking.md](work-item-tracking.md).

## Auto-activation cues — Plan-stage commands of sister frameworks

Before ad-hoc drafting, detect a sister framework at Plan and self-activate. Produce story map, per-persona stories, role hints, and test contract once; framework commands review and consume them.

| Framework | Plan-stage signal (any of these = activate this skill) | Integration contract |
|---|---|---|
| **Superpowers** | Finished `brainstorming`; about to call `writing-plans`; generating a plan; slice 1 stories not written | Existing `design.md` / brainstorming output → brief; `storymap.md` slice 1 → `writing-plans` task decomposition |
| **gstack** | User invokes `/office-hours`, `/autoplan`, any `/plan-*-review` including `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/plan-dev-design-review`, `/plan-devex-review`; or a generated `design.md` is being adjusted into a plan | Existing `design.md` → brief and `/plan-ceo-review`; slice 1 → `/plan-eng-review`; persona narratives + `role-hints.md` → `/plan-design-review` / `/plan-dev-design-review`; `backlog.md` → `/plan-devex-review` |
| **GSD** | User invokes `/gsd discuss`, `/gsd plan-milestone`; or authors `.gsd/Brief.md` / `.gsd/Roadmap.md` / new `.gsd/Milestones/Mn/` | `design.md` → `.gsd/Brief.md`; slice 1 → `.gsd/Milestones/M1/`; `backlog.md` → `.gsd/Roadmap.md` |

Under a sister framework, do not author framework-specific files (especially `.gsd/`); use its vocabulary in the final hand-off.

**Disambiguation rule.** If this skill and a sister-framework slash-command trigger together (e.g., `/office-hours we need to plan our refund flow`), run this skill *first*, produce canonical artifacts, then let the framework consume them. Do not satisfy both in one nested invocation.

## gstack (garrytan/gstack)

[gstack](https://github.com/garrytan/gstack) — Garry Tan (Y Combinator) — is a Claude Code slash-command pack for Think → Plan → Build → Review → Test → Ship → Reflect. It exposes 23+ commands: `/office-hours`, `/autoplan`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/plan-dev-design-review`, `/design-review`, `/review`, `/qa`, `/ship`, `/retro`.

This skill consumes or produces gstack **Plan** artifacts. If gstack already wrote `design.md`, use it as the authoritative brief and append/update only the story-map addendum (bottom line, context trace, persona interactions, decisions); don't rewrite the gstack-owned framing. In the tracker case, `backlog.md` is **not** emitted; `/plan-devex-review` reads the ranked tracker view, and opt-in `tracker-status-update.<ext>` populates burn-down fields ([output-routing.md § What each branch produces](output-routing.md#what-each-branch-produces)).

```
gstack /office-hours          ──→ user-story-mapping (the loop)
gstack /autoplan                  ↳ consumes/updates design.md + produces storymap.md + backlog.md
gstack /plan-ceo-review       ──→ reviews design.md (the "why")
gstack /plan-eng-review       ──→ reviews storymap.md slice-1 (the "what to build first")
gstack /plan-design-review    ──→ reviews user activities + persona narratives
gstack /plan-dev-design-review──→ reviews developer/design fit across story slices
gstack /plan-devex-review     ──→ reviews backlog ranking
                                ↓
gstack /ship, /canary, /qa, /retro work the resulting slices
```

Practical gstack mapping:

| gstack command | What it reads from this skill |
|---|---|
| `/office-hours` (refine an idea) | Read `design.md`: personas, opportunities, hypotheses |
| `/autoplan` (turn a goal into work) | If `design.md` exists, use it as brief; skip if `storymap.md` exists; point to first slice |
| `/plan-ceo-review` | Review `design.md` for outcome clarity and core question |
| `/plan-eng-review` | Review `storymap.md` slice 1 for feasibility; surface `role-hints.md`§Architect open questions |
| `/plan-design-review` | Review persona narratives, activity backbone, `role-hints.md`§UX |
| `/plan-dev-design-review` | Review slice-1 developer/design fit; use `storymap.md`, `design.md`, and both `role-hints.md` sections |
| `/plan-devex-review` | Review `backlog.md` ranking |
| `/ship`, `/canary` | Operate on built stories; this skill stops at plan |
| `/retro`, `/learn` | Use `design.md` Hypotheses table as retro input |

If active, say: "Outputs are ready for `/plan-ceo-review` on `design.md`, `/plan-eng-review` on slice 1 of `storymap.md` + `role-hints.md`§Architect, and `/plan-design-review` on persona narratives + `role-hints.md`§UX."

**Don't auto-invoke gstack commands.** They are user-facing; this skill produces their *inputs*.

## GSD — Get Shit Done (getshitdone.help)

[GSD](https://getshitdone.help/solo-guide/why-gsd/) is a Claude Code context layer for solo builders. It enforces Research → Plan → Execute → Validate → Complete with `.gsd/` project state: Brief, Roadmap, Decisions, task summaries.

GSD uses **Milestone → Slice → Task**; map by scope, not by identical names:

| This skill | GSD term | Mapping note |
|---|---|---|
| The whole `storymap.md` | A multi-milestone **Roadmap** | Full backbone may span 2-3 GSD milestones |
| One **slice** (walking-skeleton / PI 1 / MVP / Now) | One GSD **Milestone** | Slice = Milestone-sized work |
| One **activity** within a slice | A GSD **Slice** (yes, names collide) | Backbone activity scoped to its milestone share |
| One **story** | A GSD **Task** | Atomic execution unit |
| `design.md` | The GSD **Brief** | Direct "why and what" input doc |
| `backlog.md` | The GSD **Roadmap** | Add a per-row note like `[gsd-milestone: 1]` for clarity |

**Important terminology collision:** "slice" differs by system. Here it is a horizontal cut across the backbone (MVP, R2, R3). In GSD it is a milestone sub-unit, closer to an *activity*. For GSD teams, use GSD vocabulary and add a one-line mapping note in `design.md`. Translate, never equate.

GSD handoff (no tracker; with tracker, opt-in burn-down writes replace `backlog.md`):

```
This skill (the loop)
   ├── design.md             →   .gsd/Brief.md
   ├── storymap.md slice 1   →   .gsd/Milestones/M1/...
   ├── individual stories    →   GSD Tasks for /gsd execute-task
   └── backlog.md            →   .gsd/Roadmap.md   (when no issue tracker)
                                 ↓
                             GSD /gsd discuss → /gsd plan-milestone → /gsd auto
```

If active, say: "Outputs map to GSD as: design.md → Brief; slice 1 of storymap.md → Milestone 1 (with 5 GSD slices = 5 backbone activities, ~15 GSD tasks); role-hints.md (UX + architect) sits alongside the Brief for the team to work through. Ready for `/gsd discuss` to confirm framing or `/gsd plan-milestone` to start the pipeline."

**Don't write directly to `.gsd/` from inside this skill** — GSD owns that directory/state machine. Produce canonical files and suggested import lines; user or GSD commands import.

## Superpowers (obra/superpowers)

[Superpowers](https://github.com/obra/superpowers) — Jesse Vincent / Prime Radiant — is an agentic skills framework with 7 stages: `brainstorming` → `using-git-worktrees` → `writing-plans` → `subagent-driven-development` → `test-driven-development` → `requesting-code-review` → `finishing-a-development-branch`.

This skill slots between **`brainstorming`** and **`writing-plans`**:

```
brainstorming  →  user-story-mapping  →  writing-plans  →  rest of Superpowers
   (intent)        (sliced delivery        (2-5 min
                   plan + design doc)       tasks)
```

**Handoff in:** Superpowers `brainstorming` or plan generation may produce an intent `design.md`. Use it as the loop's brief and framework-owned source; do not overwrite it.

**Handoff out:** First slice of `storymap.md` feeds `writing-plans`; each story → 2-5 min tasks. `design.md` (original brief plus story-map addendum) and `backlog.md` stay scope-authoritative. `role-hints.md` is a designer/architect *head-start*: resolve open questions before `writing-plans`, but don't treat hints as scope-authoritative.

If active, say: "Slice 1 is ready for `writing-plans`. design.md and backlog.md are authoritative for scope; role-hints.md (UX + architect) is a head-start — work through its open questions first."

## Jira / Azure DevOps / GitHub Issues / Linear / Trello / spreadsheets

For tracker routing, see [output-routing.md](output-routing.md). For existing projects, sister-framework state dirs are usually right. For imports, see [work-item-tracking.md](work-item-tracking.md). CSV outputs are import sources; don't recreate stories by hand.

## SAFe ART tooling (Jira Align, Targetprocess, Tempo)

These speak SAFe natively and support WSJF directly. Use the SAFe mapping (Activity→Epic, Task→Feature, Story→Story) and let the tool calculate WSJF.

## What NOT to do

- **Don't auto-invoke any sister-framework slash command** from inside this skill — they are user-facing review commands; this skill produces only the *inputs*.
- **Don't write directly into a framework's state directory** (`.gsd/` especially). Emit suggested import lines; let the user or framework commands import.
- **Don't equate a GSD "slice" with this skill's slice** — they collide. Translate using the table above.
- **Don't push unmentioned tooling integration.** Canonical files for a human to read, edit, and act on are the supported/common case.

## When the user has none of these

Produce the canonical files. The user reads, edits, and decides next steps. Do not push tooling integration unless the user mentions it.
