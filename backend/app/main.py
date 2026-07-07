from fastapi import FastAPI

app = FastAPI(
    title="Predict11 API",
    version="0.1.0"
)

@app.get("/")
def root():
    return {
        "message": "Welcome to Predict11 API!"
    }