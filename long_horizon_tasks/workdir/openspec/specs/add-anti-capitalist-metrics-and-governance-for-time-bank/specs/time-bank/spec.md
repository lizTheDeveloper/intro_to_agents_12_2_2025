## ADDED Requirements

### Requirement: Community Bank Governance and Eligibility Rules
The system SHALL support community-defined rules for when and how the community bank pool may be used, including eligibility criteria and collective decision-making processes.

#### Scenario: Community approves eligibility rules
- **WHEN** designated community governors or a defined quorum of members propose and approve eligibility rules for using community bank hours
- **THEN** the system SHALL record the active version of those rules, including who can request community bank coverage and under what conditions
- **AND** the system SHALL apply these rules when evaluating requests for community bank-funded sessions.

#### Scenario: Community updates eligibility rules
- **WHEN** the community follows the defined governance process to change eligibility rules (for example, after a vote or assembly)
- **THEN** the system SHALL allow the new rules to be recorded as a new version
- **AND** the system SHALL apply the updated rules only to future requests while preserving history of past decisions.

### Requirement: Equity and Accessibility for Members With Limited Capacity to Reciprocate
The system SHALL allow communities to designate members or member categories who may draw on the community bank even if they cannot always reciprocate in hours, and SHALL prevent punitive behavior toward these members.

#### Scenario: Member with access needs receives community-funded help
- **WHEN** a member who is designated by the community as having access needs or limited capacity to reciprocate requests help
- **AND** that request is approved for community bank coverage under the community rules
- **THEN** the system SHALL allow the session to be funded entirely from the community bank pool without requiring the recipient to have or incur a negative personal time balance.

#### Scenario: System prevents punitive blocking based on low or negative balance
- **WHEN** a member with low or negative personal time balance is eligible under the community rules for community bank coverage
- **THEN** the system SHALL NOT block that member from requesting help solely because of their personal balance
- **AND** the system SHALL clearly indicate when the community bank is being used so the member understands that the community is supporting them.

### Requirement: Anti-Hoarding and Balance Fairness Protections
The system SHALL provide configuration options that discourage hoarding of time balances and support a fair distribution of hours within the community.

#### Scenario: Community sets maximum recommended balance band
- **WHEN** the community defines a recommended upper bound for individual time balances (e.g., a maximum healthy balance band)
- **THEN** the system SHALL be able to track when members exceed this band
- **AND** the system SHALL support non-punitive nudges or prompts (such as encouraging members with high balances to volunteer or donate hours back to the community bank) rather than automatic penalties.

### Requirement: Community Health, Safety, and Restorative Dispute Handling
The system SHALL support restorative approaches to handling disputes and safety concerns in addition to, or instead of, purely punitive actions.

#### Scenario: Dispute is resolved through a restorative process
- **WHEN** a member files a dispute or report about a help session or another member
- **AND** moderators or community-appointed stewards choose a restorative outcome (such as mediated conversation, clarification of expectations, or agreement on future boundaries)
- **THEN** the system SHALL allow the dispute to be marked as resolved with a restorative outcome type
- **AND** the system SHALL record notes or outcomes in a way that is visible only to the appropriate stewards and not as a public, punitive rating.

### Requirement: Non-Punitive Feedback and Reputation
The system SHALL provide feedback mechanisms that emphasize safety, care, and mutual learning rather than competitive star ratings or public shaming.

#### Scenario: Member leaves care-focused feedback after a session
- **WHEN** a help session is completed
- **THEN** the system MAY invite both participants to leave structured feedback focused on safety, communication, and mutual expectations (for example, checkboxes and free-text prompts)
- **AND** the system SHALL avoid aggregating this feedback into a single public score for individuals (such as a star rating)
- **AND** the system SHALL ensure that any summaries shared with the community emphasize patterns and safety considerations rather than ranking individuals.

### Requirement: Community-Controlled, Non-Extractive Metrics
The system SHALL support aggregated, community-controlled metrics that help the community understand how the time bank is functioning without exposing surveillance-style, individualized analytics.

#### Scenario: Community views aggregated redistribution and equity metrics
- **WHEN** authorized community members or governors view time bank metrics
- **THEN** the system SHALL provide aggregated views such as:
  - total hours exchanged over a period
  - total hours funded by the community bank vs 1:1 exchanges
  - distribution of balances across members in bands (e.g., low/medium/high) rather than by named individual
  - total hours spent on access, care, or support work as defined by the community
- **AND** the system SHALL NOT expose per-member detailed time histories or rankings in this aggregated view.

#### Scenario: Community reviews and approves what metrics are collected
- **WHEN** the set of metrics to be collected or displayed is changed
- **THEN** the system SHALL require confirmation through the defined community governance process before enabling new metrics
- **AND** the system SHALL document which metrics are currently active and make this documentation visible to members.

### Requirement: Participation and Governance Metrics
The system SHALL track governance and participation metrics that help the community understand whether engagement is broad and inclusive, while respecting privacy and avoiding coercion.

#### Scenario: Community monitors participation in governance processes
- **WHEN** a governance event occurs (such as a vote, assembly, or proposal to change rules)
- **THEN** the system SHALL record anonymized counts of participation (e.g., number of members invited, number who participated, approximate distribution across neighborhoods or affinity groups if tracked)
- **AND** the system SHALL present these metrics back to the community in aggregate form so they can see whether decisions are being made by a small group or broad participation.
