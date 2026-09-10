from pydantic import BaseModel


class League(BaseModel):
    slug: str
    name: str
    country: str
    provider: str
    prediction_model: str


class LeagueTeam(BaseModel):
    id: int
    name: str
    short_name: str | None = None
    crest: str | None = None


class LeagueMatch(BaseModel):
    id: int
    utc_date: str
    status: str
    matchday: int | None = None
    home_team: LeagueTeam
    away_team: LeagueTeam
    home_score: int | None = None
    away_score: int | None = None


class LeagueStanding(BaseModel):
    position: int
    team: LeagueTeam
    played_games: int
    won: int
    draw: int
    lost: int
    points: int
    goals_for: int
    goals_against: int
    goal_difference: int
