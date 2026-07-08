from fastapi import APIRouter
from app.schemas.team import Team

from app.services.team_service import get_all_teams

router = APIRouter()


@router.get("/teams", response_model=list[Team])
def get_teams():
    return get_all_teams()