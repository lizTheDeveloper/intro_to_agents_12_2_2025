from __future__ import annotations

import random
from dataclasses import dataclass

from mtg_team.data.index import CardIndex
from mtg_team.deck.models import Deck


@dataclass(frozen=True, slots=True)
class GoldfishMetrics:
    keepable_rate: float
    land_rate: float


def evaluate_goldfish(deck: Deck, idx: CardIndex, *, seed: int = 1, n: int = 200) -> GoldfishMetrics:
    """Very lightweight playability proxy.

    We simulate opening hands only:
      - keepable if lands in [2,5]
    """

    random.seed(seed)

    # Expand deck into a list of uuids
    pool: list[str] = []
    for dc in deck.mainboard:
        pool.extend([dc.uuid] * dc.count)

    lands = {c.uuid for c in idx.lands(deck.format)}

    keep = 0
    total_lands = 0

    for _ in range(n):
        hand = random.sample(pool, 7)
        n_lands = sum(1 for u in hand if u in lands)
        total_lands += n_lands
        if 2 <= n_lands <= 5:
            keep += 1

    return GoldfishMetrics(keepable_rate=keep / n, land_rate=total_lands / (7 * n))
