from fastapi import APIRouter, HTTPException

from app.schemas.match import Match
from app.services.match_service import (
    get_all_matches,
    get_match_by_id
)

router = APIRouter(tags=["Matches"])


@router.get("/matches", response_model=list[Match])
def get_matches():
    return get_all_matches()


@router.get("/matches/{match_id}", response_model=Match)
def get_match(match_id: int):

    match = get_match_by_id(match_id)

    if match is None:
        raise HTTPException(
            status_code=404,
            detail="Match not found"
        )

    return match