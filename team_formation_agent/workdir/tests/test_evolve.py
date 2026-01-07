from __future__ import annotations

from mtg_team.data.load import load_mtgjson
from mtg_team.evolve.evolution import evolve_playability


def test_evolve_runs_on_fixture() -> None:
    cfg = {
        "format": "pioneer",
        "data": {"mtgjson": {"all_printings_json_path": "tests/fixtures/tiny_all_printings.json"}},
    }
    idx = load_mtgjson(cfg)
    pop = evolve_playability(idx, "pioneer", seed=1, pop=6, generations=2)
    assert len(pop) == 6
    assert pop[0].fitness >= pop[-1].fitness
