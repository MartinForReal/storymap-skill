# Persistent knowledge across sessions

Persist memory selectively and opt-in: off by default, read before write, hints not gospel, visible. Owns `.user-story-mapping/state.json` (including `tracker`), decisions-log **append-only / never-overwrite**, and opt-in lifecycle. Helps active multi-PI projects; hurts throwaways.

## When to use this

Use for *continuing* efforts; avoid one-offs.

| Memory helps | What to remember |
|---|---|
| **Iterative refinement (the loop on a non-empty baseline)** | Prior story map, so "extend it" carries backbone forward |
| **Cross-team coordination** | Same-PI commitments; dependencies stay visible |
| **User preferences** | Default method (WSJF / RICE / MoSCoW), slicing strategy, terminology |
| **Project context cache** | Personas + backbone candidates from last context-collection; Step 0 skips re-mining |
| **Hypothesis tracking** | Validated/rejected hypotheses for next batch |
| **Decisions-log continuity** | Cumulative PI-planning decisions |

| Memory hurts | Why |
|---|---|
| **One-shot exploration** | Don't pollute state with throwaway "what if" maps |
| **Multi-tenant / multi-project agent** | One project's preferences must not leak |
| **Rapidly evolving projects** | Personas/activities from 3 months ago may mislead |
| **Fresh-eyes review** | User may want re-discovery, not cache |

Default: enable active multi-PI; disable one-shots.

## Two storage backends

Pick by travel distance.

### A. Project-scoped — `.user-story-mapping/` directory in the repo

For one-project state. It can live in version control (or `.gitignore` if private), travels with the project, is team-shared/inspectable. Needs repo write access.

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

Canonical shape. Write first block when memory is enabled; write `tracker` when defined.

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

**The `tracker` block** records project configuration, not user content, so it is **written by default whenever a tracker is defined** (test in [output-routing.md](output-routing.md#detecting-the-empty-baseline-no-tracker-defined)). Fields:

| Field | Meaning |
|---|---|
| `type` | Detected tracker (`jira`, `azure-devops`, `github`, …) |
| `project_key` | Tracker project/board identifier |
| `process` | Tracker process template (e.g. `agile`, `scrum`, `basic`) |
| `mapping` | Tracker field for story-map concepts (activity, slice, persona, score) |
| `taxonomy` | Read-only **snapshot** of categories — epics, fix_versions, components, labels — so next run reuses vocabulary |
| `snapshot_at` | When taxonomy snapshot was taken |

Capture taxonomy for team categories. Reuse rule (pull read-only, propose-don't-create) lives in [work-item-tracking.md](work-item-tracking.md#align-to-the-existing-tracker-taxonomy). Treat saved taxonomy as a **hint**: re-verify; refresh on drift.

### B. Cross-session — MCP memory server (e.g. `mcp__plugin_pe-shared_memory__*`)

Use for state across machines, agents, or projects. Stores knowledge-graph entities/relations, survives `.gsd/`-style cleanup, works across agents, and supports graph queries ("all hypotheses still open across all my projects"). Tradeoffs: MCP availability, harder inspection, user-account scope.

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

**Off by default.** Memory engages on user signal:

- "remember this" / "save this for next time" → **write**
- "use what you learned last time" / "extend the prior map" → **read**
- Extend prior map / "what changed since last PI" (non-empty baseline loop) → **automatically read** prior storymap

**Always read before write.** Remembered facts are *hints*, not gospel; verify. If cached "CS rep" conflicts with README, override and update.

**Always show what was loaded.** Add "Loaded from memory" to `design.md`; tag loaded facts `[memory: <date>]` (source tags/priority order live in [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run); user-stated input outranks memory).

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

Transparency is non-negotiable; hidden state loses trust.

### Refresh policy

- **Read on every invocation** when memory is enabled.
- **Write only when:**
  - User explicitly asks ("remember this").
  - Successful end — write a **delta**, not full state.
  - **Decisions log: append on every invocation; never overwrite.** `decisions.log.md` is append-only; corrections are new superseding entries.
- **Stale-check on read:**
  - If `state.json` is older than 90 days, warn before applying it.
  - If main branch has had >50 commits since last scan, re-mine context.

## Wiring into the loop

Memory load is a cheap **starter signal** at **Step 0** entry, alongside `ls`, prompt re-read, README, and interview notes:

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

- **Specific user prompts.** Privacy + storage bloat. Summarize; don't quote.
- **Generated artifact bodies.** They live in repo; use pointers.
- **Stale priorities.** PI-2025-Q4 commitments aren't relevant in PI-2026-Q3 unless carried over.
- **Disagreements / corrections.** If user says "no, the persona is X not Y," update cache to X. Don't record the disagreement. (In the append-only decisions log, later reversal is a new superseding entry, not deletion.)

## Verify, then trust

Test: enable memory for one project, run twice. If run 2 is *meaningfully better* — faster context-scan, grounded backbone, fewer questions — memory pays. If merely *same answer* faster, savings are marginal. Silent wrong memory costs more than "use prior state".
