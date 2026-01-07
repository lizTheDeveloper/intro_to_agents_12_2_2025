from __future__ import annotations

from dataclasses import dataclass

from mtg_team.mtg.card import Card


@dataclass(frozen=True, slots=True)
class CardRoles:
    is_threat: bool = False
    is_removal: bool = False
    is_counter: bool = False
    is_draw: bool = False
    is_ramp: bool = False
    is_sweeper: bool = False


def infer_roles(card: Card) -> CardRoles:
    """Heuristic role tagging from type line + oracle text.

    This is intentionally simple and explainable; later we can replace with ML.
    """

    t = " ".join(card.types).lower()
    text = (card.oracle_text or "").lower()

    is_threat = ("creature" in t) or ("planeswalker" in t)

    is_counter = "counter target" in text

    # removal heuristics
    removal_phrases = ["destroy target", "exile target", "deals", "-x/-x", "damage to any target"]
    is_removal = any(p in text for p in removal_phrases) and not is_counter

    # draw heuristics
    is_draw = ("draw" in text and "card" in text) and (not is_counter)

    # ramp heuristics
    ramp_phrases = ["search your library for a land", "add {", "treasure"]
    is_ramp = any(p in text for p in ramp_phrases)

    # sweeper heuristics
    is_sweeper = ("each creature" in text and ("destroy" in text or "deals" in text))

    return CardRoles(
        is_threat=is_threat,
        is_removal=is_removal,
        is_counter=is_counter,
        is_draw=is_draw,
        is_ramp=is_ramp,
        is_sweeper=is_sweeper,
    )
