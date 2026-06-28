# Progress reconciliation (Step 0.5)

Reconcile non-empty baseline (storymap, tracker, code). **Tracker is authority for status; storymap is authority for intent; code is evidence.** Surface drift in `handoff.md`; never absorb. Owns Step 0.5 taxonomy/drift/graduation.

Reconciliation is in-loop; no-ops when prior-state sources are empty.

## When Step 0.5 has work to do

**Has work** when ≥1:
- Prior `storymap.md` / `backlog.csv` exists (non-empty baseline)
- Step 0 mined an active tracker (Jira / ADO / GitHub / Linear) with backbone-tied issues
- Code has shipped surfaces (deployed routes, merged PRs, named integration tests) mapped to backbone activities

**No-op** when:
- Data sources empty — empty/near-empty repo, no tracker, no prior storymap (remaining state follows [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run))
- User said "ignore the tracker, treat this as fresh" — honor it; tag every status `[user-stated]` or `[inferred]`
- Solo founder mid-build, no tracker, prior storymap from yesterday — trivial diff; skip

For "tracker defined", see [output-routing.md](output-routing.md#detecting-the-empty-baseline-no-tracker-defined) § Detecting the empty baseline (no tracker defined).

## The three inputs

| Source | Tells you | Does NOT tell you | Authority for... |
|---|---|---|---|
| **Prior storymap.md / backlog.csv** | Intent, slice, scoring | Shipped? | Intent + slicing rationale + dependencies |
| **Tracker (Jira / ADO / GitHub / Linear)** | Status, Fix Version, assignee | Backbone/persona mapping | Tracked-story status |
| **Code state (routes, tests, commits, PRs)** | Surfaces, tests, issue-id commits | AC/user/prod acceptance | Evidence escalating tracker status |

Weight by authority.

## Status taxonomy

Every current/prior story gets one of six statuses:

| Status | Definition | Detection signals (need ≥1 strong + tracker confirmation for `done`) |
|---|---|---|
| `done` | Implemented/merged; ACs satisfied or tracker closed | Tracker = closed/done **AND** (code surface OR tracker commit-id) |
| `in-progress` | Active commits / PR / branch | Tracker in-progress/in-review OR PR references story ID OR branch commits in last 14 days |
| `blocked` | Unresolved dependency | Tracker blocked label OR `depends_on` unresolved hard dep |
| `deferred` | Moved out (next PI / Later / cut) | Tracker Fix Version pushed forward OR storymap future slice |
| `cut` | No longer in scope at all | Tracker closed-as-wontfix OR explicit user statement |
| `unchanged` | In storymap; no active/shipped evidence | Default when tracker unchanged and no code surface |

In `storymap.md`, `[status:<state> | <evidence>]` rides with `[slice:…]` and `[persona:…]`:

```markdown
- [slice:1] [persona:CSRep] [status: done | 2026-05-12 | tracker: PROJ-142]
  As a CS rep, I want SSO, so that passwords drop.

- [slice:1] [persona:CSRep] [status: in-progress | branch: feat/refund-routing | tracker: PROJ-148]
  As a CS rep, I want auto-approve refunds, so that simple cases close.

- [slice:2] [persona:CSRep] [status: deferred | from: 1 | tracker: PROJ-151]
  As a CS rep, I want bulk import, so that month-end avoids 4 hours.
```

In `backlog.csv`, add `status`, `status_evidence` (free-text source), `status_date`.

## Reconciliation algorithm

```
inputs:
  prior_storymap = storymap.md or empty
  prior_backlog  = backlog.csv or empty
  tracker_state  = Step 0 tracker MCP or .gsd/Roadmap.md
  code_state     = Step 0 routes, tests, recent commits

for each story in (prior_storymap ∪ tracker_state ∪ inferred-from-code):
  1. Match across sources (id, else fuzzy persona+action)
  2. Apply authority rules:
     - If tracker has definitive status (closed, blocked, in-progress) → use it
     - Else if code shows shipped surface AND tracker has matching open issue → flag confirmation (likely done, tracker open)
     - Else if storymap had prior slice and tracker has later Fix Version → mark deferred
     - Else status = unchanged
  3. Record evidence (date, tracker id, file path, commit sha)
```

Run drift detectors.

### Drift detector 1 — Orphan tracker issues

Tracker issues with no matching storymap story.

Action: list under `## Detected drift — orphan tracker items` in `handoff.md`; propose:
- "Map to existing story `S027`" (your best guess; user confirms)
- "Belongs to backbone activity `<X>` but no story — write one?"
- "Out of scope; close with explanation in tracker?"
- "Indicates a missing backbone activity — re-run Step 1?"

Each orphan needs a user decision before slicing.

### Drift detector 2 — Orphan storymap stories

Prior storymap stories without matching tracker issue.

Action: list under `## Detected drift — untracked storymap items`; for each:
- "Was this never tracked because it was deferred / cut?" → propose `deferred` or `cut`
- "Does this still belong to slice 1?" → if yes, queue for tracker write-back at Step 6
- "Is this still relevant?" → re-confirm against user-stated truth ([../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run))

### Drift detector 3 — Backbone activity graduation

For each activity, count `done` vs total. If 100% done:

- Move it to `## Shipped foundation` in `storymap.md` (after active backbone, before cross-cutting)
- Note in `design.md` under `## Activity status`: `<Activity name>` graduated on `<date>`; `<N>` shipped; `<M>` active remain
- Graduated activities leave slice-1 coverage. Rule applies only to **active** activities; see [slicing-strategies.md](slicing-strategies.md#the-slice-1-rule--mechanics-why-and-violations) § The slice-1 rule.
- If a graduated activity later gains stories, it returns active; graduation is reversible.

If activity has 0 done stories despite prior slice-1 targeting, flag *stale* slice in `handoff.md` `## Slice realism check`.

## Conflict resolution table

When sources disagree:

| Storymap says | Tracker says | Code says | Resolution |
|---|---|---|---|
| slice-1 (planned) | closed/done | matching surface exists | `done` — remove from slice-1; graduate if now 100% done |
| slice-1 (planned) | closed/done | **no** surface, **no** commit ref | **claimed-but-unverified** — confirm; do **not** auto-mark `done` |
| slice-1 (planned) | open/in-progress | partial surface | `in-progress` — keep in slice-1, flag completion |
| slice-1 (planned) | open | no matching surface | `unchanged` — proceed as planned |
| slice-1 (planned) | not in tracker | no surface | `unchanged` — flag under "orphan storymap items" |
| slice-2 (deferred) | open in current sprint | active branch | **conflict** — current work despite deferral; surface; honor user |
| not in storymap | open in tracker | active branch | **orphan tracker item** — likely story; map/escalate |
| done (in prior storymap) | re-opened in tracker | new commits | `in-progress` — flag regression; ask if AC changed |
| cut (user stated previously) | open in tracker | no surface | **stale tracker** — propose close; queue write-back |

If conflict touches user-stated preference (Person A: "we don't need RBAC in slice 1"), user wins per [../SKILL.md#rules-that-govern-every-run](../SKILL.md#rules-that-govern-every-run). Tag `[user-stated]`; update intent + write-back.

## Outputs of Step 0.5

Step 0.5 appends; no new top-level file.

1. **`design.md`** gets two new sections:
   ```markdown
   ## Implementation status (Step 0.5)

   | Activity | Total stories | Done | In-progress | Blocked | Deferred | Cut | Unchanged | Notes |
   |---|---|---|---|---|---|---|---|---|
   | 1. Sign in | 4 | 4 | 0 | 0 | 0 | 0 | 0 | **GRADUATED** |
   | 2. Find transaction | 5 | 2 | 1 | 0 | 1 | 0 | 1 |
   | 3. Submit refund | 7 | 0 | 2 | 1 | 0 | 0 | 4 |
   | ... | | | | | | | |

   Sources reconciled:
   - Prior storymap.md (2026-04-15)
   - Jira tracker MCP (live, snapshot 2026-06-10)
   - Code: src/routes/ (12 routes), tests/e2e/ (61 tests), git log --since="2026-04-15"

   ## Activity status

   - **Sign in** — graduated 2026-05-12. 4 shipped; historical; excluded from active slicing.
   - **Find transaction** — partial; 2/5 done, 1 in-progress (PROJ-203, `feat/find-by-email`).
   ```

2. **`storymap.md`** gets status annotations and `## Shipped foundation` if any activity graduated.

3. **`backlog.csv`** gets `status`, `status_evidence`, `status_date`. Done/cut skip Step 4 re-prioritization; old scores remain audit trail.

4. **`handoff.md`** gets `## Detected drift`: every orphan, conflict, proposed write-back.

## Write-back to the tracker

Reconciliation yields pull-only and push-required changes. Resolved `status` is native tracker **burn-down field** (with story-points and sprint/iteration) when tracker is system of record; see [work-item-tracking.md](work-item-tracking.md#enable-the-tracker-burn-down).

### Pull-only (tracker → storymap)

Tracker says PROJ-142 is closed; storymap pulls `status: done`. **No write-back needed**.

### Push-required (storymap → tracker)

User confirms story `cut`; tracker still open. **Write-back required** — generate script.

Follow [output-routing.md](output-routing.md) opt-in: never auto-execute. Generate `tracker-status-update.<ext>`; say what it would do.

#### Per-tracker script templates

**Jira** — `tracker-status-update.sh`:
```bash
#!/usr/bin/env bash
# Review before running. Each line is one ticket transition.
jira issue assign PROJ-151 --to "" --comment "Cut from current scope per storymap reconciliation 2026-06-10"
jira issue transition PROJ-151 "Won't Do"
jira issue update PROJ-148 --label "in-storymap-slice-1" --fix-version "PI-2026-Q3"
```

**Azure DevOps** — `tracker-status-update.sh` (uses `az devops` or the project's ADO MCP — pick one):
```bash
az boards work-item update --id 1234 --state "Removed" --discussion "Cut from scope per storymap reconciliation 2026-06-10"
az boards work-item update --id 1240 --iteration "Project\\PI-2026-Q3" --fields "Storymap.Slice=1"
```

**GitHub Issues** — `tracker-status-update.sh`:
```bash
gh issue close 142 --comment "Closed via storymap reconciliation: confirmed shipped in PR #289"
gh issue edit 151 --add-label "wontfix" --remove-label "in-progress"
gh issue close 151 --reason "not planned" --comment "Cut from current scope per storymap reconciliation"
```

**Linear** — call Linear MCP once per change; emit `tracker-status-update.md` listing calls, not script.

Each script includes a header summary:
```bash
# tracker-status-update.sh — generated 2026-06-10 by user-story-mapping skill
# Summary: 4 issues closed (cut), 2 issues moved to PI-2026-Q3, 1 label updated.
# Review each line before running. To revert a transition, see your tracker's audit log.
```

### Hard rules for write-back

1. **Never auto-execute.** User runs script and reviews every batch, even after write-back approval.
2. **One direction at a time.** Do not push storymap → tracker AND pull tracker → storymap together. Pull auto; push opt-in.
3. **No silent state changes.** Log every `handoff.md` `## Tracker write-back actions`: ticket id, before-state, after-state, reason.
4. **Reversibility note.** End with undo instructions (e.g., "To revert a Jira transition, use `jira issue transition <ID> <prior-state>` or audit-log restore").
5. **Tracker is one of many destinations.** If using sister-framework state (`.gsd/`, prior `TODO.md`) instead of tracker, write there per [output-routing.md](output-routing.md)'s cascade. Never push unapproved.

## Anti-patterns

- **Don't infer `done` from code alone.** Route/test evidence needs tracker confirmation or AC pass.
- **Don't silently absorb orphan tracker issues.** 12 unmapped issues mean 12-line `handoff.md`, not invisible append.
- **Don't push status to the tracker without opt-in.** Even after "yes, sync the tracker", review batches.
- **Don't graduate a backbone activity from `done` count alone.** Confirm retirement (e.g., "Sign in is shipped and stable, no further work expected for ≥1 PI"). Maintenance stays active.
- **Don't re-litigate prior status decisions.** If `backlog.csv` had `status: cut` for S027 and tracker confirms closed, use append-only decision. Re-evaluate only if re-opened; see [persistent-knowledge.md](persistent-knowledge.md).
- **Don't conflate intent and status.** Re-sliced (intent: now slice-2) differs from deferred (status: deferred). Storymap owns intent; tracker owns status.

## Cost ceiling

Step 0.5 should consume 5-10% of turn budget: diff + drift detection using Step 0 inputs.

If 0.5 exceeds 15%, you are re-mining (use `## Context loop trace`) or over-comparing. Sample first 20 tracker issues + recent 30 days commits + prior slice-1 stories; no drift likely means rest is fine.

For trackers with >500 issues, pre-filter to active labels / area paths / repos; drift past 100 is rare.

## Reconciliation across loop passes

Loop passes over non-empty baseline (iteration / refinement — extending existing storymap) **always run Step 0.5**:

```
Step 0   — context loop, including prior storymap as input
Step 0.4 — fill new gaps (decisions log carries forward)
Step 0.5 — reconcile (this reference)
Step 1   — backbone (preserved unless user re-derives; graduated activities marked)
Step 2   — decompose new stories (Step 2 per-persona sweep applies)
... etc.
```

The iteration diff in `handoff.md` (per [iterative-refinement-and-snapshots.md](iterative-refinement-and-snapshots.md)) includes Step 0.5 `## Status changes since prior run`:

```markdown
## Status changes since prior run (2026-04-15 → 2026-06-10)

ADDED:
- 3 new stories under Activity 4 (Approver decision) — from interview notes
- 2 new tracker issues mapped to backbone activities

GRADUATED:
- Activity 1 (Sign in) — 4/4 done; moved to Shipped foundation

CHANGED STATUS:
- S005 → done (PROJ-148 closed 2026-05-30; commit 8a3f12c)
- S012 → in-progress (active branch feat/refund-routing)
- S027 → cut (user confirmed in this run)

UNCHANGED: 18 stories carry forward as-is.

WRITE-BACK QUEUED:
- tracker-status-update.sh: 1 issue close (S027), 0 transitions, 0 label changes — review and run
```

## Where this fits with sister frameworks

Reconciliation reads sister-framework state and writes back to its destination. State conventions and GSD slice/Milestone collision: [framework-integration.md](framework-integration.md).

- **GSD** — `.gsd/task-summaries/` is authoritative status for `/gsd execute-task`. When active, write-back targets `.gsd/` (per [output-routing.md](output-routing.md)'s cascade), not tracker.
- **Superpowers** — `plans/` step status gives `done` evidence. Do not push to Superpowers-managed tracker; let `writing-plans` handle next-slice decomposition.
- **gstack** — `/retro` reads storymap Hypotheses; `## Implementation status` helps. Mention "status table is ready for `/retro` if you want to evaluate which hypotheses played out".

## TL;DR

- Step 0.5 reconciles `prior storymap ⊕ tracker ⊕ code` when any two exist.
- Tracker = **status**; storymap = **intent**; code = **evidence**.
- Drift goes to `handoff.md`, not silence.
- All-`done` activities graduate from active slicing but stay visible.
- Tracker write-back is opt-in, scripted, never auto-executed.
- Reconciliation runs in-loop; no-ops without prior state.
