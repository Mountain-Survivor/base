from fastapi import APIRouter
from pydantic import BaseModel
import redis

r = redis.Redis(
    host = "127.0.0.1",
    port = "6379",
    decode_responses = True
)

router = APIRouter()

class JobRequest(BaseModel):
    value: int

@router.post("/jobs")
def create_job(request: JobRequest):
    r.lpush("tasks", request.value)
    return {"message": "작업 접수", "value": request.value}

@router.get("/jobs/result")
def get_job_result():
    result = r.get("prediction_result")

    return{
        "prediction": result
    }