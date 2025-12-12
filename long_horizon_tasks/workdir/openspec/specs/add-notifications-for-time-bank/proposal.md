# Change: Add Notifications for Time Bank

## Why
Members of the time banking application should receive timely notifications about offers, requests, and completed help sessions so they can coordinate and stay engaged.

## What Changes
- Introduce a `notifications` capability for email or in-app notifications.
- Define triggers for key time bank events (new request, accepted offer, completed session).
- Provide basic member-level notification preferences.

## Impact
- Affected specs: `time-bank`, `notifications` (new capability)
- Affected code: notification service, email/in-app delivery, event hooks from time bank flows.
