# Collecting customer intent from context

Customer intent rarely lives in one place. The user states *part* of it (in the prompt), the codebase encodes *part* of it (in structure, tests, docs), and the rest is in adjacent systems (Jira, Confluence, analytics, production telemetry, prior conversations). **Mining this context before driving discovery makes the resulting story map dramatically more grounded** — backbone activities reflect real user journeys, not aspirational guesses; non-goals reflect work the team already decided not to do; hypotheses are framed against existing data.

Do this **as Step 0**, before mode detection. It applies to every mode (A/B/C/D).

## Loop, don't pipeline

Context collection is NOT a linear pipeline that always mines all six sources. That wastes turns on empty sources (from-scratch projects) and over-investigates when one signal already answers the question. Instead: **hypothesis-driven loop**.

```
hypothesis = "unknown"
turns_used = 0

loop until hypothesis is stable for 2 iterations OR turns_used >= cap:
    1. Pick the cheapest source that would best refine the current hypothesis
    2. Mine it (one targeted call, narrow scope)
    3. Update hypothesis based on signal (or its absence)
    4. Surface contradictions immediately
```

The loop adapts:
- **From-scratch verbal idea** (empty dir, no codebase): loop exits after 2-3 turns (`ls` + check for README + re-read prompt). Skips code/test/ADR mining entirely.
- **Mature existing project**: loop iterates through cheap signals first (README, manifests) then deeper ones (routes, tests, ADRs, commits, tracker MCP) only as the hypothesis demands more.
- **Mixed-signal project**: contradictions surface early (e.g., README says one thing, code does another) → user asked to clarify before continuing.
- **Mode D with prior artifact**: load it, then mine only the *delta* — what changed since the prior map.

### Starter signals (always try first, in order)

1. **Working directory listing** (free) — empty? populated? what languages?
2. **User's prompt re-read** (free) — re-anchor on the highest-priority source
3. **`.user-story-mapping/state.json`** (cheap) — prior runs to extend (Mode D signal)
4. **`README.md`** (cheap) — one-line product description, often the outcome statement
5. **Interview notes in the prompt** (already in context) — switch to synthesis mode

After these 5, you should know: from-scratch vs existing-project, which Mode applies, tech stack hint.

### Branch-conditional sources

Only mine these if the hypothesis warrants:

| Source | Mine when hypothesis includes... |
|---|---|
| `package.json` / manifests | Existing codebase; confirms tech + app type |
| `Dockerfile`, `k8s/` | Multi-service / cloud deploy |
| `src/routes/` / `pages/` | Web/API/mobile codebase; routes = activity candidates |
| Test names | Test suite present; names = golden paths |
| `docs/`, `ARCHITECTURE.md`, `docs/adr/` | Mature docs; ADRs reveal constraints |
| `git log --oneline -50` | Git repo; reveals current activity |
| Tracker MCP | User mentioned tool OR Mode C |
| Analytics/runtime MCP | User mentioned production concern |
| **Framework state directories** — `.gsd/`, `.superpowers/`, prior `design.md` anywhere in the tree | If any sister-framework is in use |

#### Framework artifacts — the "always check first" sources

When users work inside Claude Code skill frameworks (gstack, GSD, Superpowers), the framework's state directory often contains everything you'd otherwise extract by asking the user — but in cleaner, more authoritative form.

| Source | Path | What it gives you |
|---|---|---|
| GSD Brief | `.gsd/Brief.md` | Direct outcome statement + scope (functionally equivalent to a PRD) |
| GSD Roadmap | `.gsd/Roadmap.md` | Existing milestone/slice plan — load as prior state |
| GSD Decisions | `.gsd/Decisions/*.md` | Architecture + scoping decisions already made |
| GSD task summaries | `.gsd/task-summaries/*.md` | What got shipped and learned in prior milestones |
| Superpowers brainstorming output | wherever the user saved it (often `brainstorming.md`) | The "intent" doc the user wrote before this skill ran |
| Superpowers plans | `plans/<recent>.md` | What the team intended to do recently |
| gstack `/plan-*-review` outputs | Whatever the user saved | Reviewer feedback on prior plans |
| Prior `design.md` / `storymap.md` from this skill | `**/design.md`, `**/storymap.md` | Mode D signal — re-use the prior backbone criteria + decisions log |

**Posture: know everything that's already written before asking the user.** Reading `.gsd/Brief.md` is much cheaper than asking "what's the outcome you're going after?". If `design.md` from a prior run exists, the prior backbone criteria + decisions log are reusable — don't re-derive.

Only ask the user when the artifacts don't answer the question. And when you do ask, ask in batches (3-5 questions at a time) — not one at a time.

### Invoking other installed skills as context sources

Sometimes another installed skill has already done — or can quickly do — work that would otherwise be your context-mining burden. **When that's true, invoke the skill rather than re-deriving its output by hand or asking the user.**

Available skills appear in the runtime's system-reminders. Only invoke skills that are explicitly listed (don't guess names).

| Other skill (examples) | When invoking helps |
|---|---|
| `code-explorer` / `codebase-summarizer` | Existing-project with large codebase — get a richer summary than `ls + grep routes` |
| `db-schema-analyzer` / `schema-summary` | Data-heavy domain — the schema reveals user entities/activities (e.g., `clients`, `time_entries`, `invoices`) |
| `customer-interview-summarizer` | Many interview transcripts; pre-summarize before this skill clusters |
| `competitive-analysis` / `prior-art-search` | New product space — others' shape can frame non-goals (what NOT to build) |
| `gstack: /office-hours` | Idea-stage refinement — invoke before backbone if the user is still framing |
| `superpowers: brainstorming` | Same — the brainstorming output IS the design-doc input |
| `db-erd` / `system-diagram` | Existing system — diagrams reveal touchpoints/handoffs |
| Domain-specific skills | E.g., a `compliance-mapper` skill that turns OKR text into KR-tagged backlog rows |

#### Invocation pattern

1. **Detect what's installed.** Read system-reminder content listing available skills. Filter to ones whose descriptions match your current discovery need.
2. **Decide if invoking is cheaper than alternatives.** A skill invocation costs 1 turn + the skill's own budget. If the alternative (asking the user 3-5 questions, or mining 5-10 files yourself) is cheaper, do the alternative.
3. **Invoke via the `Skill` tool** with a precise scope. Don't ask the skill to do everything; ask for the specific input you need.
4. **Capture the output as a context source** in `design.md` with tag `[skill: <name>]`. Don't re-derive what it returned.
5. **Honor the same priority order** — user-stated > interview > memory > context > simulated > inferred. A `[skill: <name>]` source sits in the "context" tier; it doesn't override user statements.

#### Cost ceiling

Invoking another skill is expensive: it loads that skill's SKILL.md, may spawn its own subagents, and adds latency. Budget at most **one skill invocation per context-loop run** unless the user explicitly OKs more. If you find yourself wanting to chain 3+ skills, the work is probably too unscoped — stop and ask the user to narrow the discovery first.

#### Don't auto-invoke skills with side effects

Some installed skills *do things* (deploy, send messages, modify code). Never invoke those from inside Step 0 — they're not context-gathering tools. The acid test: if the skill's name or description suggests it modifies state outside its own output, treat it as not-a-context-source and skip.

#### When the user mentions a skill by name

If the user says "use my `<skill-name>` skill" or "ask my `<skill-name>` what it knows about X", that's an explicit invocation request — invoke the skill (per the user-input-authoritative principle, user-instructed actions always go through). Record what the invoked skill returned in `design.md` under the appropriate context section.

### Exit conditions

Stop the loop when ANY:
- Hypothesis stable for 2 iterations
- ≥15% of total turn budget consumed
- User said "we have enough, proceed"
- Empty working dir + no interview notes → pivot to Step 0.4
- Strong from-scratch signal + no codebase → skip code/test/ADR mining
- Single strong signal already gave the outcome (e.g., README explicit) → don't keep digging for redundancy

## When to do this — and when to skip entirely

**Do it when:** any of these is true:
- The working directory is a code repo (you can see `package.json`, `pyproject.toml`, `Cargo.toml`, `.git/`, etc.)
- The user mentions a tool (Jira, ADO, GitHub, Linear, Confluence, Notion, Sentry, Datadog, Mixpanel) and an MCP for it is available
- The user references an existing system ("our refund flow", "the onboarding screen 3 cliff", "PROP-110")
- Mode C (from existing backlog) — context collection IS the discovery

**Skip or shorten when:**
- Mode A from-scratch on a brand-new idea with no codebase yet (loop will exit fast)
- Working dir is empty / unrelated to the project
- User has explicitly provided a complete brief and asked for fast turnaround
- User explicitly says "skip context"

Context collection is supposed to *speed up* discovery by reducing the questions you need to ask the user. If it would take longer to scan context than to ask, skip it.

## The six context sources

Mine these in roughly this order — cheapest signal first. Stop early when you have enough to draft a backbone.

### 1. Environment (cheap, high signal)

Reveals the tech stack, deployment topology, and team conventions — which constrain what's realistic to ship.

| What to read | What it tells you |
|---|---|
| `README.md`, `README.*` | The team's own one-line description of the product. Often the cleanest outcome statement available. |
| `package.json`, `pyproject.toml`, `Cargo.toml`, `go.mod`, `Gemfile` | Tech stack — implies app type (web/mobile/CLI/etc.) and what integrations exist |
| `Dockerfile`, `docker-compose.yml`, `k8s/`, `helm/` | Runtime topology — multi-service? data layer? message queue? |
| `.github/workflows/`, `azure-pipelines.yml`, `.circleci/` | Deploy cadence, test matrix, target environments |
| `CHANGELOG.md`, recent git tags | Release rhythm, what's shipped vs in flight |
| `.env.example`, `config/` | Integration surface (don't read secret values) |
| `LICENSE` | OSS vs proprietary — affects how stories around contribution/forking land |

How to use: `Glob` for these file patterns, `Read` only the small/relevant ones. Don't read `node_modules` or build output.

### 2. Code structure (medium cost, high signal)

The folder layout and public exports encode the team's current mental model of activities and modules.

| What to read | What it tells you |
|---|---|
| Top-level directory listing | Sub-products, services, or major features as the team conceives them today |
| `src/routes/`, `app/`, `pages/`, `views/`, `controllers/` | Explicit user journey — every route is an activity candidate |
| `src/api/`, `internal/handlers/`, `*Controller` | The current API surface — implies what the system promises users |
| State machines, workflow definitions (Temporal, Step Functions, XState) | Explicit user transitions — gold for backbone discovery |
| Recent commits / PRs (last 30 days) | What the team is *actually* working on right now |
| TODO/FIXME/XXX comments | Known gaps the team has already flagged |

How to use: start with `Glob` for paths like `src/**/*.{ts,tsx,py,go,rs}` and a top-level `ls`. For routes, grep for routing decorators (`@app.route`, `@RequestMapping`, `<Route path=`). Read 3-5 representative files, not every file.

### 3. Tests (medium cost, very high signal)

Test names and scenarios encode the team's understanding of expected user behavior — often more precisely than docs.

| What to read | What it tells you |
|---|---|
| E2E / integration test names (`describe()`, `test()` blocks) | Golden paths — these ARE the user activities |
| Snapshot tests | What screens / outputs exist |
| Test fixtures (`fixtures/`, `factories/`, `seed/`) | Canonical user shapes, data shapes |
| Coverage report (if available) | Under-served features (low-coverage = under-tested = often under-thought) |
| Skipped tests (`xit`, `xdescribe`, `@unittest.skip`) | Known broken or pending behavior |

How to use: `grep -r "test(\|describe(\|it(" tests/ spec/ e2e/` and read the names. The full test code is rarely needed; names are enough to extract the journey.

### 4. Docs (cheap, often outdated — verify)

User-facing docs are the team's most polished statement of intent — and often the most stale.

| What to read | What it tells you |
|---|---|
| `docs/`, `documentation/`, `*.md` in repo root | Stated purpose, features, integrations |
| `openapi.yaml`, `swagger.json`, `*.graphql` | Explicit API contract — backbone candidates if user IS a developer |
| `CONTRIBUTING.md` | OSS contribution flow (relevant for CLI/library projects) |
| `ARCHITECTURE.md`, `ADR*/`, `decisions/` | Architectural decisions — often reveal hidden constraints |
| Notion / Confluence / Wiki (via MCP) | Strategy, OKRs, retros — the "why" behind the work |

How to use: read `README.md` always. Skim other docs only if they look fresh (recent git modify time). Flag stale docs in the design doc as "Docs say X but code does Y" — these are valuable hypotheses.

### 4a. Decision logs / ADRs (cheap, very high signal for "why")

Architectural Decision Records (ADRs) and decision logs encode the *reasoning* behind past choices. They are gold for understanding constraints the user might not mention — and for avoiding re-litigating decisions the team already made.

Look in: `docs/adr/`, `docs/decisions/`, `architecture/decisions/`, `decisions/`, or a single `DECISIONS.md`. Most repos that use ADRs follow a numbered convention (`0001-record-architecture-decisions.md`, `0002-use-postgres.md`, etc.).

| ADR field | What it gives you |
|---|---|
| **Title** | One-line decision (e.g., "Use OAuth2 instead of SAML for v1") |
| **Status** (Accepted/Superseded/Deprecated) | Whether the decision is still in force — superseded ADRs are worth reading for context but not constraint |
| **Context** | The pressure that forced the decision — often reveals a constraint to honor in slicing |
| **Decision** | What was decided |
| **Consequences** | What's locked-in / what's traded away — these become non-goals candidates |

Read the latest 5-10 accepted ADRs. For each, ask: "Does this constrain the backbone or eliminate work I might have proposed?" If yes, record in `design.md` under "Constraints" with an ADR-id reference (`Per ADR-0017: ...`).

If a recent ADR contradicts a user statement ("we want OAuth" but ADR-0023 just deprecated OAuth in favor of OIDC), surface as an **open question** — don't silently pick one.

### 4b. Commit log (cheap, very high signal for "what's actually happening")

The commit log is the most honest source of intent the team has. It tells you what's getting built *right now*, what got abandoned, who's working on what, and where the friction is.

Pull the last 30-50 commits on the default branch (or PI window if known). Look for:

| Signal | What it means |
|---|---|
| **Recent commits clustering on a directory** | Active work area — likely a candidate for current slice (or a recently-shipped activity to mark as "done") |
| **Revert commits** | Abandoned work — the reverted change is a *negative* signal about the approach |
| **`fix:` vs `feat:` ratio** | High fix ratio means the team is in stabilization mode (slice should focus on hardening); high feat ratio means greenfield momentum |
| **Commits by author** | Who has been doing what — informs persona of *contributor* (relevant for OSS / CLI scenarios) |
| **Long PR descriptions for small commits** | Often a sign of contentious changes — read the PR body for context on what was traded off |
| **`chore:` / `refactor:` commits in a cluster** | Pre-work for a bigger upcoming feature — ask the user what that feature is |

How to fetch: `git log --oneline -50` and (if you want bodies) `git log -10 --format=fuller`. Don't read every commit body — sample 3-5 recent ones from each cluster.

**Combined ADR + commit signal**: an ADR proposes something; the commit log shows whether it actually got implemented. ADRs that were "Accepted" but the commit log shows zero implementation work are red flags worth raising.

### 5. Runtime / simulation (high cost, ground truth)

The actual behavior of the running system reveals intent the team may not have articulated.

| What to read | What it tells you |
|---|---|
| Staging / demo URLs (if provided) | The product as it exists today |
| Analytics dashboards (Mixpanel, Amplitude, Posthog) via MCP | What users actually do — the real backbone |
| Error tracking (Sentry, Bugsnag) via MCP | Where users get stuck — high-leverage backlog candidates |
| Production logs (Datadog, Loki) via MCP | Volume of each activity, peak times |
| Playwright / Cypress recorded sessions | Recent user paths through the UI |
| Feature flags (LaunchDarkly, Split) via MCP | What's behind toggles — reveals work in flight |

How to use: only mine runtime data if MCP is wired up. Don't speculate from screenshots or descriptions; either get the data or skip this source.

### 6. Other MCPs — work-item systems (high cost, very high signal for Mode C)

Existing tracker data is often the single richest source of customer intent.

| MCP | What to fetch |
|---|---|
| Jira / ADO (via Azure DevOps MCP) | Active sprint, backlog, recent epics, current PI's commitments |
| GitHub (via gh CLI or GitHub MCP) | Open issues by label, recent PRs, discussions, milestones |
| Linear MCP | Current cycle, roadmap |
| Notion / Confluence MCP | Strategy docs, OKRs, design specs |
| Slack MCP | Recent product-channel conversations |
| Anthropic Memory MCP | Prior conversations about the project |

**For Mode C (existing backlog)**, this is your primary source — the CSV the user pastes is the surface, but the tracker has metadata (labels, priorities, comments, links to PRs) the CSV loses. Always ask: "Would it help to pull the live tracker via MCP, or is the export sufficient?"

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

Then proceed to Mode detection and the normal workflow.
```

## How to surface findings in artifacts

In `design.md`, add a **"Context sources mined"** section near the top:

```markdown
## Context sources mined
- README (last modified 2026-04-12) — product positioning, 3 explicit goals
- `src/routes/` — 12 routes; backbone candidates: auth, billing, dashboard, settings
- Test suite — 47 e2e tests; golden paths: checkout, refund, exports
- Jira (via MCP) — 31 open issues, top label "billing-v2" (8 issues)
- Sentry — top error class "PaymentTimeout" (412/wk) → suggests reliability gap

## Contradictions / staleness flagged
- README says "supports SAML SSO" but code only has OAuth2 — clarify
- ARCHITECTURE.md is 18 months old, predates current refund flow
```

This makes the resulting story map auditable: a reviewer can see what evidence drove which activity.

## When you find conflicting context

Don't quietly resolve conflicts. Surface them as **open questions** in `design.md` and (where they affect ranking) as **hypotheses** to validate in slice 1. Examples:

- README claims "10 min onboarding" but analytics show median 47 min → hypothesis H1: simplifying flow X reduces time-to-activation by Y%
- Test suite covers checkout exhaustively but no e2e tests for refund → flagged as coverage gap, not as scope expansion
- Jira has 6 "must-fix" P0 bugs in dashboard, but user prompt focuses on a new feature → ask: should the bugs go in slice 1 first?

## Cost ceiling

Total Step-0 context collection should consume **<15% of total turns/tokens** for the skill invocation. If you find yourself reading 20+ files or making 30+ MCP calls, you've gone too deep — the budget belongs to producing the actual artifacts. Stop, synthesize what you have, and proceed.

A good rule of thumb: 5-15 tool calls for context collection on a typical repo. Reach for breadth (sampling many sources) over depth (reading entire files).
