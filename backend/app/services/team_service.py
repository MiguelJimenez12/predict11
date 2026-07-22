from app.schemas.team import Team
from app.services.football_api_service import get_teams as get_teams_api


def get_teams():

    teams = get_teams_api()

    result = []

    for team in teams:

        result.append(
            Team(
                id=team["team"]["id"],
                name=team["team"]["name"],
                country=team["team"]["country"],
                logo=team["team"]["logo"]
            )
        )

    return result