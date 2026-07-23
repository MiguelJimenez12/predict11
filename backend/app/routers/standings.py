from fastapi import APIRouter

from app.schemas.standing import Standing
from app.services.standings_service import get_standings

router = APIRouter()


@router.get("/", response_model=list[Standing])
def read_standings():

    return get_standings()