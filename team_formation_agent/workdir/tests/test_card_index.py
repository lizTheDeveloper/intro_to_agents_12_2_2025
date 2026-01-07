from mtg_team.data.index import CardIndex
from mtg_team.mtg.card import Card


def test_legality_and_land_filters():
    c1 = Card.from_mtgjson(
        {
            "uuid": "1",
            "name": "Forest",
            "types": ["Basic", "Land"],
            "legalities": {"pioneer": "Legal"},
        }
    )
    c2 = Card.from_mtgjson(
        {
            "uuid": "2",
            "name": "Fancy Spell",
            "types": ["Instant"],
            "legalities": {"pioneer": "Legal"},
        }
    )
    c3 = Card.from_mtgjson(
        {
            "uuid": "3",
            "name": "Banned Card",
            "types": ["Sorcery"],
            "legalities": {"pioneer": "Banned"},
        }
    )

    idx = CardIndex(cards_by_uuid={c1.uuid: c1, c2.uuid: c2, c3.uuid: c3})

    legal = idx.legal_in("pioneer")
    assert {c.uuid for c in legal} == {"1", "2"}

    lands = idx.lands("pioneer")
    assert [c.name for c in lands] == ["Forest"]

    nonlands = idx.nonlands("pioneer")
    assert {c.name for c in nonlands} == {"Fancy Spell"}
