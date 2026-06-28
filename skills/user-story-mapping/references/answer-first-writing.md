# Answer-first writing (the Pyramid Principle for storymap artifacts)

Open `design.md`, `backlog.md`, and `handoff.md` with `## Bottom line`: the answer in 1-3 sentences before context, methodology, or inventory. Readers who stop there still get the message; arguments and evidence follow.

Barbara Minto's Pyramid Principle for artifacts: **answer** → **arguments** (why) → **evidence/detail**. SKILL.md Rule 3 ([`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run)) points here.

## When to use

Use only for **human-facing narrative artifacts**: `design.md`, `backlog.md`, `handoff.md`, including iteration re-runs where the bottom line becomes diff + next decision. If `design.md` is framework-owned (gstack/Superpowers), preserve its existing order and put this skill's answer-first content in the story-map addendum instead of rewriting the whole file.

Do **not** apply it to machine artifacts `storymap.csv` / `storymap.mmd` or to `storymap.md`; its `## Activity:` / `### Task:` / `- [slice:...]` structure is parser-load-bearing and must not be reordered.

## The shape

```
[ Bottom line — the answer, 1-3 sentences ]
        ├─ Argument 1 (why)        ├─ Argument 2        ├─ Argument 3
        │   └─ evidence/detail     │   └─ evidence       │   └─ evidence
```

`## Bottom line` is mandatory and first for storymap-owned files. For framework-owned `design.md`, add/update a story-map `## Bottom line` addendum as high as safely possible without clobbering the framework's sections. State the answer, then descend: supporting arguments, then evidence.

## Per-artifact

| Artifact | Bottom line (lead with this) | Then — arguments | Then — evidence |
|---|---|---|---|
| **handoff.md** | The **one decision** the user must make next + your recommendation | Contents; uncertainties; re-run diff | Per-item detail, math checks, sister-framework next command |
| **backlog.md** | **Start here:** the slice-1 headline — what to build first and why, in one line | Top-10 ranked; per-slice tables | Full scoring in `backlog.csv` |
| **design.md** | The **outcome** + the **question this work answers** + the core bet (hypothesis) | Personas, backbone activities, opportunities, hypotheses | Context sources, backbone criteria, decisions log |

`design.md`'s `## Backbone criteria` and `## Context sources mined` are *process / reproducibility metadata*; keep them **below**. In a framework-owned `design.md`, these belong in the story-map addendum, not in the framework's own framing sections.

On an iteration re-run (the [loop](../SKILL.md#the-loop) on a non-empty baseline), the bottom line carries the change: `handoff.md` leads with the smallest next decision + diff; `backlog.md` leads with whether slice 1 moved.

## Anti-patterns (burying the lede)

- **Inventory-first handoff.** Opening `handoff.md` with "What's in the box" buries the decision. Lead with it.
- **Process-first design doc.** Opening `design.md` with criteria or sources hides the build target. Lead with outcome + question.
- **Flat backlog.** A long ranked table with no headline makes the reader infer "what do I start." State it in one line.
- **Chronological narration.** "We mined the README, then the tests, then the tracker, and concluded X." Invert it: "X. Evidence: README, tests, tracker."

## Checklist

- [ ] Storymap-owned `design.md` / `backlog.md` / `handoff.md` opens with `## Bottom line` (the answer, ≤3 sentences); framework-owned `design.md` has a story-map addendum with its own `## Bottom line`
- [ ] Stopping after the bottom line still gives the core message
- [ ] Arguments share one abstraction level and support the bottom line
- [ ] Process / criteria / inventory sit **below** the answer
- [ ] `handoff.md` leads with the smallest real next decision

Worked examples: Barbara Minto, *The Pyramid Principle: Logic in Writing and Thinking*.
