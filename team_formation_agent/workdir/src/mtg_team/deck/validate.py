from __future__ import annotations

from dataclasses import dataclass, field

from mtg_team.data.index import CardIndex
from mtg_team.deck.models import Deck
from mtg_team.deck.rules import FormatRules


@dataclass(slots=True)
class ValidationReport:
    errors: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return not self.errors


def validate_deck(deck: Deck, idx: CardIndex, rules: FormatRules) -> ValidationReport:
    rep = ValidationReport()
    fmt = deck.format.lower()

    if deck.total_mainboard() != rules.mainboard_size:
        rep.errors.append(
            f"Mainboard size {deck.total_mainboard()} != required {rules.mainboard_size}"
        )

    for uuid, count in deck.counts_by_uuid().items():
        card = idx.cards_by_uuid.get(uuid)
        if card is None:
            rep.errors.append(f"Unknown card uuid in deck: {uuid}")
            continue

        if card.legality(fmt) != "Legal":
            rep.errors.append(f"Illegal in {fmt}: {card.name} ({card.legality(fmt)})")

        if not card.is_basic_land and count > rules.max_copies:
            rep.errors.append(f"Too many copies: {card.name} x{count} > {rules.max_copies}")

    return rep
