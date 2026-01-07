from __future__ import annotations

import itertools
from dataclasses import dataclass

from mtg_team.generate.strategy import Strategy, Team, compatibility_score


@dataclass(frozen=True, slots=True)
class TeamSearchResult:
    team: Team
    score: float


def best_team(strategies: list[Strategy], *, k: int = 2) -> TeamSearchResult:
    if k < 1:
        raise ValueError("k must be >= 1")
    if len(strategies) < k:
        raise ValueError("Not enough strategies")

    best: TeamSearchResult | None = None
    for combo in itertools.combinations(strategies, k):
        team = Team(strategies=combo)
        score = compatibility_score(team)
        if best is None or score > best.score:
            best = TeamSearchResult(team=team, score=score)

    assert best is not None
    return best
