from fastapi import APIRouter

from app.services.match_service import get_matches
from app.services.league_service import list_matches

router = APIRouter()


@router.get("/upcoming")
def get_upcoming_matches(league: str):
    return list_matches(league, status="SCHEDULED")


@router.get("/{team_id}")
def get_team_matches(team_id: int):
    return get_matches(team_id)
