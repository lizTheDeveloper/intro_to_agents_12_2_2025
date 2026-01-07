from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from mtg_team.data.index import CardIndex
from mtg_team.mtg.card import Card


def load_all_printings_json(path: str | Path, *, limit_cards: int | None = None) -> CardIndex:
    """Load MTGJSON AllPrintings.json.

    This is slower/larger than SQLite but good for portability.

    Expected shape (MTGJSON v5-ish):
      {"data": {"SET": {"cards": [...]}, ...}}

    We deduplicate by UUID across printings.
    """

    p = Path(path)
    obj: dict[str, Any] = json.loads(p.read_text())
    data = obj.get("data") or {}

    cards_by_uuid: dict[str, Card] = {}
    seen = 0

    for _set_code, set_blob in data.items():
        for c in (set_blob.get("cards") or []):
            card = Card.from_mtgjson(c)
            if card.uuid and card.uuid not in cards_by_uuid:
                cards_by_uuid[card.uuid] = card
                seen += 1
                if limit_cards is not None and seen >= limit_cards:
                    return CardIndex(cards_by_uuid=cards_by_uuid)

    return CardIndex(cards_by_uuid=cards_by_uuid)
