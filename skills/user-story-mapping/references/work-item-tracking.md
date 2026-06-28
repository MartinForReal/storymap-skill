# Work item tracking integration

**The CSV is the import source — never re-enter stories by hand or invent existing tracker structure.** No tracker: seed from `storymap.csv` / `backlog.csv` using tables below. Tracker defined: read taxonomy read-only; map onto team epics, fix-versions, labels, custom fields. Writes are reviewed opt-in scripts; this skill proposes, never auto-creates.

## When to use

Two directions:

- **Seeding (empty baseline, no tracker defined).** Team wants backlog in Jira / ADO / GitHub / Linear / spreadsheet. Use imports below. Storymap authoritative; populate empty tracker.
- **Aligning (a tracker is defined).** Tracker is system of record. Read taxonomy in Step 0 and map onto it (next section). Tracker owns *structure*; storymap owns *intent*.

Check [output-routing.md](output-routing.md#detecting-the-empty-baseline-no-tracker-defined) first; it owns the "tracker defined" test/routing. Fresh stories into a populated tracker require opt-in.

Status pull-back/write-back after Step 0.5 reconciles storymap ↔ tracker ↔ code are governed by [progress-reconciliation.md](progress-reconciliation.md), not this file. Mappings stay; authority changes. Seeding: storymap authoritative. Reconciling: tracker owns *status*, storymap owns *intent*. Read it before write-back scripts.

## Align to the existing tracker taxonomy

When tracker is system of record, do **not** invent parallel structure. In Step 0, read taxonomy read-only via tracker MCP and map the storymap onto it. This reverses the fresh-tracker tables below.

**Pull, read-only:** **process template** (agile/scrum/CMMI/basic), issue types, **labels/tags**, **components**, **epics**, **fix-versions / iteration-paths / cycles / milestones**, priority scheme, relevant **custom fields** (story points, WSJF/RICE). Reuse names:

| Storymap | Reuse from the tracker |
|---|---|
| Activity | existing **epic**/**component** (match meaning) |
| Slice | existing **fix-version / iteration / cycle / milestone** |
| Persona | existing **label** (e.g. `persona:cs-rep`) or user-picker |
| Score / method | existing **custom field** (don't add a parallel one) |
| Priority | existing scheme |

- **Propose, never auto-create.** Missing tracker category (new epic, new fix-version) becomes *proposed*. Writes are opt-in scripts only.
- **Keep user-narrative name in description, tool name in title.** If discovery says "Find a property" and tracker convention says "Epic-style: Improve search", keep **both**: user-narrative in description, tool-convention in title. User-narrative is discovery signal; overwriting loses map value. (See also "what NOT to do" below.)
- **Persist the mapping.** Save field mapping + taxonomy snapshot to the `tracker` block of `.user-story-mapping/state.json` ([persistent-knowledge.md §A](persistent-knowledge.md#a-project-scoped--user-story-mapping-directory-in-the-repo)). Treat saved taxonomy as *hint*: reload, verify live tracker, refresh on drift.

## Enable the tracker burn-down

When tracker is system of record, the skill does **not** emit `backlog.{md,csv}` or `storymap.mmd` ([output-routing.md § What each branch produces](output-routing.md#what-each-branch-produces)); tracker provides live ranked view + visualization. `storymap.csv` remains checked-in items+status snapshot. Opt-in write-back sets burn-down fields:

| Burn-down field | Source in the plan | Jira | Azure DevOps | GitHub Projects |
|---|---|---|---|---|
| **Estimate / story points** | Step 4 sizing (WSJF job-size or RICE effort) | `Story Points` | `Microsoft.VSTS.Scheduling.StoryPoints` | `Points` number field |
| **Sprint / iteration** | slice → tracker iteration (per [§ Align to the existing tracker taxonomy](#align-to-the-existing-tracker-taxonomy)) | Sprint / `fixVersion` | `IterationPath` | `Iteration` |
| **Status** | Step 0.5 reconciled status (owned by [progress-reconciliation.md](progress-reconciliation.md)) | workflow state | `State` | `Status` field |

(Linear maps the same way: estimate property, Cycle, issue status.)

- **Estimate ≠ raw WSJF size if the team already calibrates points.** Propose size as points; if taxonomy read finds calibrated points, flag delta instead of overwriting.
- **Reuse existing iterations/sprints; never invent.** Slice maps to existing fix-version/iteration; new one is *proposed*, not auto-created.
- **Opt-in, never auto-run.** Field writes use the same `tracker-status-update.<ext>` script governed by [progress-reconciliation.md § Write-back to the tracker](progress-reconciliation.md#write-back-to-the-tracker): one direction, every action logged, reversibility noted. Skill generates; user runs.
- Once points + iteration + status are set, native burn-down (Jira Sprint Report, ADO Sprint Burndown, GitHub Projects insights) works with no extra artifact.

Below assumes **seeding**.

## Jira

### Hierarchy mapping

| This skill | Jira |
|---|---|
| Activity | Epic |
| Task | Initiative, label, or skip if team uses 2 levels |
| Story | Story |
| Slice | Fix Version, custom field, or sprint mapping |
| Persona | Custom user-picker field, or label like `persona:buyer` |
| Outcome | Description ("As a... so that..." form) |
| WSJF/RICE score | Custom number field |
| Reasoning | Description body |

### Import path

Jira CSV importer: Settings → System → External System Import → CSV.

```
1. Map columns: activity → Epic Name, story → Summary, outcome → Description
2. Set issue type per activity vs. story
3. Map slice → Fix Version (create the versions in advance)
4. Set custom fields for score + method
```

For hundreds, run a 5-row dry run; Jira "Begin Import" is non-reversible at scale.

### When the Jira instance is restrictive

If CSV import is disabled for non-admins, output `jira create` REST calls or JSONL for admin. Don't drive UI.

### Custom field gotchas

- **Story Points ≠ Job Size.** WSJF uses relative size; points may be calibrated differently. Don't auto-fill.
- **Epic Link vs. Parent.** Jira changed this in NextGen / company-managed projects. Confirm project type before mapping.
- **Workflow states.** Backlog rows land in "Backlog", not "To Do" — those differ.

## Azure DevOps (ADO)

### Hierarchy mapping

| This skill | ADO (Agile) | ADO (Scrum) |
|---|---|---|
| Activity | Epic | Epic |
| Task | Feature | Feature |
| Story | User Story | Product Backlog Item |
| Slice | Iteration Path | Iteration Path |
| Persona | Custom field or Tag `persona:<name>` | same |
| Outcome | Acceptance Criteria | Acceptance Criteria |
| Score | Custom field | Custom field |
| Reasoning | Description | Description |

ADO template (Agile / Scrum / CMMI / Basic) determines work item types. Ask which applies before importing.

### Import path

Two paths:

1. **Excel import** (most reliable): open CSV in Excel, install Azure DevOps Excel plugin, map columns, publish. Plugin enforces fields.
2. **`az boards` CLI**: generate one `az boards work-item create` per row. Better for CI.

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

- Iteration paths must exist before assignment. Create slice iterations first.
- Tags use `;`-separated format in CSV.
- Story→Feature parent uses `--parent <id>`, not a column — chain creates and capture IDs.

## GitHub Issues + Projects (v2)

### Hierarchy mapping

GitHub Issues is flat; use labels and Projects for hierarchy.

| This skill | GitHub |
|---|---|
| Activity | Label `activity:<name>`, Milestone, and/or Project category |
| Task | Label `task:<name>` |
| Story | Issue title |
| Slice | Milestone, Project iteration, or Label `slice:<name>` |
| Persona | Label `persona:<name>` |
| Outcome | Issue body |
| Score | Project number field |
| Method | Project single-select: WSJF/RICE/MoSCoW |

### Recommended setup

1. Create a Project (v2).
2. Add fields: Score (number), Method (single-select), Slice (single-select), Activity (single-select).
3. Use GitHub CLI or bulk-import API to create issues from CSV.
4. Attach issues; Project automation populates fields from labels.

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

GitHub lacks stable native sub-issues (Tasks under Stories). Linked-issue hierarchies add clicks. Use Labels + Projects.

## Linear

Linear is startup-common and cleaner than Jira.

| This skill | Linear |
|---|---|
| Activity | Project (within a Team) |
| Task | (skip, or use Cycle) |
| Story | Issue |
| Slice | Cycle *or* Project milestone |
| Persona | Label |
| Score | Custom property (Premium) or `Priority` enum (Free) |

Linear CSV importer reads `storymap.csv`; map columns in UI. Free tier limits custom fields, so put WSJF/RICE breakdown in Description if needed.

## Trello / Notion / Airtable / "we use a spreadsheet"

For lightweight setups, use CSV as-is:

- **Trello**: import CSV per list (one list/slice).
- **Notion**: import CSV as database, group by `slice`, sort by `score`.
- **Airtable**: import CSV as base, build views per slice.
- **Spreadsheet**: open `backlog.csv`.

## ART tools (Jira Align, Targetprocess, Tempo)

These speak SAFe and support WSJF. Use SAFe mapping (Activity→Epic, Task→Feature, Story→Story); let the tool calculate WSJF.

For Jira Align, push to Jira, then sync.

## Decision tree for the user

```
Does user mention a tool?
├── YES → use that section above
└── NO  → ask once: "Will you push these into Jira/ADO/GitHub/Linear/other,
         or just keep them as files for now?"

One-shot import or ongoing sync?
├── ONE-SHOT → CSV import is fine
└── ONGOING SYNC → out of scope. Recommend exporting/regenerating
                  rather than syncing — story map is a discovery artifact,
                  not a live database.
```

## What NOT to do

- **Don't auto-create issues without asking.** Generate scripts; never run them without confirmation. Tracker write-back is opt-in only.
- **Don't lose the reasoning column.** Ensure WSJF/RICE/MoSCoW *reasoning* lands somewhere readable. Score without reasoning rots within a quarter.
- **Don't rename activities to fit the tool.** If Jira convention says "Epic-style: Improve X" and this skill produced "Find a property", keep both: user-narrative in Description, tool-style in Title. User-narrative is discovery signal; losing it loses map value.
- **Don't create missing taxonomy.** Propose new epics / fix-versions / labels for approval; never add silently.
