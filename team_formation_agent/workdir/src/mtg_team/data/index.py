from __future__ import annotations

from dataclasses import dataclass, field

from mtg_team.generate.roles import CardRoles, infer_roles
from mtg_team.mtg.card import Card


@dataclass(slots=True)
class CardIndex:
    cards_by_uuid: dict[str, Card]
    _roles_by_uuid: dict[str, CardRoles] = field(init=False, repr=False)

    def __post_init__(self) -> None:
        # Cached role tags for fast strategy/deck building.
        self._roles_by_uuid = {u: infer_roles(c) for u, c in self.cards_by_uuid.items()}

    @property
    def cards(self) -> list[Card]:
        return list(self.cards_by_uuid.values())

    def roles(self, uuid: str) -> CardRoles:
        return self._roles_by_uuid[uuid]

    def legal_in(self, fmt: str) -> list[Card]:
        f = fmt.lower()
        return [c for c in self.cards if c.legality(f) == "Legal"]

    def lands(self, fmt: str | None = None) -> list[Card]:
        cards = self.cards if fmt is None else self.legal_in(fmt)
        return [c for c in cards if c.is_land]

    def nonlands(self, fmt: str | None = None) -> list[Card]:
        cards = self.cards if fmt is None else self.legal_in(fmt)
        return [c for c in cards if not c.is_land]

    def by_role(self, fmt: str, role: str) -> list[Card]:
        """Filter legal cards by an inferred role.

        Roles: threat, removal, counter, draw, ramp, sweeper
        """

        role = role.lower()
        out: list[Card] = []
        for c in self.nonlands(fmt):
            r = self.roles(c.uuid)
            if role == "threat" and r.is_threat:
                out.append(c)
            elif role == "removal" and r.is_removal:
                out.append(c)
            elif role == "counter" and r.is_counter:
                out.append(c)
            elif role == "draw" and r.is_draw:
                out.append(c)
            elif role == "ramp" and r.is_ramp:
                out.append(c)
            elif role == "sweeper" and r.is_sweeper:
                out.append(c)
        return out
