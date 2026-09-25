"""Floor tile order count: area method + optional grid layout preview."""

from app.engines.helpers import ceil_units


def tile_count(
    room_l: float,
    room_w: float,
    tile_l: float,
    tile_w: float,
    waste_pct: float,
    pieces_per_box: int = 1,
) -> dict:
    """
    raw_count: ceil(room_area / tile_piece_area)
    order_count: ceil(raw * (1 + waste_pct/100)) — before box rounding
    box_count / order_count_rounded: order_count rounded up to whole boxes
    of pieces_per_box (pieces_per_box == 1 leaves order_count unchanged).
    Open-path helpers may call box_round again with the live carton size.
    """
    area = float(room_l) * float(room_w)
    piece = float(tile_l) * float(tile_w)
    if piece <= 0 or area < 0:
        raise ValueError("invalid dimensions")
    raw = ceil_units(area / piece)
    with_waste = ceil_units(raw * (1 + float(waste_pct) / 100.0))
    boxes, rounded = box_round(with_waste, pieces_per_box)
    layout = layout_preview(room_l, room_w, tile_l, tile_w)
    return {
        "area_m2": round(area, 3),
        "piece_m2": round(piece, 4),
        "raw_count": raw,
        "waste_pct": float(waste_pct),
        "order_count": with_waste,
        "pieces_per_box": int(pieces_per_box),
        "box_count": boxes,
        "order_count_rounded": rounded,
        "layout": layout,
    }


def box_round(order_count: int, pieces_per_box: int) -> tuple[int, int]:
    """Round an order up to a whole number of boxes.

    Returns (box_count, rounded_piece_count). pieces_per_box must be a
    positive integer; N == 1 is the identity.
    """
    n = int(pieces_per_box)
    if n <= 0:
        raise ValueError("pieces_per_box must be a positive integer")
    count = int(order_count)
    boxes = -(-count // n)
    return boxes, boxes * n


def layout_preview(room_l: float, room_w: float, tile_l: float, tile_w: float) -> dict:
    """Grid count if tiles are laid on a full rectangular lattice (may exceed area method)."""
    cols = ceil_units(float(room_l) / float(tile_l))
    rows = ceil_units(float(room_w) / float(tile_w))
    grid_count = cols * rows
    return {
        "cols": cols,
        "rows": rows,
        "grid_count": grid_count,
    }
