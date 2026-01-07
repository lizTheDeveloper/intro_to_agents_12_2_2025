from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import Any

from mtg_team.data.index import CardIndex
from mtg_team.mtg.card import Card


def _row_to_card(row: dict[str, Any]) -> Card:
    # SQLite schema can vary slightly; we attempt a minimal compatible mapping.
    # MTGJSON AllPrintings.sqlite typically has a `cards` table with many JSON-ish columns.
    legalities = {}
    if row.get("legalities"):
        try:
            import json

            legalities = json.loads(row["legalities"]) or {}
        except Exception:
            legalities = {}

    def parse_json_list(field: str) -> list[str]:
        v = row.get(field)
        if v is None:
            return []
        try:
            import json

            return json.loads(v) or []
        except Exception:
            return []

    d = {
        "uuid": row.get("uuid"),
        "name": row.get("name"),
        "manaCost": row.get("manaCost"),
        "manaValue": row.get("manaValue"),
        "types": parse_json_list("types"),
        "colors": parse_json_list("colors"),
        "colorIdentity": parse_json_list("colorIdentity"),
        "text": row.get("text"),
        "legalities": legalities,
    }
    return Card.from_mtgjson(d)


def load_all_printings_sqlite(path: str | Path, *, limit_cards: int | None = None) -> CardIndex:
    """Load cards from MTGJSON AllPrintings.sqlite.

    We query the `cards` table and deduplicate by UUID.

    NOTE: Users must download the SQLite file separately.
    """

    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    conn = sqlite3.connect(str(p))
    conn.row_factory = sqlite3.Row

    cards_by_uuid: dict[str, Card] = {}
    try:
        cur = conn.cursor()
        cur.execute("SELECT uuid, name, manaCost, manaValue, types, colors, colorIdentity, text, legalities FROM cards")
        for r in cur:
            row = dict(r)
            card = _row_to_card(row)
            if card.uuid and card.uuid not in cards_by_uuid:
                cards_by_uuid[card.uuid] = card
                if limit_cards is not None and len(cards_by_uuid) >= limit_cards:
                    break
    finally:
        conn.close()

    return CardIndex(cards_by_uuid=cards_by_uuid)
