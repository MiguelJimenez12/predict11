from pydantic import BaseModel


class Match(BaseModel):
    id: int
    home_team_id: int
    away_team_id: int
    date: str
    competition: str
    round: int
    stadium: str
    home_score: int | None = None
    away_score: int | None = None
    status: str