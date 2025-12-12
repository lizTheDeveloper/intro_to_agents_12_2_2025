## Requirements

### Requirement: Member Enrollment and Profiles
The system SHALL allow people in the community to create a member profile and join the time bank so they can earn and redeem time credits.

#### Scenario: New member joins the time bank
- **WHEN** a person signs up and provides required basic information (name, contact, neighborhood/area)
- **THEN** the system SHALL create a member profile
- **AND** the system SHALL initialize their personal time balance to zero hours
- **AND** the member SHALL be able to view and edit their profile details.

### Requirement: Offering and Requesting Help
The system SHALL allow members to publish offers of help and requests for help, with enough detail for other members to understand what is needed or offered and how long it will take.

#### Scenario: Member posts an offer to help
- **WHEN** a member creates an offer specifying skill/category, description, estimated duration, and availability
- **THEN** the system SHALL publish the offer so other members can discover it
- **AND** the system SHALL associate the offer with the member’s profile.

#### Scenario: Member posts a request for help
- **WHEN** a member creates a request specifying skill/category, description, estimated duration, and preferred time
- **THEN** the system SHALL publish the request so potential volunteers can see it
- **AND** the system SHALL associate the request with the member’s profile.

### Requirement: Time Earning and Community Bank Credits
The system SHALL allow members to earn hours by helping other members directly or by volunteering into a community time bank pool, and SHALL credit time in whole or fractional hours.

#### Scenario: Member earns hours by helping another member
- **WHEN** a help session between two members is marked as completed with an agreed duration
- **THEN** the system SHALL increase the helper’s personal time balance by the agreed number of hours
- **AND** the system SHALL decrease the recipient’s personal time balance by the same amount, if the help is paid from their balance rather than the community bank.

#### Scenario: Member volunteers into the community time bank
- **WHEN** a member completes a volunteering session that is designated as "community bank" work with an agreed duration
- **THEN** the system SHALL increase the community bank pool balance by the agreed number of hours
- **AND** the system MAY optionally award a small personal bonus to the volunteer (if configured by the community administrators).

### Requirement: Redeeming Community Bank Hours
The system SHALL allow eligible members to use hours from the community bank pool to receive help, subject to community rules.

#### Scenario: Member redeems hours from the community bank
- **WHEN** a member with insufficient personal balance receives help on a request approved for community bank coverage
- **THEN** the system SHALL decrease the community bank pool balance by the agreed number of hours
- **AND** the system SHALL increase the helper’s personal time balance by the same number of hours
- **AND** the system SHALL record that the session was funded by the community bank.

### Requirement: Time Ledger and Balances
The system SHALL maintain an auditable ledger of all time transactions and expose current balances for members and the community bank.

#### Scenario: System records a completed help session
- **WHEN** any help session is marked completed (whether funded by a member’s balance or the community bank)
- **THEN** the system SHALL create a time transaction record including helper, recipient, duration, funding source, and timestamp
- **AND** the system SHALL update the relevant balances (helper, recipient if applicable, and/or community bank)
- **AND** members involved SHALL be able to view the transaction in their history.

### Requirement: Basic Moderation and Trust
The system SHALL provide basic moderation tools so the community can handle abuse, disputes, or unsafe behavior.

#### Scenario: Member reports another member or session
- **WHEN** a member submits a report about another member or a specific help session (e.g., no-show, inappropriate behavior)
- **THEN** the system SHALL record the report and notify designated moderators or administrators
- **AND** moderators SHALL be able to review the report, access relevant transaction details, and mark the report as resolved or take actions such as warning, temporary suspension, or removal of the reported member from the time bank.
