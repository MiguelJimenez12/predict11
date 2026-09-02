from pydantic import BaseModel


class HeadToHead(BaseModel):
    fixture_id: int

    home_team: str
    away_team: str

    home_goals: int
    away_goals: int

    date: str