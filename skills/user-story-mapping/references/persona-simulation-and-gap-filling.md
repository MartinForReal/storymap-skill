# Persona simulation and gap-filling

**Simulate personas proactively — before the interview, not as fallback inside it.** Once discovery names personas, spawn one in-character subagent per persona to surface, *first*, **cross-persona interactions** (handoffs / dependencies / conflicts), then conflicts/gaps worth asking. Step 0.4 resolves *blocking* ones. **User always wins over simulation**: simulated answers are hypotheses; disagreement logs future-slice risks. This reference owns subagent protocol, **persona interaction map** (handoffs → `depends_on` edges → slice-1 feasibility risks), conflict matrix, and gap classes (blocking / stage-local / deferrable).

## When to use

Use simulation when personas exist but voices are thin. Skip when data is complete or user wants speed-with-documented-gaps.

| Situation | Good fit |
|---|---|
| Named personas, no detail on what each wants | ✅ |
| Rich interview data for 1 persona, none for others | ✅ |
| Suspected stakeholder conflict (e.g., admin vs end-user), one interviewed | ✅ |
| Missing edge cases / failure modes / regulatory view | ✅ |
| Complete data for all personas | ❌ — skip |
| User wants fast turnaround with documented gaps | ❌ — skip |
| Personas vague/contradictory; simulation would amplify noise | ❌ — ask user first |

Simulation runs at **Step 0.3** after context collection (Step 0) and diff, before interview, feeding **Step 0.4** (interview + gap gate). Re-run only if persona roster changed.

## Classify every gap before you spend a turn on it

Classify before blocking planning. Step 0.4 gates **only blocking gaps**.

| Class | Definition | When to resolve | Example |
|---|---|---|---|
| **Blocking** | Changes backbone/slicing or contradicts authoritative input | **At Step 0.4** (gate planning) | "Two stakeholders want incompatible flows — which one wins?"; "Is this single-persona or multi-persona?" |
| **Stage-local** | Affects one downstream stage, not backbone/others | **At the stage's entry** (mini-resolution, just-in-time) | "Don't know the WSJF size of S027" (affects Step 4 only); "Don't know what regex S015 should match" (affects Step 4a only) |
| **Deferrable** | Refines output; missing info is precision | **In `handoff.md`** as open questions | "Don't know exact pricing tier — assumed $10 for RICE calc"; "Don't know exact Salesforce field name — referenced as 'opportunity ID'" |

### Resolving each class

**Blocking:** Step 0.3 surfaced these; present in interview and **let the user resolve**. User wins. Do not proceed to Step 1 until blocking conflicts are resolved (user decided/punted) AND unfilled gaps are documented as open questions OR user said "proceed with these gaps".

**Stage-local:** Note under `## Stage-local gaps to resolve` in `design.md`. At later stages, re-scan: do I have what THIS stage needs? If blocked, run mini Step 0.4 *scoped to that stage*: ask only its need, simulate relevant persona, mine relevant source. Resolve and continue; don't rewind.

**Deferrable:** Note under `## Open questions (deferrable)` in `design.md`; apply a reasonable default; tag field with `[inferred — see open question Q-XX]`; surface in `handoff.md`. **Never apply a default without disclosure.**

### Mid-stage discovery

If a NEW gap surfaces mid-stage (e.g., Step 2 reveals unknown persona X needs):

1. **Classify it** (blocking / stage-local / deferrable)
2. If **blocking** and would invalidate an earlier decision: stop, surface to user (or single-shot `handoff.md`), pause or proceed with flagged conditional commitment
3. If **stage-local** and addressable now: resolve in-place (ask / simulate / mine), continue
4. If **deferrable**: note it, apply a default, continue

### Late-stage escalation

If Step 4 or Step 4a reveals a gap that *would have changed* Step 1 (backbone) or Step 3 (slicing):

1. **Don't silently rewrite** Steps 1-3 — that loses the audit trail
2. Surface in `handoff.md` under `## Late-discovered gaps`: gap, affected output, current assumption
3. Recommend (a) accept current output with caveat, or (b) re-run from affected stage with new info
4. User decides

### Why classify at all

Classification keeps Step 0.4 tight. Without it, the gate blocks on minor details or gets bypassed ("I'll figure it out as I go"), burying assumptions. Only true planning risks block; everything else resolves later.

## User input wins over simulation

When simulation and user disagree, user wins — always. Log simulated objection as future-slice risk; don't re-litigate. Full priority order and source-tag vocabulary (including `[simulated: <name>]`, required on simulated output) live in [`SKILL.md`](../SKILL.md#rules-that-govern-every-run); they apply here verbatim.

## The simulation protocol

### Step 1 — Inventory gaps

Before spawning subagents, list concrete questions. "We need more discovery" is not a gap; "How does admin prioritize RBAC vs setup speed?" is.

Put the gap checklist in the design doc draft:

```markdown
## Gaps blocking commitment

- [ ] How does Tenant Admin prioritize RBAC complexity vs setup time?
- [ ] What's End User's tolerance for switching between projects mid-task?
- [ ] Does Compliance care about real-time audit visibility or daily-batch is fine?
- [ ] How will Sales price the on-prem tier vs SaaS?
```

### Step 2 — Brief each persona subagent

For each gap, identify best-fit persona(s), then brief a subagent:

```
You are <persona name>, a <role> at <company-type>.

Background:
- <day-to-day responsibilities>
- <tools you use>
- <pain points you've expressed>
- <verbatim quotes if available>
- <constraints you operate under>

Other personas:
- <persona B>: <one-line role + what they do>
- <persona C>: <one-line role + what they do>

Answer planning questions in-character.
- Speak in first person ("I would..." not "they would...")
- If you don't know, say "I don't know" — do not invent
- If ambiguous, ask for clarification
- **Name your cross-persona interactions explicitly.** For handoffs, dependencies, or received work, say so ("I submit the refund, then it goes to the Approver"; "I can't audit until Compliance gets the event stream"). Cross-references matter as much as own steps.
- If your perspective conflicts with another stakeholder, flag it ("I think X, but I bet the admin team would push back because...")

Do not synthesize. You are one voice. The orchestrator will arbitrate.

Questions:
1. <gap question 1>
2. <gap question 2>
...
```

### Step 3 — Spawn subagents in parallel

Spawn one subagent per persona, all in one turn. Each returns in-character answers.

If a subagent says "I don't know", escalate to the user.

### Step 4 — Aggregate: detect conflicts and map interactions

Arbitration produces **conflict matrix** (personas disagree) and **persona interaction map** (personas connect).

Build conflict matrix first:

```markdown
## Persona perspective matrix

| Question | Tenant Admin (sim) | End User (sim) | Compliance (sim) | Conflict? |
|---|---|---|---|---|
| RBAC granularity | "Role-based, not user-based; easier to manage" | "Give me a 'follow' button without admin" | "Audit needs user-level, not role-level" | YES (admin↔compliance) |
| Real-time audit | "Daily batch is fine" | (not asked) | "Real-time for breach detection; batch for compliance" | YES (admin↔compliance) |
| Project switching | "I don't switch" | "Need 2-click switching with state preserved" | (not asked) | NO |
```

Conflicts are findings, not failures. Resolve by user input ("compliance wins — go user-level"), product strategy ("surface role-level for admins, user-level for compliance"), or deferral ("park to slice 2").

#### Persona interactions

Conflicts show where personas *disagree*; interactions show where they *connect*: handoffs, dependencies, touchpoints. Build this artifact in `design.md` under `## Persona interactions`:

```markdown
## Persona interactions

| From → To | At which activity | Interaction | Becomes |
|---|---|---|---|
| CS rep → Approver | Issue refund | Hands off refunds above auto-approve limit | cross-persona `depends_on` (approver story blocks on rep story) |
| System → Compliance | Audit | Emits Compliance event stream | shared touchpoint + sequencing note |
| Admin → End user | Sign in | Admin provisions SSO before end-user sign-in | cross-persona `depends_on` |
```

Each row becomes:

- a **cross-persona `depends_on` edge** in `backlog.csv` (Step 4) when one persona's story is another's precondition. Every precondition becomes a Hard (`H:`) edge; mechanics, cycle detection, and feasibility math live in [dependency-tracking.md](dependency-tracking.md). This map is where `H:` edges are *born*.
- a **handoff annotation** on the story, or
- a **shared-touchpoint sequencing note**.

A handoff crossing a slice boundary is a **slice-1 feasibility risk**: downstream can't ship without upstream. Flag it so Step 3/4 can pull upstream into slice 1 or move downstream out. Model only slicing/sequencing handoffs.

### Step 5 — Present back to user

```markdown
## Findings from persona simulation

I simulated 3 personas before backbone work. Highlights:

**Conflicts requiring your decision:**
- RBAC granularity: Admin wants role-based; Compliance needs user-level audit. Suggest: ship both, default role-level, log user-level. Need your call.
- Real-time audit: Admin says batch; Compliance needs real-time breach detection. Suggest: real-time emit, batch consumption — call on batch-only in slice 1.

**Gaps simulation couldn't fill — need you:**
- On-prem pricing strategy (no persona knows — escalate to Sales)
- App Store review buffer (operational, not persona-based — escalate to release manager)

**Confirmed (no conflict, low risk):**
- Project switching: ~2-click, state preserved — both personas align
- Daily-active-user dashboards: admins want, end users don't care, compliance neutral
```

Record user conflict decisions in design doc decisions log with date/reasoning.

### Step 6 — Gate the planning step

**Do not proceed to Step 1 (Establish backbone) until either:**

- All conflicts are resolved (user decided or explicitly punted), AND
- All gaps that simulation couldn't fill are documented as open questions OR the user has said "proceed with these gaps"

If forced to proceed with open gaps (e.g., rushed PI planning), tag affected `backlog.csv` stories with `gap_dependency:<question-id>` so conditional commitments are visible.

## Anti-patterns

- **Don't let simulation override user statements.** If user said "we don't need RBAC in PI 1" and simulated Compliance says "you absolutely need RBAC", user wins. Surface objection as future-slice risk; don't re-litigate.
- **Don't simulate a persona you have no information about.** "I'll just role-play a CFO" — based on what? Without verbatim/role context, simulation produces stereotypes. Gather context or skip.
- **Don't fabricate verbatim quotes from simulation.** Simulated outputs are inferences, not data. Tag `[simulated: <name>]` always. Keep interview verbatims separate.
- **Don't infinite-loop on gap closure.** If gaps remain after 2 rounds of simulation + user-confirmation, stop. Document conditionality, proceed with caveat, schedule follow-up.

## Cost ceiling

Each persona subagent costs about a small synthesis run. For 3 personas and 5 gaps, budget ~15-20% of turns. If gaps exceed 10 questions or personas exceed 5, ask user to narrow scope before simulating.

## Wiring into the workflow

```
Step 0    — Context collection loop (memory + interview synthesis as sub-flavors)
Step 0.3  — Simulate (this reference): one subagent/persona → interaction map + conflict matrix + gap inventory
           ↓
Step 0.4  — Interview: present findings; user resolves blocking conflicts/gaps (user wins over simulation)
           ↓
           Gate: do not proceed until conflicts resolved + gaps documented
           ↓
Step 1+   — Establish backbone
```

## Single-shot caveat

When automated evals or hands-off invocations prevent mid-task user response:

- Still spawn persona simulations
- Still build conflict matrix and persona interaction map
- Document conflicts/gaps as "blocking decisions" in `handoff.md`
- Proceed with strongest defensible interpretation, but tag every conditional commitment with the gap-id
- Handoff names the smallest next decision before commitment

User-input-authoritative still holds: any preference in the original prompt wins over simulated conflict.
