"""The prod guard sits in front of the Postgres read path.

analysis/readiness_gate.py connect() (also used by analysis/precompute.py)
targets 127.0.0.1:5433 by default -- a `flyctl proxy` tunnel to production
when one is open. This test fakes a flyctl listener and asserts nothing
connects.
"""

import pathlib
import sys

import psycopg2
import pytest

sys.path.insert(0, str(pathlib.Path(__file__).parent.parent / "analysis"))

import prod_guard  # noqa: E402  (analysis/prod_guard.py, as readiness_gate imports it)
import readiness_gate  # noqa: E402

CFG = {"host": "127.0.0.1", "port": "5433", "dbname": "db", "user": "u",
       "password": "", "sslmode": "disable"}


def test_connect_refuses_fly_tunnel(monkeypatch):
    seen = []
    monkeypatch.delenv("ALLOW_PROD_DB", raising=False)
    monkeypatch.setattr(prod_guard, "_listener", lambda port: seen.append(port) or "flyctl")
    monkeypatch.setattr(psycopg2, "connect", lambda *a, **kw: pytest.fail("connected"))
    with pytest.raises(prod_guard.ProdDatabaseError):
        readiness_gate.connect(CFG)
    assert seen == [5433]
