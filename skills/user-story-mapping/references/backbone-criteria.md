# Backbone criteria — choosing the right shape for the backbone

The backbone is present-tense, active **user-voice activities** chosen under **six explicitly declared criteria** recorded in `design.md`. Anything not tied to one user-activity column — tech debt, infrastructure, localization, theming, observability, compliance — is **cross-cutting** and belongs in `## Non-backbone / cross-cutting` *below* the backbone, never as a sixth column. This defines both choices.

## When to use

Use during Step 1 and non-empty-baseline iteration to decide framing, consistency, and classification. Test: can I write `As a <user>, I want to…` tied to one column? [slicing-strategies.md](slicing-strategies.md) and SKILL.md Rule 4.

## The six criteria to declare (default in **bold**)

Framing changes shape; pick, confirm, record criteria.

| Criterion | Options | Why it matters |
|---|---|---|
| **Frame** | **Activity flow** / Jobs-to-be-done / System interaction / Customer journey | Activity flow = Patton classic; JTBD = "when [situation] I want to [motivation] so I can [outcome]"; system interaction = API/touchpoints |
| **Persona perspective** | **Primary user** (one specified by user) / Multiple parallel personas (admin + end-user) / Aggregate across personas | Divergent personas (admin vs end-user) favor single-perspective; parallel can double columns |
| **Time horizon** | **Single end-to-end session** / Day-in-the-life / Lifecycle (signup → power user → churn) | Controls count. Session: 4-6. Day-in-life: 6-10. Lifecycle: 8-15. |
| **Granularity** | **5-7 activities** / 3-5 (high-level) / 8-12 (detailed) | Convention is 5-7; fewer is hard to slice, more hard to read. |
| **Scope** | **Happy path only** / Happy path + error recovery / Full surface (incl. edge cases) | Happy path default; recovery paths usually become slice-2/3 stories |
| **Aggregation** | **Single role per activity** / Multiple roles per activity (collaboration arrows) | Single-role cleaner; multi-role only when handoffs ARE activity |

## Workflow — propose, confirm, record, generate

1. **Propose criteria** from context-loop findings and prompt.
2. **Confirm** in one message: "Proposing backbone with these criteria: [list]. Confirm or override?"
3. **Record confirmed criteria** in `design.md` under `## Backbone criteria`.
4. **Generate the backbone** with those criteria.
5. **On a non-empty baseline (re-runs / iteration):** reuse prior `design.md` criteria unless the user changes them.

When user is silent (single-shot / automated mode), apply defaults and write "Applied defaults: [list]. Override by re-running with criteria= …" in `design.md`. Never choose silently.

### Why recording the criteria matters

Without criteria, one prompt may yield "activity flow", "jobs-to-be-done", or "lifecycle", causing slicing/prioritization drift. Recording makes it:

- **Reproducible** — same prompt + same criteria + same context = same backbone.
- **Reviewable** — stakeholders see *why* this shape was chosen.
- **Refinable** — iterations extend with the same criteria, so additions stay consistent.

## Backbone voice rules (apply regardless of criteria)

Use **user voice, present tense, active**.

- ✅ Good: `Sign up`, `Find a property`, `Schedule a viewing`, `Make an offer`
- ❌ Bad: `User onboarding flow`, `Search functionality`, `Booking module`, `Offer submission API`

System language (modules, APIs, services) leaks implementation and breaks slicing. In `storymap.md`, each backbone activity is a `## Activity:` heading; its steps are `### Task:` headings beneath it.

## Cross-cutting / non-backbone work — the full rule

**Cross-cutting work does not belong in the backbone.** Put tech debt, infrastructure, localization, theming, observability, and compliance *below* it.

**The test:** if you cannot write "As a `<user>`, I want to…" for a **single backbone column**, the item is cross-cutting. (Story form is `As a/an <persona>, I want to <action>, so that <outcome>`.)

**The encoding the parser reads.** Put cross-cutting under `## Non-backbone / cross-cutting`; each theme is a `### Theme:` header. Items are prioritized in `backlog.csv` and surface in `storymap.csv` with `activity = "Non-backbone: <theme>"`, but **excluded from the slice-1 coverage check** (active backbone activities only — see [slicing-strategies.md](slicing-strategies.md)). Parser accepts either:

- `## Non-backbone / cross-cutting` + `### Theme: <theme>` (themed section), or
- a `## Activity: Non-backbone: <theme>` line directly.

Either way, the CSV renders `activity = "Non-backbone: <theme>"`. Never add a sixth backbone column for tech debt or infra.

- ❌ Wrong: 6 backbone columns where #6 is "Tech debt" — no user-facing story fits under it, so slice-1 coverage breaks.
- ✅ Right: 5 user-activity columns + `## Non-backbone / Tech debt` below. The backbone stays narrative.

SKILL.md Rule 4 states this in one line (see [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run)); this file owns mechanics and encoding.

## Common anti-patterns

- **System-shaped backbones** (Login, Database, API) — no user journey to demo; slicing fails.
- **Time-as-backbone** (Week 1, Week 2, Week 3) — schedule, not story map; slicing handles time.
- **Mixing personas across activities** (Activity 1 admin-flow, Activity 2 end-user-flow) — pick one perspective or use parallel-personas explicitly.
- **Single-activity sprawl** — Activity 1 has 12 stories while Activities 2-5 have 1 each; re-derive.
- **Burying a user activity below the line** — if `As a <user>, I want to…` fits one column, put it *on* the backbone.
- **Skipping "criteria recorded"** — document defaults even when the user is silent; iterations depend on them.
