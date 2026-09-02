from fastapi import APIRouter

from app.schemas.head_to_head import HeadToHead
from app.services.head_to_head_service import get_head_to_head

router = APIRouter()


@router.get("/{home_team}/{away_team}", response_model=list[HeadToHead])
def read_head_to_head(home_team: int, away_team: int):

    return get_head_to_head(home_team, away_team)