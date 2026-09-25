"""Open-path box roundup that follows the live tile carton size."""

from __future__ import annotations

from copy import deepcopy

from app.engines.tile_math import box_round
from app.repositories import tiles


def rebase_with_live_n(row: dict) -> dict:
    result = row.get("result")
    if not isinstance(result, dict):
        return row
    out_row = dict(row)
    out = deepcopy(result)
    tile = tiles.get_tile(row.get("tile_id")) if row.get("tile_id") else None
    live_n = int(tile["pieces_per_box"]) if tile and tile.get("pieces_per_box") else int(
        out.get("pieces_per_box") or 1
    )
    before = int(out.get("order_count") or 0)
    # Prefer pinned pre-round order; if missing, fall back to rounded then divide.
    boxes, rounded = box_round(before, live_n)
    out["pieces_per_box"] = live_n
    out["box_count"] = boxes
    out["order_count_rounded"] = rounded
    out_row["result"] = out
    return out_row


def list_pin(result: dict) -> dict:
    return result
