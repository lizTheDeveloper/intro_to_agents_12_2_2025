# Change: Add Notifications Capability Spec

## Why
The time banking application already has a change proposal (`add-notifications-for-time-bank`) that introduces a `notifications` capability for email or in-app notifications. However, there is no standalone `notifications` capability spec under `openspec/specs/`. This change formalizes the notifications capability requirements so they can be implemented and validated consistently across the system.

## What Changes
- Define a `notifications` capability spec with clear requirements and scenarios.
- Capture triggers for key time bank events (new request, new offer, accepted offer, completed help session).
- Specify member-level notification preferences (channels and event types).
- Specify basic delivery guarantees and failure handling expectations.

## Impact
- Affected specs: `notifications` (new capability).
- Affected code: notification service, email/in-app delivery mechanisms, event hooks from time bank flows, and any configuration for member notification preferences.
