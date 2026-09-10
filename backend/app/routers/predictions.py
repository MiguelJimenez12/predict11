from fastapi import APIRouter, HTTPException

from app.schemas.model_prediction import ModelMetrics, ModelPredictionRequest, ModelPredictionResponse
from app.services.model_prediction_service import metrics, predict, predict_match_id

router = APIRouter()


@router.post("/", response_model=ModelPredictionResponse)
def create_prediction(request: ModelPredictionRequest):
    try:
        return predict(request.league, request.home_team, request.away_team)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error


@router.get("/models/{league}/metrics", response_model=ModelMetrics)
def read_model_metrics(league: str):
    try:
        return metrics(league)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/{league}/{match_id}", response_model=ModelPredictionResponse)
def read_match_prediction(league: str, match_id: int):
    try:
        return predict_match_id(league, match_id)
    except (ValueError, RuntimeError) as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
