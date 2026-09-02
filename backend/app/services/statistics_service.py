from app.schemas.statistics import Statistics
from app.services.football_api_service import (
    get_statistics as get_statistics_api
)


def get_statistics(team_id: int):

    stats = get_statistics_api(team_id)

    return Statistics(
        team_id=stats["team"]["id"],
        team_name=stats["team"]["name"],
        league=stats["league"]["name"],
        season=stats["league"]["season"],

        matches_played=stats["fixtures"]["played"]["total"],
        wins=stats["fixtures"]["wins"]["total"],
        draws=stats["fixtures"]["draws"]["total"],
        losses=stats["fixtures"]["loses"]["total"],

        goals_for=stats["goals"]["for"]["total"]["total"],
        goals_against=stats["goals"]["against"]["total"]["total"],

        clean_sheets=stats["clean_sheet"]["total"],
        failed_to_score=stats["failed_to_score"]["total"]
    )
