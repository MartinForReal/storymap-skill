# <Project Name> — Design Doc

## Bottom line

<2-3 sentences, answer-first (Pyramid Principle): the outcome we're after, the one question this work answers, and the core bet. A reader who stops here still has the gist. Everything below is supporting structure — read on for the why and the evidence.>

## Backbone criteria

These are the criteria chosen when the backbone was generated. **Re-runs of this skill should use the same criteria to keep the backbone stable across runs.**

| Criterion | Choice | Rationale |
|---|---|---|
| Frame | <Activity flow / JTBD / System interaction / Journey> | <why> |
| Persona perspective | <Primary user / Multiple parallel / Aggregate> | <why> |
| Time horizon | <Single session / Day-in-life / Lifecycle> | <why> |
| Granularity | <5-7 / 3-5 high-level / 8-12 detailed> | <why> |
| Scope | <Happy path / +error recovery / Full surface> | <why> |
| Aggregation | <Single role / Multi-role with handoffs> | <why> |

Status: `[user-confirmed]` or `[default applied — user override pending]`

## The question this work answers

<One sentence. Not "build feature X" — "is hypothesis Y true?", or "can we
move metric Z by N%?".>

## Outcome

<What is measurably different in 6 months, for whom, if this succeeds.>

## Trigger

<Why now? What changed that makes this worth doing this quarter and not next.>

## Personas

### <Primary persona name>
- **Role:** <what they do>
- **Goal in this work:** <what they want to accomplish>
- **Today they:** <how they currently solve this — even if poorly>
- **Pain:** <what makes the current way frustrating>

### <Secondary persona name>
- ...

## Persona interactions

How the personas hand off to, depend on, and connect with each other (not just where they conflict — see the conflict matrix for that). One row per interaction that shapes slicing or sequencing.

| From → To | At which activity | Interaction | Becomes |
|---|---|---|---|
| <persona A> → <persona B> | <activity> | <handoff / dependency / shared touchpoint> | <cross-persona `depends_on` / handoff annotation / sequencing note> |

A handoff that crosses a slice boundary is a slice-1 feasibility risk — the downstream persona's story can't ship without the upstream one. Omit this section only when there is a single persona.

## User activities (the backbone)

The narrative flow, left-to-right, in user voice:

1. <Activity 1>
2. <Activity 2>
3. <Activity 3>
4. ...

See `storymap.md` for tasks and stories under each.

## Opportunities

What changes for users if each activity is well-supported. One line per activity.

| Activity | Opportunity |
|---|---|
| <Activity 1> | <user benefit> |
| <Activity 2> | <user benefit> |

## Hypotheses

The bets we're making that could be wrong. Mark which slice will validate each.

| # | Hypothesis | Validates in slice | Method |
|---|---|---|---|
| H1 | <e.g., users will accept <constraint> if <benefit>> | walking-skeleton | <usability test \| metric \| interview> |
| H2 | ... | ... | ... |

## Constraints

- **Hard deadlines:** <dates and why they're hard>
- **Platform / integrations:** <what we have to work with>
- **Team / skills:** <what we have, what would stretch us>

## Non-goals

What is explicitly out of scope. Recording these prevents re-litigation.

- <Thing 1 that someone will ask about>
- <Thing 2>

## Open questions

- <Question we can't answer yet but will need to>
- <...>

## Decisions log

| Date | Decision | Reasoning |
|---|---|---|
| YYYY-MM-DD | <e.g., chose Now/Next/Later over WSJF> | <why> |
