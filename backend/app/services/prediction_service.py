from app.schemas.prediction import PredictionResponse

from app.services.statistics_service import get_statistics
from app.services.head_to_head_service import get_head_to_head


def predict_match(home_team: int, away_team: int):

    home = get_statistics(home_team)
    away = get_statistics(away_team)

    h2h = get_head_to_head(home_team, away_team)

    home_score = (
        home.wins
        - home.losses
        + (home.goals_for - home.goals_against)
    )

    away_score = (
        away.wins
        - away.losses
        + (away.goals_for - away.goals_against)
    )

    # Bonus por historial

    home_h2h = 0
    away_h2h = 0

    for match in h2h:

        if match.home_team == home.team_name:

            if match.home_goals > match.away_goals:
                home_h2h += 1

            elif match.home_goals < match.away_goals:
                away_h2h += 1

        else:

            if match.away_goals > match.home_goals:
                home_h2h += 1

            elif match.away_goals < match.home_goals:
                away_h2h += 1

    home_score += home_h2h
    away_score += away_h2h

    total = home_score + away_score

    if total <= 0:
        total = 1

    home_probability = round(home_score / total * 100, 1)
    away_probability = round(away_score / total * 100, 1)

    draw_probability = round(
        100 - home_probability - away_probability,
        1
    )

    if draw_probability < 0:
        draw_probability = 0

    if home_probability > away_probability:
        score = "2-1"
    elif away_probability > home_probability:
        score = "1-2"
    else:
        score = "1-1"

    return PredictionResponse(
        home_team=home.team_name,
        away_team=away.team_name,

        home_win_probability=home_probability,
        draw_probability=draw_probability,
        away_win_probability=away_probability,

        predicted_score=score
    )