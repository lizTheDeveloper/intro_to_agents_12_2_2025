from __future__ import annotations

from pathlib import Path
from typing import Any

from mtg_team.data.index import CardIndex
from mtg_team.data.mtgjson_json import load_all_printings_json
from mtg_team.data.mtgjson_sqlite import load_all_printings_sqlite


def load_mtgjson(cfg: dict[str, Any], *, limit_cards: int | None = None) -> CardIndex:
    """Load MTGJSON from configured source.

    Config schema (subset):
      data:
        mtgjson:
          sqlite_path: path/to/AllPrintings.sqlite
          all_printings_json_path: path/to/AllPrintings.json

    Preference: sqlite_path if both set.
    """

    src = (cfg.get("data") or {}).get("mtgjson") or {}

    sqlite_path = src.get("sqlite_path")
    json_path = src.get("all_printings_json_path")

    if sqlite_path:
        return load_all_printings_sqlite(Path(sqlite_path), limit_cards=limit_cards)
    if json_path:
        return load_all_printings_json(Path(json_path), limit_cards=limit_cards)

    raise ValueError("Config missing data.mtgjson.sqlite_path or data.mtgjson.all_printings_json_path")
