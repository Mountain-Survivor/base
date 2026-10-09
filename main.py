from fastapi import FastAPI
from routers import health, predict, models, jobs

app = FastAPI()

app.include_router(health.router)
app.include_router(predict.router)
app.include_router(models.router)
app.include_router(jobs.router)