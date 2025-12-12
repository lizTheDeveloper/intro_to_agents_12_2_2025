# Change: Add API Gateway and Authorization for Time Bank

## Why
The time banking application exposes APIs that must be protected so only authenticated and authorized clients can access member data and time transactions.

## What Changes
- Introduce an `api-gateway-and-authz` capability to front the time bank APIs.
- Define requirements for authenticating API calls and enforcing basic role-based authorization.
- Define protections such as rate limiting for public-facing endpoints.

## Impact
- Affected specs: `api-gateway-and-authz` (new capability), `time-bank`.
- Affected code: API gateway configuration, service authorization checks, client integration.
