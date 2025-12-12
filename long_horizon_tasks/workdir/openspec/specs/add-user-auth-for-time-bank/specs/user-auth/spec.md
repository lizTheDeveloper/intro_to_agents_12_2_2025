## ADDED Requirements

### Requirement: Member Account Creation and Authentication
The system SHALL provide secure user accounts so community members can sign up, authenticate, and access their time bank profiles.

#### Scenario: Member signs up for a new account
- **WHEN** a person submits required signup information (email or username, password, and basic profile details)
- **THEN** the system SHALL create a new user account
- **AND** the system SHALL associate the account with a time bank member profile
- **AND** the system SHALL prevent creation of duplicate accounts with the same unique identifier (e.g., email).

#### Scenario: Member logs in with valid credentials
- **WHEN** a member submits valid credentials
- **THEN** the system SHALL authenticate the member
- **AND** the system SHALL establish a session or issue an access token that allows access to time bank features for a limited time.

#### Scenario: Member login fails with invalid credentials
- **WHEN** a login attempt is made with invalid credentials
- **THEN** the system SHALL reject the login attempt
- **AND** the system SHALL return a generic error that does not reveal which part of the credentials was incorrect.

#### Scenario: Member resets a forgotten password
- **WHEN** a member initiates a password reset flow and successfully proves control of their account identifier (e.g., via email link)
- **THEN** the system SHALL allow the member to set a new password
- **AND** the system SHALL invalidate any existing sessions associated with the old password.
