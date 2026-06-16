# Acceptance criteria (Given/When/Then)

Step 4a turns each slice-1 story into testable Gherkin (Given/When/Then) scenarios and runs the INVEST check on it — this is what converts a one-line story into something engineering can build and verify against. Stories in `storymap.md` stay deliberately concise (`As a <persona>, I want to <action>, so that <outcome>` — enough for slicing and prioritization); acceptance criteria are added separately, only for the stories about to be committed, and live in their own file so the map stays clean.

Use Gherkin because it is portable across teams, drops straight into BDD frameworks, and forces precision (a vague AC is a non-testable AC). The scenarios produced here are the per-story unit of the team's test playbook; the end-to-end thread that strings them together is the separate [e2e-verification-and-contract.md](e2e-verification-and-contract.md) deliverable.

## When to use

Generate ACs at Step 4a, after slicing (Step 3) has fixed which stories are in slice 1.

- **Always** — for slice-1 stories. They are the ones being committed in the next PI/sprint.
- **Optional** — for slice 2+. Wait until they get pulled into slice 1, since requirements often shift before then.
- **Skip** — for trivial stories ("rename button label", "fix typo"). Overhead exceeds value.

If the user explicitly asks for ACs across the full backlog, oblige; otherwise default to slice 1 only. Output lands in `slice-1-acceptance-criteria.md` (an optional artifact alongside the always-produced design.md / storymap.md / storymap.csv / backlog.md / backlog.csv set).

## The Given/When/Then template

```
Scenario: <one-line scenario name>
  Given <pre-condition>
  And <additional pre-condition, optional>
  When <user action or event>
  Then <observable outcome>
  And <additional outcome, optional>
```

Most stories need 2-4 scenarios:

- The **happy path** (it works for the typical case)
- 1-2 **edge cases** (boundary, missing input, max input)
- 1 **failure case** (error handling)

## Worked examples

### Story: "As a CS rep, I want to submit a refund, so that the customer is refunded within 24 hours"

```gherkin
Scenario: CS rep submits a refund within their auto-approve limit
  Given I am signed in as a CS rep
  And I am viewing transaction TX-12345 ($45.00)
  And my auto-approve limit is $100
  When I click "Refund full amount"
  And I enter "Customer requested" as the reason
  And I confirm
  Then the refund is created with status "submitted"
  And an audit log entry records me as the submitter, amount, and reason
  And the customer receives an email confirmation within 60 seconds

Scenario: CS rep tries to refund above their auto-approve limit
  Given I am signed in as a CS rep
  And I am viewing transaction TX-99999 ($500.00)
  And my auto-approve limit is $100
  When I click "Refund full amount"
  Then the refund is queued in status "pending_approval"
  And a notification is sent to the on-duty approver
  And no money has moved

Scenario: Refund attempt on an already-refunded transaction
  Given I am signed in as a CS rep
  And transaction TX-12345 has already been fully refunded
  When I view the transaction
  Then the "Refund" button is disabled
  And the existing refund (date, amount, submitter) is shown inline
```

### Story: "As a developer, I want pagination on the list endpoint, so that I don't load 50,000 records at once"

```gherkin
Scenario: First page returns default page size
  Given the customer has 10,000 records
  When I call GET /v1/records
  Then the response contains 50 records
  And the response includes a "next_cursor" token

Scenario: Cursor pagination returns next page
  Given the customer has 10,000 records
  When I call GET /v1/records?cursor=<prev_response.next_cursor>
  Then the response contains the next 50 records
  And the records are different from the first page

Scenario: Invalid cursor returns 400
  When I call GET /v1/records?cursor=garbage
  Then the response status is 400
  And the response body includes error code "invalid_cursor"
```

## Where the ACs go

For slice 1, write a separate file `slice-1-acceptance-criteria.md` alongside the other artifacts, keyed by story ID:

```markdown
# Slice 1 — Acceptance Criteria

## S001 — As a CS rep, I want to sign in with SSO...

Scenario: ...

## S005 — As a CS rep, I want to submit a refund...

Scenario: ...
```

Story IDs are the `S001`… identifiers from `storymap.csv`. Folding ACs into `storymap.md` clutters the map — keep the map for sequencing/slicing and keep ACs in the sibling file for engineering handoff.

## The INVEST check

After generating ACs, run the INVEST checklist on each slice-1 story:

| Property | Question |
|---|---|
| **I**ndependent | Can it ship without depending on a not-yet-built story? (cross-check `depends_on`) |
| **N**egotiable | Are the ACs prescriptive on outcome, not implementation? |
| **V**aluable | Does the story move a real user-observable outcome? |
| **E**stimable | Is it small enough that the team can size it? (T-shirt or points) |
| **S**mall | Can it ship in a single sprint? If not, split. |
| **T**estable | Can each AC be turned into a passing/failing assertion? |

Stories that fail INVEST get an inline comment in `slice-1-acceptance-criteria.md`:

```markdown
## S027 — As an admin, I want to configure tenant-wide policies...

**INVEST issue: NOT SMALL.** This story bundles 4 different policy types
(retention, RBAC, SSO, audit). Recommend split into S027a, S027b, S027c, S027d
before sprint commitment.
```

An INVEST failure on **I**ndependent is a slicing signal: if a slice-1 story can only ship after a story that is not itself in slice 1, the slice does not stand alone — kick it back to [slicing-strategies.md](slicing-strategies.md). A failure on **S**mall means split before sprint commitment.

## When the team doesn't use Gherkin

Some teams prefer prose acceptance criteria or bulleted "Definition of Done" lists. The structure — pre-condition → action → observable outcome — is what matters; the syntax is portable. If the user says "we don't use Gherkin", produce the same content as bulleted ACs:

```markdown
## S005 — Submit refund (happy path)

Pre-conditions:
- Signed in as CS rep
- Viewing a refundable transaction within auto-approve limit

Steps:
- Click "Refund full amount"
- Enter reason
- Confirm

Acceptance:
- Refund created with status "submitted"
- Audit log entry written
- Customer email sent within 60s
```

Same precision, different shell.

## Anti-patterns

- **Acceptance criteria that restate the title.** "Given a refund, when submitted, then it's refunded" is not testable. Force concrete pre-conditions and observable post-conditions.
- **Implementation in the ACs.** "When the user clicks the React button…" — don't say React. Say "user action". The AC governs outcome, not mechanism.
- **Time-based criteria without measurement.** "Then customer receives email quickly" — *quickly* is not testable. Pick a number ("within 60 seconds").
- **Over-coverage on edge cases for slice 1.** Slice 1 is the walking skeleton; cover happy path + 1-2 edge cases. Save the long tail for slice 2+.
- **Generating ACs before the slice is fixed.** Run Step 4a after slicing, or you will write criteria for stories that get re-sliced out.
