# MTG Team Formation Deck Creator + Evolutionary Testing (MTGJSON)

**Date:** 2026-01-07  
**Owner:** Chief Data Scientist (this agent)  
**Status:** Draft  

## 1. Context / Problem
We want to solve a *team formation problem* using Magic: The Gathering (MTG) deck construction as the domain.

- A *team* is a set of **strategies** (archetypes/plans) that must work together to produce decks that are:
  - **Playable** (format-legal, coherent mana/curve, functional game plan)
  - **Competitive** (high win rate vs. a benchmark meta or population)
  - **Fun** (diversity, interaction, novelty, non-degenerate patterns)

We will use **MTGJSON** data as the canonical card database (sets, card attributes, rulings, legalities, prices if needed).

We also need an **evolutionary testing algorithm** that can evaluate and improve decks over iterations, with automated simulations and multi-objective scoring.

## 2. Goals
1. Build a software system that can:
   - ingest MTGJSON datasets
   - represent cards, rules constraints, and decklists
   - generate candidate decks from strategy “teams”
   - evaluate decks via simulation + heuristics
   - evolve decks over time to improve fitness
2. Implement an evolutionary algorithm with:
   - mutation/crossover operators tailored to MTG
   - constraint repair (legality + mana base + curve)
   - multi-objective optimization (competitive + fun + playability)
   - reproducible experiments and logging
3. Produce decks for a chosen format (initially **Standard** or **Pioneer**, configurable).

## 3. Non-goals
- Building a full rules engine equivalent to MTGO/Arena.
- Perfect play or exhaustive game tree search.
- Real-time UI or full web product (CLI + artifacts is sufficient initially).
- Price optimization (optional later).

## 4. Users & Use-cases
- **Researcher / data scientist:** run experiments, compare variants, export best decks.
- **Player:** request decks given constraints (format, colors, archetype preferences).
- **Instructor:** demonstrate team formation concepts (strategy synergy) using MTG as a domain.

Use-cases:
1. Generate N candidate decks for a format and color identity.
2. Evolve decks against a benchmark meta population.
3. Produce a “team of strategies” (e.g., ramp + payoff + interaction package) that yields coherent decks.

## 5. Data Sources (MTGJSON)
From https://mtgjson.com/getting-started/

Primary files (initial):
- `AllPrintings.json` or `AllPrintings.sqlite` (preferred for performance)
- `AllCards.json` (if needed)
- `SetList.json` for set metadata
- Legalities / formats fields per card

We will implement a data layer that supports:
- filtering by format legality
- card types, colors, mana value, keywords, text
- identifying lands vs spells
- simple synergy signals (shared keywords, tribal tags, mechanic tags)

## 6. System Design (Components)
### 6.1 High-level architecture
1. **Data Layer**
   - MTGJSON loader (JSON/SQLite)
   - normalized in-memory index (cards, legalities, text tokens)
2. **Domain Model**
   - `Card`
   - `Deck` (mainboard, sideboard, constraints)
   - `FormatRules`
   - `Strategy` (archetype plan + package definitions)
   - `Team` (set of strategies with compatibility constraints)
3. **Deck Generator**
   - builds decks from a Team + constraints
   - includes mana-base constructor
   - includes repair operators
4. **Evaluator / Simulator**
   - fast “goldfish” simulation (draws, mana development, curve)
   - simplified matchup simulation vs. opponents
   - heuristic scoring for interaction, resilience, consistency
5. **Evolution Engine**
   - population management
   - selection, crossover, mutation
   - multi-objective ranking (Pareto / weighted)
   - experiment logging + reproducibility
6. **Outputs**
   - decklist export (txt/mtgo format)
   - run reports (CSV/JSON), plots later

### 6.2 Proposed repo structure
- `src/mtg/` (domain model)
- `src/data/` (mtgjson ingestion)
- `src/generate/` (strategy + deck construction)
- `src/eval/` (heuristics + simulation)
- `src/evolve/` (EA loop)
- `experiments/` (configs, seeds, outputs)
- `tests/` (unit + property tests)

## 7. Strategies as “Team Formation”
We represent strategies as composable modules. A **Team** is a set of strategies whose combined requirements are mutually satisfiable.

### 7.1 Strategy representation
A `Strategy` is defined by:
- **Core plan:** e.g., “go-wide aggro”, “ramp into big threats”, “graveyard value”, “spells-matter”.
- **Required packages** (soft/hard constraints):
  - threats package
  - interaction package
  - engines/draw
  - mana requirements
- **Synergy tags:** keywords/mechanics/tribal/archetype tags.
- **Incompatibilities:** e.g., “needs many creatures” vs “needs many noncreatures”.
- **Target curve/mana value distribution**.

### 7.2 Team compatibility scoring
Given strategies S1..Sk:
- **Requirement satisfiable score:** do combined constraints allow a 60-card deck?
- **Tag synergy score:** overlap/complement in synergy tags.
- **Resource compatibility:** colors, creature/noncreature ratios, graveyard reliance, etc.

The Team problem: search for a team that maximizes downstream deck fitness while maintaining internal coherence.

## 8. Evaluation & Fitness
We use **multi-objective fitness** with three top-level objectives:

1. **Playability (P)**
   - format legality (hard)
   - mana base health: color source counts vs pip requirements
   - curve smoothness, mulligan rate proxy
   - goldfish stability: can cast spells on curve

2. **Competitive strength (C)**
   - win rate vs. benchmark opponent set (population)
   - interaction density and timing
   - resilience (ability to recover after disruption)

3. **Fun (F)**
   - diversity / novelty vs. known lists (distance in card-space)
   - interaction and decision richness proxies
   - avoid degenerate patterns (e.g., non-games via extreme mana screw/flood)

### 8.1 Simulators
We implement two levels:
- **Goldfish simulator** (fast, 10k runs):
  - sample opening hands, draw sequences
  - estimate turns-to-functional-plan, castability rates
  - compute mana screw/flood probability
- **Lightweight matchup simulator** (slower, 1k runs):
  - abstract opponent as pressure + interaction profile
  - compute expected game outcome using state features (board power, hand resources)

### 8.2 Fitness function
We store raw metrics and compute:
- `P` in [0,1]
- `C` in [0,1]
- `F` in [0,1]

Selection uses either:
- weighted sum: `wP*P + wC*C + wF*F`
- or Pareto ranking (NSGA-II style) + constraints

## 9. Evolutionary Algorithm (EA)
### 9.1 Genome
A deck genome encodes:
- mainboard card multiset
- sideboard (optional in phase 2)
- strategy/team assignment metadata

### 9.2 Initialization
- sample a Team of strategies from a library (seed archetypes)
- generate deck via package assembly:
  - choose core cards, fill support, then mana base
- repair to meet:
  - 60 cards (or format-specific)
  - copies <= 4 (non-basic)
  - legalities

### 9.3 Selection
- tournament selection or Pareto-front selection
- maintain diversity using novelty search or minimum distance constraints

### 9.4 Variation operators
- **Mutation (card-level):** swap 1–4 cards within role constraints
- **Mutation (package-level):** replace a subpackage (e.g., removal suite)
- **Mana mutation:** adjust lands to satisfy color/pip targets
- **Crossover:**
  - role-aligned crossover (merge threats from parent A with interaction from parent B)
  - keep curve/mana constraints via repair

### 9.5 Constraint repair
After variation:
- enforce legality/copies
- recompute pip requirements and rebuild mana base
- adjust curve by adding/removing low/high MV cards

### 9.6 Evaluation budget
Configurable budgets:
- `N_pop` (e.g., 200)
- generations (e.g., 50)
- goldfish sims per deck (e.g., 2k)
- matchup sims per deck (e.g., 200)

### 9.7 Benchmarking opponents
- Start with a **synthetic meta** defined by archetype profiles.
- Later: ingest real lists (optional) if available.

## 10. Metrics & Acceptance Criteria
Minimum acceptance for “playable” deck:
- 100% format legal
- >= 90% keepable opening hands by heuristic
- can cast at least one 2-drop by turn 2 in >= 75% of goldfish runs (if deck has 2-drops)

Minimum acceptance for “competitive” (prototype):
- >= 55% win rate vs. baseline population (synthetic meta) averaged across matchups

Minimum acceptance for “fun” (prototype):
- novelty score above a threshold OR entropy of card choices above baseline
- interaction proxy: includes meaningful disruption (removal/counters) above minimum

## 11. Risks & Mitigations
- **Rules complexity:** mitigate via abstractions + goldfish-first.
- **Evaluation mismatch to real MTG:** keep metrics transparent and configurable; add regression against known decklists later.
- **Search degeneracy (overfitting to simulator):** incorporate diversity pressure + holdout opponent profiles.
- **Data volume/performance:** prefer MTGJSON SQLite + indexing.

## 12. Implementation Plan (Phases)
### Phase 0: Project scaffolding
- repo structure, config system, logging

### Phase 1: Data ingestion
- MTGJSON loader
- format legality filtering
- card feature extraction (colors, types, MV, text tokens)

### Phase 2: Deck representation + constraints
- deck legality validation
- mana base constructor + pip counting

### Phase 3: Strategy/team library + generator
- define initial strategies (e.g., aggro, midrange, control, ramp)
- package assembly into 60-card lists

### Phase 4: Evaluator
- goldfish simulation
- basic matchup abstraction

### Phase 5: Evolution engine
- population loop, operators, multi-objective selection
- experiment runner + artifacts

### Phase 6: Calibration + reporting
- sanity check on known archetypes
- performance profiling
- documentation

## 13. Testing Plan
- Unit tests:
  - legality rules (copies, format legality)
  - mana base pip-source calculations
  - deterministic shuffling with seeds
- Property tests:
  - repair always yields legal deck (or fails with reason)
- Integration tests:
  - end-to-end run produces decks and metrics
- Experiment tests:
  - small-pop quick EA run completes under time budget

## 14. Reproducibility
- All runs require:
  - config file snapshot (YAML/JSON)
  - git commit hash
  - random seed
- Output:
  - best decks per generation
  - full metrics table
  - serialized population genomes

