# Where the items land — output-routing decision

After the backbone, slices, and ranked backlog exist, decide where the items physically go. Wrong destination is expensive — pushing 50 fresh stories into a mature Jira backlog pollutes a curated work queue; keeping the plan only in chat means it evaporates.

## The decision in one sentence

**From-scratch project → seed an issue tracker.** **Existing project → persist to framework state, plain `TODO.md`, or Memory MCP.** Claude Code's `TodoWrite` is an orthogonal in-session execution helper — pair it with a persistent destination when the user is about to code.

## Detecting "from-scratch"

ALL of the following = from-scratch:

- No package manifest (`package.json` / `pyproject.toml` / `Cargo.toml` / `go.mod` / `Gemfile`)
- No populated `.git` history (≤3 commits, all setup)
- User's prompt didn't mention an existing tracker, ticket id, or running system
- No tracker MCP used during Step 0
- No `.gsd/`, `.superpowers/`, or `.user-story-mapping/`

Any failure → **existing**. Mode A invocation usually = from-scratch; Modes B/C/D usually = existing — but the signals above win over the Mode label.

Two edge cases worth knowing:

| Signal | Branch |
|---|---|
| Mature repo, but user says "ignore the existing backlog, this is a clean PI" | From-scratch (user override wins per the user-input-authoritative principle) |
| Empty working dir, but user says "this is for the existing `acme-billing` repo, I just haven't cloned it" | Existing — the project exists even if the working dir doesn't |

When signals conflict, **ask once**: "treat as new (seed tracker) or existing (keep in framework state)?"

## The from-scratch branch

Goal: give the team a tracker to work out of, populated from `backlog.csv`.

Pick the tracker per `work-item-tracking.md`'s "Decision tree for the user" section (it covers the GitHub-remote / ADO-remote / Linear / Jira / ask-user logic). Generate the import script — don't auto-run it. Also write a thin `.user-story-mapping/state.json` per `persistent-knowledge.md` §A so a future Mode-D run can find the tracker.

Do NOT also write to `TODO.md` or Memory MCP on this branch — the tracker is the system of record now.

## The existing-project persistence cascade

Walk in order. Write to **the first destination that applies**; optionally add Memory MCP if cross-session recall matters.

### 1. Sister-framework state (highest priority when present)

| Detected | Where to write |
|---|---|
| `.gsd/` | `.gsd/Roadmap.md` (append); slice-1 → `.gsd/Milestones/M<n>/` |
| `.superpowers/` or `plans/` in use by Superpowers | `plans/<dated-name>.md` next to existing plans |
| `.user-story-mapping/` from a prior run | `.user-story-mapping/state.json` delta + `decisions.log.md` append |

Conventions: `framework-integration.md` (gstack / GSD / Superpowers handoff lines) and `persistent-knowledge.md` §A (the `.user-story-mapping/` schema). Don't invent new file shapes.

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

When `mcp__*_memory__*` is available AND the user has opted in or asked the skill to "remember" the plan. Project / PI / hypothesis entity shapes live in `persistent-knowledge.md` §B — don't duplicate them. Add one new entity per slice-1 story (skip the deferred ones — too noisy):

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

- **Pushing to a populated tracker without asking.** A mature backlog is someone's curated queue. From-scratch detection + explicit opt-in for existing projects only.
- **Silently overwriting `TODO.md`.** Always append with a dated header.
- **Dumping the full backlog into TodoWrite.** Slice 1 only — it's a working list, not an archive.
- **Using TodoWrite alone on an existing project.** It evaporates with the session.

## Cross-references

- Tracker mechanics + per-tool decision tree: `work-item-tracking.md`
- Sister-framework state conventions: `framework-integration.md`
- `.user-story-mapping/` schema + Memory MCP entity shapes: `persistent-knowledge.md`
- Memory opt-in rules: `persistent-knowledge.md` §"Recommended default"
