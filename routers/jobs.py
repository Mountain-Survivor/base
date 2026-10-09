from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

class JobRequest(BaseModel):
    value: int

@router.post("/jobs")
def create_job(request: JobRequest):
    return {"message": "작업 접수", "value": request.value}