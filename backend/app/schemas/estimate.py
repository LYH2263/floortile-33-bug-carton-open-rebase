from pydantic import BaseModel, Field


class EstimateRequest(BaseModel):
    room_id: int
    tile_id: int
    waste_pct: float | None = None
    save: bool = False
    note: str = ""


class EstimateResponse(BaseModel):
    room_id: int
    tile_id: int
    room_name: str
    tile_name: str
    area_m2: float
    piece_m2: float
    raw_count: int
    waste_pct: float
    order_count: int
    pieces_per_box: int
    box_count: int
    order_count_rounded: int
    layout: dict
    run_id: int | None = None
