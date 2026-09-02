from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routers.teams import router as teams_router
from app.routers.matches import router as matches_router
from app.routers.standings import router as standings_router
from app.routers.statistics import router as statistics_router
from app.routers.head_to_head import router as head_to_head_router
from app.routers.prediction import router as prediction_router

app = FastAPI(
    title="Predict11 API",
    description="API de analisis y predicciones de partidos de Liga MX.",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_origin_regex=r"http://(localhost|127\.0\.0\.1):\d+",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    return {
        "name": "Predict11 API",
        "status": "ok",
        "version": "1.0.0"
    }


@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy"}


app.include_router(
    teams_router,
    prefix="/teams",
    tags=["Teams"]
)

app.include_router(
    matches_router,
    prefix="/matches",
    tags=["Matches"]
)

app.include_router(
    standings_router,
    prefix="/standings",
    tags=["Standings"]
)

app.include_router(
    statistics_router,
    prefix="/statistics",
    tags=["Statistics"]
)

app.include_router(
    head_to_head_router,
    prefix="/head-to-head",
    tags=["Head To Head"]
)

app.include_router(
    prediction_router,
    prefix="/predict",
    tags=["Prediction"]
)
