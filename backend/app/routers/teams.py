from fastapi import APIRouter

from app.services.team_service import get_teams

router = APIRouter()


@router.get("/", tags=["Teams"])
def read_teams():
    return get_teams()