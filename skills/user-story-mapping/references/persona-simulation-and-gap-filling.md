# Persona simulation and gap-filling

After context collection (Step 0), customer-interview synthesis (when notes were provided), and any persistent-memory load, you usually still have **gaps** — questions the user hasn't answered, perspectives that haven't been heard, edge cases nobody articulated. Two ways to fill them:

1. **Ask the user.** Always the first choice. User input is authoritative.
2. **Simulate the persona.** When asking the user would mean 20 questions for an ambiguous topic, spawn a role-play subagent for each persona and let them fill gaps in-character.

Both feed into the same arbitration step. **The user's word always overrides the simulation.** Simulated input is a hypothesis, not a commitment.

## The user-input-authoritative principle

This is the meta-rule that governs every step of the skill — not just this one.

```
priority order:
  1. What the actual user said in this conversation
  2. What real customers said in interview notes (if provided)
  3. What persistent memory recorded from prior sessions (with the user's prior approval)
  4. What context collection mined from artifacts (README, code, tests, tracker)
  5. What persona simulation inferred in-character
  6. What you (the skill) inferred from general knowledge
```

When two sources disagree, the higher-priority one wins. Never silently average them or pick by your own preference. When the user contradicts a lower-priority source, **update the cache** (memory, design doc) to match the user — don't keep the old version around.

When the user is silent on a topic, you may use lower-priority sources to fill — but tag the result explicitly:
- `[user-stated]` when from the prompt
- `[from interview: Aisha]` when from interview notes
- `[from memory: 2026-04-23]` when from cache
- `[from code: src/routes/billing.ts]` when from context
- `[simulated: Marcus persona]` when from a persona-sim subagent
- `[inferred]` when you guessed from general knowledge

Inferred content is a sign of a missing piece. Surface it; don't hide it.

## When to use persona simulation

| Situation | Good fit |
|---|---|
| User has named personas but provided no detail on what each wants | ✅ |
| User has provided rich interview data for 1 persona, none for others | ✅ |
| Conflict suspected between two stakeholder groups (e.g., admin vs end-user) but only one was interviewed | ✅ |
| Edge cases / failure modes / regulatory perspectives missing from happy-path narrative | ✅ |
| User has provided complete data on all personas | ❌ — skip |
| User wants fast turnaround with documented gaps rather than thorough exploration | ❌ — skip |
| Personas are vague or contradictory; simulation would amplify noise | ❌ — ask user first |

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

You will be asked questions from a planning conversation. Answer in-character.
- Speak in first person ("I would..." not "they would...")
- Where you don't know, say "I don't know" — do not invent
- Where the question is ambiguous, ask for clarification
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

### Step 4 — Aggregate and detect conflicts

Build a conflict matrix:

```markdown
## Persona perspective matrix

| Question | Tenant Admin (sim) | End User (sim) | Compliance (sim) | Conflict? |
|---|---|---|---|---|
| RBAC granularity | "Make it role-based not user-based, easier to manage" | "Give me a 'follow' button to share without admin involved" | "Audit needs user-level, not role-level" | YES (admin↔compliance) |
| Real-time audit | "Daily batch is fine" | (not asked) | "Real-time for breach detection, batch for compliance" | YES (admin↔compliance) |
| Project switching | "I don't care, I don't switch" | "Need 2-click switching with state preserved" | (not asked) | NO |
```

Conflicts are findings, not problems. Some get resolved by user input ("compliance wins — go user-level"), some by product strategy ("we need both views — surface role-level for admins, user-level for compliance"), some by deferring ("park the switching debate to slice 2").

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
- **Don't fabricate verbatim quotes from simulation.** Simulated outputs are inferences, not data. Tag them `[simulated]` always. Real verbatims from interviews stay separate.
- **Don't infinite-loop on gap closure.** If after 2 rounds of simulation + user-confirmation you still have open gaps, stop. Document them as conditional, proceed with the caveat, schedule a follow-up after slice 1 lands.

## Cost ceiling

Each persona subagent costs roughly the same as a small synthesis run. For a typical scenario with 3 personas and 5 gap questions, budget ~15-20% of total turns. If gaps exceed 10 questions or personas exceed 5, the discovery is too unbounded — push back to the user to narrow scope before simulating.

## Wiring into the workflow

```
Step 0    — Context collection (artifacts)
Step 0a   — Memory load (if enabled)
Step 0b   — Interview synthesis (if notes provided)
Step 0c   — Persona simulation (this step — when gaps remain)
           ↓
           Arbitration: user input wins over simulation
           ↓
           Gate: do not proceed until conflicts resolved + gaps documented
           ↓
Step 1+   — Establish backbone (normal flow)
```

## Single-shot mode caveat

In automated evals or hands-off invocations where the user can't respond mid-task:
- Still spawn the persona simulations
- Still build the conflict matrix
- Document conflicts and gaps as "blocking decisions" in `handoff.md`
- Proceed to planning with the strongest defensible interpretation, but tag every conditional commitment with the gap-id
- The handoff message names the smallest next decision the user must make before commitment

User-input-authoritative still holds: if the user's original prompt expressed a preference, that preference wins over any simulated conflict.
