# Answer-first writing (the Pyramid Principle for storymap artifacts)

Open every human-facing narrative artifact with the answer, not the process: each of `design.md`, `backlog.md`, and `handoff.md` leads with a `## Bottom line` section — the single most important thing the reader needs, in 1-3 sentences — before any context, methodology, or inventory. A reader who stops after the bottom line still has the core message; supporting arguments and evidence sit below it.

This is Barbara Minto's Pyramid Principle applied to artifacts: lead with the **answer**, then the **arguments** (why), then the **evidence/detail**. SKILL.md Rule 3 ([`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run)) points here for the per-artifact specifics.

## When to use

Apply this to the three **human-facing narrative artifacts** the skill produces: `design.md`, `backlog.md`, and `handoff.md`. Reach for it whenever you author or update any of them — including on an iteration re-run, where the bottom line shifts to the diff and the next decision.

It does **not** apply to the machine artifacts `storymap.csv` / `storymap.mmd`, nor to `storymap.md` — the latter's `## Activity:` / `### Task:` / `- [slice:...]` structure is load-bearing for the parser and must not be reordered for narrative effect.

## The shape

```
[ Bottom line — the answer, 1-3 sentences ]
        ├─ Argument 1 (why)        ├─ Argument 2        ├─ Argument 3
        │   └─ evidence/detail     │   └─ evidence       │   └─ evidence
```

The `## Bottom line` section is mandatory and comes first. State the answer, then descend one level of abstraction at a time: arguments that each support the bottom line, then the evidence beneath each argument.

## Per-artifact

| Artifact | Bottom line (lead with this) | Then — arguments | Then — evidence |
|---|---|---|---|
| **handoff.md** | The **one decision** the user must make next + your recommendation | What's in the box; what's uncertain; the diff (on a re-run) | Per-item detail, math checks, the sister-framework next command |
| **backlog.md** | **Start here:** the slice-1 headline — what to build first and why, in one line | Top-10 ranked; per-slice tables | Full scoring lives in `backlog.csv` |
| **design.md** | The **outcome** + the **question this work answers** + the core bet (hypothesis) | Personas, backbone activities, opportunities, hypotheses | Context sources, backbone criteria, decisions log |

`design.md`'s `## Backbone criteria` and `## Context sources mined` are *process / reproducibility metadata* — keep them, but **below** the bottom line, not above it. The reader wants the answer before the methodology.

On an iteration re-run (the [loop](../SKILL.md#the-loop) on a non-empty baseline), the bottom line carries the change, not a re-statement of the whole: `handoff.md` leads with the smallest next decision plus the diff, and `backlog.md` leads with whether slice 1 moved.

## Anti-patterns (burying the lede)

- **Inventory-first handoff.** Opening `handoff.md` with "What's in the box" (a file list) buries the decision the user actually has to make. Lead with the decision.
- **Process-first design doc.** Opening `design.md` with backbone criteria or "context sources mined" forces the reader to wade through methodology to find what you're building. Lead with the outcome + question.
- **Flat backlog.** A long ranked table with no headline makes the reader infer "what do I start." State it in one line.
- **Chronological narration.** "We mined the README, then the tests, then the tracker, and concluded X." Invert it: "X. Evidence: README, tests, tracker."

## Checklist

- [ ] Each of `design.md` / `backlog.md` / `handoff.md` opens with a `## Bottom line` (the answer, ≤3 sentences)
- [ ] A reader who stops after the bottom line still has the core message
- [ ] Arguments under it sit at one level of abstraction and each supports the bottom line
- [ ] Process / criteria / inventory sit **below** the answer, not above
- [ ] `handoff.md`'s lead decision = the smallest next decision the user must actually make

Detail and worked examples: Barbara Minto, *The Pyramid Principle: Logic in Writing and Thinking*.
