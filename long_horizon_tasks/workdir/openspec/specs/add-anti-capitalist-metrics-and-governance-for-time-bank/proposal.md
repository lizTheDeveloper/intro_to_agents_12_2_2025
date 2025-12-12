# Change: Add Anti-Capitalist Metrics and Governance for Time Bank

## Why
The current time bank specs cover core economic flows (enrollment, offers/requests, earning and redeeming hours, ledger, basic moderation) and several supporting capabilities. However, they do not yet explicitly encode anti-capitalist goals such as equitable redistribution, inclusion of people who cannot "pay back" in hours, community-led governance of the community bank, and non-extractive use of data and metrics.

Without clear requirements and success metrics for these goals, the implementation risks quietly reproducing capitalist dynamics (hoarding, exclusion, surveillance-style metrics) instead of supporting solidarity, care, and mutual aid.

## What Changes
- Refine and extend the `time-bank` spec to:
  - Add requirements for community-bank governance (who can use the pool, how rules are set/changed, collective decision-making).
  - Add requirements for equity and accessibility (inclusion of members who cannot always reciprocate in hours, anti-hoarding protections, safeguards against replicating existing hierarchies).
  - Add requirements for community health and safety that favor restorative processes and non-punitive feedback over star-rating style reputation.
  - Add requirements for data, privacy, and community control over what is measured and how it is used.
- Introduce explicit, anti-capitalist-aligned success metrics for the time bank, grouped around:
  - Redistribution and equity (e.g., use of community-bank hours, distribution of balances, share of hours going to care/access work).
  - Community participation and resilience (e.g., active members, retention, diversity of exchanges).
  - Safety, care, and governance (e.g., time to resolve disputes, restorative outcomes, member participation in governance, perceived fairness and inclusion).

## Impact
- Affected specs:
  - `time-bank` (core capability) – new and/or modified requirements.
  - (Optional) new governance-focused capability if needed, e.g. `community-bank-governance`.
- Affected code (conceptually):
  - Business rules for use of the community bank pool.
  - UI flows for governance, accessibility options, dispute resolution, and surveys.
  - Any analytics/metrics collection related to time bank usage.
