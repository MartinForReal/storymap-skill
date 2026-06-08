# Persistent knowledge across sessions

Should this skill remember things across invocations? Answer: **yes, but selectively and opt-in.** Memory helps in specific situations and hurts in others; this reference defines which is which and how to wire it cleanly.

## When persistent memory helps

| Situation | What to remember |
|---|---|
| **Iterative refinement (Mode D)** | The prior story map (so "extend it" doesn't re-derive backbone from scratch) |
| **Cross-team coordination** | What other teams committed in the same PI (so dependencies are visible) |
| **User preferences** | Default prioritization method (WSJF vs RICE vs MoSCoW), default slicing strategy, preferred terminology |
| **Project context cache** | Personas, backbone candidates derived from last run's context-collection — avoids re-mining the repo each invocation |
| **Hypothesis tracking** | Which hypotheses from prior runs got validated/rejected — informs new hypotheses |
| **Decisions log continuity** | Cumulative decisions across PI planning sessions |

## When persistent memory hurts

| Situation | Why memory is bad |
|---|---|
| **One-shot exploration** | Don't pollute the user's memory with a throwaway "what if" map |
| **Multi-tenant / multi-project agent** | One project's preferences shouldn't leak into another |
| **Rapidly evolving projects** | Personas / activities from 3 months ago may be misleading now |
| **Fresh-eyes review** | Sometimes the user wants the skill to re-discover, not lean on cached assumptions |

## Two storage backends

Pick based on persistence scope:

### A. Project-scoped: `.user-story-mapping/` directory in the repo

For state tied to a specific project. Lives in version control (or `.gitignore` if private).

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

**Pros:** travels with the project; team-shared via git; obvious where state lives.
**Cons:** requires write access to the repo; users may not want this in source control.

`state.json` minimal shape:

```json
{
  "last_run": "2026-06-05T14:23:00Z",
  "method_preference": "WSJF",
  "slicing_preference": "pi",
  "personas_cache": ["CS rep", "CS lead", "Admin"],
  "backbone_cache": ["Sign in", "Find transaction", "Issue refund", "Audit"],
  "active_pi": "PI-2026-Q2",
  "context_sources_last_scanned": ["README.md", "src/routes/", "tests/e2e/"]
}
```

### B. Cross-session: MCP memory server (e.g., `mcp__plugin_pe-shared_memory__*`)

For state that should persist across machines, agents, or projects.

Use the knowledge-graph primitives:

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

**Pros:** survives `.gsd/`-style cleanup, accessible across agents, supports graph queries (e.g., "all hypotheses still open across all my projects").
**Cons:** depends on MCP availability; harder to inspect/edit manually; user-account-scoped, not project-scoped.

## Recommended default

**Off by default.** Opt-in via user signal:
- User says "remember this" / "save this for next time" → write to one of the backends
- User says "use what you learned last time" / "extend the prior map" → read
- User asks for Mode D iterative refinement → automatically read from prior storymap

**Always read before write.** When reading, treat memory as *hints* not *gospel* — verify each remembered fact against current state. If a remembered persona is "CS rep" but the current README says the product pivoted away from CS, override and update.

**Always show what was loaded.** In `design.md`, add a "Loaded from memory" section:

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

## Refresh policy

- **Read on every invocation** when memory is enabled
- **Write only when:**
  - User explicitly asks ("remember this")
  - At end of successful invocation, write a delta (not the full state)
  - Decisions log: append on every invocation; never overwrite
- **Stale-check** on read:
  - If `state.json` is older than 90 days, warn the user before applying
  - If the repo's main branch has had >50 commits since last scan, re-mine context

## Wiring into the workflow

Add as **Step 0a** (before context collection):

```
Step 0a (memory) — if .user-story-mapping/state.json exists OR memory MCP available:
  - Read prior state
  - Surface in design.md "Loaded from memory" section
  - Use as hints for Step 0 context collection (e.g., focus re-scan on changed areas)
  - On user signal "ignore memory", skip
Step 0 (context collection) — proceeds as normal, augmented by memory hints
Step 1+ — normal workflow
```

End-of-run:

```
Step 7 (post-handoff) — if memory enabled OR user said "remember this":
  - Write delta to chosen backend
  - Append to decisions log
  - Tell user what was saved, in one line
```

## What NOT to remember

- **Specific user prompts.** Privacy + storage bloat. Summarize, don't quote.
- **Generated artifact bodies.** They're already in the repo; pointers suffice.
- **Stale priorities.** PI-2025-Q4 commitments aren't relevant in PI-2026-Q3 unless explicitly carried over.
- **Disagreements / corrections.** If the user said "no, persona is X not Y," update the cache to X. Don't record the disagreement itself.

## Verify, then trust

Final test: turn memory on for one project, run twice, compare. If the second run is *meaningfully better* (faster context-scan, more grounded backbone, fewer questions), memory is paying for itself. If the second run is just *the same answer* arrived at faster, the savings are marginal — consider whether the overhead is worth it.

For most teams in most projects: enable for active multi-PI projects, disable for one-shot explorations. The cost of getting it wrong silently is higher than the cost of typing "use prior state" each time.
