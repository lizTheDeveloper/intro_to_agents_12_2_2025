from __future__ import annotations

import random
from dataclasses import dataclass

from mtg_team.data.index import CardIndex
from mtg_team.deck.rules import FormatRules
from mtg_team.deck.validate import validate_deck
from mtg_team.eval.goldfish import evaluate_goldfish
from mtg_team.generate.baseline import generate_baseline_deck


@dataclass(frozen=True, slots=True)
class Individual:
    deck_json: dict
    fitness: float


def _deck_to_json(deck) -> dict:
    return {
        "format": deck.format,
        "mainboard": [{"uuid": dc.uuid, "name": dc.name, "count": dc.count} for dc in deck.mainboard],
        "sideboard": [],
    }


def evolve_playability(
    idx: CardIndex,
    fmt: str,
    *,
    seed: int = 1,
    pop: int = 20,
    generations: int = 10,
) -> list[Individual]:
    """Prototype evolutionary loop optimizing only goldfish keepable rate.

    This is the first slice of the OpenSpec EA; later we add multi-objective + team strategies.
    """

    random.seed(seed)
    rules = FormatRules(name=fmt)

    def make_one(s: int):
        deck = generate_baseline_deck(idx, fmt, seed=s, rules=rules)
        rep = validate_deck(deck, idx, rules)
        if not rep.ok:
            return None
        m = evaluate_goldfish(deck, idx, seed=s, n=200)
        return Individual(deck_json=_deck_to_json(deck), fitness=m.keepable_rate)

    population: list[Individual] = []
    s = seed
    while len(population) < pop:
        ind = make_one(s)
        s += 1
        if ind is not None:
            population.append(ind)

    for g in range(generations):
        # select top half
        population.sort(key=lambda x: x.fitness, reverse=True)
        parents = population[: max(2, pop // 2)]

        # reproduce by reseeding (placeholder mutation)
        children: list[Individual] = []
        while len(children) + len(parents) < pop:
            p = random.choice(parents)
            # mutation = new random seed
            s += 1
            ind = make_one(s)
            if ind is not None:
                children.append(ind)

        population = parents + children

    population.sort(key=lambda x: x.fitness, reverse=True)
    return population
