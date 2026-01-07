from __future__ import annotations

from mtg_team.data.load import load_mtgjson
from mtg_team.deck.rules import FormatRules
from mtg_team.deck.validate import validate_deck
from mtg_team.eval.goldfish import evaluate_goldfish
from mtg_team.generate.baseline import generate_baseline_deck


def test_goldfish_runs_on_fixture() -> None:
    cfg = {
        "format": "pioneer",
        "data": {"mtgjson": {"all_printings_json_path": "tests/fixtures/tiny_all_printings.json"}},
    }
    idx = load_mtgjson(cfg)
    deck = generate_baseline_deck(idx, "pioneer", seed=1, rules=FormatRules(name="pioneer"))
    rep = validate_deck(deck, idx, FormatRules(name="pioneer"))
    assert rep.ok

    m = evaluate_goldfish(deck, idx, seed=1, n=50)
    assert 0.0 <= m.keepable_rate <= 1.0
    assert 0.0 <= m.land_rate <= 1.0
