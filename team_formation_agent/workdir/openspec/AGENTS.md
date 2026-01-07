# OpenSpec Agents Guide (Project Local)

This repo uses **OpenSpec** as a lightweight change-spec system.

## When to write a spec
Write a spec before implementing changes that are:
- new capability / major feature
- architectural change
- breaking change
- complex performance/security work
- ambiguous requirements

## Where specs live
- Primary spec files live in: `openspec/specs/`
- Each spec should be a standalone Markdown document.

## Spec naming
Use:
- `openspec/specs/YYYY-MM-DD_<short-title>.md`

Example:
- `openspec/specs/2026-01-07_mtg-team-formation-deck-generator.md`

## Spec template
Include these sections:
1. Title
2. Context / Problem
3. Goals
4. Non-goals
5. Users & Use-cases
6. Data sources
7. System design (components)
8. Algorithms (incl. evaluation)
9. Metrics & acceptance criteria
10. Risks & mitigations
11. Implementation plan (phases)
12. Testing plan
13. Reproducibility

## Conventions
- Prefer deterministic pipelines where possible.
- Log every experiment run with configuration + random seeds.
- Keep MTG rules/format constraints explicit.

