# Integration with sibling skill frameworks and SAFe tooling

Storymap answers **what belongs in the first usable release across the whole journey?** The framework owns its design approval, specialist reviews, and engineering work breakdown. An approved brief sets constraints; it is not itself an approved slice. Treat a framework-owned `design.md` as the brief and update only the story-map addendum.

## When to use

Read this for sister-framework Plan signals, exact hand-off lines, or GSD "slice" terminology. For tracker routing, see [output-routing.md](output-routing.md); for imports, see [work-item-tracking.md](work-item-tracking.md).

## Auto-activation cues — Plan-stage commands of sister frameworks

Map when the user asks to shape a journey or release slice, or when a Plan-stage transition exposes that decision. Use an existing approved map when scope is unchanged. If the user only asked for a framework command, keep its workflow in charge: use `/office-hours` or `brainstorming` to settle open framing first; for review-only or task planning, point to the existing slice rather than starting a second discovery loop. If a review changes who is served, what outcome ships, or what must be deferred, surface the delta to the user and re-enter this skill's approval gate before changing the map.

| Framework | Plan-stage cues (scope decision must be open) | Integration contract |
|---|---|---|
| **Superpowers** | Finished `brainstorming`; about to call `writing-plans`; generating a plan; slice 1 stories not written | Existing `design.md` / brainstorming output → brief; `storymap.md` slice 1 → `writing-plans` task decomposition |
| **gstack** | `/office-hours`, `/autoplan`, `/plan-*-review` (including `/plan-dev-design-review`), or a scope change to a generated `design.md` | Existing brief → map; send the slice to the relevant review below |
| **GSD** | `/gsd discuss`, `/gsd plan-milestone`, or Brief/Roadmap authoring | Agreed outcomes and dependencies → suggested milestone scope and demo proof |

Under a sister framework, do not author framework-specific files (especially `.gsd/`); use its vocabulary in the final hand-off.

**Disambiguation rule.** For `/office-hours` on an unsettled idea, let discovery lead and offer mapping at the scope boundary. For an explicit mapping request on an agreed brief, use the brief and ask only about unresolved slice decisions; do not repeat approved framing or invoke the next command.

## Slice handoff

At Step 6, when another planner or reviewer is the next consumer, put a `## Slice 1 handoff` section in `handoff.md`, after `## Bottom line`. The section is a scope contract, not a second backlog:

| Field | What the receiver needs |
|---|---|
| **Outcome** | Who gets what result, and a link to the approved brief or decision that bounds the slice. |
| **In scope** | A link to slice 1 of `storymap.md` and any launch-critical persona handoff that must stay intact. Use existing tracker IDs when available; otherwise use activity + story title, not regenerated CSV IDs. |
| **Demo** | One observable end-to-end walkthrough with the minimum starting state, persona transitions, and final observable result. Link acceptance criteria or the E2E contract only if emitted. |
| **Deferred** | Named tempting additions deliberately excluded; keep them out of the downstream plan. |
| **Next** | One next review or planning action and its input. If any unresolved decision can change the outcome, acceptance, or scope, name it here and hand off for review, not implementation. |

For example, an expense flow demos an employee submitting a valid receipt, a manager approving it, and the employee seeing the approved state. Bulk approvals stay deferred; if no one has agreed who may approve, that decision goes to review before implementation planning. A planner may split a story into several tasks or share a prerequisite across stories, but those tasks must still trace back to the agreed outcome. A scope-changing finding loops back to the map; it is not a task-list edit.

Before marking it ready, compare the brief, slice-1 stories, and demo: each in-scope user outcome and critical handoff must have a story and observable proof; deferred work must stay outside slice 1. Report mismatches in **Next** with the source and decision owner. The demo describes expected behavior, not proof that tests have run.

## gstack (garrytan/gstack)

[gstack](https://github.com/garrytan/gstack) — Garry Tan (Y Combinator) — is a Claude Code slash-command pack for Think → Plan → Build → Review → Test → Ship → Reflect. It exposes 23+ commands: `/office-hours`, `/autoplan`, `/plan-ceo-review`, `/plan-eng-review`, `/plan-design-review`, `/plan-dev-design-review`, `/design-review`, `/review`, `/qa`, `/ship`, `/retro`.

Provide gstack's next review with the relevant brief and slice context explicitly. Do not assume the command automatically discovers Storymap files or can read a tracker view.

| gstack command | What to supply |
|---|---|
| `/office-hours` (refine an idea) | Prior map only when relevant; the accepted discovery brief becomes input to mapping |
| `/autoplan` (review a plan) | Use the approved brief and slice handoff; revisit the existing map only if scope changes |
| `/plan-ceo-review` | Review `design.md` for outcome clarity and core question |
| `/plan-eng-review` | Slice 1, dependencies, demo, and any open architecture questions |
| `/plan-design-review` | Persona narratives, activity backbone, and transitions in the demo |
| `/plan-dev-design-review` | Affected developer journey and its user-facing acceptance criteria, if emitted |
| `/plan-devex-review` | Use the affected developer journey; reference `backlog.md` only when it exists |
| `/ship`, `/canary` | Operate on built stories; this skill stops at plan |
| `/retro`, `/learn` | Use `design.md` Hypotheses table as retro input |

If active, recommend the next relevant review, not the whole pipeline: `/plan-ceo-review` for scope/outcome choices, `/plan-eng-review` for feasibility of slice 1, or `/plan-design-review` for the user journey. Include role hints only if produced.

**Don't auto-invoke gstack commands.** They are user-facing; this skill produces their *inputs*.

## GSD — Get Shit Done (getshitdone.help)

Use the installed GSD variant's brief, requirements, or milestone context as input. In variants using **Milestone → Slice → Task**, a Storymap slice is a release cut across the journey; a GSD slice is a capability within a milestone. Use the release cut as input to milestone planning. GSD may group several activities into one capability to prove a risky handoff, or split one story into several tasks. Do not prescribe cardinality, paths, or IDs.

If active, propose how the actual activities fit within a milestone. Recommend `/gsd discuss` when framing is open or `/gsd plan-milestone` for an approved slice; use the commands and vocabulary of the installed GSD variant.

**Don't write directly to `.gsd/` from inside this skill** — GSD owns that directory/state machine. Produce canonical files and suggested import lines; user or GSD commands import.

## Superpowers (obra/superpowers)

[Superpowers](https://github.com/obra/superpowers) — Jesse Vincent / Prime Radiant — is an agentic skills framework with 7 stages: `brainstorming` → `using-git-worktrees` → `writing-plans` → `subagent-driven-development` → `test-driven-development` → `requesting-code-review` → `finishing-a-development-branch`.

This skill slots between **`brainstorming`** and **`writing-plans`**:

```
brainstorming  →  user-story-mapping  →  writing-plans  →  rest of Superpowers
   (intent)        (sliced delivery        (2-5 min
                   plan + design doc)       tasks)
```

**Handoff in:** Use the actual approved design file (often `docs/superpowers/specs/*-design.md`) as the brief; do not overwrite it. If the active workflow requires `writing-plans` immediately after approval, do not interpose another skill. Map in a separate user-directed shaping pass and supply the result to the plan or revision.

**Handoff out:** Give `writing-plans` the approved brief, slice-1 handoff, and any acceptance artifacts actually emitted. It owns task granularity, files, tests, and execution sequencing. Keep deferred stories visible but out of its task list. Role hints are advisory, not scope-authoritative.

If active and unblocked, say: "Use the approved brief and `handoff.md` to run `writing-plans` for slice 1 only."

## Other planners

For a spec-first planner such as Spec Kit, give it the approved outcomes, exclusions, and demo as inputs to its specification and acceptance workflow. An independently testable story is not a replacement for the multi-persona slice demo. Translate deliberately: the planner's priority labels and tasks may not match this map's slices or story count. Offer the handoff on request; do not add an automatic trigger or write planner-owned files.

## Jira / Azure DevOps / GitHub Issues / Linear / Trello / spreadsheets

For tracker routing, see [output-routing.md](output-routing.md). For imports, see [work-item-tracking.md](work-item-tracking.md). CSV outputs are import sources; don't recreate stories by hand.

## SAFe ART tooling (Jira Align, Targetprocess, Tempo)

These speak SAFe natively and support WSJF directly. Use the SAFe mapping (Activity→Epic, Task→Feature, Story→Story) and let the tool calculate WSJF.

## What NOT to do

- **Don't auto-invoke any sister-framework slash command** from inside this skill — they are user-facing review commands; this skill produces only the *inputs*.
- **Don't write directly into a framework's state directory** (`.gsd/` especially). Emit suggested import lines; let the user or framework commands import.
- **Don't equate a GSD "slice" with this skill's slice** — they collide. Translate using the table above.
- **Don't push unmentioned tooling integration.** Canonical files for a human to read, edit, and act on are the supported/common case.

## When the user has none of these

Produce the canonical files. The user reads, edits, and decides next steps. Do not push tooling integration unless the user mentions it.
