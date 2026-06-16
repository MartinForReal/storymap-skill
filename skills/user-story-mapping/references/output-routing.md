# Where the items land — output-routing decision

Route by the baseline, not by chat: an **empty baseline (no tracker defined) → seed an issue tracker** so the team has somewhere to work; a **non-empty baseline (tracker defined) → persist to sister-framework state, a plain `TODO.md`, or Memory MCP** and never push into the curated queue uninvited. Wrong destination is expensive both ways — pushing 50 fresh stories into a mature Jira backlog pollutes a curated work queue; keeping the plan only in chat means it evaporates.

## When to use

Read this at Step 5/6, once the backbone, slices, and ranked backlog exist and you must decide where the items physically go. The routing decision hinges on one predicate computed earlier — "is a tracker defined?" — whose operational detector this file owns (below). Claude Code's `TodoWrite` is an orthogonal in-session execution helper, covered here too — pair it with a persistent destination when the user is about to code.

## The decision in one sentence

**Empty baseline (no tracker defined) → seed an issue tracker.** **Non-empty baseline (tracker defined) → persist to framework state, plain `TODO.md`, or Memory MCP.** `TodoWrite` is orthogonal — pair it with a persistent destination, never use it as the system of record.

## Detecting the empty baseline (no tracker defined)

This is the operational detector for the **"tracker defined" test** — the predicate itself is stated once in [../SKILL.md#the-loop](../SKILL.md#the-loop). The loop decides it once in Step 0 — from the data sources, not from anything the user labels the work — and reuses it everywhere: the routing below, **which files get produced** ([§ What each branch produces](#what-each-branch-produces)), the conditional `storymap.mmd`, and the tracker burn-down write-back.

ALL of the following = empty baseline / **no tracker defined**:

- No package manifest (`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Gemfile`)
- No populated `.git` history (≤3 commits, all setup)
- User's prompt didn't mention an existing tracker, ticket id, or running system
- No tracker MCP used during Step 0
- No `.gsd/`, `.superpowers/`, or `.user-story-mapping/`

Any failure → **non-empty baseline / tracker defined** (the "existing" branch). A passing mention of a tool the company uses elsewhere — no MCP connected, no project named for *this* work — does **not** count as a tracker defined. Decide this once in Step 0 and reuse it; do not re-derive at Step 6.

Two edge cases worth knowing:

| Signal | Branch |
|---|---|
| Mature repo, but user says "ignore the existing backlog, this is a clean PI" | Empty baseline — user override wins per the user-input-authoritative priority order ([../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run)) |
| Empty working dir, but user says "this is for the existing `acme-billing` repo, I just haven't cloned it" | Tracker defined — the project exists even if the working dir doesn't |

When signals conflict, **ask once**: "treat as new (seed tracker) or existing (keep in framework state)?"

## What each branch produces

The output **set** keys off one thing: **is an issue tracker (Jira / ADO / GitHub Issues / Linear) the system of record?** — the "tracker defined" predicate above. (Sister-framework state like `.gsd/` is a non-empty baseline but *not* an issue tracker.) Canonical tier list: [../SKILL.md § What it produces](../SKILL.md#what-it-produces).

- **Always, every run:** `design.md` (rationale) + `storymap.md` (the authored narrative the parser/import reads).
- **No issue tracker** (empty baseline *or* an existing project whose system of record is framework state / `TODO.md`): also emit the local renderings — `storymap.csv`, `storymap.mmd`, `backlog.md`, `backlog.csv` — because the plan needs somewhere to live. Persist or seed them per the branches below.
- **Issue tracker defined:** do **not** emit those local data files; the tracker is the system of record. The plan goes into the tracker via the opt-in write-back, which also sets each item's **burn-down fields** (points + sprint + status) — see [work-item-tracking.md § Enable the tracker burn-down](work-item-tracking.md#enable-the-tracker-burn-down). The ranked "start here" summary moves into `handoff.md`.

## The seed branch (empty baseline)

Goal: give the team a tracker to work out of, populated from `backlog.csv`.

Pick the tracker per the decision tree in [work-item-tracking.md](work-item-tracking.md#decision-tree-for-the-user) — it covers the GitHub-remote / ADO-remote / Linear / Jira / ask-user logic. Generate the import script; don't auto-run it. Also write a thin `.user-story-mapping/state.json` per [persistent-knowledge.md §A](persistent-knowledge.md) (including the `tracker` block once a tracker is chosen) so a future iteration of the loop can find the tracker and stay consistent.

Do NOT also write to `TODO.md` or Memory MCP on this branch — the tracker is the system of record now.

## The keep branch — persistence cascade (tracker defined)

Walk in order. Write to **the first destination that applies**; optionally add Memory MCP if cross-session recall matters.

### 1. Sister-framework state (highest priority when present)

| Detected | Where to write |
|---|---|
| `.gsd/` | `.gsd/Roadmap.md` (append); slice-1 → `.gsd/Milestones/M<n>/` |
| `.superpowers/` or `plans/` in use by Superpowers | `plans/<dated-name>.md` next to existing plans |
| `.user-story-mapping/` from a prior run | `.user-story-mapping/state.json` delta + `decisions.log.md` append |

Conventions: [framework-integration.md](framework-integration.md) (gstack / GSD / Superpowers handoff lines) and [persistent-knowledge.md §A](persistent-knowledge.md) (the `.user-story-mapping/` schema). Don't invent new file shapes.

### 2. Plain `TODO.md` at the repo root (universal fallback)

Safe default for projects with code + history but no framework state.

```markdown
# TODO

> Updated 2026-06-09 by user-story-mapping skill — slice 1 of <project-name>
> See storymap.md / backlog.md for full context.

## Slice 1 — Walking skeleton (target: <date>)

- [ ] **Sign in via SSO** — *CS rep* — `WSJF: 22` — depends on: none
- [ ] **Find transaction by order id** — *CS rep* — `WSJF: 18` — depends on: Sign in
- [ ] **Issue full refund** — *CS rep* — `WSJF: 17` — depends on: Find transaction

## Deferred

- [ ] **Partial refunds** — *CS rep* — `WSJF: 9`
```

**Always append, never overwrite.** If `TODO.md` already exists, add a dated section with a `---` rule above it — the existing content is someone's prior work.

### 3. Anthropic Memory MCP (cross-session recall)

When `mcp__*_memory__*` is available AND the user has opted in or asked the skill to "remember" the plan. Project / PI / hypothesis entity shapes live in [persistent-knowledge.md §B](persistent-knowledge.md) — don't duplicate them. Add one new entity per slice-1 story (skip the deferred ones — too noisy):

```
Entity: story:S001
  observation: "Title: Sign in via SSO"
  observation: "Persona: CS rep"
  observation: "WSJF: 22"
  observation: "Status: not-started"
  relation: belongs-to → slice:<repo-name>:walking-skeleton
  relation: depends-on → story:S000   # if applicable
```

## Claude Code `TodoWrite` — orthogonal in-session helper

Not a persistence destination. When the user is about to execute slice 1 in the same Claude Code session, populate the in-session todo list so the stories appear in the working list:

```
TodoWrite([
  { content: "Sign in via SSO (CS rep, WSJF 22)", activeForm: "Implementing SSO sign-in", status: "pending" },
  ...
])
```

Slice-1 stories only — don't dump the full backlog. **Always pair with one of the three persistence destinations above**; `TodoWrite` dies with the session.

## The handoff line

Tell the user in one line where the items landed and what to do next:

```
"Slice 1 (12 stories) → .gsd/Roadmap.md + .user-story-mapping/state.json;
 8 loaded into TodoWrite. Run /gsd discuss when ready."
```

```
"Slice 1 (12 stories) → TODO.md at repo root. Import script for GitHub Projects
 at storymap.csv if you want a board later."
```

## Anti-patterns

- **Pushing to a populated tracker without asking.** A mature backlog is someone's curated queue. Seed only on an empty baseline; require explicit opt-in for a defined tracker.
- **Silently overwriting `TODO.md`.** Always append with a dated header.
- **Dumping the full backlog into TodoWrite.** Slice 1 only — it's a working list, not an archive.
- **Using TodoWrite alone when a tracker is defined.** It evaporates with the session.
- **Re-deriving the baseline at Step 6.** Decide "tracker defined?" once in Step 0 and reuse it; a late flip silently changes both routing and whether `storymap.mmd` ships.

## Cross-references

- Tracker mechanics + per-tool decision tree: [work-item-tracking.md](work-item-tracking.md)
- Sister-framework state conventions: [framework-integration.md](framework-integration.md)
- `.user-story-mapping/` schema + Memory MCP entity shapes: [persistent-knowledge.md](persistent-knowledge.md)
- Memory opt-in lifecycle: [persistent-knowledge.md](persistent-knowledge.md#the-opt-in-lifecycle)
