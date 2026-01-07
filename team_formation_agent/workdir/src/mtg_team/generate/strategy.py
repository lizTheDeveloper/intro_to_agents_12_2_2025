from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True, slots=True)
class Strategy:
    name: str
    # Coarse constraints (v1): desired color identity set, and a desired land ratio.
    desired_colors: set[str] = field(default_factory=set)
    land_ratio: float = 0.4
    # Tagging for team formation (v1): simple string tags
    tags: set[str] = field(default_factory=set)
    incompatible_tags: set[str] = field(default_factory=set)


@dataclass(frozen=True, slots=True)
class Team:
    strategies: tuple[Strategy, ...]

    def tags(self) -> set[str]:
        out: set[str] = set()
        for s in self.strategies:
            out |= set(s.tags)
        return out


def compatibility_score(team: Team) -> float:
    """Toy compatibility score.

    +1 for each shared tag across strategies, -2 for tag incompatibilities.
    """

    tags = team.tags()
    score = 0.0

    for s in team.strategies:
        # reward tags present in team
        score += len(s.tags & tags)
        # penalize incompatible tags present in team
        score -= 2.0 * len(s.incompatible_tags & tags)

    return score
