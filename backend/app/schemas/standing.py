from pydantic import BaseModel


class Standing(BaseModel):
    position: int
    team_id: int
    team_name: str
    team_logo: str
    played: int
    win: int
    draw: int
    lose: int
    goals_for: int
    goals_against: int
    goal_difference: int
    points: int