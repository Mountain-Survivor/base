FROM python:3.14-slim

WORKDIR /app

RUN pip install fastapi uvicorn

COPY main.py .
COPY routers/ ./routers/

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
