from __future__ import annotations

import random
from collections import Counter

from mtg_team.data.index import CardIndex
from mtg_team.deck.models import Deck, DeckCard
from mtg_team.deck.rules import FormatRules


def _choose_basics(idx: CardIndex, fmt: str, colors: set[str]) -> list[tuple[str, str]]:
    """Return list of (uuid, name) for basic lands matching colors.

    On the tiny fixture, we only have Forest/Island.
    """

    basics = [c for c in idx.lands(fmt) if c.is_basic_land]
    if not basics:
        raise ValueError("No basic lands available in dataset")

    if not colors:
        # Colorless: just pick any basic.
        c = basics[0]
        return [(c.uuid, c.name)]

    # Prefer basics whose colorIdentity intersects desired colors.
    preferred = [c for c in basics if set(c.color_identity) & colors]
    if preferred:
        basics = preferred

    return [(c.uuid, c.name) for c in basics]


def generate_baseline_deck(idx: CardIndex, fmt: str, *, seed: int = 1, rules: FormatRules | None = None) -> Deck:
    """Very naive baseline deck: random legal nonlands + basics.

    This is intentionally simple; it exists to bootstrap later strategy/team+EA work.
    """

    random.seed(seed)
    rules = rules or FormatRules(name=fmt)

    legal_nonlands = idx.nonlands(fmt)
    if not legal_nonlands:
        raise ValueError("No legal nonland cards available")

    # Choose up to 9 unique nonlands at 4 copies each = 36 spells, leaving 24 lands.
    n_unique = min(9, len(legal_nonlands))
    chosen = random.sample(legal_nonlands, n_unique)

    main: list[DeckCard] = []
    colors: set[str] = set()

    for c in chosen:
        main.append(DeckCard(uuid=c.uuid, name=c.name, count=min(4, rules.max_copies)))
        colors |= set(c.color_identity)

    spell_count = sum(dc.count for dc in main)
    lands_needed = rules.mainboard_size - spell_count

    basics = _choose_basics(idx, fmt, colors)
    # Split lands roughly evenly among available basics
    per = lands_needed // len(basics)
    rem = lands_needed % len(basics)

    for i, (uuid, name) in enumerate(basics):
        cnt = per + (1 if i < rem else 0)
        if cnt > 0:
            main.append(DeckCard(uuid=uuid, name=name, count=cnt))

    return Deck(format=fmt, mainboard=main, sideboard=[])
