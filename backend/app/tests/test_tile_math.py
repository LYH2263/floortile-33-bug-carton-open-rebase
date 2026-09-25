import pytest

from app.engines.tile_math import box_round, layout_preview, tile_count


def test_guest_room_600_waste8():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["area_m2"] == 27.0
    assert r["raw_count"] == 75
    assert r["order_count"] == 81
    assert r["layout"]["cols"] == 10
    assert r["layout"]["rows"] == 8
    assert r["layout"]["grid_count"] == 80


def test_layout_preview_small_room():
    lp = layout_preview(2.5, 2.0, 0.6, 0.6)
    assert lp["cols"] == 5
    assert lp["rows"] == 4
    assert lp["grid_count"] == 20


def test_zero_waste():
    r = tile_count(3.0, 3.0, 1.0, 1.0, 0.0)
    assert r["raw_count"] == 9
    assert r["order_count"] == 9


def test_box_round_identity_when_one_per_box():
    assert box_round(81, 1) == (81, 81)


def test_box_round_rounds_up_to_whole_boxes():
    assert box_round(81, 4) == (21, 84)
    assert box_round(17, 3) == (6, 18)


def test_box_round_exact_multiple_unchanged():
    assert box_round(80, 4) == (20, 80)


@pytest.mark.parametrize("n", [0, -1, -8])
def test_box_round_rejects_non_positive_n(n):
    with pytest.raises(ValueError):
        box_round(10, n)


def test_tile_count_with_box_rounding():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0, 4)
    assert r["order_count"] == 81
    assert r["pieces_per_box"] == 4
    assert r["box_count"] == 21
    assert r["order_count_rounded"] == 84


def test_tile_count_default_box_is_identity():
    r = tile_count(6.0, 4.5, 0.6, 0.6, 8.0)
    assert r["pieces_per_box"] == 1
    assert r["box_count"] == r["order_count"]
    assert r["order_count_rounded"] == r["order_count"]
