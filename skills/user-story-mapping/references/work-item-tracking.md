# Work item tracking integration

**The CSV is the import source — never re-enter stories by hand into a tracker, and never invent a structure that already exists there.** When no tracker is defined, seed a fresh one from `storymap.csv` / `backlog.csv` using the per-tool import tables below. When a tracker *is* defined, do the reverse: read its existing taxonomy read-only and map the storymap onto the team's own epics, fix-versions, labels, and custom fields. Writes are always opt-in scripts the user reviews — this skill proposes, it never auto-creates.

## When to use

Two directions, both rooted here:

- **Seeding (empty baseline, no tracker defined).** The team wants the backlog pushed into Jira / ADO / GitHub / Linear / a spreadsheet. Use the per-tool import sections. The storymap is authoritative — you are populating an empty system.
- **Aligning (a tracker is defined).** A tracker is already the system of record. Read its taxonomy in Step 0 and map onto it (the next section). Here the tracker owns *structure*; the storymap owns *intent*.

Check [output-routing.md](output-routing.md#detecting-the-empty-baseline-no-tracker-defined) first — it owns the operational "tracker defined" test and the routing decision. Pushing fresh stories into a populated tracker without opt-in is usually the wrong destination.

Status pull-back and write-back (existing projects, after Step 0.5 has reconciled storymap ↔ tracker ↔ code) are governed by [progress-reconciliation.md](progress-reconciliation.md), not this file. The per-tracker mappings are the same; what differs is *who's authoritative for what* — when seeding, the storymap is; when reconciling, the tracker is authoritative for *status*, the storymap for *intent*. Read `progress-reconciliation.md` before generating any tracker write-back script.

## Align to the existing tracker taxonomy

When a tracker is already the system of record, do **not** invent a parallel structure. Read its existing taxonomy in Step 0 — read-only, via the tracker MCP — and map the storymap onto it. This is the reverse of the per-tool import tables below (which assume a fresh, empty tracker).

**Pull, read-only:** the **process template** (agile/scrum/CMMI/basic), issue types, **labels/tags**, **components**, **epics**, **fix-versions / iteration-paths / cycles / milestones**, the priority scheme, and relevant **custom fields** (story points, WSJF/RICE). Then map, reusing existing names:

| Storymap | Reuse from the tracker |
|---|---|
| Activity | an existing **epic** or **component** (match by meaning) |
| Slice | an existing **fix-version / iteration / cycle / milestone** |
| Persona | an existing **label** (e.g. `persona:cs-rep`) or user-picker field |
| Score / method | the existing **custom field** (don't add a parallel one) |
| Priority | the tracker's existing scheme |

Rules:

- **Propose, never auto-create.** If the storymap needs a category the tracker lacks — a new epic, a new fix-version — list it as a *proposed* addition for the user. Don't create it. Writes are opt-in scripts only.
- **Keep the user-narrative name in the description, the tool name in the title.** When the storymap's discovery name ("Find a property") and the team's tracker convention ("Epic-style: Improve search") differ, keep **both** — put the user-narrative version in the description and the tool-convention name in the title. The user-narrative is the discovery signal; overwriting it loses the map's value. (See also "what NOT to do" below.)
- **Persist the mapping.** Save the chosen field-mapping + taxonomy snapshot to the `tracker` block of `.user-story-mapping/state.json` ([persistent-knowledge.md §A](persistent-knowledge.md#a-project-scoped--user-story-mapping-directory-in-the-repo)) so the next run stays consistent. Treat the saved taxonomy as a *hint* — reload and re-verify it against the live tracker before reusing, and refresh on drift.

## Enable the tracker burn-down

When an issue tracker is the system of record, the skill does **not** emit `backlog.{md,csv}` or `storymap.mmd` ([output-routing.md § What each branch produces](output-routing.md#what-each-branch-produces)) — the tracker provides the live ranked view + visualization. `storymap.csv` is still produced as a checked-in items+status snapshot. The opt-in write-back sets three native fields per item so the tracker's own burn-down chart renders. Map them from artifacts the skill already produces:

| Burn-down field | Source in the plan | Jira | Azure DevOps | GitHub Projects |
|---|---|---|---|---|
| **Estimate / story points** | the Step 4 sizing (WSJF job-size or RICE effort) | `Story Points` custom field | `Microsoft.VSTS.Scheduling.StoryPoints` | a `Points` number field |
| **Sprint / iteration** | the slice → the tracker's existing iteration (per [§ Align to the existing tracker taxonomy](#align-to-the-existing-tracker-taxonomy)) | Sprint / `fixVersion` | `IterationPath` | an `Iteration` field |
| **Status** | the Step 0.5 reconciled status (owned by [progress-reconciliation.md](progress-reconciliation.md)) | workflow state | `State` | a `Status` field |

(Linear maps the same way: the estimate property, a Cycle, and issue status.)

Rules:

- **Estimate ≠ raw WSJF size if the team already calibrates points.** Propose the size as the points value; if the tracker already carries team-calibrated points (pulled in the taxonomy read), don't overwrite — flag the delta for the user.
- **Reuse existing iterations/sprints; never invent.** The slice maps onto the team's existing fix-version/iteration; a new one is a *proposed* addition, not an auto-create.
- **Opt-in, never auto-run.** These field writes ride the same `tracker-status-update.<ext>` script governed by [progress-reconciliation.md § Write-back to the tracker](progress-reconciliation.md#write-back-to-the-tracker) — one direction, every action logged, reversibility noted. The skill generates it; the user runs it.
- Once points + iteration + status are set on every item, the tracker's native burn-down (Jira Sprint Report, ADO Sprint Burndown, GitHub Projects insights) works with no extra artifact.

Everything below assumes the **seeding** direction.

## Jira

### Hierarchy mapping

| This skill | Jira |
|---|---|
| Activity | Epic |
| Task | Initiative under Epic, *or* a label, *or* skip if your team uses 2 levels |
| Story | Story |
| Slice | Fix Version, *or* a custom field, *or* a sprint mapping |
| Persona | Custom user-picker field, *or* a label like `persona:buyer` |
| Outcome | Description body (use the "As a... so that..." form) |
| WSJF/RICE score | Custom number field |
| Reasoning | Description body |

### Import path

Jira's CSV importer is the right tool. Settings → System → External System Import → CSV.

```
1. Map columns: activity → Epic Name, story → Summary, outcome → Description
2. Set issue type per row using the activity vs. story distinction
3. Map slice → Fix Version (create the versions in advance)
4. Set custom fields for score + method
```

If you have hundreds of rows, do a 5-row dry run first. Jira's "Begin Import" button is non-reversible at scale.

### When the Jira instance is restrictive

Many enterprise Jira tenants disable CSV import for non-admins. In that case, output the rows as a list of `jira create` REST calls or generate a JSONL file the user's admin can run. Don't try to drive Jira through the UI from here.

### Custom field gotchas

- **Story Points ≠ Job Size.** WSJF uses relative size; story points may already be calibrated differently. Don't auto-fill.
- **Epic Link vs. Parent.** Jira changed this in NextGen / company-managed projects. Confirm with the user which project type before mapping.
- **Workflow states.** Backlog rows should land in the project's "Backlog" state, not "To Do" — those mean different things.

## Azure DevOps (ADO)

### Hierarchy mapping

| This skill | ADO (Agile process) | ADO (Scrum process) |
|---|---|---|
| Activity | Epic | Epic |
| Task | Feature | Feature |
| Story | User Story | Product Backlog Item |
| Slice | Iteration Path | Iteration Path |
| Persona | Custom field, or Tag `persona:<name>` | same |
| Outcome | Acceptance Criteria | Acceptance Criteria |
| Score | Custom field | Custom field |
| Reasoning | Description | Description |

ADO's process template (Agile / Scrum / CMMI / Basic) determines the work item types. Ask the user which one their project uses before importing.

### Import path

Two options:

1. **Excel import** (most reliable): open the CSV in Excel, install the Azure DevOps Excel plugin, paste with proper column mapping, publish. The plugin enforces field validity.
2. **`az boards` CLI**: generate a shell script with one `az boards work-item create` per row. More reliable in CI pipelines.

```bash
# Example az boards command this skill can generate
az boards work-item create \
  --type "User Story" \
  --title "$story" \
  --description "$outcome" \
  --area-path "Project\\Team" \
  --iteration-path "Project\\Sprint 1"
```

### ADO Boards quirks

- Iteration paths must exist before you assign to them. Create the slices as iterations first.
- Tags use `;`-separated format in CSV.
- Linking a Story to a Feature parent uses `--parent <id>`, not a column — chain creates and capture IDs.

## GitHub Issues + Projects (v2)

### Hierarchy mapping

GitHub Issues is flatter than Jira/ADO. Use labels and Projects to encode hierarchy.

| This skill | GitHub |
|---|---|
| Activity | Label `activity:<name>` *and/or* a Milestone *and/or* a Project category |
| Task | Label `task:<name>` |
| Story | Issue title |
| Slice | Milestone *or* Project iteration *or* Label `slice:<name>` |
| Persona | Label `persona:<name>` |
| Outcome | Issue body |
| Score | Project custom field (number) |
| Method | Project custom field (single-select: WSJF/RICE/MoSCoW) |

### Recommended setup

1. Create a Project (v2) for the work.
2. Add custom fields: Score (number), Method (single-select), Slice (single-select), Activity (single-select).
3. Use the GitHub CLI or the bulk-import API to create issues from the CSV.
4. Attach issues to the Project — fields populate from labels via Project automation.

```bash
# Bulk-create from CSV using gh CLI
while IFS=',' read -r id activity task story persona outcome slice; do
  gh issue create \
    --title "$story" \
    --body "$(printf 'Persona: %s\nOutcome: %s\nSlice: %s' "$persona" "$outcome" "$slice")" \
    --label "activity:$activity,slice:$slice,persona:$persona"
done < storymap.csv
```

### Why labels over a deep hierarchy

GitHub doesn't have native sub-issues (Tasks under Stories) outside of beta features. Trying to fake it with linked issues creates clicking overhead. Labels + Projects is the path of least resistance.

## Linear

Increasingly popular in startups. Has cleaner abstractions than Jira.

| This skill | Linear |
|---|---|
| Activity | Project (within a Team) |
| Task | (skip, or use Cycle) |
| Story | Issue |
| Slice | Cycle *or* Project milestone |
| Persona | Label |
| Score | Custom property (Premium plan) or `Priority` enum (Free) |

Linear has a great CSV importer — point it at `storymap.csv` and map columns in the UI. The free tier limits custom fields, so you may need to overload Description with the WSJF/RICE breakdown.

## Trello / Notion / Airtable / "we use a spreadsheet"

For lightweight setups, the CSV files this skill produces are usable as-is. No special handling needed:

- **Trello**: import CSV per list (one list per slice).
- **Notion**: import CSV as a database, group by `slice`, sort by `score`.
- **Airtable**: import CSV as a base, build views per slice.
- **Spreadsheet**: open `backlog.csv` directly.

## ART tools (Jira Align, Targetprocess, Tempo)

These speak SAFe natively and have first-class WSJF support. Use the SAFe column mapping (Activity→Epic, Task→Feature, Story→Story) and let the tool calculate WSJF rather than pre-computing.

For Jira Align: it imports from Jira, so push to Jira first then sync.

## Decision tree for the user

```
Does the user explicitly mention a tool?
├── YES → use that tool's section above
└── NO  → ask once: "Will you push these into Jira/ADO/GitHub/Linear/other,
         or just keep them as files for now?"

Does the user want a one-shot import or ongoing sync?
├── ONE-SHOT → CSV import is fine
└── ONGOING SYNC → out of scope for this skill. Recommend exporting/regenerating
                  rather than syncing — the story map is a discovery artifact,
                  not a live database.
```

## What NOT to do

- **Don't auto-create issues without asking.** Generating a script is helpful; running it in the user's tracker without confirmation is not. Tracker write-back is opt-in only.
- **Don't lose the reasoning column.** When importing, ensure the WSJF/RICE/MoSCoW *reasoning* lands somewhere readable. A score with no reasoning rots within a quarter.
- **Don't rename the activities to fit the tool.** If the team's Jira convention is "Epic-style: Improve X" and this skill produced "Find a property", keep both — put the user-narrative version in the Description and the tool-style version in the Title. The user-narrative is the discovery signal; losing it loses the map's value.
- **Don't create taxonomy the tracker is missing.** Propose new epics / fix-versions / labels for the user to approve; never add them silently.
