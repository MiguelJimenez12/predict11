from app.schemas.standing import Standing
from app.services.football_api_service import get_standings as get_standings_api


def get_standings():

    standings = get_standings_api()

    return [

        Standing(
            position=team["rank"],
            team_id=team["team"]["id"],
            team_name=team["team"]["name"],
            team_logo=team["team"]["logo"],
            played=team["all"]["played"],
            win=team["all"]["win"],
            draw=team["all"]["draw"],
            lose=team["all"]["lose"],
            goals_for=team["all"]["goals"]["for"],
            goals_against=team["all"]["goals"]["against"],
            goal_difference=team["goalsDiff"],
            points=team["points"],
        )

        for team in standings

    ]