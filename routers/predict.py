from fastapi import APIRouter
from pydantic import BaseModel
from model import predict_model
from database import save_prediction

router = APIRouter()

class PredictRequest(BaseModel):
    value: int

class PredictResponse(BaseModel):
    prediction: int

@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
    result = predict_model(request.value)
    save_prediction(request.value, result)
    return {"prediction": result}