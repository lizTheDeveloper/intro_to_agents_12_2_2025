## Requirements

### Requirement: Member Account Creation
The system SHALL allow community members to create user accounts that are linked to their time bank member profiles.

#### Scenario: Member signs up
- **WHEN** a person provides required signup information (such as name, email, and password)
- **THEN** the system SHALL create a user account
- **AND** the system SHALL link the user account to a time bank member profile.

### Requirement: Member Login and Logout
The system SHALL allow members to authenticate and end sessions securely.

#### Scenario: Member logs in
- **WHEN** a member submits valid credentials
- **THEN** the system SHALL authenticate the member
- **AND** the system SHALL create a session that can be used to access their time bank features.

#### Scenario: Member logs out
- **WHEN** a member chooses to log out
- **THEN** the system SHALL invalidate the session so it can no longer be used.

### Requirement: Password Reset
The system SHALL provide a secure way for members to reset their passwords if they can no longer log in.

#### Scenario: Member resets password
- **WHEN** a member initiates a password reset using a verified contact method (such as email)
- **THEN** the system SHALL issue a time-bound reset token
- **AND** the system SHALL allow the member to set a new password using that token.
