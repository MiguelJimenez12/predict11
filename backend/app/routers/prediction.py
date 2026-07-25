from fastapi import APIRouter

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

    return predict_match(
        request.home_team,
        request.away_team
    )