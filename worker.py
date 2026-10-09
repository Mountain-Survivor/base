import redis
from model import predict_model

r = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True
)

print("Worker 시작!")

while True:
    print("작업 기다리는 중...")

    task = r.brpop("tasks", timeout=5)

    if task:
        print("작업 받음:", task[1])
        result = predict_model(int(task[1]))
        print("예측 결과:", result)
        r.set("prediction_result", result)
