## ADDED Requirements

### Requirement: API Gateway for Time Bank Services
The system SHALL expose time bank APIs through an API gateway that fronts backend services.

#### Scenario: Client calls time bank API through gateway
- **WHEN** a client sends a request to a time bank API endpoint
- **THEN** the request SHALL pass through the API gateway
- **AND** the gateway SHALL route the request to the appropriate backend service.

### Requirement: Authentication and Authorization for APIs
The system SHALL authenticate API calls and enforce basic role-based authorization for time bank operations.

#### Scenario: Authenticated request with sufficient permissions
- **WHEN** a client sends a request with a valid authentication token and required roles or scopes
- **THEN** the gateway or backend SHALL allow the request to proceed.

#### Scenario: Unauthenticated or unauthorized request
- **WHEN** a client sends a request without valid authentication or without required permissions
- **THEN** the system SHALL reject the request with an appropriate error status.

### Requirement: Rate Limiting for Public Endpoints
The system SHALL protect public-facing endpoints with basic rate limiting.

#### Scenario: Client exceeds allowed rate
- **WHEN** a client makes requests to a public endpoint more frequently than the configured limit
- **THEN** the system SHALL respond with an error that indicates the rate limit has been exceeded
- **AND** subsequent requests during the limiting window MAY be denied.
