# Project Context

## Purpose
Build a community-run **time bank** that helps people meet needs through mutual aid, solidarity, and care. The application exists to:
- Make it easier to offer and request help within a community.
- Support equitable access to help (including for members who cannot always reciprocate).
- Strengthen community relationships and collective capacity.

## Values / Principles (Anti-Capitalist Alignment)
The system is intentionally designed to avoid reproducing extractive, competitive, or exclusionary dynamics.

### Core principles
- **One person’s time has equal value** (no wage-tiering or market pricing).
- **Inclusion over reciprocity**: inability to "pay back" in hours must not become a barrier to receiving support.
- **Community governance**: rules for community bank eligibility, safety processes, and metrics are decided by community process.
- **Non-extractive data**: metrics exist to help the community care for itself, not to rank individuals or optimize growth.
- **Restorative safety**: prefer restorative and consent-based dispute handling over punitive or carceral patterns.

### Explicit non-goals
- Monetization, advertising, or selling member data.
- Per-member leaderboards, public star ratings, or competitive gamification.
- Surveillance-style analytics that expose individual behavior beyond what is necessary for coordination and accountability.

## Domain Overview
A **member** can publish **offers** of help and **requests** for help. When an offer is accepted, the system creates a **help session** that can be scheduled, completed, cancelled, or disputed.

Time is tracked via an auditable **ledger** of time transactions. The community may also maintain a **community bank** pool of hours to support members according to community-defined eligibility rules.

## Success Metrics (What “success” means here)
Success is measured by community wellbeing and equity, not revenue or growth.

The system SHOULD support community-controlled, privacy-preserving measurement of:
- **Redistribution & equity**: share of hours funded via community bank; balance distribution in bands; hours spent on care/access work (community-defined).
- **Participation & resilience**: active members and retention; diversity of exchanges (aggregate).
- **Safety & care**: dispute rates; time-to-resolution; restorative vs punitive outcomes (aggregate).
- **Governance legitimacy**: participation rates in governance events; representation distribution where explicitly consented and governed.

## Project Conventions

### Spec-first workflow
- `openspec/specs/` are the current truth.
- `openspec/changes/` contain proposals/deltas.

### Spec organization guidance
- Keep requirements within the capability they govern (e.g., anti-extractive metrics live in `time-bank/spec.md`).
- Prefer adding new requirements over modifying existing ones unless behavior is truly changing.

## Important Constraints
- Community consent and governance approval are required for enabling new metrics.
- Protect member privacy: prefer aggregated/banded views; avoid per-member rankings.
- Accessibility: support low-barrier participation (simple UI, low-bandwidth friendliness) as the product evolves.

## External Dependencies
- Email provider or in-app notification system (notifications capability)
- Authentication provider or in-house auth (user-auth capability)
- Hosting/deployment platform (devops-platform capability)
