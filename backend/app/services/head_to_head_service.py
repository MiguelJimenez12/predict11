from app.schemas.head_to_head import HeadToHead
from app.services.football_api_service import get_head_to_head as get_head_to_head_api


def get_head_to_head(home_team: int, away_team: int):

    matches = get_head_to_head_api(home_team, away_team)

    return [
        HeadToHead(
            fixture_id=match["fixture"]["id"],
            home_team=match["teams"]["home"]["name"],
            away_team=match["teams"]["away"]["name"],
            home_goals=match["goals"]["home"],
            away_goals=match["goals"]["away"],
            date=match["fixture"]["date"],
        )
        for match in matches
    ]
