from __future__ import annotations

import argparse
import json
from pathlib import Path

from mtg_team.data.load import load_mtgjson
from mtg_team.deck.rules import FormatRules
from mtg_team.deck.validate import validate_deck
from mtg_team.generate.baseline import generate_baseline_deck
from mtg_team.util.config import load_config
from mtg_team.util.rng import seed_everything


def build_parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(prog="mtg-team")
    sub = p.add_subparsers(dest="cmd", required=True)

    p_load = sub.add_parser("load-data", help="Load MTGJSON and print summary stats.")
    p_load.add_argument("--config", required=True, help="Path to config YAML/JSON")
    p_load.add_argument("--limit-cards", type=int, default=None, help="Optional cap for quick dev")

    p_gen = sub.add_parser("generate-deck", help="Generate a baseline legal deck.")
    p_gen.add_argument("--config", required=True)
    p_gen.add_argument("--seed", type=int, default=1)
    p_gen.add_argument("--out", required=True)

    p_test = sub.add_parser("self-test", help="Run minimal self-tests without pytest.")

    return p


def cmd_load_data(cfg: dict, limit_cards: int | None) -> int:
    fmt = (cfg.get("format") or "pioneer").lower()
    idx = load_mtgjson(cfg, limit_cards=limit_cards)

    summary = {
        "format": fmt,
        "cards_total": len(idx.cards),
        "cards_legal": len(idx.legal_in(fmt)),
        "lands_legal": len(idx.lands(fmt)),
        "nonlands_legal": len(idx.nonlands(fmt)),
    }
    print(json.dumps(summary, indent=2))
    return 0


def cmd_generate_deck(cfg: dict, seed: int, out: str) -> int:
    fmt = (cfg.get("format") or "pioneer").lower()
    seed_everything(seed)
    idx = load_mtgjson(cfg)

    deck = generate_baseline_deck(idx, fmt, seed=seed)
    rep = validate_deck(deck, idx, FormatRules(name=fmt))
    if not rep.ok:
        raise SystemExit("Deck validation failed: " + "; ".join(rep.errors))

    Path(out).parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "format": deck.format,
        "mainboard": [{"uuid": dc.uuid, "name": dc.name, "count": dc.count} for dc in deck.mainboard],
        "sideboard": [{"uuid": dc.uuid, "name": dc.name, "count": dc.count} for dc in deck.sideboard],
    }
    Path(out).write_text(json.dumps(payload, indent=2))
    print(f"Wrote {out}")
    return 0


def cmd_self_test() -> int:
    from mtg_team.util.mini_test import run

    return run()


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    if args.cmd == "self-test":
        return cmd_self_test()

    cfg = load_config(args.config)

    if args.cmd == "load-data":
        return cmd_load_data(cfg, args.limit_cards)

    if args.cmd == "generate-deck":
        return cmd_generate_deck(cfg, args.seed, args.out)

    raise RuntimeError(f"Unknown cmd: {args.cmd}")


if __name__ == "__main__":
    raise SystemExit(main())
