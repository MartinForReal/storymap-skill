# Customer interview synthesis

Mine customer notes/transcripts, survey verbatims, sales calls, support themes, or debriefs into five story-map inputs — personas, activities, problems, hypotheses, non-goals — before derivation. Real-user evidence outranks simulation. Companion to [context-collection.md](context-collection.md): mines **artifacts** (code/tests/docs/tracker); this mines **unstructured conversation data**.

Verbatim user evidence beats simulated personas; see [the source-priority order in SKILL.md](../SKILL.md#rules-that-govern-every-run). With transcripts, synthesize before Step 1.

## When to use this

Use this for:

- Customer discovery notes ("here's what Aisha at Northwind said about their refund flow")
- Gong/Fireflies/Otter/Read.ai transcript exports
- Survey verbatims (Typeform/SurveyMonkey open-text)
- Sales-call blocker notes
- Themed support-ticket batches
- User-research debriefs

For dense input (>3 pages or >20 quotes), extract statements, then cluster.

## Extraction taxonomy

Extract five categories.

### 1. Roles / personas
Direct evidence: speaker identity, title, team, responsibility, tools.

| In transcript | Goes in design.md as |
|---|---|
| "I'm a CS rep, I handle ~40 tickets a day" | Persona: CS Rep; 40 tickets/day |
| "Our admin team has 3 people" | Persona: Admin; 3-person team |
| "I report to a director who reports to the CFO" | Persona org context |

### 2. Activities (the "what they do")
Direct evidence: actions; listen for verbs + objects.

| In transcript | Goes in storymap.md backbone as |
|---|---|
| "First I open the dashboard, then I find the customer..." | Activity: Find customer |
| "After I issue the refund, I have to log it in a separate spreadsheet" | Activities: Issue refund; Log to ledger |
| "I never use the bulk-action feature because it's confusing" | Activity: Bulk actions — low-adoption signal |

Activities are backbone candidates. Promotion rules: [backbone-criteria.md](backbone-criteria.md).

### 3. Problems (the "what's broken")
Direct evidence: pain, friction, workarounds, complaints.

| In transcript | Goes in design.md as |
|---|---|
| "It takes 20 minutes every time" | Pain: latency (quantified) |
| "We export to Excel and do it there" | Pain: workaround / feature gap |
| "I just memorize the customer IDs of our problem accounts" | Pain: missing surfacing |
| "I wish I could just..." | Hypothesis candidate, not commitment |

### 4. Hypotheses (the "we should..." statements)
Indirect evidence: opinions, suggestions, "if you built X then Y would happen".

| In transcript | Goes in design.md Hypotheses table |
|---|---|
| "If we had a one-click refund button, my whole day would change" | H: One-click refund cuts refund time by ≥50% |
| "I'd pay for a slack integration" | H: Slack integration drives ≥X% conversion |

Tag each hypothesis with its customer; single-customer hypotheses are weaker than cross-customer themes.

### 5. Non-goals / anti-needs
Direct evidence: what people DON'T want.

| In transcript | Goes in design.md Non-goals as |
|---|---|
| "Please don't make us learn another new tool" | Non-goal: net-new UI / separate app |
| "We don't need analytics on this, our BI team handles that" | Non-goal: analytics layer (delegated to BI) |
| "Keep it simple — we're not Stripe" | Non-goal: feature parity with major competitors |

## The clustering pass

After extraction, cluster across customers/transcripts:

- **Theme strength** — customer count; single-customer signals stay in the transcript log.
- **Persona variance** — contradictions are design constraints, not code problems.
- **Sequence consistency** — different activity orders imply parallel paths; consider splitting personas.

Record cluster strength:

```markdown
## Themes (from N=7 customer interviews, Apr-May 2026)

| Theme | Customers mentioning | Verbatim example |
|---|---|---|
| "Refund takes >15 min" | 6/7 | "It's like a 20-minute process every time" — Aisha, Northwind |
| "Approval threshold unclear" | 4/7 | "I just guess at the limit" — Marcus, Acme |
| "Want bulk action" | 2/7 (both enterprise) | "We do refund batches monthly" — Priya, Globex |
```

Vote count IS the strength signal. Keep low-vote items; they may be enterprise-only or persona-specific.

When personas conflict, surface it; do not average it away. Use [persona-simulation-and-gap-filling.md](persona-simulation-and-gap-filling.md).

## What NOT to do

- **Don't translate customer language into team jargon.** "Refund button" stays, not "refund action handler"; translate only for acceptance criteria.
- **Don't promote feature requests into stories.** "I'd love a slack integration" is a customer-attributed hypothesis, not a build commitment.
- **Don't average-out persona differences.** Admins want X and end users want NOT-X means persona split, not "design compromise".
- **Don't drop verbatim quotes.** Put 1-2 quotes per persona in `design.md`; they keep the doc auditable when scope creeps.

## Handoff into the rest of the skill

After synthesis, you have:
- Personas + quotes → `design.md`
- Customer-voice activities → backbone
- Quantified problems → opportunities
- Hypotheses + votes → `design.md` Hypotheses
- Non-goals → `design.md` Non-goals

Then continue with Step 1 (Establish the backbone) of the normal workflow — the synthesis output IS the discovery input.

## Cost ceiling

For one dense transcript (~5k tokens of customer speech), budget ~10-20% of turns. For 5-10 transcripts, parallelize via subagents: each extracts one; main agent clusters.
