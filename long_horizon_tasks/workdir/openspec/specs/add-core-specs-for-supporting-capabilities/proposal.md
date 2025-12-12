# Change: Add Core Specs for Supporting Capabilities

## Why
Several supporting capabilities for the time bank application (notifications, user authentication, API gateway and authorization, and DevOps platform) are referenced in existing change proposals but do not yet have standalone capability specs under `openspec/specs/`. This makes it difficult to implement and validate these cross-cutting concerns consistently.

## What Changes
- Define a `notifications` capability spec that captures notification triggers, channels, preferences, and delivery behavior.
- Define a `user-auth` capability spec that captures member signup, login, logout, password reset, and session management.
- Define an `api-gateway-and-authz` capability spec that captures API gateway, authentication, authorization, and rate limiting behavior for the time bank APIs.
- Define a `devops-platform` capability spec that captures CI/CD, environment management, monitoring, and rollback behavior.

## Impact
- Affected specs: `notifications` (new), `user-auth` (new), `api-gateway-and-authz` (new), `devops-platform` (new).
- Affected code: authentication service, API gateway configuration, notification service, deployment and monitoring tooling.
