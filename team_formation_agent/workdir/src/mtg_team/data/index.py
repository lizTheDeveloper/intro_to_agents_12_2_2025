from __future__ import annotations

from dataclasses import dataclass

from mtg_team.mtg.card import Card


@dataclass(slots=True)
class CardIndex:
    cards_by_uuid: dict[str, Card]

    @property
    def cards(self) -> list[Card]:
        return list(self.cards_by_uuid.values())

    def legal_in(self, fmt: str) -> list[Card]:
        f = fmt.lower()
        return [c for c in self.cards if c.legality(f) == "Legal"]

    def lands(self, fmt: str | None = None) -> list[Card]:
        cards = self.cards if fmt is None else self.legal_in(fmt)
        return [c for c in cards if c.is_land]

    def nonlands(self, fmt: str | None = None) -> list[Card]:
        cards = self.cards if fmt is None else self.legal_in(fmt)
        return [c for c in cards if not c.is_land]
