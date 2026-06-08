# Backbone as E2E verification contract

The backbone activities — once stable — are the highest-leverage source of end-to-end test scenarios you'll find. Every activity must be demonstrably reachable; every slice-1 story has Given/When/Then acceptance criteria that are already shaped like E2E test cases. **Treat the backbone as the E2E contract**, and the test pyramid is roughly written for you.

## Why the backbone is the right contract surface

- **Right abstraction level.** Unit tests live below activities (per function); contract tests below activities (per API). The backbone is the layer where business value is observable. Tests against the backbone verify what users actually do.
- **Reproducible.** Backbone criteria (Step 1) make the activity set stable across runs. Tests written against backbone activities stay valid as long as the criteria don't change.
- **Demoable.** Slice-1 must traverse every backbone activity end-to-end. That's the same property an E2E suite is supposed to verify: the user can complete the whole journey.
- **Compositional.** Adding a new activity in Mode D forces a new E2E swimlane. Removing an activity forces deletion. The map and the suite stay in sync.

## The contract surface

For each backbone activity, the test contract is:

```
GIVEN <pre-condition reachable from prior activity>
WHEN <user action defined in the activity's stories>
THEN <observable outcome that enables the next activity>
```

That's not a unit test, it's not a contract test, it's an E2E. The "next activity reachable" property is what makes it a contract — without it, the activities are isolated, not a journey.

## How to produce the contract from existing artifacts

After Step 4a (acceptance criteria for slice 1), generate `e2e-test-contract.md` from:
- The backbone activities (`storymap.md`)
- The slice-1 ACs (`slice-1-acceptance-criteria.md`)
- The dependencies (`depends_on` column in `backlog.csv`)

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

That's one test that touches every backbone activity. It's the slowest E2E in the suite, runs nightly, and is the gate for shipping slice 1.

## Per-activity scenarios

Each activity also gets 1-3 focused scenarios derived from its slice-1 stories:

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

This sequence drives test setup: fixture builders should match the dependency order so setup-for-later tests doesn't redundantly run earlier flows.

## What the contract *doesn't* cover

The E2E contract handles the **backbone happy path + slice-1 stories**. It explicitly does NOT cover:
- Unit-level logic (covered by unit tests below the activities)
- Cross-service contracts (covered by contract tests at each service boundary)
- Visual regression (separate suite if needed)
- Cross-cutting non-backbone work (those need their own test plans — e.g., audit-retention tests for the audit theme)
- Slice 2+ stories (write E2E contracts for those when they enter slice 1, not before)

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

## Mode D and the contract

When iterative refinement adds a new backbone activity (Step D.3 detects it), the E2E contract must update:
- Add a new row to the coverage matrix
- Generate ≥1 new per-activity scenario
- Re-validate E2E-HAPPY to ensure the new activity is reachable end-to-end
- If the new activity isn't in slice 1: contract acquires a future-slice entry; don't write scenarios yet

When refinement removes an activity (rare, usually a backbone re-derivation), archive the corresponding scenarios — don't delete them silently. Future devs need to know why the test went away.

## What to skip for solo / pre-PMF builders

For a solo founder pre-PMF: the E2E contract is overkill. Skip `e2e-test-contract.md` and just keep the slice-1 ACs as the de facto contract. Re-introduce the formal contract when the team is ≥3 engineers OR there's a paying customer who depends on the system not breaking.

Default: produce `e2e-test-contract.md` whenever `slice-1-acceptance-criteria.md` is produced, except when the user explicitly says they're solo / pre-PMF / "just exploring".

## Cost ceiling

The E2E contract is mostly bookkeeping — backbone activities and ACs already exist. Budget 5-10% of total turns for generating it. If you find yourself writing new ACs at this step, you've spilled Step 4a work into Step 4b — go back and fix Step 4a instead.
