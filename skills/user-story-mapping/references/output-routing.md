# Where the items land — output-routing decision

Route by baseline, not chat: **empty baseline (no tracker defined) → seed an issue tracker**; **non-empty baseline (tracker defined) → persist to sister-framework state, `TODO.md`, or Memory MCP** and never push into curated queues uninvited. Wrong: stories pollute Jira; chat-only plans evaporate.

## When to use

At Step 5/6, after backbone, slices, and ranked backlog. Routing hinges on "is a tracker defined?" — detector owned here. `TodoWrite` is in-session only; pair it with persistence before coding.

## The decision in one sentence

**Empty baseline (no tracker defined) → seed an issue tracker.** **Non-empty baseline (tracker defined) → framework state, `TODO.md`, or Memory MCP.** `TodoWrite` is orthogonal — pair with persistence; never system of record.

## Detecting the empty baseline (no tracker defined)

Detector for the **"tracker defined" test** — predicate stated once in [../SKILL.md#the-loop](../SKILL.md#the-loop). Step 0 decides from data, not labels, then reuses it for routing, **which files get produced** ([§ What each branch produces](#what-each-branch-produces)), conditional `storymap.mmd`, and burn-down write-back.

ALL following = empty baseline / **no tracker defined**:

- No package manifest (`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Gemfile`)
- No populated `.git` history (≤3 commits, all setup)
- User's prompt didn't mention an existing tracker, ticket id, or running system
- No tracker MCP used during Step 0
- No `.gsd/`, `.superpowers/`, or `.user-story-mapping/`

Any failure → **non-empty baseline / tracker defined** (the "existing" branch). Generic company-tool mention — no MCP, no project for *this* work — does **not** count. Decide once in Step 0; don't re-derive at Step 6.

Edge cases:

| Signal | Branch |
|---|---|
| Mature repo, but user says "ignore the existing backlog, this is a clean PI" | Empty baseline — user override wins per the user-input-authoritative priority order ([../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run)) |
| Empty working dir, but user says "this is for the existing `acme-billing` repo, I just haven't cloned it" | Tracker defined — the project exists even if the working dir doesn't |

When signals conflict, **ask once**: "new (seed tracker) or existing (keep in framework state)?"

## What each branch produces

The output **set** depends on: **is an issue tracker (Jira / ADO / GitHub Issues / Linear) system of record?** (`.gsd/`-style state is non-empty baseline but *not* issue tracker.) Tiers: [../SKILL.md § What it produces](../SKILL.md#what-it-produces).

- **Always, every run:** `design.md` (create if absent; if gstack/Superpowers already wrote it, preserve their sections and append/update this skill's story-map addendum) + `storymap.md` (parser/import narrative) + `storymap.csv` (flat items+status manifest; deterministic `storymap.md` projection).
- **No issue tracker** (empty baseline *or* existing project whose system of record is framework state / `TODO.md`): also emit `storymap.mmd`, `backlog.md`, and `backlog.csv` for navigation/ranking. Persist/seed below.
- **Issue tracker defined:** do **not** emit `storymap.mmd` / `backlog.{md,csv}`; tracker provides navigation/ranking. Opt-in write-back sets **burn-down fields** (points + sprint + status) — see [work-item-tracking.md § Enable the tracker burn-down](work-item-tracking.md#enable-the-tracker-burn-down). Put ranked "start here" in `handoff.md`; still produce `storymap.csv` as manifest.

## The seed branch (empty baseline)

Goal: create tracker from `backlog.csv`.

Pick tracker via [work-item-tracking.md](work-item-tracking.md#decision-tree-for-the-user): GitHub-remote / ADO-remote / Linear / Jira / ask-user. Generate import script; don't auto-run it. Write `.user-story-mapping/state.json` per [persistent-knowledge.md §A](persistent-knowledge.md), including `tracker`, for future iterations.

Do NOT write to `TODO.md` or Memory MCP here — tracker is system of record.

## The keep branch — persistence cascade (tracker defined)

Walk in order. Write to **the first destination that applies**; optionally add Memory MCP.

### 1. Sister-framework state (highest priority when present)

| Detected | Where to write |
|---|---|
| `.gsd/` | `.gsd/Roadmap.md` (append); slice-1 → `.gsd/Milestones/M<n>/` |
| `.superpowers/` or `plans/` in use by Superpowers | `plans/<dated-name>.md` next to existing plans |
| `.user-story-mapping/` from a prior run | `.user-story-mapping/state.json` delta + `decisions.log.md` append |

Conventions: [framework-integration.md](framework-integration.md) (gstack / GSD / Superpowers handoff lines) and [persistent-knowledge.md §A](persistent-knowledge.md) (`.user-story-mapping/` schema). Don't invent shapes.

### 2. Plain `TODO.md` at the repo root (universal fallback)

Default for code + history with no framework state.

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

**Always append, never overwrite.** If `TODO.md` exists, add a dated section with a `---` rule above it.

### 3. Anthropic Memory MCP (cross-session recall)

Use when `mcp__*_memory__*` is available AND user opted in or asked to "remember". Project / PI / hypothesis shapes live in [persistent-knowledge.md §B](persistent-knowledge.md) — don't duplicate them. Add one entity per slice-1 story; skip deferred:

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

`TodoWrite` is not persistence. If the user will execute slice 1 now, populate the working list:

```
TodoWrite([
  { content: "Sign in via SSO (CS rep, WSJF 22)", activeForm: "Implementing SSO sign-in", status: "pending" },
  ...
])
```

Slice-1 stories only — not full backlog. **Always pair with one of the three persistence destinations above**; `TodoWrite` dies with the session.

## The handoff line

Tell the user landing spot and next step:

```
"Slice 1 (12 stories) → .gsd/Roadmap.md + .user-story-mapping/state.json;
 8 loaded into TodoWrite. Run /gsd discuss when ready."
```

```
"Slice 1 (12 stories) → TODO.md at repo root. Import script for GitHub Projects
 at storymap.csv if you want a board later."
```

## Anti-patterns

- **Pushing to a populated tracker without asking.** Mature backlog = curated queue. Seed only on empty baseline; require opt-in for defined tracker.
- **Silently overwriting `TODO.md`.** Always append with dated header.
- **Dumping the full backlog into TodoWrite.** Slice 1 only — working list, not archive.
- **Using TodoWrite alone when a tracker is defined.** It evaporates.
- **Re-deriving the baseline at Step 6.** Decide "tracker defined?" once in Step 0; late flips change routing and `storymap.mmd` shipping.

## Cross-references

- Tracker mechanics: [work-item-tracking.md](work-item-tracking.md)
- Sister-framework conventions: [framework-integration.md](framework-integration.md)
- `.user-story-mapping/` schema + Memory MCP shapes: [persistent-knowledge.md](persistent-knowledge.md)
- Memory opt-in: [persistent-knowledge.md](persistent-knowledge.md#the-opt-in-lifecycle)
