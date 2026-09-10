import httpx
from fastapi import APIRouter, HTTPException, Query

from app.schemas.league import League, LeagueMatch, LeagueStanding, LeagueTeam
from app.services.league_service import list_leagues, list_matches, list_teams, standings

router = APIRouter()


@router.get("/", response_model=list[League])
def read_leagues():
    return list_leagues()


@router.get("/{slug}/teams", response_model=list[LeagueTeam])
def read_league_teams(slug: str):
    try:
        return list_teams(slug)
    except (ValueError, RuntimeError, httpx.HTTPError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/{slug}/matches", response_model=list[LeagueMatch])
def read_league_matches(
    slug: str,
    status: str | None = Query(default=None, pattern="^(SCHEDULED|TIMED|IN_PLAY|PAUSED|FINISHED)$"),
    date_from: str | None = Query(default=None, alias="dateFrom"),
    date_to: str | None = Query(default=None, alias="dateTo"),
):
    try:
        return list_matches(slug, status=status, date_from=date_from, date_to=date_to)
    except (ValueError, RuntimeError, httpx.HTTPError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/{slug}/standings", response_model=list[LeagueStanding])
def read_league_standings(slug: str):
    try:
        return standings(slug)
    except (ValueError, RuntimeError, httpx.HTTPError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
