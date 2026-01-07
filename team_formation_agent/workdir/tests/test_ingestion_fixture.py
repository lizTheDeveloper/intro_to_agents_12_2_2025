from __future__ import annotations

from mtg_team.data.load import load_mtgjson


def test_load_tiny_fixture_counts() -> None:
    cfg = {
        "format": "pioneer",
        "data": {"mtgjson": {"all_printings_json_path": "tests/fixtures/tiny_all_printings.json"}},
    }
    idx = load_mtgjson(cfg)
    assert len(idx.cards) == 5
    assert len(idx.legal_in("pioneer")) == 4
    assert len(idx.lands("pioneer")) == 2
    assert len(idx.nonlands("pioneer")) == 2
