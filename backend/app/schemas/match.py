from pydantic import BaseModel


class Match(BaseModel):
    id: int

    home_team: str
    away_team: str

    home_logo: str
    away_logo: str

    date: str

    league: str

    status: str

    home_goals: int | None
    away_goals: int | None