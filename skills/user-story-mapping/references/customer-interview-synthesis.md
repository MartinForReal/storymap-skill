# Customer interview synthesis

Raw customer-interview notes, call transcripts, survey verbatims, or sales-call recordings are the richest discovery input you can get — mine them into the five things a story map needs (personas, activities, problems, hypotheses, non-goals) before you derive anything else, because real-user evidence outranks anything you would simulate. This is the companion to [context-collection.md](context-collection.md): that one mines existing **artifacts** (code/tests/docs/tracker); this one mines **unstructured conversation data** from real users.

Verbatim user evidence sits near the top of the source hierarchy and beats simulated personas — see [the source-priority order in SKILL.md](../SKILL.md#rules-that-govern-every-run). So when you have real transcripts, run this synthesis first and let its output be the discovery input to Step 1.

## When to use this

Reach for this reference whenever the user hands you one of:

- Notes from a customer discovery call ("here's what Aisha at Northwind said about their refund flow")
- A transcript export from Gong/Fireflies/Otter/Read.ai
- Survey verbatims (open-text responses from a Typeform/SurveyMonkey)
- Sales-call notes ("the deal blockers we keep hearing")
- A batch of support tickets categorized by theme
- User-research debrief notes

If the input is dense (>3 pages or >20 quotes), work in two passes: first extract atomic statements, then cluster.

## Extraction taxonomy

Pull these five categories from the raw text.

### 1. Roles / personas
Direct evidence: who is the speaker? Their job title, team, day-to-day responsibility, tools they use.

| In transcript | Goes in design.md as |
|---|---|
| "I'm a CS rep, I handle ~40 tickets a day" | Persona: CS Rep, day-to-day: 40 tickets/day |
| "Our admin team has 3 people" | Persona: Admin (size: 3-person team) |
| "I report to a director who reports to the CFO" | Org context for the persona |

### 2. Activities (the "what they do")
Direct evidence: explicit user actions. Listen for verbs + objects.

| In transcript | Goes in storymap.md backbone as |
|---|---|
| "First I open the dashboard, then I find the customer..." | Activity: Find customer |
| "After I issue the refund, I have to log it in a separate spreadsheet" | Activity: Issue refund, Activity: Log to ledger |
| "I never use the bulk-action feature because it's confusing" | Activity: (current backbone) Bulk actions — note: low adoption signal |

These activities become candidate backbone columns. The backbone-voice and six-criteria rules for promoting an activity onto the backbone live in [backbone-criteria.md](backbone-criteria.md).

### 3. Problems (the "what's broken")
Direct evidence: explicit pain, friction, workarounds, complaints.

| In transcript | Goes in design.md as |
|---|---|
| "It takes 20 minutes every time" | Pain: latency — quantified |
| "We export to Excel and do it there" | Pain: workaround — feature gap |
| "I just memorize the customer IDs of our problem accounts" | Pain: missing surfacing |
| "I wish I could just..." | Pain: feature request (treat as hypothesis, not commitment) |

### 4. Hypotheses (the "we should..." statements)
Indirect: opinions, suggestions, "if you built X then Y would happen".

| In transcript | Goes in design.md Hypotheses table |
|---|---|
| "If we had a one-click refund button, my whole day would change" | H: One-click refund cuts refund time by ≥50% |
| "I'd pay for a slack integration" | H: Slack integration drives ≥X% conversion |

Tag each hypothesis with the customer who said it. Single-customer hypotheses are weaker than themes across multiple customers.

### 5. Non-goals / anti-needs
Direct evidence: explicit rejection. People often tell you what they DON'T want.

| In transcript | Goes in design.md Non-goals as |
|---|---|
| "Please don't make us learn another new tool" | Non-goal: net-new UI / separate app |
| "We don't need analytics on this, our BI team handles that" | Non-goal: analytics layer (delegated to BI) |
| "Keep it simple — we're not Stripe" | Non-goal: feature parity with major competitors |

## The clustering pass

After atomic extraction, cluster across customers/transcripts. Look for:

- **Theme strength** — how many customers said this? Single-customer signals stay in the transcript log, not the design doc.
- **Persona variance** — does Persona A say something contradictory to Persona B? That's a design constraint, not a problem to resolve in code.
- **Sequence consistency** — does the order of activities differ across users? If yes, your backbone has parallel paths; consider splitting personas.

Record cluster strength explicitly:

```markdown
## Themes (from N=7 customer interviews, Apr-May 2026)

| Theme | Customers mentioning | Verbatim example |
|---|---|---|
| "Refund takes >15 min" | 6/7 | "It's like a 20-minute process every time" — Aisha, Northwind |
| "Approval threshold unclear" | 4/7 | "I just guess at the limit" — Marcus, Acme |
| "Want bulk action" | 2/7 (both enterprise) | "We do refund batches monthly" — Priya, Globex |
```

The vote count IS the strength signal. Don't drop low-vote items — they may be enterprise-only or persona-specific.

When two personas want opposite things, that's a conflict to surface, not average away — handle it with the conflict matrix in [persona-simulation-and-gap-filling.md](persona-simulation-and-gap-filling.md).

## What NOT to do

- **Don't translate customer language into team jargon.** If they said "refund button" don't write "refund action handler". Keep verbatim phrases in the design doc; translate only when writing acceptance criteria.
- **Don't promote a feature request straight into a story.** "I'd love a slack integration" is a hypothesis to validate, not a commitment to build. Put it in the Hypotheses table with the customer attribution.
- **Don't average-out persona differences.** If admins want X and end users want NOT-X, that's a persona-split signal, not a "design compromise" signal.
- **Don't drop the verbatim quotes.** When you write `design.md`, include 1-2 verbatim quotes per persona in the persona section. They make the doc auditable later when scope creeps.

## Handoff into the rest of the skill

After synthesis, you have:
- A personas section (with verbatim quotes) → goes into `design.md`
- An activities list (in customer voice) → becomes the backbone candidate
- A problems list (quantified where possible) → becomes the opportunities section
- A hypotheses table (with vote counts) → goes into `design.md` Hypotheses
- A non-goals list → goes into `design.md` Non-goals

Then continue with Step 1 (Establish the backbone) of the normal workflow — the synthesis output IS the discovery input.

## Cost ceiling

For a single dense transcript (~5k tokens of customer speech), budget ~10-20% of total turns to synthesis. For a batch of 5-10 transcripts, do them in parallel via subagents if available — each agent extracts atomic statements from one transcript, then the main agent clusters across the batch.
