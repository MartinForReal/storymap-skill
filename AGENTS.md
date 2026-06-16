# AGENTS.md

Canonical guide for all coding agents (Claude Code, Codex, Gemini CLI, Copilot) working in this repo.

## What this repo is

This is **not an application**. It is a Claude Code **plugin** that distributes a single **Agent Skill** — `user-story-mapping`, a Jeff-Patton-style story-mapping workflow that turns a vague goal, brief, or messy backlog into a sliced delivery plan with per-persona user stories. The shipped product is markdown + a few stdlib Python helpers, distributed two ways: (1) as a Claude Code plugin/marketplace via `.claude-plugin/`, and (2) as a portable Agent Skills v1 `.skill` zip attached to GitHub releases. There is no server, no web app, no compiled output. "Building" means zipping the skill; "testing" means scoring agent-authored markdown against eval assertions.

## Repository layout

```
.claude-plugin/
  plugin.json              Claude Code plugin manifest. version, author, license, SHORT description, 20 keywords.
  marketplace.json         Self-contained marketplace manifest. metadata.version + plugins[0].version + LONG description.
skills/user-story-mapping/ THE SKILL — source of truth. Bundle is rooted HERE (SKILL.md ends up at zip root).
  SKILL.md                 Entry point: frontmatter + the re-entrant loop (discover→diff→simulate→interview→backbone→generate/update) over step bodies 0-6 + perf hard rules + references index.
  references/              20 prose .md files (~175 KB), loaded ON DEMAND by SKILL.md (progressive disclosure).
  scripts/                 storymap_to_csv.py, storymap_to_mermaid.py — deterministic parsers for storymap.md.
  assets/                  4 fill-in templates: design-doc, storymap, backlog.csv header, backlog-summary.
  evals/evals.json         25 eval scenarios (source of truth for the benchmark harness).
scripts/build_skill_bundle.py  Repo-level builder → user-story-mapping.skill (stdlib only).
tests/                     Eval grading + benchmark + viewer pipeline (NOT a unit-test suite).
  README.md                Operator runbook — read FIRST before touching pipeline scripts.
  grade_runs.py            ~1320-line grader. Per-eval regex/substring assertions → grading.json.
  build_benchmark.py       Aggregates grading.json + timing.json → benchmark.{json,md} per iteration.
  build_viewer.py          Generates review.html (side-by-side with-skill vs baseline + feedback).
  run-benchmark.sh         Interactive end-to-end wrapper (scaffold → prompt operator → grade → build).
benchmark/                 CURATED v0.0.3 / iteration-12 release artifacts (different schema from build_benchmark.py output).
examples/                  3 full output bundles (from-scratch / multi-stakeholder / iteration-snapshot). Unedited eval outputs = the schema.
.github/workflows/release.yml  Tag-triggered (v*) build + GitHub Release with the .skill attached.
CHANGELOG.md               Keep-a-Changelog + SemVer. Currently 0.0.4 (unreleased). Hand-maintained; NOT read by CI.
README.md / LICENSE        User-facing docs / MIT.
```

Top-level `user-story-mapping.skill` and `user-story-mapping-workspace/` are **never committed** (`.gitignore` excludes `*.skill` and the workspace dir).

## How the skill works

- **SKILL.md is the orchestration spec.** Its YAML frontmatter is an Agent Skills v1 manifest (`name`, `description`, `license`, `compatibility`, `metadata{author,version,homepage}`, `allowed-tools`). The body defines a single re-entrant **loop** (discover → diff vs. what exists → apply saved prefs → **simulate personas** → interview until approved → backbone → generate/update idempotently → derive + hand off) over step bodies 0-6 (sub-steps 0.3, 0.4, 0.5, 2.5, 4a, 4b). The **diff** (existing = a reconciled snapshot with code-vs-tracker conflicts surfaced as drift; desired = the prior map amended/overridden by the user's new input) and a **"tracker defined" test** replace the old A/B/C/D modes; "from scratch" is just the loop running on empty data sources, not a branch. Plus performance hard rules, the user-input-authoritative source hierarchy, and an index of reference files.
- **Progressive disclosure.** The 20 files in `references/` are the deep playbook. SKILL.md points at them per step and they are loaded **on demand only** — never pre-read, never inlined into SKILL.md. Some references self-budget with a `## Cost ceiling` section (8 of 20 currently do). SKILL.md itself is a lean answer-first spine (loop → rules → steps table → references index); the detailed step bodies live in the references.
- **Runtime flow the skill drives:** mine context (Step 0) → optionally reconcile prior progress (Step 0.5) → **simulate personas before the interview (Step 0.3) to surface cross-persona interactions + conflicts** → interview-to-approval → backbone → generate per-persona stories (Step 2; parallelize via Agent tool when personas ≥3) → slice + prioritize → emit outputs (Step 5) and a handoff (Step 6).
- **Deterministic output layer.** `storymap.md` (LLM-authored, canonical) is parsed by the two Python scripts into `storymap.csv` and `storymap.mmd`. These derived files are **generated, never hand-written**. `storymap_to_mermaid.py` imports `parse_storymap` from `storymap_to_csv.py` — that function is the single source of truth for the `## Activity:` / `### Task:` / `- [slice:...]` grammar.
- **Tiered output set:** only `design.md` + `storymap.md` are **always** produced. `storymap.csv`, `storymap.mmd`, `backlog.md`, `backlog.csv` are produced **only when no issue tracker is defined** (the conditional-artifact rule); when an issue tracker is the system of record the opt-in write-back sets each item's burn-down fields (points + sprint + status) instead. Optional: `handoff.md`, `role-hints.md`, `slice-1-acceptance-criteria.md`, `e2e-test-contract.md`, `breach-decisions.md` (iteration/breach), `tracker-status-update.<ext>` (Step 0.5/6).
- The skill is **informational/generative only**: no network calls, no edits to working-dir code, no auto-invoking other skills, no state persistence without opt-in. Tracker write-back is opt-in — it emits a review-then-run script, never auto-executes.

## Build, test & release

All commands run from the repo root. Python is stdlib-only; no `pip install`, no `requirements.txt`.

**Build the bundle** (same command CI runs):
```bash
python scripts/build_skill_bundle.py
# → user-story-mapping.skill at repo root. SKILL.md lands at zip ROOT (not nested).
```

**Verify the bundle** (local equivalent of the CI smoke check):
```bash
python -c "import zipfile; z=zipfile.ZipFile('user-story-mapping.skill'); assert 'SKILL.md' in z.namelist(); print(f'{len(z.namelist())} files')"
```

**Generate derived artifacts from a storymap.md:**
```bash
python skills/user-story-mapping/scripts/storymap_to_csv.py storymap.md > storymap.csv      # or -o storymap.csv
python skills/user-story-mapping/scripts/storymap_to_mermaid.py storymap.md > storymap.mmd   # or -o storymap.mmd
```

**Eval / benchmark harness** (host-agnostic — it scaffolds and grades but **does NOT run the agents**; the operator runs agents between scaffolding and grading):
```bash
./tests/run-benchmark.sh                 # interactive: auto-detect next iteration, scaffold, BLOCKS on read -r, then grade+build
python tests/grade_runs.py iteration-12  # grade an existing iteration (positional arg; defaults iteration-12)
ITERATION_OVERRIDE=iteration-12 python tests/build_benchmark.py   # aggregate → benchmark.{json,md} in the iteration dir
ITERATION_OVERRIDE=iteration-12 python tests/build_viewer.py      # generate review.html
PYTHONUTF8=1 python tests/grade_runs.py iteration-12             # recommended on Windows (avoids mojibake)
```

The harness reads/writes a `.gitignore`d workspace: `user-story-mapping-workspace/iteration-N/eval-<id>-<name>/{with_skill,without_skill}/{outputs/, timing.json, grading.json}`, plus an `eval_metadata.json` (`{eval_id, eval_name, prompt, assertions}`) per eval. `timing.json` = `{total_tokens, duration_ms, total_duration_seconds}`; `grading.json` = `{expectations:[{text, passed, evidence}]}` (the viewer/benchmark index those exact keys). You run the agents to fill `outputs/`; the scripts never spawn agents.

**Release** (tag-driven — only `v*` tags fire the workflow):
```bash
git tag v0.0.4 && git push origin v0.0.4
```
`release.yml` (ubuntu-latest, Python 3.11) runs the builder, inline-verifies SKILL.md is at zip root, then creates a GitHub Release via `softprops/action-gh-release@v2` (`generate_release_notes: true`, `fail_on_unmatched_files: true`) with `user-story-mapping.skill` attached.

**End-user install (Claude Code):**
```
/plugin marketplace add martinforreal/storymap-skill
/plugin install storymap-skill@storymap-skill
```

### What you CANNOT run locally
- **No test runner, linter, formatter, or type-checker anywhere.** No `pytest`/`ruff`/`mypy`/`pre-commit`/`tox`/`conftest.py`. Do not look for them; do not assume an implicit baseline. The only CI verification is the inline `assert 'SKILL.md' in names`.
- The eval harness **never executes agents**. `run-benchmark.sh` blocks on `read -r` waiting for you to run them externally. `grade_runs.py` only scores artifacts already on disk; missing `outputs/` silently scores 0/0.
- Skill-description optimization (`skill-creator`'s `run_loop.py`) uses `select.select()` on pipes — **Linux/Mac/WSL only**, not native Windows.

## Conventions

### SKILL.md
- Preserve the frontmatter shape exactly. `allowed-tools` is a space-separated list: `Bash(python:*) Read Write Edit Glob Grep Agent Skill`.
- Bump `metadata.version` on non-trivial workflow/schema changes.
- References load on demand by step — **never collapse a reference's content into SKILL.md inline**. Keep the Quick Reference table (top) and References table (bottom) in sync with `references/`.
- Performance hard rules are guardrails, not aspirations — do not relax numerically without explicit user request: total stories ≤50, slice-1 ≤15, backbone 5-7 (hard max 10), context loop ≤20 tool calls, 80% turn-budget stop, skill-chaining caps (sister-framework 1/run, advisor skills 3/Step 2.5).
- Keep auto-trigger phrasing intact (Superpowers brainstorming→writing-plans, gstack `/office-hours` `/autoplan` `/plan-*-review`, GSD `/gsd discuss` `/gsd plan-milestone` Brief/Roadmap) — that text is how the skill is matched in sister-framework Plan stages.
- Emoji-free headings; `❌`/`✅` only in existing Wrong/Right contrasts.

### Reference docs (`references/`)
- Pure prose markdown — no frontmatter, no code, no tests. Pattern: `# Title` → intro → `## When to use` → tables/templates → `## Anti-patterns` (or `## What NOT to do`) → `## Cost ceiling`.
- Cross-link by relative markdown link; **do not duplicate content** (reference-by-link, e.g. "see persistent-knowledge.md §B"). Copy-paste creates drift.
- The user-input-authoritative priority order (user-stated > interview > memory > context > simulated > inferred) is canonically stated in SKILL.md — reference its anchor, do not re-list it.
- Source-tag vocabulary is shared across all artifacts: `[user-stated]`, `[interview: <name>]`, `[code: <path>]`, `[memory: <date>]`, `[tracker: <id>]`, `[skill: <name>]` (optionally ` @ <date>`), `[simulated: <name>]`, `[inferred]`. Adding a tag means updating it everywhere.

### Scripts (`skills/user-story-mapping/scripts/`)
- stdlib only; `#!/usr/bin/env python3`; `from __future__ import annotations`. No third-party deps, ever.
- CLI shape: positional `input: Path`, optional `-o/--output: Path`, default to stdout, `return int` from `main()`, `sys.exit(main())`. Stdout is reserved for output; the only diagnostic goes to `sys.stderr`.
- Story IDs are `S{n:03d}` (`S001`...), assigned in document order, **regenerated** by the script (not tracker IDs).
- CSV column order is fixed: `id, activity, task, story, persona, outcome, slice, status, status_evidence` (9 cols since v0.0.3; on-disk example `storymap.csv` files still show the legacy 7-col schema — regenerating overwrites them to 9).
- `storymap_to_mermaid.py` mutates `sys.path` to import from its sibling — keep `scripts/` flat or fix the import if you package it.

### Assets / templates (`assets/`)
- Angle-bracket placeholders (`<Project Name>`, `<persona>`). Author notes go inside `<!-- ... -->` blocks — the parser specifically skips them.
- `backlog-template.csv` is a 23-column header + one example row with trailing empty fields (`,,,,,`) — **do not hand-trim the commas**; every row must have 23 columns.
- Load-bearing storymap headings (all the parser recognizes): `## Activity:`, `### Task:`, `### Theme:`, and any `## ` line containing `non-backbone`. Cross-cutting work renders in the CSV as `activity = "Non-backbone: <theme>"` via either encoding — `## Activity: Non-backbone: <theme>` directly (from-scratch example) or `## Non-backbone / cross-cutting` + `### Theme: <theme>` (multi-stakeholder example). Never add a 6th backbone column for tech-debt/infra.
- Every story bullet needs `[slice:<id>]` (required) and optionally `[persona:<name>]`, `[status:<state> | <evidence>]`.

### CHANGELOG / version bumps
- Keep-a-Changelog 1.1.0 + SemVer. Each release uses a subset of Added / Changed / Removed / Behavior changes / Migration notes / Benchmark / Test infrastructure (the order varies by release). Heading carries a dash-separated headline: `## [X.Y.Z] — YYYY-MM-DD — <headline>`.
- Git tag is `vX.Y.Z` (with the `v` prefix). Plain `X.Y.Z` does NOT trigger the release.
- CHANGELOG is hand-maintained and **never read by CI** — update it by hand before tagging.

## When editing X, also do Y

- **Bumping the version** → edit ALL of: `.claude-plugin/plugin.json` `version`, `.claude-plugin/marketplace.json` `metadata.version`, `.claude-plugin/marketplace.json` `plugins[0].version`, AND add a `## [X.Y.Z] — ...` block to `CHANGELOG.md` — then tag `vX.Y.Z`. The three version fields are not auto-synced; bumping one silently desyncs the listing.
- **Changing user-visible skill behavior** → update `marketplace.json` `plugins[0].description` (the LONG form — includes Step 0.5, iteration/diff, tracker write-back) AND `plugin.json` `description` (the SHORT Claude Code UI form). Keep both keyword arrays and both `license` fields aligned.
- **Editing `storymap.md` grammar** (heading / tag / comment style) → update `scripts/storymap_to_csv.py` regexes (`SLICE_RE`, `PERSONA_TAG_RE`, `STATUS_TAG_RE`, `AS_A_RE`, `SO_THAT_RE`) FIRST (mermaid inherits via import), then `assets/storymap-template.md`, then `grade_runs.py` matchers, then any matching example bundle.
- **Changing the always/conditional output tiers or CSV headers** → update `grade_runs.py` `REQUIRED_FILES_CANONICAL` (always = `design.md` + `storymap.md`) and keep the conditional-artifact graders (`grade_csv_header`, `grade_mermaid`, `grade_method_columns`, `grade_first_slice_coverage`) tolerant-when-absent, plus `grade_csv_header`'s accepted-headers list (7-col legacy + 9-col current), per-eval branches reading specific filenames, AND `SKILL.md` § What it produces + `output-routing.md` § What each branch produces + `assets/` + the examples.
- **Adding/renaming/removing a reference file** → update SKILL.md's References table AND Quick Reference table AND any cross-links in sibling references.
- **Adding a new output artifact** → update `output-routing.md`, `framework-integration.md`, the SKILL.md file-structure tree + handoff lines, and (if relevant) the examples.
- **Adding an eval** → allocate the next monotonic `id` in `evals/evals.json`, kebab-case `name`, add `prompt` + (informational-only) `assertions`, AND add an `elif eval_id == N:` branch in `grade_runs.grade_run()`. The `assertions` in evals.json are documentation only — the real checks are the Python branches.
- **Adding a throw-away file type** → extend `EXCLUDE_DIRS`/`EXCLUDE_SUFFIXES` in `build_skill_bundle.py`, don't filter ad hoc.
- **Editing README claims or benchmark numbers** → re-run the eval suite and refresh `benchmark/benchmark.json` + `benchmark.md` before publishing (README cites 99.6% / 255-of-256 from iteration-12).
- **Editing `examples/*`** → don't hand-patch. README states outputs are unedited from test runs; if behavior changes, regenerate via the eval.

## Gotchas / do-not

- **`*.skill` is a release-only artifact.** Do not commit it. The build writes it to the repo ROOT (not `dist/`) and `unlink()`s any prior copy before rebuild (no atomic swap — a crashed build leaves no file).
- **The builder bundles ONLY `skills/user-story-mapping/`.** Anything in `scripts/`, `tests/`, `examples/`, `benchmark/`, or repo root is excluded from the `.skill`. A runtime helper must be copied INTO the skill dir to ship.
- **Bundle filename `user-story-mapping.skill` is hardcoded in 3 places** (`build_skill_bundle.py` `OUT_PATH`, `release.yml` verifier + `files:`). It matches the skill DIR name, not the plugin name `storymap-skill`. Rename all three together or never.
- **Release fires on `push: tags: v*` only.** Commits, PRs, and UI-created releases without a matching tag do nothing. Any `v*` tag (even `vfoo`) triggers it — be careful with non-SemVer tags. Release notes are auto-generated from commit/PR titles, NOT from CHANGELOG.md.
- **No PyPI / npm / marketplace push.** `release.yml` only attaches the `.skill` to a GitHub Release. Claude Code install is client-side via `/plugin marketplace add` reading `marketplace.json` directly.
- **Don't introduce a build system / test runner / linter expectation** into SKILL.md or `release.yml` without actually adding the tooling — the compatibility line promises "Python 3.10+, no other system dependencies" and CI does no `pip install`.
- **`grading.json` schema is `{expectations:[{text,passed,evidence}]}`** — `build_viewer.py` and `build_benchmark.py` index those exact keys. Renaming any silently breaks both.
- **Eval dir naming `eval-<id>-<name>`** and the workspace tree `iteration-N/eval-<id>-<name>/{with_skill,without_skill}/{outputs/,timing.json,grading.json}` are load-bearing. Don't renumber evals 1-25 (IDs are referenced by integer in `grade_run()` and in the published benchmark).
- **Two distinct `benchmark.json` schemas coexist.** `tests/build_benchmark.py` writes into the iteration workspace dir; `benchmark/benchmark.json` is the hand-curated v0.0.3 release artifact with a different shape. Do NOT overwrite the curated `benchmark/` files by re-running the builder.
- **Known dead/cosmetic code** — `grade_runs.py` has unreachable OKR-grader-style code after a `return` inside `grade_multi_stakeholder_conflict` (~lines 658-708; `grade_okr_alignment` itself is defined once at line 711 and is fine); `build_viewer.py` hardcodes "iteration 5" title strings (lines 107, 147); `build_benchmark.py` sets `PREV_ITERATION = None` so prev-iteration comparison is inert. Don't "clean up" without checking call paths. Stale doc numbers: README/tests-README mention both 20 and 25 evals (actual: 25) and 17 vs 18 references (actual: **20** after v0.0.4 added `answer-first-writing.md` + `decomposition-and-stories.md`).
- **Eval 16 (iteration/breach eval) resets `results = []`** and skips the 4 standard base assertions — intentional. New global base checks won't apply to it unless added inside that branch.
- **The local data files are conditional** — `storymap.csv`, `storymap.mmd`, `backlog.md`, `backlog.csv` are generated only when no issue tracker is defined (when a tracker is the system of record, the burn-down write-back populates the tracker instead — `work-item-tracking.md` § Enable the tracker burn-down). The grader reflects this: `REQUIRED_FILES_CANONICAL` is just `design.md` + `storymap.md`, and `grade_csv_header` / `grade_mermaid` / `grade_method_columns` / `grade_first_slice_coverage` pass when their file is absent and validate when present. Don't re-add the conditional files to the required set.
- **Iteration rule:** carry the prior backbone forward — never silently re-derive it; only ADD activities, and each new one needs its own slice-1 coverage. Preserve user/tracker IDs in `backlog.csv` (`max(prior_id)+1` for new); only `storymap.csv` IDs are sequentially regenerated.
- **The unbreakable slicing rule:** slice 1 must include ≥1 story from EVERY active backbone activity. A persona with zero slice-1 candidates means re-run Step 3/1 — never silently drop.
- **Step 0.5 runs whenever the diff baseline is non-empty; skipped when empty.** Keep `iterative-refinement-and-snapshots.md` and `progress-reconciliation.md` consistent on this.
- **GSD "slice" collision:** in this skill a slice is a horizontal cut across the backbone; in GSD it's a sub-unit of a Milestone (closer to "activity" here). Translate, never equate. Never write to `.gsd/` directly — emit suggested import lines.
- **Tracker write-back is opt-in and never auto-executed.** One direction at a time, every action logged in handoff.md, reversibility note required. Case-sensitive grader checks mean lowercased tracker keys (`prop-103` vs `PROP-103`) fail preservation checks.
- **Do not hand-edit derived files** (`storymap.csv`, `storymap.mmd`) — regenerate with the scripts; hand-edits diverge from the parser's view. The parser silently drops bullets before the first `## Activity:`/`### Task:` (a malformed map yields zero rows with only a stderr warning).
