from pydantic import BaseModel


class ModelPredictionRequest(BaseModel):
    league: str
    home_team: str
    away_team: str


class ModelPredictionResponse(BaseModel):
    league: str
    home_team: str
    away_team: str
    home_win: float
    draw: float
    away_win: float
    confidence: str
    model_version: int


class ModelMetrics(BaseModel):
    league: str
    algorithm: str
    training_matches: int
    test_matches: int
    accuracy: float
    log_loss: float
    brier_score: float
    precision: dict[str, float]
    recall: dict[str, float]
    confusion_matrix: list[list[int]]
