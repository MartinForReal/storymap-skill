# Changelog

All notable changes to **storymap-skill** are documented here. Format follows [Keep a Changelog](https://keepachangelog.com/en/1.1.0/); versioning is [SemVer](https://semver.org/).

## [0.0.2] — 2026-06-09 — output-routing decision

Adds an explicit decision branch for *where* the generated items physically land, so the agent stops defaulting to "push to a tracker" on mature projects with curated backlogs.

### Added
- New reference [`skills/user-story-mapping/references/output-routing.md`](skills/user-story-mapping/references/output-routing.md) — the from-scratch vs existing detection rule + the three-destination persistence cascade (sister-framework state → `TODO.md` → Memory MCP) with `TodoWrite` as an orthogonal in-session execution helper.
- Two new evals (#19 `output-routing-from-scratch`, #20 `output-routing-existing-cascade`) in [`skills/user-story-mapping/evals/evals.json`](skills/user-story-mapping/evals/evals.json) with matching grader handlers in [`tests/grade_runs.py`](tests/grade_runs.py). Eval suite is now 20 scenarios (was 18).
- New `TODO.md` row schema (persona / score / depends-on / dated section header) for projects without sister-framework state.

### Changed
- `SKILL.md` Step 6 now leads with `Route the items first` instead of asking "where should this go?" at handoff — the from-scratch / existing decision is explicit.
- `SKILL.md` "Pushing the artifacts into a tracker" renamed to `Where the artifacts land`; the per-tracker mapping bullets remain authoritative in [`work-item-tracking.md`](skills/user-story-mapping/references/work-item-tracking.md).
- Callouts at the top of `work-item-tracking.md` and inside `framework-integration.md` flag the routing decision before readers jump to per-tool mechanics.
- README "What it does" gains an *Output routing* bullet.

### Behavior change
- **From-scratch (empty/near-empty repo, no tracker mentioned, no framework state)** → generates a tracker import script via `work-item-tracking.md`; writes a thin `.user-story-mapping/state.json` for Mode-D continuity; does not also populate `TODO.md` (the tracker is the system of record).
- **Existing project** → walks the persistence cascade (sister-framework state → `TODO.md` → Memory MCP); does not push to a populated tracker without explicit user opt-in. `TodoWrite` is opt-in pairing for when the user is about to execute slice 1.

## [0.0.1] — 2026-06-08 — initial public release

First public release. The skill was built and validated over 11 internal iterations before being shipped here as a single commit.

### Skill capabilities
- Conforms to the [Agent Skills v1 specification](https://agentskills.io/specification) — works in Claude Code and any compatible host (Cursor, Codex CLI, Goose, Letta, Roo, Kiro, OpenCode, ~30 others)
- Four invocation modes: from-scratch / from-brief / from-backlog / Mode D iterative refinement
- Adaptive Step 0 context loop that mines: README, code, tests, ADRs, commit log, work-item trackers (Jira/ADO/GitHub/Linear via MCP), sister-framework state (`.gsd/`, `.superpowers/`), and prior `design.md` — before asking the user
- Customer-interview synthesis with verbatim-quote preservation
- Persona-simulation subagents that fill gaps and surface stakeholder conflicts (user-input-authoritative — simulated voices never override the actual user)
- Six-criterion backbone definition (frame / persona perspective / time horizon / granularity / scope / aggregation), user-confirmed and recorded for reproducibility across runs
- Three slicing strategies (Patton walking-skeleton/MVP/R2/R3, SAFe PI, Now/Next/Later)
- Three prioritization methods (WSJF / RICE / MoSCoW)
- Dependency tracking with cycle detection and slice-1 feasibility check
- OKR alignment with coverage matrix and orphan-KR / orphan-story surfacing
- Given/When/Then acceptance criteria + INVEST check for slice-1 stories
- Backbone-as-E2E-contract: coverage matrix + happy-path scenario + per-activity verification
- Mode D limit-breach detection (capacity / dependencies / OKR coverage / scope) — surfaces trade-offs rather than silently absorbing breaches
- Performance hard rules (50-story cap, slice-1 ≤ 15, 80% turn-budget stop) preventing truncation before backlog generation
- Opt-in persistent memory (`.user-story-mapping/state.json` or MCP memory server)
- Skill chaining — invokes other installed skills (code-explorer, db-analyzer, etc.) for context gathering

### Distribution
- **Claude Code plugin format** — repo is a self-contained marketplace via `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json`. Install with:
  ```
  /plugin marketplace add martinforreal/storymap-skill
  /plugin install storymap-skill@storymap-skill
  ```
- **Raw `.skill` bundle** for non-Claude-Code hosts — built by CI on tag push and attached to each GitHub release; can also be built locally with `python scripts/build_skill_bundle.py`
- **Manual install** — copy `skills/user-story-mapping/` into the host's skills directory (e.g. `~/.claude/skills/`)

### Benchmark
- **with-skill: 171/174 (98.3%)** across 18 evaluation scenarios × 2 configurations
- **baseline (no skill): 35/174 (20.1%)**
- **Δ: +78.2 percentage points** (~4.9× quality improvement for ~33% more tokens)
- Mean duration: 554s with-skill vs 236s baseline
- Mean tokens: 215,947 with-skill vs 162,905 baseline
- Per-eval breakdown + analyst notes: [`benchmark/benchmark.md`](./benchmark/benchmark.md)
- Raw data: [`benchmark/benchmark.json`](./benchmark/benchmark.json)
- Regenerate locally: `bash tests/run-benchmark.sh`

### Eval coverage
- 6 structural evals — modes A/B/C × 3 framework integrations (Superpowers, gstack, GSD)
- 5 app-type evals — pure API/SDK, desktop, enterprise multi-tenant SaaS, CLI, mobile B2C
- 5 capability evals — customer interview synthesis, dependency tracking, OKR alignment, persona-simulation gap discovery, multi-stakeholder conflict
- 3 advanced behavior evals — Mode D snapshot + breach detection, empty-dir loop short-circuit, framework-artifact mining + backbone criteria

### Repo layout
- `skills/user-story-mapping/` — the skill itself (SKILL.md + 14 references + 4 assets + 2 scripts + 18 evals)
- `.claude-plugin/` — Claude Code plugin manifest + marketplace
- `examples/` — sample outputs from 3 scenarios
- `tests/` — benchmark infrastructure (grader + benchmark builder + viewer builder + setup script)
- `benchmark/` — published benchmark.json + benchmark.md
- `scripts/build_skill_bundle.py` — builds the `.skill` bundle locally
- `.github/workflows/release.yml` — CI: builds and attaches `.skill` to each tagged release

[0.0.1]: https://github.com/MartinForReal/storymap-skill
