# Persona simulation and gap-filling

**Simulate the personas proactively — before the interview, not as a fallback inside it.** Once discovery names the personas, spawn one in-character subagent per persona to surface, *first*, the **cross-persona interactions** (who hands off to / depends on / conflicts with whom), then the conflicts and the gaps worth asking about. The interview (Step 0.4) then resolves the *blocking* ones — and the **user always wins over simulation**: a simulated answer is a hypothesis, and when the user disagrees the simulated objection becomes a logged future-slice risk. This reference owns the persona-simulation subagent protocol, the **persona interaction map** (cross-persona handoffs → `depends_on` edges → slice-1 feasibility risks), the conflict matrix, and how to classify a gap (blocking / stage-local / deferrable) for the interview gate.

## When to use

Reach for persona simulation when you have personas but not enough of their voices to plan honestly. Skip it when the user already gave you everything, or wants speed-with-documented-gaps over thorough exploration.

| Situation | Good fit |
|---|---|
| User has named personas but provided no detail on what each wants | ✅ |
| User has provided rich interview data for 1 persona, none for others | ✅ |
| Conflict suspected between two stakeholder groups (e.g., admin vs end-user) but only one was interviewed | ✅ |
| Edge cases / failure modes / regulatory perspectives missing from happy-path narrative | ✅ |
| User has provided complete data on all personas | ❌ — skip |
| User wants fast turnaround with documented gaps rather than thorough exploration | ❌ — skip |
| Personas are vague or contradictory; simulation would amplify noise | ❌ — ask user first |

Simulation runs at **Step 0.3** — after context collection (Step 0) and the diff, before the interview — and feeds **Step 0.4** (the interview + gap gate). Re-run it on a loop-back only if discovery materially changed the persona roster.

## Classify every gap before you spend a turn on it

Not every gap should block planning. Classify each gap first; the Step 0.4 gate applies **only to blocking gaps**, while stage-local and deferrable gaps move forward with the workflow.

| Class | Definition | When to resolve | Example |
|---|---|---|---|
| **Blocking** | Would change the backbone, slicing strategy, or contradict the user's authoritative input | **At Step 0.4** (gate planning) | "Two stakeholders want incompatible flows — which one wins?"; "Is this single-persona or multi-persona?" |
| **Stage-local** | Affects one downstream stage's output but not the backbone or other stages | **At the stage's entry** (mini-resolution, just-in-time) | "Don't know the WSJF size of S027" (affects Step 4 only); "Don't know what regex S015 should match" (affects Step 4a only) |
| **Deferrable** | Refines output but doesn't change it; missing info is precision, not direction | **In `handoff.md`** as open questions | "Don't know exact pricing tier — assumed $10 for RICE calc"; "Don't know exact Salesforce field name — referenced as 'opportunity ID'" |

### Resolving each class

**Blocking:** the simulation (Step 0.3) has already surfaced these as conflicts/gaps; present them at the interview and **let the user resolve** — the user's call always wins over the simulated position. Do not proceed to Step 1 until all blocking conflicts are resolved (user decided or explicitly punted) AND any gaps simulation couldn't fill are documented as open questions OR the user has said "proceed with these gaps".

**Stage-local:** Note under `## Stage-local gaps to resolve` in `design.md`. When entering each subsequent stage, do a quick re-scan: do I have what I need for THIS stage? If a stage-local gap blocks the stage, run a mini Step 0.4 *scoped to that stage* — ask only what that stage needs, simulate only the relevant persona, mine only the relevant source. Resolve, then continue. Don't rewind earlier stages.

**Deferrable:** Note under `## Open questions (deferrable)` in `design.md`; apply a reasonable default; tag the affected field with `[inferred — see open question Q-XX]`; surface in `handoff.md` so the user can validate. **Never silently apply a default without disclosure.**

### Mid-stage discovery

If a NEW gap surfaces mid-stage (e.g., during Step 2 you realize persona X has needs you don't know about):

1. **Classify it** (blocking / stage-local / deferrable) using the table above
2. If **blocking** and would invalidate an earlier stage's decision: stop, surface to the user (or in single-shot, to `handoff.md`), pause for user input or proceed with a clearly-flagged conditional commitment
3. If **stage-local** and addressable now: resolve in-place (ask / simulate / mine), continue
4. If **deferrable**: note it, apply a default, continue

### Late-stage escalation

If at Step 4 or Step 4a a gap emerges that *would have changed* a Step 1 (backbone) or Step 3 (slicing) decision had it been known upfront:

1. **Don't silently rewrite** Steps 1-3 — that loses the audit trail
2. Surface in `handoff.md` under `## Late-discovered gaps`: what the gap is, what stage's output it would have changed, what the current output assumed
3. Recommend either (a) accept the current output with the caveat documented, or (b) re-run from the affected stage with the new info
4. User decides

### Why classify at all

Without classification, Step 0.4 becomes a giant gate that either blocks too eagerly (every minor missing detail stops the workflow → user frustration, slow output) or is silently bypassed (agent proceeds with "I'll figure it out as I go" → buried assumptions surface in retro). Classification keeps the gate tight on what actually matters while letting the rest resolve at the right time and cost.

## User input wins over simulation

When persona simulation and the actual user disagree, the user wins — always. Log the simulated objection as a future-slice risk; don't re-litigate. The full priority order and source-tag vocabulary (including `[simulated: <name>]`, which every simulated output must carry) live once in [`SKILL.md`](../SKILL.md#rules-that-govern-every-run); they apply here verbatim.

## The simulation protocol

### Step 1 — Inventory gaps

Before spawning anything, list the specific questions you'd ask. Be concrete; "we need more discovery" is not a gap. "We don't know how the admin persona prioritizes RBAC granularity vs setup speed" is a gap.

Output the gap list in the design doc draft as a checklist:

```markdown
## Gaps blocking commitment

- [ ] How does Tenant Admin prioritize RBAC complexity vs setup time?
- [ ] What's End User's tolerance for switching between projects mid-task?
- [ ] Does Compliance care about real-time audit visibility or daily-batch is fine?
- [ ] How will Sales price the on-prem tier vs SaaS?
```

### Step 2 — Brief each persona subagent

For each gap, identify the persona(s) best suited to answer. Brief a subagent with:

```
You are <persona name>, a <role> at <company-type>.

Background (everything we know about you):
- <day-to-day responsibilities>
- <tools you use>
- <pain points you've expressed>
- <verbatim quotes if available>
- <constraints you operate under>

The other personas in this product (you interact with them):
- <persona B>: <one-line role + what they do>
- <persona C>: <one-line role + what they do>

You will be asked questions from a planning conversation. Answer in-character.
- Speak in first person ("I would..." not "they would...")
- Where you don't know, say "I don't know" — do not invent
- Where the question is ambiguous, ask for clarification
- **Name your cross-persona interactions explicitly.** Where you hand off to, depend on, or receive work from another persona, say so ("I submit the refund, then it goes to the Approver"; "I can't audit until Compliance gets the event stream"). These cross-references matter as much as your own steps.
- Where your perspective conflicts with what another stakeholder might say,
  flag the conflict explicitly ("I think X, but I bet the admin team would push back because...")

Do not provide a balanced synthesis. You are one voice. The orchestrator will
collect multiple voices and arbitrate.

Questions:
1. <gap question 1>
2. <gap question 2>
...
```

### Step 3 — Spawn subagents in parallel

One subagent per persona. Run all in the same turn. Each returns its in-character answers.

If a subagent says "I don't know" for a question, that's a real gap that simulation can't fill — must escalate to the user.

### Step 4 — Aggregate: detect conflicts and map interactions

This is the arbitration step. It produces two artifacts from the same set of answers: a **conflict matrix** (where personas disagree) and a **persona interaction map** (where personas connect).

Build the conflict matrix first:

```markdown
## Persona perspective matrix

| Question | Tenant Admin (sim) | End User (sim) | Compliance (sim) | Conflict? |
|---|---|---|---|---|
| RBAC granularity | "Make it role-based not user-based, easier to manage" | "Give me a 'follow' button to share without admin involved" | "Audit needs user-level, not role-level" | YES (admin↔compliance) |
| Real-time audit | "Daily batch is fine" | (not asked) | "Real-time for breach detection, batch for compliance" | YES (admin↔compliance) |
| Project switching | "I don't care, I don't switch" | "Need 2-click switching with state preserved" | (not asked) | NO |
```

Conflicts are findings, not problems. Some get resolved by user input ("compliance wins — go user-level"), some by product strategy ("we need both views — surface role-level for admins, user-level for compliance"), some by deferring ("park the switching debate to slice 2").

#### Persona interactions

Conflicts are where personas *disagree*; interactions are where they *connect* — handoffs, dependencies, and shared touchpoints. The conflict matrix alone misses these, so build a second artifact and record it in `design.md` under `## Persona interactions`:

```markdown
## Persona interactions

| From → To | At which activity | Interaction | Becomes |
|---|---|---|---|
| CS rep → Approver | Issue refund | Hands off refunds above the auto-approve limit | cross-persona `depends_on` (approver story blocks on rep story) |
| System → Compliance | Audit | Emits the event stream Compliance consumes | shared touchpoint + sequencing note |
| Admin → End user | Sign in | Admin provisions SSO before end-user can sign in | cross-persona `depends_on` |
```

Each row turns into one of:

- a **cross-persona `depends_on` edge** in `backlog.csv` (Step 4) — when one persona's story is a precondition for another's. Every such precondition lands as a Hard (`H:`) edge; the mechanics, cycle detection, and feasibility math are owned by [dependency-tracking.md](dependency-tracking.md). This map is where those `H:` edges are *born*.
- a **handoff annotation** on the story, or
- a **shared-touchpoint sequencing note**.

A handoff that crosses a slice boundary is a **slice-1 feasibility risk** — the downstream persona's story can't ship without the upstream one. Flag it here so Step 3/4 can either pull the upstream story into slice 1 or move the downstream story out. Don't model every pair; only the handoffs/dependencies that actually shape slicing or sequencing.

### Step 5 — Present back to user

```markdown
## Findings from persona simulation

I simulated 3 personas to fill discovery gaps before backbone work. Highlights:

**Conflicts requiring your decision:**
- RBAC granularity: Tenant Admin wants role-based for ease; Compliance needs user-level for audit. Suggest: ship both views, default to role-level, audit always logs user-level. Need your call.
- Real-time audit: Admin says batch is fine; Compliance needs real-time for breach detection. Suggest: real-time emit, batch consumption — your call on whether to commit batch-only in slice 1.

**Gaps simulation couldn't fill — need you:**
- On-prem pricing strategy (no persona has this knowledge — escalate to Sales)
- App Store review buffer (this is operational, not persona-based — escalate to your release manager)

**Confirmed (no conflict, low risk):**
- Project switching: ~2-click, state preserved — both personas align here
- Daily-active-user dashboards: admins want, end users don't care, compliance neutral
```

User responses on conflicts get recorded in the design doc decisions log with date and reasoning.

### Step 6 — Gate the planning step

**Do not proceed to Step 1 (Establish backbone) until either:**

- All conflicts are resolved (user has decided or explicitly punted), AND
- All gaps that simulation couldn't fill are documented as open questions OR the user has said "proceed with these gaps"

If forced to proceed with open gaps (e.g., rushed PI planning), every story affected by an open gap gets tagged in `backlog.csv` with `gap_dependency:<question-id>` so the team knows which commitments are conditional.

## Anti-patterns

- **Don't let simulation override user statements.** If the user said "we don't need RBAC in PI 1" and the simulated Compliance persona says "you absolutely need RBAC", the user wins. Surface the Compliance objection as a future-slice risk, don't re-litigate.
- **Don't simulate a persona you have no information about.** "I'll just role-play a CFO" — based on what? Without verbatim or role context, the simulation produces stereotypes, not insight. Either gather context first or skip.
- **Don't fabricate verbatim quotes from simulation.** Simulated outputs are inferences, not data. Tag them `[simulated: <name>]` always. Real verbatims from interviews stay separate.
- **Don't infinite-loop on gap closure.** If after 2 rounds of simulation + user-confirmation you still have open gaps, stop. Document them as conditional, proceed with the caveat, schedule a follow-up after slice 1 lands.

## Cost ceiling

Each persona subagent costs roughly the same as a small synthesis run. For a typical scenario with 3 personas and 5 gap questions, budget ~15-20% of total turns. If gaps exceed 10 questions or personas exceed 5, the discovery is too unbounded — push back to the user to narrow scope before simulating.

## Wiring into the workflow

```
Step 0    — Context collection loop (memory load + interview synthesis fold in as sub-flavors)
Step 0.3  — Simulate (this reference): one subagent per persona → cross-persona interaction map + conflict matrix + gap inventory
           ↓
Step 0.4  — Interview: present findings; user resolves blocking conflicts/gaps (user wins over simulation)
           ↓
           Gate: do not proceed until conflicts resolved + gaps documented
           ↓
Step 1+   — Establish backbone (normal flow)
```

## Single-shot mode caveat

In automated evals or hands-off invocations where the user can't respond mid-task:

- Still spawn the persona simulations
- Still build the conflict matrix and the persona interaction map
- Document conflicts and gaps as "blocking decisions" in `handoff.md`
- Proceed to planning with the strongest defensible interpretation, but tag every conditional commitment with the gap-id
- The handoff message names the smallest next decision the user must make before commitment

User-input-authoritative still holds: if the user's original prompt expressed a preference, that preference wins over any simulated conflict.
