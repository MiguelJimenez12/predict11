from pydantic import BaseModel


class PredictionRequest(BaseModel):
    home_team: int
    away_team: int


class PredictionResponse(BaseModel):
    home_team: str
    away_team: str

    home_win_probability: float
    draw_probability: float
    away_win_probability: float

    predicted_score: str
    confidence: str
    explanation: list[str]
    data_source: str
