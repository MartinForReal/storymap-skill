# Backbone as the E2E verification contract

Treat the stabilized backbone as your end-to-end test contract: each activity becomes one E2E swimlane, the whole backbone becomes a single happy-path journey, and each slice-1 story becomes one or more Gherkin scenarios. By the time the backbone and slice-1 acceptance criteria exist, the E2E layer of the test pyramid is already written — Step 4b is mostly bookkeeping that assembles `e2e-test-contract.md` from artifacts you already produced.

## When to use

Step 4b, immediately after Step 4a has produced `slice-1-acceptance-criteria.md`. Produce `e2e-test-contract.md` whenever those slice-1 ACs are produced — **except** when the user explicitly says they're solo / pre-PMF / "just exploring" (see [What to skip for solo / pre-PMF builders](#what-to-skip-for-solo--pre-pmf-builders)). The contract presupposes a stable backbone, so do not start it until the activity set has been approved.

## Why the backbone is the right contract surface

- **Right abstraction level.** Unit tests live below activities (per function), contract tests below activities (per API boundary). The backbone is the one layer where business value is observable, so tests against it verify what users actually do.
- **Reproducible.** The six backbone criteria (Step 1) make the activity set stable across runs; see [`backbone-criteria.md`](backbone-criteria.md). Tests written against backbone activities stay valid as long as those criteria hold.
- **Demoable.** Slice 1 must traverse every backbone activity end-to-end — the same property an E2E suite exists to verify (the user can complete the whole journey). That governing slice-1 rule lives in [`../SKILL.md#rules-that-govern-every-run`](../SKILL.md#rules-that-govern-every-run); its mechanics and violation handling are in [`slicing-strategies.md`](slicing-strategies.md).
- **Compositional.** On a re-run, adding a backbone activity forces a new E2E swimlane and removing one forces a deletion, so the map and the suite stay in sync.

## The contract surface

For each backbone activity, the test contract is:

```
GIVEN <pre-condition reachable from prior activity>
WHEN <user action defined in the activity's stories>
THEN <observable outcome that enables the next activity>
```

That is not a unit test and not a contract test — it is an E2E. The "next activity reachable" property is what makes it a *contract*: without it the activities are isolated checks, not a journey.

## How to produce the contract from existing artifacts

After Step 4a, generate `e2e-test-contract.md` from three inputs you already have:

- The backbone activities — `storymap.md` (`## Activity:` / `### Task:` headings).
- The slice-1 acceptance criteria — `slice-1-acceptance-criteria.md` (Step 4a; see [`acceptance-criteria.md`](acceptance-criteria.md)).
- The dependencies — the `depends_on` column in `backlog.csv`.

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

That is one test that touches every backbone activity. It is the slowest E2E in the suite, runs nightly, and is the gate for shipping slice 1.

## Per-activity scenarios

Each activity also gets 1–3 focused scenarios derived from its slice-1 stories:

```gherkin
# Activity 3: Submit refund

Scenario: E2E-04a — Refund within auto-approve limit completes immediately
  ...

Scenario: E2E-04b — Refund above limit routes to approval queue
  ...

Scenario: E2E-04c — Refund attempt on already-refunded transaction is blocked
  ...
```

Each scenario maps 1-to-1 with a Given/When/Then in `slice-1-acceptance-criteria.md`. **Don't duplicate the ACs** — reference them by story ID.

## Dependency-aware sequencing

The E2E suite has its own dependency order, driven by the backbone:

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

This sequence drives test setup: fixture builders should match the dependency order so that setup for later tests does not redundantly re-run earlier flows.

## What the contract *doesn't* cover

The E2E contract handles the **backbone happy path + slice-1 stories**. It explicitly does NOT cover:

- Unit-level logic (covered by unit tests below the activities).
- Cross-service contracts (covered by contract tests at each service boundary).
- Visual regression (a separate suite if needed).
- Cross-cutting non-backbone work — those need their own test plans (e.g. audit-retention tests for the audit theme). What is and isn't backbone is decided in [`backbone-criteria.md`](backbone-criteria.md).
- Slice 2+ stories (write E2E contracts for those when they enter slice 1, not before).

Be explicit about this scope. Engineering teams often try to make E2E suites cover everything and end up with a slow, flaky suite that times out.

## Handoff format

In `handoff.md`, alongside the design doc and story map, point to the E2E contract:

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

When the loop runs again on a non-empty baseline and a new backbone activity appears (detected in Step 0.5 / Step 1; see [`iterative-refinement-and-snapshots.md`](iterative-refinement-and-snapshots.md)), the E2E contract must update:

- Add a new row to the coverage matrix.
- Generate ≥1 new per-activity scenario.
- Re-validate E2E-HAPPY to ensure the new activity is reachable end-to-end.
- If the new activity isn't in slice 1: record it as a future-slice entry in the matrix; don't write scenarios yet.

When iteration removes an activity (rare, usually a backbone re-derivation), archive the corresponding scenarios — don't delete them silently. Future devs need to know why the test went away.

## What to skip for solo / pre-PMF builders

For a solo founder pre-PMF, the formal E2E contract is overkill. Skip `e2e-test-contract.md` and keep the slice-1 ACs as the de facto contract. Re-introduce the formal contract when the team is ≥3 engineers OR there is a paying customer who depends on the system not breaking.

## Anti-patterns

- **Writing new acceptance criteria here.** If you find yourself authoring ACs at Step 4b, you've spilled Step 4a work downstream — go back and fix Step 4a (see [`acceptance-criteria.md`](acceptance-criteria.md)), then assemble the contract from the result.
- **Making E2E cover everything.** Pushing unit, contract, and visual-regression concerns into the E2E suite yields a slow, flaky gate. Honor the scope in [What the contract *doesn't* cover](#what-the-contract-doesnt-cover).
- **Letting the matrix drift from the backbone.** A coverage matrix that lists activities the `storymap.md` no longer has — or omits ones it gained on a re-run — silently breaks the "every activity is reachable" guarantee.
- **Silently dropping scenarios on iteration.** Removing an activity without archiving its scenarios hides why coverage shrank.

## Cost ceiling

The E2E contract is mostly bookkeeping — backbone activities and ACs already exist. Budget 5–10% of total turns for generating it. If you find yourself writing new ACs at this step, you've spilled Step 4a work into Step 4b — go back and fix Step 4a instead.
