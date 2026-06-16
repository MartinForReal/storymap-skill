# Slice-1 Acceptance Criteria — F-SCIM additions

> Only the **new** F-SCIM stories have ACs here. PI 1 stories S001-S015 have ACs in the team's existing PI 1 tracker (carried forward; not re-derived per the refinement protocol).

---

## F-SCIM-01 — SCIM 2.0 endpoint scaffold with auth

**Story:** As an enterprise IT admin, I want a SCIM 2.0 endpoint scaffolded with auth, so that my IdP can discover the provisioning API.

**Given/When/Then:**

```gherkin
Feature: SCIM 2.0 endpoint discovery

  Scenario: IdP discovers the SCIM service
    Given the customer tenant has SCIM enabled
    When an IdP sends GET /scim/v2/ServiceProviderConfig with a valid bearer token
    Then the response status is 200
    And the body conforms to the SCIM 2.0 ServiceProviderConfig schema
    And the body declares supported features (patch=true, bulk=false, filter=true)

  Scenario: Unauthenticated request rejected
    Given the customer tenant has SCIM enabled
    When an IdP sends GET /scim/v2/Users without a bearer token
    Then the response status is 401
    And no user data is leaked in the body

  Scenario: Wrong-tenant token rejected
    Given tenant A has SCIM enabled
    When a request is made with tenant B's bearer token to tenant A's /scim/v2/Users
    Then the response status is 403
    And the audit log records the cross-tenant rejection
```

**INVEST check:** Independent ✓ Negotiable ✓ Valuable (admin can confirm endpoint reachable) ✓ Estimable (5 SP) ✓ Small ✓ Testable ✓

---

## F-SCIM-02 — Create + update users via SCIM

**Story:** As an enterprise IT admin, I want to create and update users via SCIM, so that new hires get refund-portal access automatically.

**Given/When/Then:**

```gherkin
Feature: SCIM user provisioning

  Scenario: Create a new user via SCIM POST
    Given the customer tenant has SCIM enabled and authenticated
    When the IdP sends POST /scim/v2/Users with a valid user payload (userName, emails, name)
    Then the response status is 201
    And the response body contains the created user with a server-assigned id
    And the user can sign in via SSO immediately
    And the audit log records the SCIM-driven user create

  Scenario: Update a user via SCIM PATCH
    Given a user previously created via SCIM
    When the IdP sends PATCH /scim/v2/Users/{id} replacing the email
    Then the response status is 200
    And the user's email in the portal reflects the new value
    And the audit log records the SCIM-driven update

  Scenario: Reject duplicate userName
    Given a user with userName "alice@corp" already exists
    When the IdP sends POST /scim/v2/Users with userName "alice@corp"
    Then the response status is 409
    And the existing user is untouched

  Scenario: Reject invalid payload
    When the IdP sends POST /scim/v2/Users with no userName
    Then the response status is 400
    And the error body identifies the missing field
```

**INVEST check:** Independent (depends on F-SCIM-01 — accepted) Negotiable ✓ Valuable ✓ Estimable (8 SP) ✓ Small ✓ Testable ✓

---

## F-SCIM-03 — SCIM DELETE / user disable

**Story:** As an enterprise IT admin, I want SCIM DELETE to disable access immediately, so that offboarded employees lose portal access (also closes a SOC 2 control).

**Given/When/Then:**

```gherkin
Feature: SCIM user deprovisioning

  Scenario: Disable a user via SCIM DELETE
    Given an active SCIM-provisioned user
    When the IdP sends DELETE /scim/v2/Users/{id}
    Then the response status is 204
    And the user can no longer sign in (within 60 seconds of the DELETE)
    And any active session for the user is terminated
    And the audit log records the SCIM-driven deprovision with timestamp + actor

  Scenario: Idempotent delete
    Given a user already disabled via prior SCIM DELETE
    When the IdP sends DELETE /scim/v2/Users/{id} again
    Then the response status is 204 (treated as idempotent, not 404)

  Scenario: SOC 2 evidence
    Given a SCIM DELETE has been processed
    When a compliance reviewer queries the audit log for the affected user
    Then the deprovision event appears with actor=SCIM, source IP, IdP identity, and timestamp
```

**INVEST check:** Independent (depends on F-SCIM-02) Negotiable ✓ Valuable ✓ (deal + SOC 2 double-count) Estimable (5 SP) ✓ Small ✓ Testable ✓

---

## F-SCIM-04 — Group → role mapping (conditional / spike-first)

> **This story is gated on a 1 SP spike in week 7 to confirm sizing.** If spike returns "8 SP confirmed," it's in PI 1. If spike returns "13 SP or more," push to PI 2 and renegotiate deal terms.

**Story:** As an enterprise IT admin, I want my IdP group memberships to map to refund-portal roles, so that I don't manually re-assign permissions per user.

**Given/When/Then (provisional — finalize after spike):**

```gherkin
Feature: IdP group to portal role mapping

  Scenario: Configure group mapping
    Given an enterprise admin with portal admin role
    When the admin maps IdP group "refund-approvers" to portal role "Approver"
    Then the mapping is saved
    And the audit log records the mapping change

  Scenario: Group membership change propagates
    Given a user in IdP group "refund-approvers"
    When the IdP pushes a SCIM PATCH adding/removing the user from the group
    Then the user gains/loses the "Approver" role in the portal within 60 seconds
    And the audit log records the role change

  Scenario: Conflict resolution (multi-group)
    Given a user in two IdP groups that map to two different portal roles
    When the SCIM event is processed
    Then the higher-privileged role is applied (Approver > CS agent)
    And the audit log records the resolution path
```

**INVEST check:** Independent (depends on F-SCIM-02) Negotiable ✓ Valuable ✓ Estimable (8 SP — **low confidence**) Small (marginal) Testable ✓

**Spike scope (week 7, 1 SP):**
- Try a one-IdP integration (Okta) end-to-end with group mapping
- Confirm whether group-membership-change SCIM events are reliably pushed (vs polled)
- Confirm whether multi-group conflict resolution requires bespoke UI work
- Output: revised SP estimate + go/no-go recommendation
