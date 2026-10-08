from fastapi import FastAPI
from pydantic import BaseModel
from fastapi import HTTPException
from routers.health import router as health_router
from routers.predict import router as predict_router

models = ["bert", "resnet"]

app = FastAPI()

class PredictRequest(BaseModel):
    value: int

app.include_router(health_router)

@app.get("/models/{model_name}")
def get_model(model_name: str, version: int = 1):
    if model_name not in models:
        raise HTTPException(
            status_code=404,
            detail="Model not found"
        )

    return {
        "model": model_name,
        "version": version
    }

app.include_router(predict_router)
