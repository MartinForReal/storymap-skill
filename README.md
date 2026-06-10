# storymap-skill

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Agent Skills standard](https://img.shields.io/badge/Agent%20Skills-standard-blueviolet)](https://agentskills.io)
[![Spec-valid](https://img.shields.io/badge/skills--ref-valid-success)](https://github.com/agentskills/agentskills/tree/main/skills-ref)
[![Benchmark](https://img.shields.io/badge/benchmark-99.6%25%20(255%2F256)-success)](#benchmark)

An [Agent Skill](https://agentskills.io) that runs user story mapping (Jeff Patton style) to turn a goal, brief, or messy backlog into a sliced, prioritized delivery plan.

Built primarily for [Claude Code](https://code.claude.com/docs/en/skills), but works across any agent that supports the [Agent Skills open standard](https://agentskills.io) — including Cursor, OpenAI Codex, GitHub Copilot, Gemini CLI, OpenCode, Goose, Letta, Roo, Kiro, and ~30 others.

It produces a project design doc, a three-format story map (markdown + Mermaid + CSV), a prioritized backlog (WSJF / RICE / MoSCoW), and optionally Given/When/Then acceptance criteria + an E2E test contract for slice 1.

**Plays well inside** [Superpowers](https://github.com/obra/superpowers), [gstack](https://github.com/garrytan/gstack), and [GSD](https://getshitdone.help/solo-guide/why-gsd/). Works fine standalone.

## What it does

- **Four invocation modes** — from scratch (verbal idea), from a brief/PRD, from an existing messy backlog, iterative refinement of a prior map
- **Adaptive context loop** — mines README, code, tests, ADRs, commit log, Jira/ADO/GitHub via MCP, sister-framework state (`.gsd/`, `.superpowers/`), and prior `design.md` BEFORE asking the user
- **Customer-interview synthesis** — extracts personas/activities/problems from raw transcripts with verbatim-quote preservation
- **Persona simulation** — spawns role-play subagents to fill gaps + surface stakeholder conflicts (user-input-authoritative — sim never overrides user)
- **Six backbone-generation criteria** — frame, persona perspective, time horizon, granularity, scope, aggregation (user-confirmed + recorded for reproducibility)
- **Three slicing strategies** — Patton classic, SAFe PI, Now/Next/Later
- **Three prioritization methods** — WSJF, RICE, MoSCoW
- **Dependency tracking** — `depends_on` column, cycle detection, slice-1 feasibility check
- **OKR alignment** — coverage matrix, orphan stories + orphan KRs
- **Acceptance criteria** — Given/When/Then for slice 1 + INVEST check
- **E2E test contract** — backbone activities as E2E swimlanes
- **Mode D limit-breach detection** — capacity / dependencies / OKR coverage / scope; surfaces trade-offs rather than silently absorbing
- **Output routing** — from-scratch projects → seed an issue tracker (Jira/ADO/GitHub Projects/Linear/Trello); existing projects → keep-in-place cascade (sister-framework state → `TODO.md` → Memory MCP), with optional Claude Code `TodoWrite` pairing when the user is about to execute
- **Persistent memory** — opt-in `.user-story-mapping/state.json` or MCP memory server
- **Skill chaining** — invokes other installed skills (code-explorer, db-analyzer, etc.) for context gathering

## Installation

### As a Claude Code plugin (recommended)

The repo is a self-contained Claude Code plugin marketplace. From inside Claude Code:

```text
/plugin marketplace add martinforreal/storymap-skill
/plugin install storymap-skill@storymap-skill
```

That's it — Claude Code picks up the `.claude-plugin/marketplace.json` and installs the bundled skill (located at `skills/user-story-mapping/`).

### As a raw Agent Skill (for any compatible host)

The packaged `.skill` artifact is built by CI on tag push and attached to each [release](https://github.com/martinforreal/storymap-skill/releases) — download `user-story-mapping.skill` from the assets and install it via your host's skill installer:

- **Cursor / Codex CLI / Goose / Letta / Roo / Kiro / OpenCode / ~30 others** — drop into the host's skills directory, or use the host's CLI installer
- **Claude Code (manual install path)** — copy `skills/user-story-mapping/` into `~/.claude/skills/`

```bash
# Manual install from source
git clone https://github.com/martinforreal/storymap-skill.git
cp -r storymap-skill/skills/user-story-mapping ~/.claude/skills/

# Or build the .skill bundle yourself:
git clone https://github.com/martinforreal/storymap-skill.git
cd storymap-skill
python scripts/build_skill_bundle.py   # writes user-story-mapping.skill
```

### Verify

Once installed, the skill triggers on prompts like:
- "What should we build first for X?"
- "Help me find the MVP slice"
- "Organize this backlog"
- "PI planning"
- "Scope this project"

## File structure

```
storymap-skill/                                   # repo root = Claude Code plugin
├── .claude-plugin/
│   ├── plugin.json                               # plugin manifest (Claude Code)
│   └── marketplace.json                          # self-marketplace entry
├── skills/
│   └── user-story-mapping/                       # the skill itself (Agent Skills v1)
│       ├── SKILL.md                              # entry point — workflow at a glance + 8 steps
│       ├── assets/
│       │   ├── storymap-template.md              # canonical markdown format the scripts parse
│       │   ├── design-doc-template.md            # design doc with Backbone criteria + source tagging
│       │   ├── backlog-template.csv              # backlog with WSJF/RICE/MoSCoW/depends_on/okr columns
│       │   └── backlog-summary-template.md
│       ├── evals/
│       │   └── evals.json                        # 20 consolidated test scenarios across 9 categories
│       ├── references/                           # 17 reference files loaded on demand (see SKILL.md References table)
│       └── scripts/
│           ├── storymap_to_csv.py                # storymap.md → storymap.csv (parses [slice:] [persona:] [status:] tags)
│           └── storymap_to_mermaid.py            # storymap.md → storymap.mmd
├── examples/                                     # sample outputs from 3 scenarios
├── tests/                                        # benchmark infrastructure
├── benchmark/                                    # latest published benchmark.json + benchmark.md
├── scripts/
│   └── build_skill_bundle.py                     # builds user-story-mapping.skill from skills/
├── .github/workflows/
│   └── release.yml                               # CI: builds .skill on tag push, attaches to release
├── CHANGELOG.md
├── LICENSE                                       # MIT
└── README.md
```

## Workflow at a glance

| Step | Purpose | Budget |
|---|---|---|
| **0** Context loop | Hypothesis-driven mining of cheap-then-conditional sources (works for both from-scratch and existing project) | <15% |
| **0.4** Fill gaps | List blocking gaps; ask user; if can't ask, spawn persona-sim subagents; gate planning on completeness | 15-20% |
| **0.5** Reconcile progress | Existing-project / Mode D only: build status map from tracker + code + prior storymap; detect graduated activities; surface drift | 5-10% |
| **1** Backbone | Left-to-right user activities; criteria user-confirmed + recorded | 5-10% |
| **2** Decompose (per-persona) | Tasks under activities; ≥1 slice-1 story per persona; parallel `Agent` subagents when persona count ≥3 | 15-20% |
| **2.5** Role hints + flow advice | Generate `role-hints.md` for UX/UI + architect; chain to installed flow-advisor skills when available | 10-15% |
| **3** Slice | Walking-skeleton/PI/Now-Next-Later; first slice covers every backbone activity | 5% |
| **4** Prioritize | WSJF/RICE/MoSCoW + OKR linkage + dependency feasibility check | 15-20% |
| **4a** ACs | Given/When/Then for slice-1 stories + INVEST check | 10-15% |
| **4b** E2E contract | Backbone-as-contract: coverage matrix, E2E-HAPPY happy path, per-activity scenarios | 5-10% |
| **5** Generate derived | Run bundled scripts for `storymap.csv` + `storymap.mmd` | <2% |
| **6** Hand off | What was produced; what's still uncertain; smallest next decision (+ opt-in `tracker-status-update.<ext>` if Step 0.5 ran) | 5% |

Target total token budget: ~200K. Story count cap: ~50 total; slice-1 ≤ 15.

## The user-input-authoritative principle

**What the actual user told you, in this conversation, always wins.** Lower-priority sources fill gaps but never override. Full 6-level source priority order and tagging conventions live in [`persona-simulation-and-gap-filling.md`](skills/user-story-mapping/references/persona-simulation-and-gap-filling.md#the-user-input-authoritative-principle); every fact in `design.md` is source-tagged so reviewers can audit later.

## Examples

The `examples/` directory contains sample outputs from three scenarios:
- `from-scratch-internal-tool/` — Mode A, verbal-only fintech-refund-portal brief, WSJF, SAFe PI
- `multi-stakeholder-conflict/` — internal developer platform with conflicting stakeholders, user-input-authoritative principle in action
- `snapshot-and-breaks-limits/` — Mode D snapshot of a mid-flight PI, new feature requested, 6 limit breaches detected with trade-off options

Each contains the canonical six-file output (design.md, storymap.md, storymap.csv, storymap.mmd, backlog.md, backlog.csv) plus any optional artifacts the run produced — role-hints.md, slice-1-acceptance-criteria.md, e2e-test-contract.md, tracker-status-update.sh, handoff.md, breach-decisions.md — where applicable.

## Tests

`evals/evals.json` contains 25 consolidated test scenarios spanning:
- Invocation modes A/B/C/D
- App types: web, mobile (consumer + B2B), desktop, API/SDK, CLI, enterprise multi-tenant
- Framework integrations: Superpowers, gstack, GSD
- Capabilities: customer interview synthesis, dependency tracking, OKR alignment, persona simulation + conflict resolution, Mode D limit-breach detection, context loop short-circuit, framework-artifact mining + backbone criteria

Test infrastructure (`grade_runs.py`, `build_benchmark.py`, `build_viewer.py`, `setup_iter10.py`) lives in `tests/`. See `tests/README.md`.

## Benchmark

Latest benchmark (iteration-12, v0.0.3, all 25 evals with-skill):

| Configuration | Pass rate | Notes |
|---|---|---|
| **with-skill** (v0.0.3) | **99.6% (255/256)** | iter-12; SKILL.md 440 lines (lean refactor); 25 evals (5 new) |
| baseline (no skill) | 20.4% (iter-11 reference) | not re-run for v0.0.3; non-skill agent behavior unchanged |
| **Δ** | **+79.2pp** | |

The v0.0.3 release shipped four bodies of work in one cycle: (1) Step 0.5 progress reconciliation, Step 2.5 role hints, per-persona slice-1 enforcement, plan-stage auto-trigger, tracker write-back; (2) structural refactor that trimmed SKILL.md from 655 → 440 lines (-33%) with all duplicated content moved to references; (3) 5 new eval scenarios covering the new behaviors (IDs 21–25, all 60/60 first-run); (4) `tests/grade_runs.py` hardening (5 categories of grader-too-strict bugs fixed). Per-eval breakdown + analyst notes in [`benchmark/benchmark.md`](./benchmark/benchmark.md); raw data in [`benchmark/benchmark.json`](./benchmark/benchmark.json).

### Where the skill earns its keep
- **Structural conformance** — all 6 canonical files in the canonical CSV/Mermaid format, every time. Baseline produces ad-hoc structures that don't import into Jira/ADO cleanly.
- **Methodology correctness** — WSJF/RICE/MoSCoW with all required columns, slice-1 backbone coverage rule honored, dependency cycles surfaced not silently broken.
- **Capability-specific behaviors** — persona conflict matrix with user-input-authoritative principle (eval-15), Mode D limit-breach detection with trade-off options (eval-16), framework-artifact mining without re-asking user (eval-18), progress reconciliation with graduated activities + drift surfacing (eval-21), per-persona slice-1 enforcement across 3+ personas (eval-22), tracker-update script generation that's never auto-run (eval-25).

### The one remaining miss
- Eval-12 (dependency-aware backlog): the agent preserved 5/14 user-provided story IDs instead of all 14. All 9 other assertions in that eval passed (depends_on column, cycle detection, slice-1 feasibility, WSJF columns). Recommended fix: emphasize ID preservation in Step 2 / Mode C reference text for the next release.

When prompts are sparse, baseline collapses to 0-2/N.

## Security considerations

Before installing **any** third-party Agent Skill (this one included):

1. **Audit the instructions.** Read `SKILL.md` and the `references/` files. Skills are loaded into your agent's context and influence what it does. Treat the skill like a configuration file with side effects on agent behavior.
2. **Audit the bundled scripts.** This skill ships two Python files in `scripts/`. Read them — they're <200 lines combined and only convert markdown to CSV / Mermaid. They do not access network, write outside the working directory, or read user secrets.
3. **Check `compatibility`** in SKILL.md frontmatter — this skill declares what it expects (Python 3.10+, no other system deps).
4. **Don't put secrets in the skill's working directory.** The skill mines context from files in the working directory. Keep `.env`, credentials, etc. outside.
5. **Tracker MCP access is opt-in.** This skill can mine Jira / ADO / GitHub via MCP if the user wires those MCPs up — it never auto-installs them.

The skill never:
- Makes network calls (no `requests`, `urllib`, `httpx` imports)
- Modifies code in the working directory (only writes to `<output-dir>/` per the user's request)
- Auto-invokes other skills (per spec — only the user does that)
- Persists state without explicit user opt-in (`.user-story-mapping/state.json` is opt-in; see `references/persistent-knowledge.md`)

If you find a security concern, please open an issue.

## License

MIT — see `LICENSE`.

## Contributing

Issues and PRs welcome. When adding capabilities:
1. Write the reference file first (`references/<your-feature>.md`)
2. Update `SKILL.md` workflow steps to call it out
3. Add at least one new test case to `evals/evals.json`
4. Update assets (`backlog-template.csv` etc.) if schema changes

## Credits

Built iteratively with Claude Code's [skill-creator](https://github.com/anthropics/skills) plugin over 10 test iterations. Story mapping methodology per Jeff Patton's [User Story Mapping](https://www.jpattonassociates.com/story-mapping/) (O'Reilly, 2014). Conforms to the [Agent Skills v1 specification](https://agentskills.io/specification).

## Changelog

See [`CHANGELOG.md`](./CHANGELOG.md).
