from fastapi import APIRouter, HTTPException

from app.schemas.prediction import (
    PredictionRequest,
    PredictionResponse
)

from app.services.prediction_service import predict_match

router = APIRouter()


@router.post(
    "/",
    response_model=PredictionResponse
)
def predict(request: PredictionRequest):
    try:
        return predict_match(request.home_team, request.away_team)
    except ValueError as error:
        raise HTTPException(status_code=400, detail=str(error)) from error
