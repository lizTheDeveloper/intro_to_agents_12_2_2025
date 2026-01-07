# Plan: MTGJSON Deck Creator + Evolutionary Testing (Team Formation)

## Goal
Create a software system that generates MTG decks that are playable, competitive, and fun by forming compatible *strategy teams* and optimizing decklists using an evolutionary algorithm.

## Step-by-step plan
1. **Bootstrap OpenSpec**
   - Ensure `openspec/AGENTS.md` exists.
   - Write initial spec in `openspec/specs/`.

2. **Define scope defaults (configurable later)**
   - Pick initial format: Standard or Pioneer.
   - Define deck size and copy rules (60 cards, max 4 copies).

3. **Data ingestion layer (MTGJSON)**
   - Prefer SQLite ingestion for performance; support JSON fallback.
   - Build indexes for: legality, colors, type line, mana value, oracle text tokens.

4. **Domain model + constraints**
   - Implement `Card`, `Deck`, `FormatRules`.
   - Implement legality checks and deck validation report.

5. **Strategy/team modeling**
   - Implement `Strategy` objects with packages, tags, and constraints.
   - Implement team compatibility scoring.

6. **Deck construction**
   - Package-based assembly.
   - Mana base builder based on pip requirements.
   - Repair operator to fix illegal/unbalanced decks.

7. **Evaluation**
   - Goldfish simulator for consistency/curve.
   - Lightweight matchup simulator vs synthetic meta profiles.
   - Compute multi-objective fitness (Playability/Competitive/Fun).

8. **Evolutionary optimization**
   - Population init from strategy teams.
   - Selection (Pareto or weighted), crossover, mutation, repair.
   - Diversity pressure / novelty.

9. **Experiment runner + outputs**
   - CLI to run EA with config + seed.
   - Export decklists, metrics, and run artifacts.

10. **Testing**
   - Unit/property/integration tests.
   - Small regression experiment to ensure deterministic outputs.
