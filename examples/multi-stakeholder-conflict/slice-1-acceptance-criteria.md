# Slice 1 (PI 1) — Acceptance Criteria

Gherkin-style Given/When/Then for every PI-1 story. INVEST checked at the end of each story.

---

## S001 — As an Application Developer, I want to sign in to the IDP with my corporate SSO

```gherkin
Scenario: Developer signs in via SSO for the first time
  Given my corporate SSO account is provisioned
  And I have never signed in to the IDP before
  When I navigate to the IDP URL
  And I click "Sign in with SSO"
  And I complete the SSO challenge
  Then I land on the IDP home page
  And my profile is auto-populated with my email, display name, and team membership claims

Scenario: Developer signs in with no SSO claims for any team
  Given my SSO account has no team-group claims
  When I sign in
  Then I land on the home page
  And the home page tells me I am not yet attached to a team workspace
  And the page links me to the team-onboarding flow (S004)

Scenario: SSO failure
  Given the SSO provider is unreachable
  When I click "Sign in with SSO"
  Then I see an error page with a correlation id and a "retry" link
  And no half-created session is left in the IDP
```

INVEST: Independent, Negotiable, Valuable, Estimable, Small, Testable — PASS.

---

## S002 — As an Application Developer, I want a "what can I do here" home page after sign-in

```gherkin
Scenario: First-time signed-in user sees actionable next steps
  Given I have just signed in
  When the home page loads
  Then I see at most 4 primary call-to-action cards: "Create a sandbox", "Browse blueprints", "Store a secret", "Deploy to staging"
  And each card has a one-line description and a "start" button

Scenario: Returning user sees their recent envs first
  Given I have at least one env in my workspace
  When the home page loads
  Then my most-recent 3 envs appear at the top with current cost and status
  And the primary call-to-action cards appear below them
```

INVEST: PASS. Note: depends on S001 (auth) being shipped first within PI 1.

---

## S004 — As an Application Developer, I want my team membership auto-resolved from SSO group claims

```gherkin
Scenario: SSO claims include a known team
  Given my SSO claims include group "eng-platform-team"
  And the IDP has a workspace mapped to that group
  When I sign in
  Then I am added to that workspace as a member
  And the home page reflects my workspace membership

Scenario: SSO claims include an unknown team
  Given my SSO claims include a group not mapped to any workspace
  When I sign in
  Then I land on the team-onboarding page
  And the page surfaces my SSO group names and an option to request a new workspace

Scenario: SSO claims update on next sign-in
  Given I have been added to a new SSO group since my last sign-in
  When I sign in again
  Then my workspace membership reflects the new group within 60 seconds
```

INVEST: PASS.

---

## S006 — As an Application Developer, I want to pick a sandbox blueprint from a catalog

```gherkin
Scenario: Developer browses the catalog
  Given I am on the "Create sandbox" page
  When the page loads
  Then I see a list of at least 3 PI-1 blueprints: "Node + Postgres", "Python + Redis", "Go + S3"
  And each blueprint shows its included services, estimated monthly cost at default size, and pre-applied policies

Scenario: Developer searches for a specific stack
  Given the catalog has at least 3 blueprints
  When I type "postgres" in the search field
  Then only blueprints that include Postgres are shown

Scenario: No blueprint matches the search
  Given the catalog has 3 blueprints
  When I type "cobol"
  Then I see an empty state with a link to "request a new blueprint" (which routes to S018 in PI 2)
```

INVEST: PASS.

---

## S007 — As an Application Developer, I want sub-5-minute sandbox creation with no approval gate

```gherkin
Scenario: Default sandbox creation succeeds end-to-end
  Given I have picked the "Node + Postgres" blueprint
  And I have filled in (or accepted pre-filled) tags for team, cost-center, env-type
  When I click "Create sandbox"
  Then the env is created in under 5 minutes
  And no approval ticket is filed, no human is paged
  And I receive a UI notification with the env URL and a "view details" link
  And the env appears in my home-page list

Scenario: Sandbox creation fails partway through
  Given I have clicked "Create sandbox"
  When provisioning fails partway (e.g., AWS API timeout)
  Then the env is automatically rolled back (no orphan resources)
  And I see a clear error with a correlation id and a "retry" button
  And the failure is logged to the audit store (S031)

Scenario: Developer attempts to create an env with a missing required tag
  Given I have picked a blueprint
  And one of the mandatory tag fields (team / cost-center / env-type) is blank
  When I click "Create sandbox"
  Then the form is blocked with an inline error on the missing field
  And no AWS resources are created
```

INVEST: PASS but flagged LARGE — this is the headline integration story and at the upper bound of "single sprint" sizing. Recommend a spike in week 1 of PI 1 to validate the 5-minute target with the chosen IaC engine before committing.

---

## S008 — As a Platform Team Engineer, I want every sandbox blueprint to pre-apply default security policies

```gherkin
Scenario: Default blueprint provisions with safe defaults
  Given a developer is creating any PI-1 blueprint with defaults
  When the env is provisioned
  Then the resulting VPC is private (no internet gateway by default)
  And all EBS volumes are encrypted at rest
  And the IAM role attached to the workload has only the permissions declared in the blueprint manifest

Scenario: Blueprint manifest is missing required policy fields
  Given a blueprint manifest does not declare a network mode, encryption setting, or IAM scope
  When the IDP tries to register the blueprint
  Then registration is rejected with a clear error referencing the missing fields
  And the blueprint is not available for selection in the catalog
```

INVEST: PASS.

---

## S011 — As an Application Developer, I want the env-creation form to pre-fill team and cost-center

```gherkin
Scenario: Form pre-fills from my profile
  Given my profile has team="eng-platform" and cost-center="CC-1234"
  When I open the "Create sandbox" form
  Then the team field is pre-filled with "eng-platform"
  And the cost-center field is pre-filled with "CC-1234"
  And the env-type field is pre-filled with the most-recently-used value from my history (or "sandbox" if none)

Scenario: Developer overrides a pre-filled tag
  Given the form has pre-filled my team
  When I change the team to a different team I am a member of
  Then the new value is accepted
  And the override is recorded in the audit store

Scenario: Developer is a member of multiple teams
  Given I am a member of 3 teams in SSO
  When I open the form
  Then the team field shows a dropdown of my 3 teams pre-selected to my most-recently-used team
```

INVEST: PASS.

---

## S012 — As a Platform Team Engineer, I want team, cost-center, env-type tags mandatory at creation

```gherkin
Scenario: Env creation with all mandatory tags succeeds
  Given a developer has filled team, cost-center, env-type
  When they submit the "Create sandbox" form
  Then the env is created and all three tags are applied to every AWS resource provisioned

Scenario: Env creation with a missing mandatory tag is blocked
  Given any of {team, cost-center, env-type} is empty
  When the developer submits
  Then the form is rejected with an inline error
  And no AWS resources are created
  And no partial state is left in the IDP

Scenario: Tags appear in the cost dashboard within 24 hours
  Given an env was created today with team="X", cost-center="Y"
  When the platform team views the spend dashboard (S027) tomorrow
  Then the env's spend is attributed to team="X" and cost-center="Y"
```

INVEST: PASS.

---

## S013 — As an Application Developer, I want to override a default policy with a one-line justification

```gherkin
Scenario: Developer opens a port to the internet with justification
  Given I am creating a sandbox
  And the default blueprint blocks ingress from 0.0.0.0/0
  When I toggle "expose port 8080 to the internet"
  Then I am prompted for a one-line justification (min 10 characters, max 500)
  And if I provide a justification, the policy is overridden for this env
  And the override (who, when, what, justification) is recorded in the audit store (S031)

Scenario: Developer skips the justification
  Given I have toggled an override
  When I leave the justification field empty
  Then the form will not submit
  And the toggle reverts to its default value

Scenario: Override does not apply to "high-risk" policies (forward-looks to S014 in PI 2)
  Given a future "high-risk" policy is in place (PI 2)
  When I attempt to override it via this UI in PI 1
  Then in PI 1 the override is allowed (since S014 is PI 2)
  And the audit entry flags it for future PI-2 review
```

INVEST: PASS. The last scenario documents the explicit "permit by default with auditing" stance per the user's decision log entry.

---

## S015 — As an Application Developer, I want to store and retrieve non-prod secrets in a self-service vault

```gherkin
Scenario: Developer stores a non-prod secret
  Given I am viewing my env
  When I open the "Secrets" tab
  And I add a key "DATABASE_URL" with a value
  Then the secret is stored encrypted in the vault, scoped to this env

Scenario: Developer rotates a secret
  Given the secret "DATABASE_URL" exists in my env
  When I edit its value
  Then the new value replaces the old one
  And the rotation is recorded in the audit store (who, when, what key — not the value)

Scenario: Developer tries to access another env's secrets
  Given env A and env B are owned by different teams
  When I, a member of team-A only, try to retrieve env-B's secrets via API
  Then the request is denied with HTTP 403
  And the access attempt is logged
```

INVEST: PASS.

---

## S016 — As an Application Developer, I want secrets injected into my env as env vars or files

```gherkin
Scenario: Secret injected as environment variable
  Given my env has secret "DATABASE_URL" stored
  And my blueprint manifest declares secret injection for "DATABASE_URL" as env var
  When my workload starts
  Then the process has DATABASE_URL set in its environment

Scenario: Secret injected as mounted file
  Given my env has secret "TLS_CERT" stored
  And my manifest declares it as a mounted file at /etc/tls/cert.pem
  When my workload starts
  Then /etc/tls/cert.pem exists with the secret's contents and mode 0400

Scenario: Secret missing at startup
  Given my manifest references a secret name that does not exist
  When the env attempts to start
  Then startup fails with a clear error naming the missing secret
  And no partial pod / workload is left running
```

INVEST: PASS.

---

## S017 — As an Application Developer, I want a list of internally-available managed services I can attach in one click

```gherkin
Scenario: Developer attaches a managed Postgres
  Given my env exists
  When I open the "Services" tab
  And I click "Attach Postgres (dev tier)"
  Then a Postgres instance is provisioned within 3 minutes
  And the connection string is stored in my env's secret vault automatically
  And the env's blueprint manifest is updated to reflect the attachment

Scenario: Developer attaches a service their team is not entitled to
  Given my team does not have access to "managed-kafka"
  When I view the services tab
  Then "managed-kafka" appears in the list as "request access" rather than "attach"
  And clicking it routes to the request flow (S018 PI 2 placeholder; in PI 1, opens an external ticket link as a fallback)
```

INVEST: PASS. Second scenario gracefully handles the fact that S018 is PI 2.

---

## S019 — As an Application Developer, I want to install arbitrary tools / images / libraries in non-prod sandboxes without a security review queue

```gherkin
Scenario: Developer installs an arbitrary container image
  Given I am running a workload in my non-prod sandbox
  When I configure the env to pull image "myorg/experimental-tool:latest"
  Then the image is pulled and run without an approval queue
  And the image, its layers, and an SBOM are submitted to the background scan job (S020)

Scenario: Developer installs in prod
  Given I am attempting to install an arbitrary image in a "prod" env-type
  When I submit the change
  Then the change is rejected with a clear message: "Prod requires allowlisted images. Request via prod-image-allowlist flow."
  And no rollout occurs
```

INVEST: PASS. Second scenario enforces the prod carve-out (Q6 agreement) without making non-prod harder.

---

## S020 — As a Platform Team Engineer, I want background SBOM/scan on BYO non-prod workloads with findings on a dashboard

```gherkin
Scenario: Scan job runs on every new BYO workload
  Given a developer launches a BYO image in non-prod
  When the image starts
  Then a scan job is queued within 60 seconds
  And the scan completes within 30 minutes
  And findings (CVE id, severity, package, version) are written to the SBOM dashboard

Scenario: Platform team views findings for a specific team
  Given findings exist for team "X"
  When the platform engineer filters the dashboard by team="X"
  Then they see all findings for X's BYO workloads grouped by severity

Scenario: No findings does not mean no scan ran
  Given a workload was scanned and had zero CVEs above the threshold
  When viewing the dashboard
  Then the workload appears as "scanned, clean" with a timestamp
  (not as "not scanned" — that's a distinct state)
```

INVEST: PASS. Note: findings escalation policy (who is notified when) is deferred to S040 in PI 2 per the prioritization. PI 1 surfaces; PI 2 escalates.

---

## S021 — As an Application Developer, I want to deploy my containerized app to staging from the IDP UI or CLI

```gherkin
Scenario: Deploy succeeds from the UI
  Given my env has a container image registered
  When I click "Deploy to staging" and choose a tag
  Then the deploy is queued
  And within 10 minutes the staging env is running the new image
  And the UI shows me the deploy status, logs, and a healthcheck result

Scenario: Deploy from the CLI
  Given I have the IDP CLI installed and authenticated
  When I run `idp deploy staging --image myorg/app:abc123`
  Then the same flow is triggered as the UI deploy
  And the CLI streams the same status / logs

Scenario: Deploy of an unhealthy build
  Given a deploy completes but the healthcheck fails
  When the post-deploy healthcheck reports unhealthy after 3 retries
  Then the deploy is marked "failed (unhealthy)"
  And the UI offers a one-click rollback to the previous image
```

INVEST: PASS.

---

## S022 — As an Application Developer, I want my deploy to show me logs and a healthcheck result in the UI

```gherkin
Scenario: Logs stream during deploy
  Given I have triggered a deploy
  When the deploy is in progress
  Then I see streaming logs from the deploy controller
  And the last 1000 lines remain visible after the deploy finishes

Scenario: Healthcheck result is shown post-deploy
  Given the deploy finishes
  When I view the deploy detail page
  Then I see a green / yellow / red badge from the healthcheck
  And clicking the badge shows the raw probe responses for the last 3 checks
```

INVEST: PASS. Trivial enough that we kept the AC count tight.

---

## S026 — As an Application Developer, I want to see my env's running cost in near-real time in the IDP UI

```gherkin
Scenario: Cost is visible within 1 hour of provisioning
  Given I created an env 65 minutes ago
  When I view the env's "Cost" tab
  Then I see a running monthly-projected cost number based on actual hourly usage
  And the number is no older than 60 minutes

Scenario: Cost is broken down by resource
  Given my env has a Postgres, an EC2 instance, and S3 storage
  When I view the cost breakdown
  Then I see line items per resource with running monthly cost

Scenario: Cost is unknown during the first hour
  Given my env was created 10 minutes ago
  When I view the cost tab
  Then I see "cost data populating — first reading in <50 min>" with no fabricated number
```

INVEST: PASS.

---

## S027 — As a Platform Team Engineer, I want a project-wide spend dashboard with per-team / per-env breakdown

```gherkin
Scenario: Platform team views org spend
  Given >=1 env exists in the IDP
  When the platform engineer opens the spend dashboard
  Then they see total org spend MTD and last-30-days
  And spend is broken down by team, cost-center, env-type, and per-env

Scenario: Dashboard surfaces outliers
  Given an env's MTD spend is in the top-5 across the org
  When viewing the dashboard
  Then that env is flagged in an "outliers" panel with its team owner

Scenario: Spend attribution requires PI-1 tags (S012)
  Given an env created in PI 1 has all mandatory tags applied
  Then 100% of its spend is attributable on the dashboard (no "untagged" bucket)
```

INVEST: PASS. Third scenario reinforces the integration with S012.

---

## S028 — As an Application Developer, I want a budget alert when my env's projected monthly cost crosses a threshold

```gherkin
Scenario: Developer is alerted at the default threshold
  Given my env has a default threshold of $500/month projected spend
  When the projected monthly cost crosses $500
  Then I receive an in-IDP notification AND an email within 30 minutes of the crossing
  And the alert names the env, the projected cost, and the trend (rising / steady)

Scenario: Developer customizes the threshold
  Given my env's threshold is $500
  When I change it to $1000
  Then the new threshold is persisted
  And no alert fires unless projected cost crosses $1000

Scenario: Alert deduplication
  Given an alert fired 6 hours ago for env X
  When the projected cost stays above the threshold but does not cross a new band
  Then no new alert is sent (only daily summary updates)
```

INVEST: PASS.

---

## S029 — As an Application Developer, I want to tear down my env in one click

```gherkin
Scenario: Teardown destroys all resources
  Given my env has a Postgres, an EC2 instance, S3 buckets, and secrets
  When I click "Tear down" and confirm
  Then within 10 minutes, every resource is destroyed
  And the IDP shows me a destruction report listing every resource and its destroyed-at timestamp
  And subsequent cost reporting shows zero spend for this env going forward

Scenario: Confirmation prevents accidental teardown
  Given I click "Tear down"
  When the confirmation dialog opens
  Then I must type the env name to confirm (not just click "OK")

Scenario: Teardown of a non-empty env
  Given my env has stored secrets and uploaded files
  When I tear down
  Then the secrets and files are also destroyed
  And the teardown report calls this out (so I can't claim I didn't know)
```

INVEST: PASS.

---

## S031 — As a Platform Team Engineer, I want every env creation, override, secret access, and deploy event logged to a queryable audit store

```gherkin
Scenario: Env creation is logged
  Given a developer creates an env
  When the creation completes
  Then an audit entry exists with: timestamp, dev id, env id, blueprint id, applied tags, applied policies, any overrides + justifications

Scenario: Policy override is logged
  Given a developer overrides a default policy with a justification
  When they submit the form
  Then an audit entry exists with the policy name, the override value, the justification text, and the dev id

Scenario: Secret access is logged (metadata only, not values)
  Given a workload retrieves a secret from the vault
  When the retrieval succeeds
  Then an audit entry exists with: timestamp, env id, secret key name, retrieving identity (workload service account)
  And the secret VALUE is NOT logged

Scenario: Audit store is queryable
  Given the platform engineer wants to investigate an incident
  When they query by env id OR by dev id OR by time range
  Then they receive results within 5 seconds for queries spanning the last 30 days
```

INVEST: PASS. Note: this story's PI-1 placement is what makes the user-stated "auditing" half of "permit by default with auditing" real.

---

## INVEST issues to flag for the PI Planning event

- **S007 (sub-5-min sandbox)** — Sized 10 (largest in the backlog). Recommend a week-1 spike to validate the 5-minute target with the chosen IaC engine. If the spike shows 5 min is unrealistic, propose splitting into S007a (env creation, no managed-service attach) and S007b (managed-service attach as a follow-on click).
- **S021 (no-ticket staging deploy)** — Sized 8. Couples to S007 + S015. If S007 splits, S021 likely also needs a split between "deploy a container" and "deploy with secret injection from S015/S016". Watch in PI Planning.

All other PI-1 stories pass INVEST cleanly.
