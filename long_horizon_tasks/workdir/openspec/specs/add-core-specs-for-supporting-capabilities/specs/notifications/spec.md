## ADDED Requirements

### Requirement: Notification Triggers for Time Bank Events
The system SHALL generate notifications for key time bank events so that members can stay informed and coordinate help.

#### Scenario: New help request created
- **WHEN** a member creates a new help request
- **THEN** the system SHALL be able to notify members who have opted into notifications for new requests (e.g., by category or area).

#### Scenario: Offer accepted
- **WHEN** a member's offer to help is accepted on a request
- **THEN** the system SHALL notify the helper and the requester with details needed to coordinate the session.

#### Scenario: Help session completed
- **WHEN** a help session is marked as completed
- **THEN** the system SHALL notify both parties with a summary of the session and resulting time credit changes.

### Requirement: Notification Channels and Preferences
The system SHALL support at least one notification channel (such as email) and basic member-level preferences for which events generate notifications.

#### Scenario: Member updates notification preferences
- **WHEN** a member changes their notification preferences for event types or channels
- **THEN** the system SHALL store the updated preferences
- **AND** the system SHALL apply those preferences to subsequent notifications.

### Requirement: Delivery and Failure Handling
The system SHALL attempt to deliver notifications reliably and record basic delivery status.

#### Scenario: Notification delivery fails
- **WHEN** a notification cannot be delivered through a channel (for example, due to an email bounce)
- **THEN** the system SHALL record the failure status
- **AND** the system SHOULD avoid continuously retrying in a way that causes excessive load.
