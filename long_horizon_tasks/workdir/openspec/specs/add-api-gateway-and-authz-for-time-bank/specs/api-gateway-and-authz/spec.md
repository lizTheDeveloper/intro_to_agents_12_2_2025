## ADDED Requirements

### Requirement: API Authentication and Gateway Routing
The system SHALL route time bank API traffic through a gateway that authenticates clients before forwarding requests.

#### Scenario: Authenticated member calls a protected endpoint
- **WHEN** a client calls a protected time bank API endpoint with a valid access token issued by the user-auth capability
- **THEN** the gateway SHALL validate the token
- **AND** the request SHALL be forwarded to the appropriate backend service with the member identity attached.

#### Scenario: Unauthenticated client is blocked
- **WHEN** a client calls a protected time bank API endpoint without valid authentication
- **THEN** the gateway SHALL reject the request with an appropriate error status
- **AND** the backend service SHALL not receive the request.

### Requirement: Basic Rate Limiting
The system SHALL protect public or high-risk endpoints with rate limiting.

#### Scenario: Excessive requests from a single client
- **WHEN** a client exceeds the configured rate limit for a given endpoint
- **THEN** the gateway SHALL throttle or reject additional requests for a defined period
- **AND** the system SHALL record the throttling event for operational visibility.
