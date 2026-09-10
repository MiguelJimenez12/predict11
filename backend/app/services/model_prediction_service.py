from functools import lru_cache
from pathlib import Path

from app.config.leagues import get_league
from app.ml.historical_model import load_artifact, predict_artifact
from app.schemas.model_prediction import ModelMetrics, ModelPredictionResponse
from app.services.football_data_service import get_match

MODEL_DIR = Path(__file__).resolve().parents[3] / "ml_models"


@lru_cache(maxsize=8)
def _artifact(slug: str):
    get_league(slug)
    path = MODEL_DIR / f"{slug}.json"
    if not path.exists():
        raise ValueError(f"No hay un modelo entrenado para {slug}.")
    return load_artifact(path)


def predict(slug: str, home_team: str, away_team: str) -> ModelPredictionResponse:
    if home_team == away_team:
        raise ValueError("Selecciona equipos diferentes.")
    artifact = _artifact(slug)
    result = predict_artifact(artifact, home_team, away_team)
    best = max(result["home_win"], result["draw"], result["away_win"])
    return ModelPredictionResponse(
        league=slug,
        **result,
        confidence="alta" if best >= 0.60 else "media" if best >= 0.48 else "baja",
        model_version=artifact["version"],
    )


def metrics(slug: str) -> ModelMetrics:
    artifact = _artifact(slug)
    values = artifact["metrics"]
    return ModelMetrics(
        league=slug,
        algorithm=artifact["algorithm"],
        training_matches=artifact["training_matches"],
        test_matches=values["matches"],
        accuracy=values["accuracy"],
        log_loss=values["log_loss"],
        brier_score=values["brier_score"],
        precision=values["precision"],
        recall=values["recall"],
        confusion_matrix=values["confusion_matrix"],
    )


def predict_match_id(slug: str, match_id: int) -> ModelPredictionResponse:
    match = get_match(match_id)
    return predict(slug, match["homeTeam"]["name"], match["awayTeam"]["name"])
