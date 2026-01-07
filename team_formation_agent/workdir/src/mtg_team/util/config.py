from __future__ import annotations

import json
from pathlib import Path
from typing import Any


def _load_yaml_fallback(text: str) -> dict[str, Any]:
    """Very small YAML subset parser.

    Supports only the needs of this repo's example configs:
      - nested maps via indentation (2 spaces)
      - string/number/bool scalars

    If you have PyYAML installed, prefer that; we avoid a hard dependency so the
    project runs in restricted environments.
    """

    root: dict[str, Any] = {}
    stack: list[tuple[int, dict[str, Any]]] = [(0, root)]

    def parse_scalar(v: str) -> Any:
        v = v.strip()
        if v.lower() in {"true", "false"}:
            return v.lower() == "true"
        try:
            if "." in v:
                return float(v)
            return int(v)
        except Exception:
            return v

    for raw in text.splitlines():
        if not raw.strip() or raw.strip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        key, _, rest = raw.strip().partition(":")
        value = rest.strip()

        while stack and indent < stack[-1][0]:
            stack.pop()
        cur = stack[-1][1]

        if value == "":
            nxt: dict[str, Any] = {}
            cur[key] = nxt
            stack.append((indent + 2, nxt))
        else:
            cur[key] = parse_scalar(value)

    return root


def load_config(path: str | Path) -> dict[str, Any]:
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(p)

    if p.suffix.lower() == ".json":
        return json.loads(p.read_text())

    if p.suffix.lower() in {".yaml", ".yml"}:
        text = p.read_text()
        try:
            import yaml  # type: ignore

            return yaml.safe_load(text) or {}
        except ModuleNotFoundError:
            return _load_yaml_fallback(text)

    raise ValueError(f"Unsupported config extension: {p.suffix}")
