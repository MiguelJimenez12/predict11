from fastapi import FastAPI

from app.routers.teams import router as teams_router
from app.routers.matches import router as matches_router
from app.routers.standings import router as standings_router
<<<<<<< HEAD
from app.routers.head_to_head import router as head_to_head_router
=======
from app.routers.statistics import router as statistics_router
>>>>>>> feature/statistics-endpoint

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
<<<<<<< HEAD
    head_to_head_router,
    prefix="/head-to-head",
    tags=["Head To Head"]
=======
    statistics_router,
    prefix="/statistics",
    tags=["Statistics"]
>>>>>>> feature/statistics-endpoint
)