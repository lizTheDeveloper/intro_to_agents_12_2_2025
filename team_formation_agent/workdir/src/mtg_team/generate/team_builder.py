from __future__ import annotations

import random
from collections import Counter

from mtg_team.data.index import CardIndex
from mtg_team.deck.models import Deck, DeckCard
from mtg_team.deck.rules import FormatRules
from mtg_team.generate.strategy import Team
from mtg_team.generate.templates import StrategyTemplate


def _add_cards_with_copy_limit(
    main: Counter[str],
    cards: list,
    need: int,
    rules: FormatRules,
) -> None:
    """Fill `main` multiset up to `need` copies from given card list."""

    if need <= 0:
        return

    random.shuffle(cards)
    for c in cards:
        if need <= 0:
            break
        cur = main[c.uuid]
        max_allowed = 999 if c.is_basic_land else rules.max_copies
        if cur >= max_allowed:
            continue
        add = min(max_allowed - cur, need)
        main[c.uuid] += add
        need -= add

    if need > 0:
        raise ValueError("Not enough candidate cards to satisfy quota")


def generate_deck_from_templates(
    idx: CardIndex,
    fmt: str,
    templates: list[StrategyTemplate],
    *,
    seed: int = 1,
    rules: FormatRules | None = None,
) -> Deck:
    random.seed(seed)
    rules = rules or FormatRules(name=fmt)

    # Aggregate quotas and colors
    total_land = max(t.land_count for t in templates)
    quotas: Counter[str] = Counter()
    colors: set[str] = set()

    for t in templates:
        colors |= set(t.strategy.desired_colors)
        for q in t.quotas:
            quotas[q.role] += q.copies_total

    # Build spells by quotas
    main: Counter[str] = Counter()
    for role, need in quotas.items():
        candidates = idx.by_role(fmt, role)
        if not candidates:
            continue
        _add_cards_with_copy_limit(main, candidates, need, rules)

    spell_count = sum(main.values())

    # Backfill threats if we don't have enough spells, then trim if over.
    if spell_count < rules.mainboard_size - total_land:
        needed = (rules.mainboard_size - total_land) - spell_count
        threats = idx.by_role(fmt, "threat")
        _add_cards_with_copy_limit(main, threats, needed, rules)

    # If too many spells, randomly drop extras (simple repair)
    while sum(main.values()) > rules.mainboard_size - total_land:
        u = random.choice(list(main.keys()))
        main[u] -= 1
        if main[u] <= 0:
            del main[u]

    # Lands: basic land filler matching available basics
    basics = [c for c in idx.lands(fmt) if c.is_basic_land]
    if not basics:
        raise ValueError("No basic lands available")

    preferred = [c for c in basics if set(c.color_identity) & colors]
    basics = preferred or basics

    lands_needed = rules.mainboard_size - sum(main.values())
    per = lands_needed // len(basics)
    rem = lands_needed % len(basics)

    for i, c in enumerate(basics):
        cnt = per + (1 if i < rem else 0)
        if cnt:
            main[c.uuid] += cnt

    # Convert to DeckCards
    deck_cards: list[DeckCard] = []
    for uuid, count in main.items():
        card = idx.cards_by_uuid[uuid]
        deck_cards.append(DeckCard(uuid=uuid, name=card.name, count=count))

    # stable-ish output ordering
    deck_cards.sort(key=lambda dc: (dc.name, dc.uuid))
    return Deck(format=fmt, mainboard=deck_cards, sideboard=[])


def generate_deck_from_team(idx: CardIndex, fmt: str, team: Team, *, seed: int = 1) -> Deck:
    # Map strategies to templates (v1 hardcoded)
    name_to_template = {
        "aggro": None,
        "control": None,
        "ramp": None,
    }
    # If strategy names don't match, fallback to baseline behavior via quotas=threats
    templates: list[StrategyTemplate] = []

    from mtg_team.generate.templates import aggro_mono_red, control_azorius, ramp_green

    for s in team.strategies:
        if s.name == "aggro":
            templates.append(aggro_mono_red())
        elif s.name == "control":
            templates.append(control_azorius())
        elif s.name == "ramp":
            templates.append(ramp_green())

    if not templates:
        # no recognized strategies, build a generic threat deck
        templates = [ramp_green()]

    return generate_deck_from_templates(idx, fmt, templates, seed=seed)
