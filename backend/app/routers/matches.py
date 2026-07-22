from fastapi import APIRouter

from app.services.match_service import get_matches

router = APIRouter()


@router.get("/{team_id}")
def get_team_matches(team_id: int):
    return get_matches(team_id)