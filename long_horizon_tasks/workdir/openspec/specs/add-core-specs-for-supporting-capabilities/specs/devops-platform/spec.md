## ADDED Requirements

### Requirement: Environments and Deployments
The system SHALL support separate environments for development, staging, and production, and provide a way to deploy changes to each.

#### Scenario: Deploy a new version to staging
- **WHEN** a new version of the time bank services is ready for testing
- **THEN** the system SHALL allow deploying it to a staging environment
- **AND** the system SHALL keep production unaffected until a production deployment is triggered.

### Requirement: Monitoring and Health Checks
The system SHALL provide basic monitoring and health checks for the time bank services.

#### Scenario: Service health is monitored
- **WHEN** a time bank service is running in any environment
- **THEN** the system SHALL expose health or readiness endpoints
- **AND** monitoring SHALL track availability or basic performance indicators.

### Requirement: Rollback of Failed Deployments
The system SHALL provide a way to roll back a deployment when a release is determined to be faulty.

#### Scenario: Roll back from a failed production deployment
- **WHEN** a production deployment causes critical errors or instability
- **THEN** the system SHALL allow operators to roll back to a previously known good version
- **AND** the system SHALL restore service health using that version.
