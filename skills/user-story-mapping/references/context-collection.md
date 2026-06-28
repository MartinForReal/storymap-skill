# Collecting customer intent from context

Mine existing context — repo, tests, docs, tracker, prior runs — before interviewing. Ground the map in journeys, decisions, evidence. Intent spans prompt, codebase, Jira, Confluence, analytics, telemetry, prior conversations; Step 0 is a hypothesis loop.

This is **Step 0**. One scan gathers intent, sets the diff baseline, and detects whether a tracker is defined. A framework-owned `design.md` (gstack/Superpowers) is input first, output second: mine it as the brief, then augment it later. No "mode detection"; "from scratch" loops empty sources. See [`../SKILL.md#the-loop`](../SKILL.md#the-loop).

## When to use

**Run it when any of these is true:**
- Code repo present (`package.json`, `pyproject.toml`, `Cargo.toml`, `.git/`, etc.).
- User mentions a tool (Jira, ADO, GitHub, Linear, Confluence, Notion, Sentry, Datadog, Mixpanel) with available MCP.
- User references an existing system ("our refund flow", "the onboarding screen 3 cliff", "PROP-110").
- Backlog pasted (CSV / Jira / ADO / GitHub) — context collection *is* discovery.

**Skip or shorten when:**
- From-scratch idea, no codebase — loop exits fast.
- Working dir empty or unrelated.
- Complete brief + fast turnaround requested.
- User explicitly says "skip context".

Collect context to reduce questions; if slower, ask.

## Loop, don't pipeline

Do **not** walk all six sources in fixed order. Use a hypothesis loop: one targeted call for empty sources, stop on strong signals.

```
hypothesis = "unknown"
turns_used = 0

loop until hypothesis is stable for 2 iterations OR turns_used >= cap:
    1. Pick the cheapest source that would best refine the current hypothesis
    2. Mine it (one targeted call, narrow scope)
    3. Update hypothesis based on signal (or its absence)
    4. Surface contradictions immediately
```

The loop handles every input:
- **From-scratch verbal idea** (empty dir, no codebase): exits after 2–3 turns (`ls` + README check + re-read prompt); skips code/test/ADR.
- **Mature existing project**: README/manifests first; routes/tests/ADRs/commits/tracker MCP only as needed.
- **Mixed-signal project**: surface contradictions early (README vs code); ask before continuing.
- **Non-empty baseline** (prior `storymap.md`/`design.md` or saved `state.json`): load it, mine only the *delta*. Iteration is loop-on-existing-map, not a mode.

### Starter signals (always try first, in order)

1. **Working directory listing** (free) — empty/populated? languages?
2. **User's prompt re-read** (free) — re-anchor on highest-priority source.
3. **`.user-story-mapping/state.json`** (cheap) — prior runs + tracker config; presence = non-empty baseline. Schema/lifecycle live in [`persistent-knowledge.md`](persistent-knowledge.md) §A.
4. **Framework `design.md`** (cheap, if present) — gstack/Superpowers design output; use as the brief and non-empty baseline.
5. **`README.md`** (cheap) — product one-liner, often outcome.
6. **Interview notes in the prompt** (already in context) — synthesize.

These reveal project/baseline type and tech-stack hint.

### Branch-conditional sources

Mine these only when the hypothesis warrants:

| Source | Mine when hypothesis includes... |
|---|---|
| `package.json` / manifests | Existing codebase; tech + app type |
| `Dockerfile`, `k8s/` | Multi-service / cloud deploy |
| `src/routes/` / `pages/` | Web/API/mobile; routes = activity candidates |
| Test names | Test suite present; names = golden paths |
| `docs/`, `ARCHITECTURE.md`, `docs/adr/` | Mature docs; constraints |
| `git log --oneline -50` | Git repo; current activity |
| Tracker MCP | User mentioned a tracker OR a backlog was pasted |
| Analytics/runtime MCP | User mentioned production concern |
| **Framework state directories** — `.gsd/`, `.superpowers/`, prior `design.md` anywhere in the tree | Sister-framework in use |

#### Framework artifacts — the "always check first" sources

Framework state directories (gstack, GSD, Superpowers) often beat interviews for authority and clarity.

| Source | Path | What it gives you |
|---|---|---|
| GSD Brief | `.gsd/Brief.md` | Outcome + scope (PRD equivalent) |
| GSD Roadmap | `.gsd/Roadmap.md` | Milestone/slice plan — load as prior state |
| GSD Decisions | `.gsd/Decisions/*.md` | Architecture + scoping decisions |
| GSD task summaries | `.gsd/task-summaries/*.md` | Shipped work + prior-milestone learning |
| Superpowers brainstorming output | wherever the user saved it (often `brainstorming.md`) | The pre-skill intent doc |
| Superpowers plans | `plans/<recent>.md` | Recent intended work |
| gstack `/office-hours` / `/autoplan` / `/plan-*-review` outputs | Usually `design.md` or wherever the user saved it | Brief + prior-plan reviewer feedback; treat as framework-owned input |
| Superpowers brainstorming / generated plan output | Often `design.md`, `brainstorming.md`, or `plans/<recent>.md` | Intent design doc; treat as the loop's brief |
| Prior `design.md` / `storymap.md` from this skill | `**/design.md`, `**/storymap.md` | Non-empty-baseline signal — reuse backbone criteria + decisions log |

Read before asking: `.gsd/Brief.md` for outcome; framework/prior `design.md` for outcome, scope, backbone criteria, and decisions log. Later, preserve framework-owned sections and append/update only the story-map addendum; don't overwrite a gstack/Superpowers design doc. Sister-framework handoff/trigger phrasing lives in [`framework-integration.md`](framework-integration.md).

Ask only for gaps; batch 3–5 questions.

### Invoking other installed skills as context sources

Invoke another installed skill only when available and cheaper than mining or asking. Treat output as context; do not re-derive.

Available skills appear in runtime system-reminders; invoke only listed skills.

| Other skill (examples) | When invoking helps |
|---|---|
| `code-explorer` / `codebase-summarizer` | Large existing-project summary beyond `ls + grep routes` |
| `db-schema-analyzer` / `schema-summary` | Data-heavy domain; entities/activities (`clients`, `time_entries`, `invoices`) |
| `customer-interview-summarizer` | Many transcripts; summarize before clustering |
| `competitive-analysis` / `prior-art-search` | New product space; frame non-goals (what NOT to build) |
| `gstack: /office-hours` | Idea-stage refinement before backbone |
| `superpowers: brainstorming` | Brainstorming output IS design-doc input |
| `db-erd` / `system-diagram` | Existing system touchpoints/handoffs |
| Domain-specific skills | E.g., `compliance-mapper` converts OKR text to KR-tagged backlog rows |

#### Invocation pattern

1. **Detect what's installed.** Filter the system-reminder skill list to the discovery need.
2. **Compare cost.** Invocation costs 1 turn plus budget. If 3–5 questions or 5–10 files is cheaper, do that.
3. **Invoke via the `Skill` tool** with narrow scope: request the specific input, not the whole job.
4. **Capture the output as a context source** in `design.md` with tag `[skill: <name>]`. Do not re-derive it.
5. **Honor source priority.** `[skill: <name>]` is context tier and never overrides users. Priority/source tags are governed in [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run).

#### Don't auto-invoke skills with side effects

Skip Step-0 skills that deploy, send messages, modify code, or change state outside their own output. Side-effect skills are not context sources.

#### When the user mentions a skill by name

If the user says "use my `<skill-name>` skill" or "ask my `<skill-name>` what it knows about X", invoke it; record output in `design.md`.

### Exit conditions

Stop when ANY holds:
- Hypothesis stable for 2 iterations.
- ≥15% of total turn budget consumed.
- User said "we have enough, proceed".
- Empty working dir + no interview notes → Step 0.4.
- Strong from-scratch signal + no codebase → skip code/test/ADR.
- Single strong outcome signal (e.g., README explicit) → stop digging.

### Surface the trace in design.md

Record the loop trace in `design.md` for auditability.

```markdown
## Context loop trace
- (1) `ls` → 47 files incl. `src/`, `tests/`, `docs/adr/` — existing project
- (2) `README.md` → product is "TimeSink, a B2B time-tracking SaaS for design agencies"
- (3) `package.json` → Next.js + Prisma + Postgres, 84 deps — mature web stack
- (4) `src/routes/` → 12 routes; backbone candidates: auth, projects, time-entries, invoices, settings
- (5) Test names (61 e2e) → golden paths: create-project, log-time, generate-invoice
- (6) `docs/adr/0017` (most recent) → "Replace Stripe Invoicing API with Paddle" (2026-04, Accepted)
- (7) Jira MCP → 23 open issues, top label "paddle-migration" (8 — ADR-0017 active)
- Hypothesis: STABLE after iteration 7. Proceeding to Step 0.4.

## Contradictions flagged
- README says "Stripe-powered invoicing" — outdated per ADR-0017 (Paddle migration). Confirm with user.
```

### Worked traces — the loop on four different inputs

- **From-scratch verbal idea**: 2–3 turns (listing + README + prompt re-read = "no codebase, no prior artifact, just an idea"); skip code/test/ADR; Step 0.4.
- **Mature existing project**: iterates README → manifests → routes → tests → ADRs → commits → tracker until stable.
- **Mixed signal**: README says "we're a mobile app" but `Cargo.toml` says Rust + Tauri → surface contradiction, pursue only ONE side.
- **Non-empty baseline + tracker MCP**: existing `storymap.md` + Jira MCP → load both, reconcile, surface deltas; skip full code mining.

## The six context sources

Mine cheapest-first; stop when you can draft a backbone.

### 1. Environment (cheap, high signal)

Environment reveals stack, topology, conventions, and slice constraints.

| What to read | What it tells you |
|---|---|
| `README.md`, `README.*` | Team's product description; often cleanest outcome |
| `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile` | Stack, app type (web/mobile/CLI/etc.), integrations |
| `Dockerfile`, `docker-compose.yml`, `k8s/`, `helm/` | Runtime topology: services, data layer, queue |
| `.github/workflows/`, `azure-pipelines.yml`, `.circleci/` | Deploy cadence, test matrix, environments |
| `CHANGELOG.md`, recent git tags | Release rhythm; shipped vs in flight |
| `.env.example`, `config/` | Integration surface (don't read secret values) |
| `LICENSE` | OSS vs proprietary; contribution/forking stories |

Use `Glob`, then `Read` only small/relevant files. Skip `node_modules` and build output.

### 2. Code structure (medium cost, high signal)

Folders and exports encode the current activity/module model.

| What to read | What it tells you |
|---|---|
| Top-level directory listing | Sub-products, services, major features |
| `src/routes/`, `app/`, `pages/`, `views/`, `controllers/` | User journey; each route is an activity candidate |
| `src/api/`, `internal/handlers/`, `*Controller` | API surface; what the system promises users |
| State machines, workflow definitions (Temporal, Step Functions, XState) | User transitions; backbone gold |
| Recent commits / PRs (last 30 days) | Current actual work |
| TODO/FIXME/XXX comments | Known flagged gaps |

Start with `Glob` for `src/**/*.{ts,tsx,py,go,rs}` and top-level `ls`. For routes, grep decorators (`@app.route`, `@RequestMapping`, `<Route path=`). Read 3–5 representative files.

### 3. Tests (medium cost, very high signal)

Tests often encode expected behavior better than docs.

| What to read | What it tells you |
|---|---|
| E2E / integration test names (`describe()`, `test()` blocks) | Golden paths/user activities |
| Snapshot tests | Existing screens/outputs |
| Test fixtures (`fixtures/`, `factories/`, `seed/`) | Canonical users/data |
| Coverage report (if available) | Under-served features (low-coverage = under-tested/under-thought) |
| Skipped tests (`xit`, `xdescribe`, `@unittest.skip`) | Known broken/pending behavior |

Use `grep -r "test(\|describe(\|it(" tests/ spec/ e2e/`; read names, not full test code.

### 4. Docs (cheap, often outdated — verify)

Docs state intent; verify freshness.

| What to read | What it tells you |
|---|---|
| `docs/`, `documentation/`, `*.md` in repo root | Purpose, features, integrations |
| `openapi.yaml`, `swagger.json`, `*.graphql` | API contract; backbone candidates for developer users |
| `CONTRIBUTING.md` | OSS contribution flow for CLI/library projects |
| `ARCHITECTURE.md`, `ADR*/`, `decisions/` | Decisions; hidden constraints |
| Notion / Confluence / Wiki (via MCP) | Strategy, OKRs, retros; the "why" |

Always read `README.md`. Skim fresh docs only (recent git modify time). Flag "Docs say X but code does Y" in `design.md`.

### 4a. Decision logs / ADRs (cheap, very high signal for "why")

ADRs explain constraints and prevent re-litigating choices.

Look in `docs/adr/`, `docs/decisions/`, `architecture/decisions/`, `decisions/`, or `DECISIONS.md`. Most use numbered names (`0001-record-architecture-decisions.md`, `0002-use-postgres.md`, etc.).

| ADR field | What it gives you |
|---|---|
| **Title** | One-line decision (e.g., "Use OAuth2 instead of SAML for v1") |
| **Status** (Accepted/Superseded/Deprecated) | Whether still in force; superseded ADRs are context, not constraint |
| **Context** | Pressure behind the decision; slicing constraints |
| **Decision** | What was decided |
| **Consequences** | Locked-in/traded-away choices; non-goal candidates |

Read latest 5–10 accepted ADRs. If one constrains the backbone or eliminates work, record it in `design.md` "Constraints" with ADR-id.

If a recent ADR contradicts the user ("we want OAuth" but ADR-0023 deprecated OAuth for OIDC), surface an **open question**.

### 4b. Commit log (cheap, very high signal for "what's actually happening")

Commits show current work, abandoned work, owners, and friction.

Pull last 30–50 commits on default branch (or PI window). Look for:

| Signal | What it means |
|---|---|
| **Recent commits clustering on a directory** | Active area; current-slice or shipped "done" candidate |
| **Revert commits** | Abandoned work; negative signal about approach |
| **`fix:` vs `feat:` ratio** | High fix = hardening; high feat = greenfield |
| **Commits by author** | Ownership; contributor persona for OSS / CLI scenarios |
| **Long PR descriptions for small commits** | Contentious changes; tradeoffs in PR body |
| **`chore:` / `refactor:` commits in a cluster** | Pre-work for upcoming feature; ask what feature |

Fetch `git log --oneline -50` and, if needed, `git log -10 --format=fuller`. Sample 3–5 commits per cluster.

**Combined ADR + commit signal**: "Accepted" ADR + zero implementation commits = red flag.

### 5. Runtime / simulation (high cost, ground truth)

Runtime behavior reveals unstated intent.

| What to read | What it tells you |
|---|---|
| Staging / demo URLs (if provided) | Current product |
| Analytics dashboards (Mixpanel, Amplitude, Posthog) via MCP | Real user behavior; real backbone |
| Error tracking (Sentry, Bugsnag) via MCP | Stuck points; high-leverage backlog |
| Production logs (Datadog, Loki) via MCP | Activity volume, peak times |
| Playwright / Cypress recorded sessions | Recent UI paths |
| Feature flags (LaunchDarkly, Split) via MCP | Toggles; work in flight |

Mine runtime only when MCP is wired. Do not infer from screenshots/prose; get data or skip source 5.

### 6. Other MCPs — work-item systems (high cost, very high signal when a tracker/backlog exists)

Tracker data is often the richest intent source.

| MCP | What to fetch |
|---|---|
| Jira / ADO (via Azure DevOps MCP) | Sprint, backlog, epics, current PI's commitments |
| GitHub (via gh CLI or GitHub MCP) | Open issues by label, PRs, discussions, milestones |
| Linear MCP | Current cycle, roadmap |
| Notion / Confluence MCP | Strategy docs, OKRs, design specs |
| Slack MCP | Product conversations |
| Anthropic Memory MCP | Prior conversations about the project |

**When a tracker or backlog exists**, treat it as primary. CSV loses labels, priorities, comments, PR links. Ask whether live MCP or export is sufficient.

**Pull taxonomy read-only too, not just issues** so Steps 2–4 reuse categories and Step 6 can persist them. Pull list, propose-don't-create rule, mapping table: [`work-item-tracking.md`](work-item-tracking.md#align-to-the-existing-tracker-taxonomy).

## The procedure

```
Step 0 (this step)
  ├── Quick env scan (5-10s of tool calls)
  │     - Glob for README, package.json, etc.
  │     - Note what's there
  ├── If code repo: light code scan (Glob src/, Grep for routes/controllers)
  ├── If tests exist: pull test names (Grep)
  ├── If docs exist: read README + ARCHITECTURE if present
  ├── If MCP available + user mentioned tool: fetch active items
  └── Synthesize:
        - What outcome is the existing system optimizing for?
        - What are the current "activities" implied by routes/tests/issues?
        - What gaps or contradictions stand out?

Then proceed to diff (Step 0.5 reconciliation when baseline is non-empty) and normal workflow.
```

## How to surface findings in artifacts

Add **"Context sources mined"** near the top of `design.md`:

```markdown
## Context sources mined
- README (modified 2026-04-12) — positioning, 3 goals
- `src/routes/` — 12 routes; backbone candidates: auth, billing, dashboard, settings
- Test suite — 47 e2e; paths: checkout, refund, exports
- Jira (via MCP) — 31 open issues, top label "billing-v2" (8 issues)
- Sentry — "PaymentTimeout" (412/wk) → reliability gap

## Contradictions / staleness flagged
- README says "supports SAML SSO" but code only has OAuth2 — clarify
- ARCHITECTURE.md is 18 months old, predates current refund flow
```

This makes activities evidence-traceable.

## When you find conflicting context

Surface conflicts as **open questions** in `design.md`; ranking conflicts become **hypotheses** for slice 1. Examples:

- README: "10 min onboarding"; analytics: median 47 min → H1: simplifying flow X reduces time-to-activation by Y%.
- Checkout has exhaustive tests; refund has no e2e → coverage gap, not scope expansion.
- Jira has 6 "must-fix" P0 dashboard bugs, but prompt focuses on a new feature → ask whether bugs belong in slice 1 first.

## What NOT to do

- Don't walk all six sources in fixed order; that's the pipeline anti-pattern.
- Don't dig after the hypothesis is stable; redundancy burns artifact budget.
- Don't infer runtime behavior from screenshots/prose — pull MCP data or skip source 5.
- Don't read secret values from `.env`; integration surface is enough.
- Don't auto-invoke side-effect skills or chain 3+ context skills in one run.
- Don't pick sides silently when context conflicts — surface an open question.

## Cost ceiling

Total Step-0 context collection should consume **<15% of total turns/tokens**: 5–15 tool calls typical; hard cap 20. Prefer breadth over depth. Another skill is expensive (loads SKILL.md, may spawn subagents, adds latency): budget **one skill invocation per context-loop run** unless user OKs more. For 3+ skills, ask the user to narrow. Near cap and unstable? Write to `design.md`, flag ambiguity, proceed.

If the user says "skip context — just build the map" or "I have a brief, work from this only", skip Step 0, treat prompt as complete, tag `[user-stated]` or `[inferred]` only.
