from __future__ import annotations

import random

from mtg_team.data.index import CardIndex
from mtg_team.deck.models import Deck
from mtg_team.deck.rules import FormatRules
from mtg_team.generate.baseline import generate_baseline_deck
from mtg_team.generate.strategy import Team


def generate_deck_from_team(idx: CardIndex, fmt: str, team: Team, *, seed: int = 1, rules: FormatRules | None = None) -> Deck:
    """V1: team influences only the RNG seed and (optionally) color preference.

    This is a placeholder until package-based strategy assembly is implemented.
    """

    # Derive a deterministic seed shift from team strategy names
    team_hash = sum(sum(ord(ch) for ch in s.name) for s in team.strategies)
    random.seed(seed + team_hash)

    # For now, just call baseline generator.
    return generate_baseline_deck(idx, fmt, seed=seed + team_hash, rules=rules)
