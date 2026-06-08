# Discovery questions

For Mode A (from-scratch) invocations. Ask in batches of 3–5, not one at a time. Skip questions whose answer is already obvious from context.

## Round 1 — Outcome and users

The goal of round 1 is to find out what success looks like and who experiences it. If you can't answer these from the user's first message, ask them.

1. **Outcome** — "If this work succeeds, what will be measurably different in 6 months? For whom?"
2. **Trigger** — "What changed recently that makes this worth doing now?"
3. **Primary users** — "Who actually uses this day-to-day? If multiple, which one are we optimizing for?"
4. **Counter-stakeholders** — "Who might lose something or be inconvenienced by this?" (often the most useful question)
5. **Definition of done** — "How will you know we shipped enough? What signal closes this work?"

Resist the urge to ask about features yet. Outcomes first.

## Round 2 — The end-to-end activity

Walk a single user through a complete instance of the goal, from before they start until after they're done.

1. **Trigger event** — "What makes the user open this in the first place?"
2. **First action** — "What's the very first thing they do?"
3. **Middle steps** — "Then what? And then? Walk me through it like a tour."
4. **End state** — "How do they know they're done?"
5. **What happens next** — "What do they do *after* this is over?"

The point of (5) is that it often reveals a missing activity at the right edge of the backbone. People forget the cleanup / handoff / followup stages.

## Round 3 — Constraints and unknowns

1. **Hard deadlines** — "Any dates we can't move? Why?" (regulatory, contracts, dependencies)
2. **Platform constraints** — "What does this need to run on / integrate with?"
3. **Skill constraints** — "What does the team know? What would be a stretch?"
4. **Knowns vs. assumptions** — "What about this work feels certain? What feels like a guess?"
5. **Past attempts** — "Has anyone tried solving this before? What happened?"

The split between knowns and assumptions in (4) is what populates the **Hypotheses** section of `design.md`. Anything an assumption is a candidate for early validation in slice 1.

## Round 4 — Scope edges

1. **Out of scope** — "What is explicitly *not* part of this work?"
2. **Adjacent systems** — "What does this touch but not own?"
3. **Future-but-not-now** — "What feels in scope but should wait? Why?"
4. **Personas you're excluding** — "Are there users we're choosing not to serve in this version?"

The answers to round 4 become the **Won't** column in MoSCoW or the **(Not on roadmap)** bucket in Now/Next/Later, and the **Non-goals** section of `design.md`.

## When to stop asking

Stop when you can write a one-paragraph project description that the user reads and says "yes, that's it" without corrections. That's enough signal to draft a backbone. Further questions are better answered against a draft than in the abstract.

## Common pitfalls in this phase

- **Asking too many questions before showing anything** — propose a draft backbone after Round 2 if possible. Concrete-vs-abstract feedback is better.
- **Letting the user list features instead of activities** — if they say "we need search, filtering, and sorting" gently redirect: "Walk me through the moment a user wants to find something. What do they do?"
- **Treating the first answer as final** — assumptions surface mid-discovery. Be willing to revise the backbone in real time.
