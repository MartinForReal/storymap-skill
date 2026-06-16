# Backbone criteria — choosing the right shape for the backbone

The backbone is a row of **user-voice activities**, written present-tense and active, chosen under **six explicitly declared criteria** that you record in `design.md` so future runs reproduce the same shape. Anything that isn't a user activity tied to one backbone column — tech debt, infrastructure, localization, theming, observability, compliance — is **cross-cutting** and lives in a `## Non-backbone / cross-cutting` section *below* the backbone, never as a sixth column. This file owns both: how to choose the backbone, and where everything that isn't backbone goes.

## When to use

Reach for this during Step 1 (define the backbone) and whenever you extend an existing backbone on a non-empty baseline (the loop running on prior data — iteration). Use it to decide the backbone's framing, to keep two runs of the same prompt from producing different backbones, and — most often — to decide whether a candidate item belongs *on* the backbone or *below* it as cross-cutting work. The cross-cutting test ("can I write `As a <user>, I want to…` tied to one column?") is the single most reused rule here; [slicing-strategies.md](slicing-strategies.md) and SKILL.md Rule 4 link straight to it.

## The six criteria to declare (default in **bold**)

A backbone can be generated under different framing choices, and the choice changes its shape. Pick the criteria explicitly, confirm with the user, and record them.

| Criterion | Options | Why it matters |
|---|---|---|
| **Frame** | **Activity flow** / Jobs-to-be-done / System interaction / Customer journey | Activity flow = Patton classic; JTBD = "when [situation] I want to [motivation] so I can [outcome]"; system interaction reads like API/touchpoints — pick one and stick with it |
| **Persona perspective** | **Primary user** (one specified by user) / Multiple parallel personas (admin + end-user) / Aggregate across personas | When personas diverge (admin vs end-user), single-perspective is cleaner; parallel risks doubling the backbone |
| **Time horizon** | **Single end-to-end session** / Day-in-the-life / Lifecycle (signup → power user → churn) | Affects how many activities. Session: 4-6. Day-in-life: 6-10. Lifecycle: 8-15. |
| **Granularity** | **5-7 activities** / 3-5 (high-level) / 8-12 (detailed) | Story-mapping convention is 5-7. Fewer is harder to slice; more is hard to read. |
| **Scope** | **Happy path only** / Happy path + error recovery / Full surface (incl. edge cases) | Happy path is the right default; recovery paths usually become slice-2/3 stories |
| **Aggregation** | **Single role per activity** / Multiple roles per activity (collaboration arrows) | Single-role is cleaner; multi-role only when handoffs ARE the activity |

## Workflow — propose, confirm, record, generate

1. **Propose criteria** based on context-loop findings and the user prompt.
2. **Confirm with the user** in a single message: "Proposing backbone with these criteria: [list]. Confirm or override?"
3. **Record the confirmed criteria** in `design.md` under a `## Backbone criteria` section.
4. **Generate the backbone** using those criteria.
5. **On a non-empty baseline (re-runs / iteration):** read the prior criteria from `design.md` and reuse the same ones unless the user explicitly says to change them — this keeps the backbone reproducible.

When the user is silent (single-shot / automated mode), apply the defaults and explicitly state "Applied defaults: [list]. Override by re-running with criteria= …" in `design.md`. Never silently choose without disclosure.

### Why recording the criteria matters

Without explicit criteria, two runs of the skill on the same prompt may produce different backbones — one agent picks "activity flow", another "jobs-to-be-done", another "lifecycle" — and the downstream slicing and prioritization diverge. Recording the criteria makes the backbone:

- **Reproducible** — same prompt + same criteria + same context = same backbone.
- **Reviewable** — a stakeholder can see *why* this backbone shape was chosen.
- **Refinable** — an iteration extends with the same criteria, so additions stay consistent.

## Backbone voice rules (apply regardless of criteria)

Backbone activities are written in **user voice, present tense, active**.

- ✅ Good: `Sign up`, `Find a property`, `Schedule a viewing`, `Make an offer`
- ❌ Bad: `User onboarding flow`, `Search functionality`, `Booking module`, `Offer submission API`

System language (modules, APIs, services) leaks implementation thinking into a discovery artifact and breaks the slicing logic later. In `storymap.md`, each backbone activity is a `## Activity:` heading; its steps are `### Task:` headings beneath it.

## Cross-cutting / non-backbone work — the full rule

**Cross-cutting work does not belong in the backbone.** Tech debt, infrastructure, localization, theming, observability, compliance — give them their own section *below* the activity backbone.

**The test:** if you can't write "As a `<user>`, I want to…" that ties to a **single backbone column**, the item is cross-cutting. (Story form is `As a/an <persona>, I want to <action>, so that <outcome>`.)

**The encoding the parser reads.** Put cross-cutting work under a `## Non-backbone / cross-cutting` section, with each theme as a `### Theme:` header. These items still get prioritized in `backlog.csv` and surface in `storymap.csv` with `activity = "Non-backbone: <theme>"`, but they are **excluded from the slice-1 coverage check** (which only spans active backbone activities — see [slicing-strategies.md](slicing-strategies.md)). Both encodings the parser accepts are equivalent:

- `## Non-backbone / cross-cutting` + `### Theme: <theme>` (themed section), or
- a `## Activity: Non-backbone: <theme>` line directly.

Either way the CSV renders `activity = "Non-backbone: <theme>"`. Never add a sixth backbone column for tech debt or infra.

- ❌ Wrong: 6 backbone columns where #6 is "Tech debt" — breaks the slice-1 coverage rule, because there's no user-facing story to put under it.
- ✅ Right: 5 user-activity columns + a `## Non-backbone / Tech debt` section below. The backbone stays a narrative.

The one-line statement of this rule lives in SKILL.md Rule 4 (see [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run)); the full mechanics and encoding are owned here.

## Common anti-patterns

- **System-shaped backbones** (Login, Database, API) — useless for slicing because there's no user journey to demo.
- **Time-as-backbone** (Week 1, Week 2, Week 3) — that's a schedule, not a story map; slicing already handles time.
- **Mixing personas across activities** (Activity 1 is admin-flow, Activity 2 is end-user-flow) — pick a perspective and stick with it, or use parallel-personas explicitly.
- **Single-activity sprawl** — if Activity 1 has 12 stories and Activities 2-5 have 1 each, the granularity is wrong; re-derive.
- **Burying a user activity below the line** — if you *can* write `As a <user>, I want to…` for it tied to one column, it belongs *on* the backbone, not in the cross-cutting section.
- **Skipping the "criteria recorded" step** — even if the user is silent, document the defaults you applied; future iterations will collapse without them.
