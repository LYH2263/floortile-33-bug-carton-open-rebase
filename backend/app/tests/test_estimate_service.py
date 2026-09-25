import pytest
from fastapi import HTTPException
from pydantic import ValidationError

import app.db as db
from app import seed
from app.repositories import history, tiles
from app.routers.tiles import TileUpdate
from app.services import estimate_service


@pytest.fixture()
def fresh_db(tmp_path, monkeypatch):
    monkeypatch.setattr(db, "DB_PATH", tmp_path / "test.db")
    seed.init_db()
    return tmp_path / "test.db"


def test_dry_run_estimate_includes_box_rounding(fresh_db):
    # seeded: room 1 = 6.0x4.5, tile 1 = 600x600 with pieces_per_box=4
    r = estimate_service.run_estimate(1, 1, None, False, "")
    assert r["run_id"] is None
    assert r["order_count"] == 81
    assert r["pieces_per_box"] == 4
    assert r["box_count"] == 21
    assert r["order_count_rounded"] == 84


def test_saved_run_keeps_snapshot_after_tile_n_change(fresh_db):
    r = estimate_service.run_estimate(1, 1, None, True, "keep")
    run_id = r["run_id"]
    assert run_id is not None
    assert r["order_count_rounded"] == 84

    # Changing the tile's default N afterwards must not rewrite saved runs.
    updated = tiles.update_pieces_per_box(1, 10)
    assert updated["pieces_per_box"] == 10

    saved = history.get_run(run_id)
    res = saved["result"]
    assert res["pieces_per_box"] == 4
    assert res["order_count"] == 81
    assert res["box_count"] == 21
    assert res["order_count_rounded"] == 84


def test_estimate_rejects_non_positive_pieces_per_box(fresh_db):
    conn = db.connect()
    conn.execute("UPDATE tiles SET pieces_per_box=0 WHERE id=1")
    conn.commit()
    conn.close()
    with pytest.raises(HTTPException) as exc:
        estimate_service.run_estimate(1, 1, None, False, "")
    assert exc.value.status_code == 422


@pytest.mark.parametrize("n", [0, -1, -8])
def test_tile_update_schema_rejects_non_positive_n(n):
    with pytest.raises(ValidationError):
        TileUpdate(pieces_per_box=n)
