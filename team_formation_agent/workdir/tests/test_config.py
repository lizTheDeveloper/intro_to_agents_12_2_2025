from __future__ import annotations

import json
import tempfile
from pathlib import Path

from mtg_team.util.config import load_config


def test_load_config_yaml() -> None:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "c.yaml"
        p.write_text("a: 1\n")
        assert load_config(p)["a"] == 1


def test_load_config_json() -> None:
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "c.json"
        p.write_text(json.dumps({"a": 2}))
        assert load_config(p)["a"] == 2
