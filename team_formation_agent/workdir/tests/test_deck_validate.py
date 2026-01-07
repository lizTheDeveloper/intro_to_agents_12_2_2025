from __future__ import annotations

from mtg_team.data.load import load_mtgjson
from mtg_team.deck.rules import FormatRules
from mtg_team.deck.validate import validate_deck
from mtg_team.generate.baseline import generate_baseline_deck


def test_generate_and_validate_baseline_with_fixture() -> None:
    cfg = {
        "format": "pioneer",
        "data": {"mtgjson": {"all_printings_json_path": "tests/fixtures/tiny_all_printings.json"}},
    }
    idx = load_mtgjson(cfg)
    deck = generate_baseline_deck(idx, "pioneer", seed=1, rules=FormatRules(name="pioneer"))
    rep = validate_deck(deck, idx, FormatRules(name="pioneer"))
    assert rep.ok, rep.errors
    assert deck.total_mainboard() == 60
