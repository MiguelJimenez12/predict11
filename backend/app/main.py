from fastapi import FastAPI

from app.routers.teams import router as teams_router
from app.routers.matches import router as matches_router
from app.routers.standings import router as standings_router
from app.routers.statistics import router as statistics_router
from app.routers.head_to_head import router as head_to_head_router

app = FastAPI(
    title="Predict11 API",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "message": "Welcome to Predict11 API!"
    }


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