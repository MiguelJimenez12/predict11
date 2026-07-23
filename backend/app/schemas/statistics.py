from pydantic import BaseModel


class Statistics(BaseModel):
    team_id: int
    team_name: str
    league: str
    season: int

    matches_played: int
    wins: int
    draws: int
    losses: int

    goals_for: int
    goals_against: int

    clean_sheets: int
    failed_to_score: int