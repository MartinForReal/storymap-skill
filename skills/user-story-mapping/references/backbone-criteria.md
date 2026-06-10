# Backbone criteria — choosing the right shape for the backbone

A backbone can be generated under different framing choices, and the choice changes the backbone's shape. **Pick the criteria explicitly, confirm with the user, and record them in `design.md` so future runs reproduce the same backbone.**

## The six criteria to declare (default in **bold**)

| Criterion | Options | Why it matters |
|---|---|---|
| **Frame** | **Activity flow** / Jobs-to-be-done / System interaction / Customer journey | Activity flow = Patton classic; JTBD = "when [situation] I want to [motivation] so I can [outcome]"; system interaction reads like API/touchpoints — pick one and stick with it |
| **Persona perspective** | **Primary user** (one specified by user) / Multiple parallel personas (admin + end-user) / Aggregate across personas | When personas diverge (admin vs end-user), single-perspective is cleaner; parallel risks doubling the backbone |
| **Time horizon** | **Single end-to-end session** / Day-in-the-life / Lifecycle (signup → power user → churn) | Affects how many activities. Session: 4-6. Day-in-life: 6-10. Lifecycle: 8-15. |
| **Granularity** | **5-7 activities** / 3-5 (high-level) / 8-12 (detailed) | Story-mapping convention is 5-7. Fewer is harder to slice; more is hard to read. |
| **Scope** | **Happy path only** / Happy path + error recovery / Full surface (incl. edge cases) | Happy path is the right default; recovery paths usually become slice-2/3 stories |
| **Aggregation** | **Single role per activity** / Multiple roles per activity (collaboration arrows) | Single-role is cleaner; multi-role only when handoffs ARE the activity |

## Workflow

1. **Propose criteria** based on context loop findings and user prompt
2. **Confirm with the user** in a single message: "Proposing backbone with these criteria: [list]. Confirm or override?"
3. **Record the confirmed criteria** in `design.md` under a `## Backbone criteria` section
4. **Generate the backbone** using those criteria
5. In **Mode D** (refinement) and re-runs: read the prior criteria from `design.md` and use the same ones unless the user explicitly says to change them — this keeps the backbone reproducible

When the user is silent (single-shot / automated mode), apply defaults and explicitly state "Applied defaults: [list]. Override by re-running with criteria= …" in `design.md`. Never silently choose without disclosure.

## Why this matters

Without explicit criteria, two runs of the skill on the same prompt may produce different backbones — one agent picks "activity flow", another picks "jobs-to-be-done", another picks "lifecycle". The downstream slicing and prioritization differ. Recording the criteria makes the backbone:

- **Reproducible** — same prompt + same criteria + same context = same backbone
- **Reviewable** — a stakeholder can see *why* this backbone shape was chosen
- **Refinable** — Mode D extension uses the same criteria so additions are consistent

## Backbone rules (apply regardless of criteria)

Backbone activities written in user voice, present tense, active.

- ✅ Good: `Sign up`, `Find a property`, `Schedule a viewing`, `Make an offer`
- ❌ Bad: `User onboarding flow`, `Search functionality`, `Booking module`, `Offer submission API`

System language (modules, APIs, services) leaks implementation thinking into a discovery artifact and breaks the slicing logic later.

**CRITICAL: Cross-cutting work doesn't belong in the backbone.** Tech debt, infrastructure, localization, theming, observability, compliance — give them their own `## Non-backbone / cross-cutting` section *below* the activity backbone, with `### Theme:` headers. They still get prioritized in `backlog.csv` (with `activity = "Non-backbone: <theme>"`) but are excluded from the slice-1 coverage check.

- ❌ Wrong: 6 backbone columns where #6 is "Tech debt" — breaks the slice-1 coverage rule (no user-facing story to put under it).
- ✅ Right: 5 user-activity columns + a `## Non-backbone / Tech debt` section below. Backbone stays a narrative.

Rule of thumb: if you can't write "As a `<user>`, I want to..." that ties to a single backbone column, the item is cross-cutting.

## Common anti-patterns

- **System-shaped backbones** (Login, Database, API) — useless for slicing because there's no user journey to demo
- **Time-as-backbone** (Week 1, Week 2, Week 3) — that's a schedule, not a story map; slicing already handles time
- **Mixing personas across activities** (Activity 1 is admin-flow, Activity 2 is end-user-flow) — pick a perspective and stick with it, or use parallel-personas explicitly
- **Single-activity sprawl** — if Activity 1 has 12 stories and Activities 2-5 have 1 each, the granularity is wrong; re-derive
- **Skipping the "criteria recorded" step** — even if the user is silent, document the defaults you applied; future Mode D runs will collapse without it
