## ADDED Requirements

### Requirement: Event-Driven Member Notifications
The system SHALL notify members about key time bank events so they can coordinate help efficiently.

#### Scenario: Member is notified when their request receives an offer
- **WHEN** another member responds to a posted request by offering help
- **THEN** the system SHALL send a notification to the requesting member through at least one configured channel
- **AND** the notification SHALL identify the offer, the helper, and the requested time window.

#### Scenario: Member is notified when their offer is accepted
- **WHEN** a requesting member accepts an offer of help
- **THEN** the system SHALL send a notification to the helper
- **AND** the notification SHALL include details of the agreed session (time, duration, and contact information as allowed by community rules).

#### Scenario: Members receive confirmation after a completed help session
- **WHEN** a help session is marked as completed and the time ledger is updated
- **THEN** the system SHALL send a confirmation notification to both the helper and the recipient
- **AND** the notification SHALL summarize the credited hours and funding source (personal balance or community bank).
