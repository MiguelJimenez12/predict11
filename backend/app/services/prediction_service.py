import math

from app.schemas.prediction import PredictionResponse

from app.services.statistics_service import get_statistics
from app.services.head_to_head_service import get_head_to_head


def predict_match(home_team: int, away_team: int):

    if home_team == away_team:
        raise ValueError("Selecciona dos equipos diferentes.")

    home = get_statistics(home_team)
    away = get_statistics(away_team)

    h2h = get_head_to_head(home_team, away_team)

    def strength(stats):
        played = max(stats.matches_played, 1)
        points_per_game = (stats.wins * 3 + stats.draws) / played
        goal_difference = (stats.goals_for - stats.goals_against) / played
        clean_sheet_rate = stats.clean_sheets / played
        return points_per_game + (goal_difference * 0.45) + (clean_sheet_rate * 0.2)

    home_h2h = away_h2h = draws_h2h = 0

    for match in h2h:

        if match.home_team == home.team_name:

            if match.home_goals > match.away_goals:
                home_h2h += 1

            elif match.home_goals < match.away_goals:
                away_h2h += 1
            else:
                draws_h2h += 1

        else:

            if match.away_goals > match.home_goals:
                home_h2h += 1

            elif match.away_goals < match.home_goals:
                away_h2h += 1
            else:
                draws_h2h += 1

    h2h_total = max(home_h2h + away_h2h + draws_h2h, 1)
    difference = strength(home) - strength(away) + 0.18
    difference += ((home_h2h - away_h2h) / h2h_total) * 0.3

    draw_probability = 0.29 - min(abs(difference) * 0.055, 0.11)
    decisive_probability = 1 - draw_probability
    home_share = 1 / (1 + math.exp(-difference * 1.35))
    home_probability = decisive_probability * home_share
    away_probability = decisive_probability - home_probability

    probabilities = [home_probability * 100, draw_probability * 100, away_probability * 100]
    rounded = [round(value, 1) for value in probabilities]
    rounded[1] = round(100 - rounded[0] - rounded[2], 1)

    home_goals = max(home.goals_for / max(home.matches_played, 1), 0.4)
    away_goals = max(away.goals_for / max(away.matches_played, 1), 0.4)
    predicted_home = min(round((home_goals * 0.65) + 0.55 + max(difference, 0) * 0.25), 4)
    predicted_away = min(round((away_goals * 0.62) + 0.25 + max(-difference, 0) * 0.25), 4)

    leader = max(rounded)
    confidence = "alta" if leader >= 60 else "media" if leader >= 48 else "baja"
    explanation = [
        f"{home.team_name}: {home.wins} victorias y diferencia de {home.goals_for - home.goals_against} goles.",
        f"{away.team_name}: {away.wins} victorias y diferencia de {away.goals_for - away.goals_against} goles.",
        f"Historial analizado: {home_h2h + away_h2h + draws_h2h} enfrentamientos.",
    ]

    return PredictionResponse(
        home_team=home.team_name,
        away_team=away.team_name,

        home_win_probability=rounded[0],
        draw_probability=rounded[1],
        away_win_probability=rounded[2],
        predicted_score=f"{predicted_home}-{predicted_away}",
        confidence=confidence,
        explanation=explanation,
        data_source="API-Football"
    )
