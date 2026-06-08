# Work item tracking integration

After this skill produces `storymap.md`, `storymap.csv`, `backlog.md`, and `backlog.csv`, most teams will want to push the result into their existing tracker. This file is the reference for doing that cleanly across the popular tools.

The pattern is the same everywhere: **the CSV is the import source, you do not need to re-enter stories by hand.** Don't reinvent the structure inside each tool — keep this skill's artifacts as the source of truth and use the tool's import.

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

- **Story Points ≠ Job Size.** WSJF uses relative size, story points may already be calibrated differently. Don't auto-fill.
- **Epic Link vs. Parent**: Jira changed this in NextGen / company-managed projects. Confirm with the user which project type before mapping.
- **Workflow states**: backlog rows should land in the project's "Backlog" state, not "To Do" — those mean different things.

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

1. **Excel import** (most reliable): Open the CSV in Excel, install the Azure DevOps Excel plugin, paste with proper column mapping, publish. The plugin enforces field validity.
2. **`az boards` CLI**: Generate a shell script with one `az boards work-item create` per row. More reliable in CI pipelines.

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

1. Create a Project (v2) for the work
2. Add custom fields: Score (number), Method (single-select), Slice (single-select), Activity (single-select)
3. Use the GitHub CLI or the bulk-import API to create issues from the CSV
4. Attach issues to the Project — fields populate from labels via Project automation

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

- Trello: import CSV per list (one list per slice)
- Notion: import CSV as a database, group by `slice`, sort by `score`
- Airtable: import CSV as a base, build views per slice
- Spreadsheet: open `backlog.csv` directly

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

## Important — what NOT to do

- **Don't auto-create issues without asking.** Generating a script is helpful; running it in the user's tracker without confirmation is not.
- **Don't lose the reasoning column.** When importing, ensure the WSJF/RICE/MoSCoW *reasoning* lands somewhere readable. A score with no reasoning rots within a quarter.
- **Don't rename the activities to fit the tool.** If the team's Jira convention is "Epic-style: Improve X", and this skill produced "Find a property", keep both — put the user-narrative version in the Description and the tool-style version in the Title. The user-narrative is the discovery signal; losing it loses the map's value.
