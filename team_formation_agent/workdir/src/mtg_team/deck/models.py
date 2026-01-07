from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class DeckCard:
    uuid: str
    name: str
    count: int


@dataclass(slots=True)
class Deck:
    format: str
    mainboard: list[DeckCard] = field(default_factory=list)
    sideboard: list[DeckCard] = field(default_factory=list)

    def total_mainboard(self) -> int:
        return sum(dc.count for dc in self.mainboard)

    def counts_by_uuid(self) -> dict[str, int]:
        out: dict[str, int] = {}
        for dc in self.mainboard:
            out[dc.uuid] = out.get(dc.uuid, 0) + dc.count
        return out
