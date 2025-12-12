## MODIFIED Requirements

### Requirement: Notification Triggers for Time Bank Events
The system SHALL generate notifications for key time bank events so that members can stay informed and coordinate help.

#### Scenario: New help request created
- **WHEN** a member creates a new help request
- **THEN** the system SHALL be able to notify members who have opted into notifications for new requests (e.g., by category or area).

#### Scenario: New request matches an existing offer
- **WHEN** a new help request is created that matches the skill/category and (optionally) neighborhood/area of an existing offer
- **THEN** the system SHALL notify the member who created the matching offer
- **AND** the notification SHALL include the request description, estimated duration, and a link or instructions to respond.

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

#### Scenario: Member opts out of a notification type
- **WHEN** a member disables notifications for a specific event type (e.g., new matching requests)
- **THEN** the system SHALL stop sending notifications of that type to the member
- **AND** the system SHALL continue to send other enabled notification types.

### Requirement: Delivery and Failure Handling
The system SHALL attempt to deliver notifications reliably and record basic delivery status.

#### Scenario: Notification delivery fails and is retried
- **WHEN** a notification cannot be delivered through a channel due to a transient error
- **THEN** the system SHALL retry delivery at least once within a reasonable time window
- **AND** if delivery ultimately fails, the system SHALL record the failure status.
