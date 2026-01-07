from __future__ import annotations

from dataclasses import dataclass
from typing import Any


@dataclass(frozen=True, slots=True)
class Card:
    """Minimal card model for generation/evaluation.

    Notes:
      - We use MTGJSON UUID as the primary key when available.
      - We keep legalities as a dict like {"pioneer": "Legal", ...}.
    """

    uuid: str
    name: str
    mana_cost: str | None
    mana_value: float | None
    types: tuple[str, ...]
    colors: tuple[str, ...]
    color_identity: tuple[str, ...]
    oracle_text: str | None
    legalities: dict[str, str]

    @property
    def is_land(self) -> bool:
        return "Land" in self.types

    @property
    def is_basic_land(self) -> bool:
        return self.is_land and any(t == "Basic" for t in self.types)

    def legality(self, fmt: str) -> str:
        return self.legalities.get(fmt.lower(), "Unknown")

    @classmethod
    def from_mtgjson(cls, d: dict[str, Any]) -> "Card":
        def tup(x: Any) -> tuple[str, ...]:
            if x is None:
                return tuple()
            return tuple(x)

        return cls(
            uuid=str(d.get("uuid")),
            name=str(d.get("name")),
            mana_cost=d.get("manaCost"),
            mana_value=d.get("manaValue"),
            types=tup(d.get("types")),
            colors=tup(d.get("colors")),
            color_identity=tup(d.get("colorIdentity")),
            oracle_text=d.get("text"),
            legalities={k.lower(): str(v) for k, v in (d.get("legalities") or {}).items()},
        )
