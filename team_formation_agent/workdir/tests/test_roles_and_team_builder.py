from __future__ import annotations

from mtg_team.data.load import load_mtgjson
from mtg_team.deck.rules import FormatRules
from mtg_team.deck.validate import validate_deck
from mtg_team.generate.strategy import Strategy, Team
from mtg_team.generate.team_builder import generate_deck_from_team


def test_team_builder_runs_on_fixture() -> None:
    cfg = {
        "format": "pioneer",
        "data": {"mtgjson": {"all_printings_json_path": "tests/fixtures/tiny_all_printings.json"}},
    }
    idx = load_mtgjson(cfg)

    team = Team(strategies=(Strategy(name="control"),))
    deck = generate_deck_from_team(idx, "pioneer", team, seed=1)
    rep = validate_deck(deck, idx, FormatRules(name="pioneer"))
    assert rep.ok, rep.errors
    assert deck.total_mainboard() == 60
