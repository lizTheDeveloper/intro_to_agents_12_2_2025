# Change: Add User Authentication for Time Bank

## Why
The time banking application needs a secure way for community members to create accounts, authenticate, and manage access to their profiles and time balances.

## What Changes
- Introduce a `user-auth` capability for member signup, login, logout, and password reset.
- Define requirements for session management and basic account security.
- Integrate member identities with the existing time bank member profiles.

## Impact
- Affected specs: `time-bank`, `user-auth` (new capability)
- Affected code: authentication service, web/mobile client auth flows, member profile linkage.
