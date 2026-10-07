from fastapi import APIRouter
from pydantic import BaseModel
from model import predict_model

router = APIRouter()

class PredictRequest(BaseModel):
	value: int

class PredictResponse(BaseModel):
	prediction: int

@router.post("/predict", response_model=PredictResponse)
def predict(request: PredictRequest):
	return = predict_model(request.value)
