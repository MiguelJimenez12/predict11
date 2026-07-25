from fastapi import APIRouter

from app.schemas.statistics import Statistics
from app.services.statistics_service import get_statistics

router = APIRouter()


@router.get("/{team_id}", response_model=Statistics)
def read_statistics(team_id: int):

    return get_statistics(team_id)