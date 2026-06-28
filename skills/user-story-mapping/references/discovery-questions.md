# Discovery questions

When sources are empty or sparse, ask four batched rounds — outcome/users, end-to-end activity, constraints, scope edges — in order, 3–5 questions per batch, until the user confirms a one-paragraph project description. Outcomes before features; draft before abstraction.

## When to use

Use these banks in the loop's interview stage, only for gaps sources could not fill: verbal ideas with no codebase, tracker, or backlog; or thin briefs where Step 0 found nothing usable. Skip answers already in README, code, tests, or tracker. User-stated and interview answers outrank inferred answers; see [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run).

Ask in batches, skip obvious answers, and gather only enough signal to draft a backbone.

## Round 1 — Outcome and users

Round 1 identifies success and who experiences it. Ask only if unanswered.

1. **Outcome** — "What will be measurably different in 6 months? For whom?"
2. **Trigger** — "What changed to make this worth doing now?"
3. **Primary users** — "Who uses this day-to-day? If multiple, whom are we optimizing for?"
4. **Counter-stakeholders** — "Who might lose something or be inconvenienced?" (often the most useful question)
5. **Definition of done** — "What signal says we shipped enough?"

Do not ask about features yet. Outcomes first.

## Round 2 — The end-to-end activity

Walk one user through a complete instance, from before start to after finish.

1. **Trigger event** — "What makes the user open this?"
2. **First action** — "What's the first thing they do?"
3. **Middle steps** — "Then what? Walk me through it like a tour."
4. **End state** — "How do they know they're done?"
5. **What happens next** — "What do they do *after* this is over?"

(5) often reveals a missing right-edge backbone activity: cleanup / handoff / followup.

## Round 3 — Constraints and unknowns

1. **Hard deadlines** — "Any immovable dates? Why?" (regulatory, contracts, dependencies)
2. **Platform constraints** — "What must this run on / integrate with?"
3. **Skill constraints** — "What does the team know? What would stretch them?"
4. **Knowns vs. assumptions** — "What feels certain? What feels like a guess?"
5. **Past attempts** — "Any prior attempts? What happened?"

The knowns/assumptions split in (4) populates `design.md` **Hypotheses**. Every assumption is a slice-1 validation candidate.

## Round 4 — Scope edges

1. **Out of scope** — "What is explicitly *not* included?"
2. **Adjacent systems** — "What does this touch but not own?"
3. **Future-but-not-now** — "What should wait? Why?"
4. **Personas you're excluding** — "Who are we not serving in this version?"

Round 4 feeds the **Won't** column in MoSCoW, the **(Not on roadmap)** bucket in Now/Next/Later, and `design.md` **Non-goals**.

## When to stop asking

Stop when the user accepts a one-paragraph project description with "yes, that's it" and no corrections. Draft the backbone; answer later questions against it.

## Anti-patterns

- **Asking too long before showing anything** — propose a draft backbone after Round 2 if possible; concrete feedback beats abstract.
- **Letting features replace activities** — if they say "we need search, filtering, and sorting" redirect: "Walk me through the moment a user wants to find something. What do they do?"
- **Treating first answers as final** — assumptions surface mid-discovery; revise the backbone in real time.
