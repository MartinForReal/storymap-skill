# Decomposition into tasks and per-persona stories (Step 2)

Decompose backbone activities into user tasks and deliverable per-persona stories. At **≥3 personas, run the generation as a parallel `Agent` sweep** — one subagent per persona — then merge and dedupe. This generate/update stage turns the backbone into attributed stories.

## When to use

Step 2 runs after the backbone is set (Step 1) and before slicing (Step 3). On a non-empty baseline (an iteration), carry prior tasks/stories forward — see [On a non-empty baseline](#on-a-non-empty-baseline).

## Tasks and stories

- **Tasks** = user steps within an activity.
- **Stories** = deliverable increments under tasks. Use **As a/an `<persona>`, I want to `<action>`, so that `<outcome>`** unless noisy.
- If a task has **>7 stories**, split it.
- **Stories are a blueprint, not the final spec.** They capture *intent*, not *behavior*; Step 4a (Gherkin acceptance criteria) and Step 4b (E2E contract) pin behavior down. Implementation detail ("click a React button that calls `/api/v1/refunds` with an idempotency key…") belongs in ACs.

Each `storymap.md` story bullet carries `[slice:<id>]` (required), optionally `[persona:<name>]` and `[status:<state> | <evidence>]`. Derived `storymap.csv` IDs are `S001`…, document-order, parser-regenerated — never hand-assigned here.

## Per-persona coverage is mandatory

Every persona in `design.md` must be the `<persona>` of **at least one slice-1 story**. This is Rule 2 in [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run); [slicing-strategies.md](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations) owns mechanics and violations. Step 2 supplies raw material so slice 1 doesn't optimize only for the loudest persona.

- One activity can produce stories for multiple personas (e.g. "Sign in" → admin SSO setup, end-user sign-in, compliance role-claim verification).
- Stories with no persona (pure infra / cron) live in the cross-cutting section and **do not** count toward coverage.
- If a persona has **zero** slice-1 candidates, treat it as a signal — **never** a silent drop. [slicing-strategies.md](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations) owns re-slice vs. re-derive.

## Parallelize via the `Agent` tool when persona count ≥3

Spawn **one subagent per persona**. Each receives:

- the backbone,
- that persona's verbatim quotes / pain points / constraints,
- **the full persona roster** (so it can spot cross-persona handoffs — see below),
- the story-form template, and
- an "in-character" instruction.

Run one message with multiple `Agent` calls. Then **merge, dedupe, and flag conflicts**: duplicate activity across personas is often one story from different angles. Keep the most user-voiced framing, fold in the rest, and mark genuine conflicts. For **≤2 personas**, generate inline; the sweep isn't worth it.

Attribute stories by the priority order in [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run): real user quote beats simulated invention, and the bullet's source tag records provenance.

## Refine the cross-persona interaction map

The `## Persona interactions` map is **first built at Step 0.3** (pre-interview simulation) from anticipated activities. Step 2 **refines** it against the real backbone: bind interactions to activities, finalize `H:` `depends_on` edges where one persona preconditions another, and fold in handoffs subagents find.

The full protocol — interaction-map table, handoff → cross-persona `depends_on` edge, conflict routing, slice-1 feasibility risk — lives in [persona-simulation-and-gap-filling.md](persona-simulation-and-gap-filling.md) (protocol Step 4 — Aggregate: the persona interaction map). Don't re-derive it; refine activity bindings and link.

## On a non-empty baseline

On an existing codebase or tracker (an iteration), treat routes / components / handlers / endpoints as **pre-existing task candidates** under their activity. Reuse team naming and tracker epics / components / labels read-only; don't invent parallel taxonomy ([work-item-tracking.md](work-item-tracking.md#align-to-the-existing-tracker-taxonomy) owns reuse). Carry prior task/story IDs forward; new items get `max(prior_id) + 1` — never renumber.

## Anti-patterns

- **Generating 80+ stories then running out of turns.** The common failure. Cap proactively (≤50 total, slice-1 ≤15).
- **Writing implementation detail into stories.** Step 4a/4b territory; endpoint/button names over-specify.
- **Skipping the parallel sweep at ≥3 personas** and hand-rolling serially — slow, biased toward the first persona.
- **Silently dropping a persona with no slice-1 candidate** instead of re-running Step 3 or Step 1.
- **Inventing a new tracker epic/component** on an iteration when an existing one fits — drift instead of reuse.

## Cost ceiling

Step 2 should consume **15-20%** of the run budget. With ≥3 personas, the parallel sweep is the bulk; cap stories (≤50 total, slice-1 ≤15). Generating 80+ stories and running out of turns is the dominant failure.
