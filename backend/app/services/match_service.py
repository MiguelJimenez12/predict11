from app.schemas.match import Match
from app.services.football_api_service import get_matches as get_matches_api


def get_matches(team_id: int):

    matches = get_matches_api(team_id)

    result = []

    for match in matches:

        result.append(
            Match(
                id=match["fixture"]["id"],
                home_team=match["teams"]["home"]["name"],
                away_team=match["teams"]["away"]["name"],
                home_logo=match["teams"]["home"]["logo"],
                away_logo=match["teams"]["away"]["logo"],
                date=match["fixture"]["date"],
                league=match["league"]["name"],
                status=match["fixture"]["status"]["short"],
                home_goals=match["goals"]["home"],
                away_goals=match["goals"]["away"]
            )
        )

    return result