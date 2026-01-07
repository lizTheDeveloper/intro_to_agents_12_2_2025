from __future__ import annotations

import importlib
import pkgutil
import traceback


def run() -> int:
    """Minimal test runner so the project can self-test without pytest installed.

    Convention:
      - Test modules are under `tests/` but importable as top-level modules when
        running with PYTHONPATH=src.
      - Each test module exposes functions named `test_*`.

    For this educational repo, we keep it intentionally simple.
    """

    # Discover tests by walking installed top-level modules named 'tests.*'
    # In our environment we will just explicitly import the two test modules.
    test_modules = [
        "tests.test_config",
        "tests.test_card_index",
    ]

    failures: list[str] = []

    for mod_name in test_modules:
        try:
            mod = importlib.import_module(mod_name)
        except Exception:
            failures.append(f"IMPORT FAILED: {mod_name}\n{traceback.format_exc()}")
            continue

        for attr in dir(mod):
            if attr.startswith("test_"):
                fn = getattr(mod, attr)
                if callable(fn):
                    try:
                        fn()  # type: ignore[misc]
                    except Exception:
                        failures.append(f"FAIL: {mod_name}.{attr}\n{traceback.format_exc()}")

    if failures:
        print("\n".join(failures))
        print(f"FAILED ({len(failures)})")
        return 1

    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(run())
