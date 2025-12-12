## ADDED Requirements

### Requirement: Environment Separation and Deployments
The system SHALL support separate deployment environments and automated deployments so the time bank can be changed safely.

#### Scenario: Deploying a new version to staging
- **WHEN** a new version of the time bank application is ready
- **THEN** the CI/CD pipeline SHALL build and deploy it to a staging environment
- **AND** the pipeline SHALL run automated tests and health checks before marking the deployment as successful.

#### Scenario: Promoting a tested version to production
- **WHEN** a version in staging has passed required checks
- **THEN** the system SHALL allow promotion of that version to production via an auditable process
- **AND** the same artifact or image SHALL be reused to avoid configuration drift.

### Requirement: Monitoring and Rollback
The system SHALL provide basic monitoring and the ability to roll back failed deployments.

#### Scenario: Detecting a failed deployment
- **WHEN** a deployment to production results in failing health checks or elevated error rates
- **THEN** the system SHALL surface alerts to operators
- **AND** operators SHALL be able to trigger a rollback to the last known good version.
