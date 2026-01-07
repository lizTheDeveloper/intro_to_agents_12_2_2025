from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class FormatRules:
    name: str = "pioneer"
    mainboard_size: int = 60
    max_copies: int = 4
