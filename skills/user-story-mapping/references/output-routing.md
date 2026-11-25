# Where the items land — output-routing decision

Decide artifact tier by the issue tracker actually used for this work, not by repo maturity or framework state. A separate handoff decision selects where the plan goes next. Tracker import/write-back stays opt-in and user-run.

## When to use

At Step 5/6, after backbone, slices, and ranked backlog. Routing hinges on "is a tracker defined?" — detector owned here. `TodoWrite` is in-session only; pair it with persistence before coding.

## The decision in one sentence

**Tracker defined → ranked summary in `handoff.md`; otherwise → local visualization and backlog.** Either tier can feed a downstream framework without writing its state.

## Detecting the empty baseline (no tracker defined)

Despite this section's legacy link, **tracker defined** and **non-empty diff baseline** are independent. Apply the tracker predicate in [the loop](../SKILL.md#the-loop) once in Step 0. A tracker connection must be scoped to this work and a saved `tracker` block must still apply to the current planning scope. If signals conflict, ask only which system of record the user wants for this work.

| Signal | What it establishes |
|---|---|
| Prior storymap, accepted framework brief, or relevant existing plan items | Prior context for the diff, not by itself an issue tracker |
| Package manifest, Git history/remote, framework directory, or generic mention of Jira | Context to mine, not proof of a tracker for this work |
| Empty directory, but user names the Jira project used for this work | Tracker defined; reconcile any relevant plan items you can actually read |
| Mature repo, framework brief, no applicable tracker | Use the brief and existing context; emit the no-tracker artifact tier |

## What each branch produces

The output **set** depends on: **is an issue tracker (Jira / ADO / GitHub Issues / Linear) system of record?** (`.gsd/`-style state is non-empty baseline but *not* issue tracker.) Tiers: [../SKILL.md § What it produces](../SKILL.md#what-it-produces).

- **Always, every run:** `design.md` (create if absent; if gstack/Superpowers already wrote it, preserve their sections and append/update this skill's story-map addendum) + `storymap.md` (parser/import narrative) + `storymap.csv` (flat items+status manifest; deterministic `storymap.md` projection).
- **No issue tracker** (empty baseline *or* existing project whose system of record is framework state / `TODO.md`): also emit `storymap.mmd`, `backlog.md`, and `backlog.csv` for navigation/ranking. Persist/seed below.
- **Issue tracker defined:** do **not** emit `storymap.mmd` / `backlog.{md,csv}`; tracker provides navigation/ranking. Opt-in write-back sets **burn-down fields** (points + sprint + status) — see [work-item-tracking.md § Enable the tracker burn-down](work-item-tracking.md#enable-the-tracker-burn-down). Put ranked "start here" in `handoff.md`; still produce `storymap.csv` as manifest.

## The seed branch (requested tracker import)

Use only when the user asks to seed a tracker that is not yet defined. A clean baseline alone does not select an import.

Pick tracker via [work-item-tracking.md](work-item-tracking.md#decision-tree-for-the-user). Generate the import script for the user to run. If future iterations need the mapping, mention opt-in `.user-story-mapping/state.json` in the handoff; ask before saving it ([persistence rules](persistent-knowledge.md)).

Do NOT write to `TODO.md` or Memory MCP here — tracker is system of record.

## The keep branch — handoff destinations

Use the requested destination. A named downstream workflow gets a handoff, not a write into its state. Otherwise the canonical local artifacts suffice unless the user wants another destination.

### 1. Sister-framework handoff (when a framework is the next consumer)

Write the [slice handoff](framework-integration.md#slice-handoff) in `handoff.md`, not in `.gsd/` or a framework's plan directory. Leave import, review, and task planning to the user or the owning workflow. Storymap state is separate; see [persistent-knowledge.md §A](persistent-knowledge.md).

### 2. Plain `TODO.md` at the repo root (universal fallback)

Use for an explicit in-place execution list when no framework owns the plan.

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
"Slice 1 is proposed for Milestone 1. Open handoff.md before /gsd plan-milestone;
 no .gsd/ files were changed."
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
