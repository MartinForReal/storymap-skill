# Progress reconciliation — bidirectional sync between storymap, tracker, and code

This reference covers Step 0.5 — the step that runs whenever the project isn't truly from-scratch and one or more of {prior storymap, tracker with issues, shipped code surfaces} disagree about what's done, in-progress, or in scope.

The skill already mines all three sources in Step 0. Step 0.5 is what *reconciles* them into a single status view that downstream stages (Step 3 slicing, Step 4 prioritization) can trust.

## When to run Step 0.5

**Run** when ≥1 is true:
- A prior `storymap.md` / `backlog.csv` exists in this working tree (Mode D)
- Step 0 mined an active tracker (Jira / ADO / GitHub / Linear) with issues plausibly tied to the backbone
- The codebase has shipped surfaces (deployed routes, merged feature PRs, named integration tests) that map to plausible backbone activities

**Skip** when:
- True from-scratch — empty/near-empty repo, no tracker, no prior storymap (the user-input-authoritative principle covers all the state you have)
- The user has explicitly said "ignore the tracker, treat this as fresh" — honor it; tag every status as `[user-stated]` or `[inferred]`
- Solo founder mid-build, no tracker, prior storymap is from yesterday — diff is trivially empty; skip

## The three inputs

| Source | What it tells you | What it does NOT tell you | Authority for... |
|---|---|---|---|
| **Prior storymap.md / backlog.csv** | What we *intended* to build, in what slice, with what scoring | Whether any of it actually shipped | Intent + slicing rationale + dependencies |
| **Tracker (Jira / ADO / GitHub / Linear)** | Live status of every tracked issue: open / in-progress / closed / blocked, current Fix Version, assignee, recent activity | Whether the issue maps to a backbone activity or persona | Status of stories that exist in the tracker |
| **Code state (routes, tests, commits, PRs)** | Evidence of what's been built — code surfaces that exist, tests that pass, commits that reference issue IDs | Whether what's built satisfies the AC, whether the user has accepted it, whether it's deployed to production | Evidence that *escalates* to status confirmation in the tracker |

The reconciliation algorithm uses all three, weighted by these authority columns.

## Status taxonomy

Every story (current and prior) gets exactly one status:

| Status | Definition | Detection signals (need ≥1 strong + tracker confirmation for `done`) |
|---|---|---|
| `done` | Implemented, merged, ACs satisfied (or, absent ACs, the matching tracker issue is closed) | Tracker = closed/done state **AND** (matching code surface exists OR commit-id reference in tracker) |
| `in-progress` | Open work with active commits / PR / branch | Tracker = in-progress / in-review state OR open PR referencing the story ID OR commits to a feature branch in last 14 days |
| `blocked` | Cannot proceed; depends on something not yet done | Tracker = blocked label OR `depends_on` chain has an unresolved hard dep |
| `deferred` | Was in a slice; moved out (next PI / Later / cut from current slice) | Tracker Fix Version pushed forward OR storymap re-slicing put it in a future slice |
| `cut` | No longer in scope at all | Tracker closed-as-wontfix OR explicit user statement |
| `unchanged` | None of the above — story is in the storymap, not actively being worked, no shipped evidence | Default for stories that have neither moved in tracker nor have matching code surfaces |

Annotation format in `storymap.md`:

```markdown
- [slice:1] [persona:CSRep] [status: done | 2026-05-12 | tracker: PROJ-142]
  As a CS rep, I want to sign in with SSO, so that I don't manage another password.

- [slice:1] [persona:CSRep] [status: in-progress | branch: feat/refund-routing | tracker: PROJ-148]
  As a CS rep, I want to submit a refund within my auto-approve limit, so that simple cases close fast.

- [slice:2] [persona:CSRep] [status: deferred | from: 1 | tracker: PROJ-151]
  As a CS rep, I want bulk refund import, so that month-end batches don't take 4 hours.
```

In `backlog.csv`, add columns: `status`, `status_evidence` (free-text source description), `status_date`.

## Reconciliation algorithm

```
inputs:
  prior_storymap = read storymap.md if it exists, else empty
  prior_backlog  = read backlog.csv if it exists, else empty
  tracker_state  = mined in Step 0 (tracker MCP or grep over .gsd/Roadmap.md)
  code_state     = mined in Step 0 (routes, tests, recent commits)

for each story in (prior_storymap ∪ tracker_state ∪ inferred-from-code):
  1. Match the story across sources (by id when possible; by fuzzy persona+action when not)
  2. Apply authority rules:
     - If tracker has a definitive status (closed, blocked, in-progress) → use it
     - Else if code state shows shipped surface AND tracker has matching open issue → flag for confirmation (likely done, not yet closed in tracker)
     - Else if storymap had it in a prior slice and tracker has it in a later Fix Version → mark deferred
     - Else status = unchanged
  3. Record evidence sources for the status (date, tracker id, file path, commit sha)
```

Then run three drift detectors:

### Drift detector 1 — Orphan tracker issues

Issues in the tracker that don't match any storymap story.

Action: list them under `## Detected drift — orphan tracker items` in `handoff.md`. For each, propose one of:
- "Map to existing story `S027`" (your best guess; user confirms)
- "Belongs to backbone activity `<X>` but no story written — write a new story?"
- "Out of scope; close with explanation in tracker?"
- "Indicates a missing backbone activity — re-run Step 1?"

Don't silently absorb. Each orphan needs a user decision before slicing proceeds.

### Drift detector 2 — Orphan storymap stories

Stories in the prior storymap with no matching tracker issue.

Action: list under `## Detected drift — untracked storymap items`. For each:
- "Was this never tracked because it was deferred / cut?" → propose `deferred` or `cut` status
- "Does this still belong to slice 1?" → if yes, queue for tracker write-back at Step 6
- "Is this still relevant?" → may need re-confirmation under the user-input-authoritative principle

### Drift detector 3 — Backbone activity graduation

For each backbone activity, count `done` vs total. If 100% done:

- Move the activity to a new `## Shipped foundation` section in `storymap.md` (heading after the active backbone, before the cross-cutting section)
- Note in `design.md` under `## Activity status`: `<Activity name>` graduated on `<date>`; total `<N>` stories shipped; current backbone now has `<M>` active activities
- The slice-1 coverage rule (every backbone activity gets ≥1 slice-1 story) applies only to **active** backbone activities. Graduated ones don't need re-coverage.
- If a graduated activity later acquires new stories (Mode D extension), it returns to active status — graduation is reversible.

Symmetrically: if status reconciliation reveals an activity has 0 done stories despite being targeted in slice 1 from a prior run, that's a *stale* slice — flag in `handoff.md` under `## Slice realism check`.

## Conflict resolution table

When the three sources disagree on a single story:

| Storymap says | Tracker says | Code says | Resolution |
|---|---|---|---|
| slice-1 (planned) | closed/done | matching surface exists | `done` — already shipped; remove from slice-1, add to graduated set if activity now 100% done |
| slice-1 (planned) | open/in-progress | partial surface | `in-progress` — keep in slice-1, flag for completion |
| slice-1 (planned) | open | no matching surface | `unchanged` — proceed as planned |
| slice-1 (planned) | not in tracker | no surface | `unchanged` — but flag as untracked under "orphan storymap items" |
| slice-2 (deferred) | open in current sprint | active branch | **conflict** — tracker shows the team is doing it now despite storymap deferring it. Surface to user; honor the user's decision. |
| not in storymap | open in tracker | active branch | **orphan tracker item** — likely a new story; propose mapping or escalate |
| done (in prior storymap) | re-opened in tracker | new commits | `in-progress` (work resumed) — flag as a regression candidate; ask if AC has changed |
| cut (user stated previously) | open in tracker | no surface | **stale tracker** — propose closing the tracker issue; queue for write-back |

Whenever a conflict involves a user-stated preference (Person A said "we don't need RBAC in slice 1"), the user wins. Tag the resolution `[user-stated]` and update both storymap intent and the proposed tracker write-back.

## Outputs of Step 0.5

Step 0.5 doesn't produce a new top-level file — it appends to existing artifacts:

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
   - Code state: src/routes/ (12 routes), tests/e2e/ (61 tests), git log --since="2026-04-15"

   ## Activity status

   - **Sign in** — graduated 2026-05-12. All 4 stories shipped to production; activity remains in storymap as historical context but is excluded from active slicing.
   - **Find transaction** — partial; 2/5 done, 1 in-progress (PROJ-203, branch `feat/find-by-email`).
   ```

2. **`storymap.md`** gets per-story status annotations (see format above) and a new `## Shipped foundation` section if any activity has graduated.

3. **`backlog.csv`** gets `status`, `status_evidence`, `status_date` columns. Done/cut stories are excluded from re-prioritization in Step 4 (their old scores remain as audit trail).

4. **`handoff.md`** gets a `## Detected drift` section listing every orphan / conflict / proposed write-back. This is the Step 0.5 hand-off to the user for decisions.

## Write-back to the tracker

Reconciliation produces two kinds of status changes:

### Pull-only (tracker → storymap)

Tracker says PROJ-142 is closed; storymap pulls in `status: done`. **No write-back needed** — the tracker was already authoritative; we're just reflecting it locally.

### Push-required (storymap → tracker)

User confirms a story is `cut`; tracker still has it open as a pending issue. **Write-back required** — generate an update script.

Same opt-in protocol as `output-routing.md`: don't auto-execute. Generate `tracker-status-update.<ext>` and tell the user what running it would do.

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

**Linear** — call the Linear MCP directly with one operation per change; emit a `tracker-status-update.md` enumerating the calls instead of a runnable script.

For each script, include a header comment summarizing what it would do:
```bash
# tracker-status-update.sh — generated 2026-06-10 by user-story-mapping skill
# Summary: 4 issues closed (cut), 2 issues moved to PI-2026-Q3, 1 label updated.
# Review each line before running. To revert a transition, see your tracker's audit log.
```

### Hard rules for write-back

1. **Never auto-execute.** The user runs the script. This holds even when the user has approved write-back in principle — they review every batch.
2. **One direction at a time.** Don't try to push storymap → tracker AND pull tracker → storymap in a single script. Pull is automatic; push is opt-in.
3. **No silent state changes.** Every write-back action is logged in `handoff.md` under `## Tracker write-back actions`. Includes ticket id, before-state, after-state, reason.
4. **Reversibility note.** End the script with a comment saying how to undo each kind of action in the target tracker (e.g., "To revert a Jira transition, use `jira issue transition <ID> <prior-state>` or the tracker's audit-log restore").
5. **Tracker is one of many destinations.** If the user is using a sister-framework state directory (`.gsd/`, prior `TODO.md`) instead of a populated tracker, write-back targets *that* destination per `output-routing.md`'s persistence cascade — not the tracker. Don't push to a populated tracker without explicit user opt-in.

## Anti-patterns

- **Don't infer `done` from code alone.** A matching route with no test, or a test with no AC reference, is *evidence* — not proof. Always confirm via tracker or AC pass before marking `done`. Otherwise stories silently disappear from slicing because the agent saw a stub.
- **Don't silently absorb orphan tracker issues.** If the tracker has 12 issues you can't map to backbone activities, that's a 12-line section in `handoff.md`, not a 12-issue invisible append to slice 1.
- **Don't push status to the tracker without opt-in.** Even when the user said "yes, sync the tracker" once, every write-back batch needs review — same governance as outbound slice-1 routing.
- **Don't graduate a backbone activity from `done` count alone.** Confirm with the user that the activity is genuinely retired (e.g., "Sign in is shipped and stable, no further work expected for ≥1 PI"). Activities that are 100% done but actively being maintained (auth tweaks, security patches) should *stay* active with a note.
- **Don't re-litigate prior status decisions.** If `backlog.csv` had `status: cut` for S027 and tracker confirms closed, don't re-derive whether to cut. Use the existing decision; only re-evaluate if user re-opens it.
- **Don't conflate intent and status.** A re-sliced story (intent: now slice-2) is different from a deferred story (status: deferred). Intent is storymap authority; status is tracker authority. Annotate both, don't merge.

## Cost ceiling

Step 0.5 should consume 5-10% of the total turn budget. Most of the work is mining-already-mined — Step 0 has the inputs; 0.5 is the diff + drift detection.

If 0.5 exceeds 15%, you're either re-mining sources (don't — use what Step 0 already has in `## Context loop trace`) or doing exhaustive ticket-by-ticket comparison when a sample-and-spot-check would do. Sample drift detection: scan the first 20 tracker issues + the most recent 30 days of commits + every prior slice-1 story; if no drift, the rest is probably fine.

For trackers with >500 issues, pre-filter to the project's active labels / area paths / repos before reconciling — full sweeps are too slow and rarely reveal new drift past the first 100.

## Mode D and reconciliation

Mode D (extension of an existing storymap) **always runs Step 0.5**. The Mode D protocol is:

```
Step 0   — context loop, including prior storymap as input
Step 0.4 — fill new gaps (decisions log carries forward)
Step 0.5 — reconcile (this reference)
Step 1   — backbone (preserved unless user re-derives; graduated activities marked)
Step 2   — decompose new stories (Step 2 per-persona sweep applies)
... etc.
```

The Mode D diff in `handoff.md` (per `iterative-refinement-and-snapshots.md`) now includes a `## Status changes since prior run` section sourced from Step 0.5 reconciliation:

```markdown
## Status changes since prior run (2026-04-15 → 2026-06-10)

ADDED:
- 3 new stories proposed under Activity 4 (Approver decision) — drafted from interview notes
- 2 new tracker issues mapped to existing backbone activities

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

- **GSD** — `.gsd/task-summaries/` is essentially a status log; reconciliation reads it as authoritative for tasks already executed via `/gsd execute-task`. When GSD is the active framework, write-back targets `.gsd/` (per `output-routing.md`'s persistence cascade), not a populated tracker.
- **Superpowers** — `plans/` directory has step status; reconciliation reads completed plan steps as `done` evidence. Don't push to a Superpowers-managed tracker; let `writing-plans` handle re-decomposition for the next slice.
- **gstack** — gstack's `/retro` reads the storymap's Hypotheses table; reconciliation's `## Implementation status` table is also useful input. After Step 0.5, mention "the status table is ready for `/retro` if you want to evaluate which hypotheses played out".

## TL;DR

- Step 0.5 builds a status view from `prior storymap ⊕ tracker ⊕ code` whenever any two of those exist.
- Tracker is authority for **status**; storymap is authority for **intent**; code is **evidence**.
- Drift gets surfaced to the user in `handoff.md`, not silently absorbed.
- Activities with all stories `done` graduate out of active slicing but stay visible.
- Write-back to tracker is opt-in, scripted, never auto-executed.
- Mode D always runs reconciliation; from-scratch always skips it.
