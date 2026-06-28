# Backbone as the E2E verification contract

Use the stabilized backbone as E2E contract: activity = swimlane, backbone = happy-path journey, slice-1 story = Gherkin scenarios. With backbone and slice-1 ACs, Step 4b assembles `e2e-test-contract.md`.

## When to use

At Step 4b, after Step 4a produces `slice-1-acceptance-criteria.md`, produce `e2e-test-contract.md` whenever slice-1 ACs exist — **except** when user says solo / pre-PMF / "just exploring" (see [What to skip for solo / pre-PMF builders](#what-to-skip-for-solo--pre-pmf-builders)). Wait for approval.

## Why the backbone is the right contract surface

- **Right abstraction level.** Unit tests sit below activities (per function); contract tests below activities (per API boundary). Backbone tests verify value.
- **Reproducible.** The six backbone criteria (Step 1) stabilize activities; see [`backbone-criteria.md`](backbone-criteria.md). Tests stay valid while criteria hold.
- **Demoable.** Slice 1 traverses every backbone activity end-to-end — what E2E verifies. Rule: [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run); mechanics: [`slicing-strategies.md`](slicing-strategies.md).
- **Compositional.** On re-run, added activities add swimlanes; removed activities remove them. Map and suite align.

## The contract surface

For each backbone activity:

```
GIVEN <pre-condition reachable from prior activity>
WHEN <user action defined in the activity's stories>
THEN <observable outcome that enables the next activity>
```

This is E2E, not unit or contract testing. "Next activity reachable" makes it a *contract*; otherwise activities are isolated.

## How to produce the contract from existing artifacts

After Step 4a, generate `e2e-test-contract.md` from:

- Backbone activities — `storymap.md` (`## Activity:` / `### Task:` headings).
- Slice-1 ACs — `slice-1-acceptance-criteria.md` (Step 4a; see [`acceptance-criteria.md`](acceptance-criteria.md)).
- Dependencies — `backlog.csv` `depends_on`.

### `e2e-test-contract.md` template

```markdown
# E2E Test Contract — Slice 1

## Backbone coverage matrix

| Activity | Slice-1 stories | E2E scenarios required | Notes |
|---|---|---|---|
| 1. Sign in | S001 | E2E-01 | Auth happy path |
| 2. Find transaction | S002, S003 | E2E-02, E2E-03 | Two find paths (by ID, by email) |
| 3. Submit refund | S005 | E2E-04 | Includes audit log emission |
| 4. Approver decision | S006, S007 | E2E-05 | Tests routing + UI |
| 5. Audit visibility | S008, S009 | E2E-06 | Searchable from rep's POV |

## End-to-end happy-path scenario

This is the demoable journey — every backbone activity flows into the next.

```gherkin
Scenario: E2E-HAPPY — CS rep refunds a transaction end-to-end
  Given a CS rep account exists with SSO and a $100 auto-approve limit
  And a refundable transaction TX-12345 ($45) belongs to customer cust@example.com
  When I sign in via SSO                                    # Activity 1
  And I search for transaction TX-12345                     # Activity 2
  And I open the transaction                                # Activity 2
  And I click "Refund full amount"                          # Activity 3
  And I enter "Customer requested" as the reason            # Activity 3
  And I confirm                                             # Activity 3
  Then within 60s the refund status is "submitted"
  And within 60s the customer at cust@example.com receives a refund email
  And the audit log contains an entry with my user ID, $45 amount, "Customer requested"
  And I can search the audit log for this refund and see it within 5s    # Activity 5
```

One slow nightly E2E touches every backbone activity and gates shipping slice 1.

## Per-activity scenarios

Each activity gets 1–3 focused scenarios from slice-1 stories:

```gherkin
# Activity 3: Submit refund

Scenario: E2E-04a — Refund within auto-approve limit completes immediately
  ...

Scenario: E2E-04b — Refund above limit routes to approval queue
  ...

Scenario: E2E-04c — Refund attempt on already-refunded transaction is blocked
  ...
```

Each scenario maps 1-to-1 with `slice-1-acceptance-criteria.md` Given/When/Then. **Don't duplicate ACs** — reference story IDs.

## Dependency-aware sequencing

Backbone order drives dependencies:

```
E2E-01 (Sign in) ← prerequisite for all others
   ↓
E2E-02, E2E-03 (Find)
   ↓
E2E-04 (Submit refund)  ← depends on E2E-02 (must find first)
   ↓
E2E-05 (Approver)       ← depends on E2E-04 (must have something to approve)
   ↓
E2E-06 (Audit)          ← depends on E2E-04, E2E-05 (must have log entries)
   ↓
E2E-HAPPY               ← orchestrates all of the above
```

Fixture builders follow this order so later tests do not re-run earlier flows.

## What the contract *doesn't* cover

The E2E contract covers only **backbone happy path + slice-1 stories**. It does NOT cover:

- Unit-level logic (unit tests below activities).
- Cross-service contracts (contract tests at service boundaries).
- Visual regression (separate suite if needed).
- Cross-cutting non-backbone work — needs separate test plans (e.g. audit-retention). Backbone scope: [`backbone-criteria.md`](backbone-criteria.md).
- Slice 2+ stories (write E2E contracts when they enter slice 1, not before).

State scope. Overbroad E2E suites become slow, flaky gates.

## Handoff format

In `handoff.md`, point to the E2E contract:

```markdown
## E2E test contract

`e2e-test-contract.md` enumerates the scenarios slice 1 must pass before commit.
- 1 end-to-end happy-path (E2E-HAPPY) — traverses all backbone activities
- N per-activity scenarios derived from slice-1 ACs (one-to-one with story IDs)

Recommended QA shape:
- E2E-HAPPY runs in CI on every PR (nightly), fails the merge if red
- Per-activity scenarios run as part of the developer's local pre-push hook
- All unit + contract tests run on every PR (as usual)
```

## Iteration: keeping the contract in sync

When a non-empty-baseline run plus Step 0.5 / Step 1 detects a new backbone activity (see [`iterative-refinement-and-snapshots.md`](iterative-refinement-and-snapshots.md)), update:

- Add a new row to the coverage matrix.
- Generate ≥1 new per-activity scenario.
- Re-validate E2E-HAPPY so the new activity is reachable end-to-end.
- If the new activity isn't in slice 1: record a future-slice matrix entry; don't write scenarios yet.

If iteration removes an activity (rare, usually backbone re-derivation), archive its scenarios — don't delete silently. Future devs need the reason.

## What to skip for solo / pre-PMF builders

For a solo founder pre-PMF, skip formal `e2e-test-contract.md`; slice-1 ACs suffice. Re-introduce at ≥3 engineers OR when a paying customer depends on reliability.

## Anti-patterns

- **Writing new acceptance criteria here.** If Step 4b authors ACs, Step 4a spilled — fix Step 4a (see [`acceptance-criteria.md`](acceptance-criteria.md)), then assemble.
- **Making E2E cover everything.** Unit, contract, and visual-regression concerns in E2E create a slow, flaky gate. Honor [What the contract *doesn't* cover](#what-the-contract-doesnt-cover).
- **Letting the matrix drift from the backbone.** Listing activities missing from `storymap.md` — or omitting new ones — breaks "every activity is reachable".
- **Silently dropping scenarios on iteration.** Removing without archiving hides why coverage shrank.

## Cost ceiling

The E2E contract is bookkeeping: backbone activities and ACs exist. Budget 5–10% of total turns. If writing ACs here, Step 4a spilled — go back.
