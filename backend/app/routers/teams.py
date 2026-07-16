from fastapi import APIRouter, HTTPException
from app.schemas.team import Team
from app.services.team_service import (get_all_teams, get_team_by_id)

router = APIRouter()


@router.get("/teams", response_model=list[Team])
def get_teams():
    return get_all_teams()

@router.get("/teams/{team_id}", response_model=Team)
def get_team(team_id: int):

    team = get_team_by_id(team_id)

    if team is None:
        raise HTTPException(
            status_code=404,
            detail="Team not found"
        )

    return team