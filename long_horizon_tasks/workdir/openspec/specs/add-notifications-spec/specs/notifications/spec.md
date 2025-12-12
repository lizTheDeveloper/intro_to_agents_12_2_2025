## ADDED Requirements

### Requirement: Event-Triggered Notifications
The notifications capability SHALL send notifications to members when key time bank events occur so they can coordinate and stay engaged.

#### Scenario: Notify member of new request matching their offer
- **WHEN** a new help request is created that matches the skill/category and (optionally) neighborhood/area of an existing offer
- **THEN** the system SHALL generate a notification to the member who created the matching offer
- **AND** the notification SHALL include the request description, estimated duration, and a link or instructions to respond.

#### Scenario: Notify member when their request receives an offer
- **WHEN** another member offers to fulfill a published request
- **THEN** the system SHALL generate a notification to the member who created the request
- **AND** the notification SHALL include basic details about the helper and the proposed time.

#### Scenario: Notify members when a help session is completed
- **WHEN** a help session is marked as completed
- **THEN** the system SHALL send a notification to both the helper and the recipient summarizing the session (duration, funding source, and time balance impact if applicable).

### Requirement: Member Notification Preferences
The system SHALL allow each member to configure basic notification preferences so they can control which events they are notified about and through which channels.

#### Scenario: Member configures notification channels
- **WHEN** a member updates their notification settings to choose preferred channels (e.g., email and/or in-app) for supported event types
- **THEN** the system SHALL store these preferences with the member profile
- **AND** subsequent notifications SHALL respect the member's selected channels.

#### Scenario: Member opts out of a notification type
- **WHEN** a member disables notifications for a specific event type (e.g., new matching requests)
- **THEN** the system SHALL stop sending notifications of that type to the member
- **AND** the system SHALL continue to send other enabled notification types.

### Requirement: Notification Delivery and Failure Handling
The notifications capability SHALL make a best-effort attempt to deliver each notification and provide basic observability into failures.

#### Scenario: Successful notification delivery
- **WHEN** the system sends a notification via a supported channel
- **THEN** the system SHALL record that the notification was attempted
- **AND** on success, the system SHALL record that the notification was delivered.

#### Scenario: Notification delivery failure
- **WHEN** a notification attempt fails due to a transient error (e.g., temporary email provider issue)
- **THEN** the system SHALL retry delivery at least once within a reasonable time window
- **AND** if delivery ultimately fails, the system SHALL record the failure for monitoring and potential follow-up.
