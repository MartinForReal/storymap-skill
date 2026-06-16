# Persistent knowledge across sessions

Remember across invocations **yes, but selectively and opt-in**: memory is off by default, read before write, treated as hints not gospel, and always surfaced to the user. This file owns the `.user-story-mapping/state.json` schema (including the `tracker` block), the decisions-log **append-only / never-overwrite** rule, and the memory opt-in lifecycle. Memory pays for itself on active multi-PI projects and hurts on throwaway explorations; the rest of this file is how to tell the two apart and wire it cleanly.

## When to use this

Reach for persistent memory when a run is part of a *continuing* effort, and stay away from it when the run is a one-off.

| Memory helps | What to remember |
|---|---|
| **Iterative refinement (the loop on a non-empty baseline)** | The prior story map, so "extend it" carries the backbone forward instead of re-deriving it |
| **Cross-team coordination** | What other teams committed in the same PI, so dependencies stay visible |
| **User preferences** | Default prioritization method (WSJF / RICE / MoSCoW), default slicing strategy, preferred terminology |
| **Project context cache** | Personas + backbone candidates from the last context-collection, so Step 0 doesn't re-mine the repo every run |
| **Hypothesis tracking** | Which prior hypotheses got validated/rejected — informs the next batch |
| **Decisions-log continuity** | Cumulative decisions across PI-planning sessions |

| Memory hurts | Why |
|---|---|
| **One-shot exploration** | Don't pollute the user's state with a throwaway "what if" map |
| **Multi-tenant / multi-project agent** | One project's preferences must not leak into another |
| **Rapidly evolving projects** | Personas/activities from 3 months ago may now be misleading |
| **Fresh-eyes review** | Sometimes the user wants re-discovery, not cached assumptions |

For most teams: enable for active multi-PI projects, disable for one-shot explorations.

## Two storage backends

Pick the backend by how far the state needs to travel.

### A. Project-scoped — `.user-story-mapping/` directory in the repo

For state tied to one project. Lives in version control (or `.gitignore` it if private). Travels with the project, is team-shared via git, and is obvious to inspect — but needs repo write access, which some users won't want.

```
my-project/
├── .user-story-mapping/
│   ├── state.json              # last invocation's key context
│   ├── decisions.log.md        # cumulative decisions across invocations
│   ├── prior-storymaps/        # archived prior story maps
│   │   ├── 2026-Q1-PI1.md
│   │   └── 2026-Q2-PI2.md
│   └── preferences.json        # team's preferred method/slicing/style
└── src/
```

#### `state.json` schema

The canonical shape. The first block is always written when memory is enabled; the `tracker` block is written whenever a tracker is defined.

```json
{
  "last_run": "2026-06-05T14:23:00Z",
  "method_preference": "WSJF",
  "slicing_preference": "pi",
  "personas_cache": ["CS rep", "CS lead", "Admin"],
  "backbone_cache": ["Sign in", "Find transaction", "Issue refund", "Audit"],
  "active_pi": "PI-2026-Q2",
  "context_sources_last_scanned": ["README.md", "src/routes/", "tests/e2e/"],
  "tracker": {
    "type": "jira",
    "project_key": "PROJ",
    "process": "agile",
    "mapping": {
      "activity": "epic",
      "slice": "fix_version",
      "persona": "label:persona/",
      "score_field": "customfield_10030"
    },
    "taxonomy": {
      "epics": ["Sign in", "Refunds", "Audit"],
      "fix_versions": ["PI-2026-Q2", "PI-2026-Q3"],
      "components": ["auth", "billing"],
      "labels": ["billing-v2", "persona/cs-rep"]
    },
    "snapshot_at": "2026-06-05T14:23:00Z"
  }
}
```

**The `tracker` block** records project configuration, not user content, so it is **written by default whenever a tracker is defined** (the operational "tracker defined" test lives in [output-routing.md](output-routing.md#detecting-the-empty-baseline-no-tracker-defined)). Its fields:

| Field | Meaning |
|---|---|
| `type` | Detected tracker (`jira`, `azure-devops`, `github`, …) |
| `project_key` | The tracker's project/board identifier |
| `process` | The tracker's process template (e.g. `agile`, `scrum`, `basic`) |
| `mapping` | Which tracker field carries each story-map concept (activity, slice, persona, score) |
| `taxonomy` | Read-only **snapshot** of the tracker's existing categories — epics, fix_versions, components, labels — so the next run reuses the team's own vocabulary instead of re-detecting field names |
| `snapshot_at` | When the taxonomy snapshot was taken |

The taxonomy is captured so the skill aligns to the team's existing categories rather than inventing new ones — the rule for that reuse (pull read-only, propose-don't-create) is owned by [work-item-tracking.md](work-item-tracking.md#align-to-the-existing-tracker-taxonomy). Treat the saved taxonomy as a **hint**: re-verify it against the live tracker on load and refresh it on drift.

### B. Cross-session — MCP memory server (e.g. `mcp__plugin_pe-shared_memory__*`)

For state that should survive across machines, agents, or projects. Stored as knowledge-graph entities/relations. Survives `.gsd/`-style cleanup, is reachable across agents, and supports graph queries ("all hypotheses still open across all my projects") — but depends on MCP availability, is harder to inspect by hand, and is user-account-scoped rather than project-scoped.

```
Entity: project:<repo-name>
  observation: "Uses WSJF, SAFe PI cadence"
  observation: "Active PI: 2026-Q2"
  observation: "Personas: CS rep, CS lead, Admin"

Entity: pi:2026-Q2
  observation: "Committed: S001..S045 (47 stories)"
  observation: "Team capacity: 4 eng × 12 weeks"
  relation: belongs-to → project:<repo-name>

Entity: hypothesis:H1
  observation: "One-click refund cuts time by ≥50% (proposed 2026-04-01)"
  observation: "Status: validating in PI-2026-Q2"
  relation: belongs-to → project:<repo-name>
```

## The opt-in lifecycle

**Off by default.** Memory engages only on a user signal:

- "remember this" / "save this for next time" → **write** to a backend
- "use what you learned last time" / "extend the prior map" → **read**
- Extend the prior map / "what changed since last PI" (the loop on a non-empty baseline) → **automatically read** from the prior storymap

**Always read before write.** When reading, every remembered fact is a *hint*, not gospel — verify it against current state. If a cached persona is "CS rep" but the current README shows the product pivoted away from CS, override and update the cache.

**Always show what was loaded.** Add a "Loaded from memory" section to `design.md`, and tag each loaded fact with the shared `[memory: <date>]` source tag (the full source-tag vocabulary and priority order are owned by [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run); user-stated input always outranks memory).

```markdown
## Loaded from memory
- Preference: WSJF (set 2026-04-15)
- Active PI: 2026-Q2 (from prior run 2026-04-23)
- Prior backbone: Sign in → Find transaction → Issue refund → Audit
  (kept; current context still supports this)
- Prior persona "CS lead" — NOT loaded; current README pivoted away from CS lead

The story map below builds on this state. To start fresh, delete `.user-story-mapping/state.json`
or invoke with "ignore memory".
```

Transparency is non-negotiable. Hidden state = surprise = lost user trust.

### Refresh policy

- **Read on every invocation** when memory is enabled.
- **Write only when:**
  - The user explicitly asks ("remember this").
  - At the end of a successful invocation — write a **delta**, not the full state.
  - **Decisions log: append on every invocation; never overwrite.** This is the load-bearing rule — `decisions.log.md` is append-only, so the full history of why the plan looks the way it does is always recoverable. Editing or replacing prior entries is forbidden; corrections are new appended entries that supersede, not in-place edits.
- **Stale-check on read:**
  - If `state.json` is older than 90 days, warn the user before applying it.
  - If the repo's main branch has had >50 commits since the last scan, re-mine context.

## Wiring into the loop

Memory load is one of the cheap **starter signals** at the entry of **Step 0** (context-collection loop) — alongside `ls`, the prompt re-read, the README, and any interview notes in the prompt:

```
Step 0 (context loop, starter signals) — if .user-story-mapping/state.json exists OR memory MCP available:
  - Read prior state as a cheap signal (free or near-free tool call)
  - Surface in design.md "Loaded from memory" section
  - Tag loaded facts [memory: <date>]; verify against current state
  - On user signal "ignore memory", skip
Step 0 continues — proceeds as normal, augmented by memory hints
Step 1+ — normal loop
```

End-of-run write-back rides on **Step 6 (Hand off)**:

```
Step 6 (hand off) — if memory enabled OR user said "remember this":
  - Write delta to chosen backend
  - Append to decisions log (never overwrite)
  - Tell the user what was saved, in one line
```

## What NOT to remember

- **Specific user prompts.** Privacy + storage bloat. Summarize, don't quote.
- **Generated artifact bodies.** They already live in the repo; pointers suffice.
- **Stale priorities.** PI-2025-Q4 commitments aren't relevant in PI-2026-Q3 unless explicitly carried over.
- **Disagreements / corrections.** If the user said "no, the persona is X not Y," update the cache to X. Don't record the disagreement itself. (This applies to the cache, not the append-only decisions log — a decision the user later reverses is recorded as a new superseding entry, not by deleting the original.)

## Verify, then trust

Final test: turn memory on for one project, run twice, compare. If the second run is *meaningfully better* — faster context-scan, more grounded backbone, fewer questions — memory is paying for itself. If the second run is just *the same answer* arrived at faster, the savings are marginal; weigh whether the overhead is worth it. The cost of getting it wrong silently is higher than the cost of typing "use prior state" each time.
