import os
import sys
from pathlib import Path

import pytest

# Ensure the repository root is on sys.path so `import app` works without
# needing an editable install.
REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))


@pytest.fixture(scope="session", autouse=True)
def _use_temp_db(tmp_path_factory: pytest.TempPathFactory):
    # Force the application to use a throwaway database for tests.
    db_path = tmp_path_factory.mktemp("db") / "test.sqlite3"
    os.environ["TIMEBANK_DB_PATH"] = str(db_path)
    yield
    os.environ.pop("TIMEBANK_DB_PATH", None)


@pytest.fixture(autouse=True)
def _reset_rate_limiter_state():
    # The rate limiter is a process-global in-memory object. Reset between tests
    # to keep tests deterministic.
    from app.gateway.rate_limit import PUBLIC_LIMITER

    PUBLIC_LIMITER._hits.clear()
    yield
