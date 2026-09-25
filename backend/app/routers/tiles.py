from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field

from app.repositories import tiles as tile_repo

router = APIRouter(tags=["tiles"])


class TileUpdate(BaseModel):
    pieces_per_box: int = Field(..., gt=0)


@router.get("/tiles")
def list_tiles():
    return {"items": tile_repo.list_tiles()}


@router.get("/tiles/{tile_id}")
def get_tile(tile_id: int):
    row = tile_repo.get_tile(tile_id)
    if not row:
        raise HTTPException(404, "tile not found")
    return row


@router.put("/tiles/{tile_id}")
def update_tile(tile_id: int, body: TileUpdate):
    row = tile_repo.update_pieces_per_box(tile_id, body.pieces_per_box)
    if not row:
        raise HTTPException(404, "tile not found")
    return row
