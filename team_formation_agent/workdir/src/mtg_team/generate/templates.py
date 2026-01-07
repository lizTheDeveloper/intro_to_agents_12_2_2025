from __future__ import annotations

from dataclasses import dataclass

from mtg_team.generate.strategy import Strategy


@dataclass(frozen=True, slots=True)
class RoleQuota:
    role: str
    copies_total: int


@dataclass(frozen=True, slots=True)
class StrategyTemplate:
    strategy: Strategy
    quotas: tuple[RoleQuota, ...]
    land_count: int


def aggro_mono_red() -> StrategyTemplate:
    # simple example; colors are just tags for mana base later
    s = Strategy(name="aggro", desired_colors={"R"}, tags={"fast", "creature"}, incompatible_tags={"big_mana"})
    return StrategyTemplate(
        strategy=s,
        quotas=(RoleQuota("threat", 28), RoleQuota("removal", 8)),
        land_count=24,
    )


def control_azorius() -> StrategyTemplate:
    s = Strategy(name="control", desired_colors={"U", "W"}, tags={"interactive"}, incompatible_tags={"fast"})
    return StrategyTemplate(
        strategy=s,
        quotas=(RoleQuota("counter", 10), RoleQuota("removal", 8), RoleQuota("draw", 8), RoleQuota("threat", 6)),
        land_count=28,
    )


def ramp_green() -> StrategyTemplate:
    s = Strategy(name="ramp", desired_colors={"G"}, tags={"big_mana"}, incompatible_tags={"fast"})
    return StrategyTemplate(
        strategy=s,
        quotas=(RoleQuota("ramp", 12), RoleQuota("threat", 16), RoleQuota("removal", 4)),
        land_count=28,
    )
