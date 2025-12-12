# Capability Map

This directory contains the canonical capability specifications for the time bank application.

## Capabilities

- `time-bank/`  Core domain: member profiles, offers/requests, help sessions, ledger/balances, community bank, moderation/safety, governance & metrics.
- `user-auth/`  Member account creation, login/logout, password reset, sessions/tokens.
- `api-gateway-and-authz/`  API gateway routing, authentication/authorization enforcement, rate limiting.
- `notifications/`  Event-triggered notifications, member preferences, delivery/failure handling.
- `devops-platform/`  Environments, deployments, monitoring/health checks, rollback.

## Spec conventions

- `openspec/specs/` is the current truth (what exists / is intended to be built as the system).
- Change proposals live in `openspec/changes/` and include delta requirements (ADDED/MODIFIED/REMOVED).
- Specs should use `## Requirements` (not delta headings).

## Anti-capitalist alignment

See `openspec/project.md` for project purpose, principles, explicit non-goals, and success metrics categories.
