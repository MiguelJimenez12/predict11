from fastapi import FastAPI
from app.routers.teams import router as teams_router
from app.routers.matches import router as matches_router

app = FastAPI(
    title="Predict11 API",
    version="0.1.0"
)
app.include_router(teams_router)
app.include_router(matches_router)

@app.get("/")
def root():
    return {
        "message": "Welcome to Predict11 API!"
    }