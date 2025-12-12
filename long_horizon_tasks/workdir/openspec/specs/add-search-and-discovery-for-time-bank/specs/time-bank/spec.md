## ADDED Requirements

### Requirement: Searching Offers and Requests
The system SHALL allow members to search and filter published offers and requests so they can quickly find relevant opportunities to give or receive help.

#### Scenario: Member searches for offers by skill and area
- **WHEN** a member searches for offers specifying a skill/category and neighborhood/area
- **THEN** the system SHALL return a list of matching offers
- **AND** the system SHALL support basic sorting (e.g., by newest first).

#### Scenario: Member filters requests by availability window
- **WHEN** a member applies a date/time or availability filter while browsing requests
- **THEN** the system SHALL return only requests that fall within the selected availability window.

### Requirement: Discovery of Relevant Opportunities
The system SHALL provide simple discovery views that highlight relevant offers and requests, even when the member does not perform a targeted search.

#### Scenario: Member views recent and nearby offers
- **WHEN** a member opens the offers discovery view
- **THEN** the system SHALL display a list of recent offers
- **AND** the system SHOULD prioritize offers from the member's neighborhood/area when that information is available.
