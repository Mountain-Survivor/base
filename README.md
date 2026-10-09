# MLOps 학습 기록 — Week 1~7

> Anyone AI Sprint 03 학습 내용을 바탕으로 진행한 **개인 실습 기록**입니다.  
> **현재 상태:** Week 1~7 완료 처리(7/8주, 87.5%), Week 8 통합 실습 예정.

## 1. 프로젝트 개요

FastAPI로 예측 요청을 받고, Redis 큐에 작업을 넣은 뒤, 별도 Worker가 모델을 실행하여 결과를 Redis에 저장하는 MLOps 기초 흐름을 학습했습니다.

> **구분:** 제공된 `Sprint03-Project.zip`은 별도의 Sprint 03 참고/과제 프로젝트입니다. 이 README의 `main.py`, `routers/jobs.py`, `worker.py` 등은 대화 중 `/workspaces/base`에서 진행한 **학습용 실습 코드**를 설명합니다. 두 프로젝트의 디렉터리 구조가 같다고 가정하지 않습니다.

## 2. 주차별 학습 현황

| 주차 | 주제 | 진행 상태 | 학습 내용 |
|---|---|---|---|
| Week 1 | MLOps 기초 | 완료 처리 | 개발과 운영, 배포 흐름 이해 |
| Week 2 | FastAPI | 완료 처리 | API와 라우터, 예측 엔드포인트 |
| Week 3 | Docker | 완료 처리 | 이미지와 컨테이너, Dockerfile |
| Week 4 | Docker Compose | 완료 처리 | 여러 서비스의 실행 및 구성 |
| Week 5 | API + 모델 연동 | 완료 처리 | `POST /predict`에서 모델 호출 |
| Week 6 | PostgreSQL | 사용자 요청에 따라 완료 처리 | 예측 기록 저장 코드 작성. **컨테이너 간 DB 연결 문제 미해결** |
| Week 7 | Redis + Worker | **완료** | 작업 큐, Worker, 결과 저장 및 조회 테스트 성공 |
| Week 8 | 전체 시스템 통합 | 예정 | API, DB, Redis, Worker 통합 및 장애 점검 |

**진도 계산:** 7/8주 = **87.5%**. 학습 일정상의 완료율이며, 프로덕션 배포 준비율은 아닙니다.

## 3. 사용 기술

- Python 3.14 / 가상환경 `.venv`
- FastAPI, Uvicorn, Pydantic
- Docker, Docker Compose
- PostgreSQL, `psycopg`
- Redis, Python `redis` 패키지
- GitHub Codespaces

## 4. 실습 프로젝트 주요 파일

```text
/workspaces/base/
├── main.py               # FastAPI 앱 및 라우터 등록
├── model.py              # 간단한 예측 함수 (입력값 × 2)
├── database.py           # PostgreSQL 예측 로그 저장
├── worker.py             # Redis 큐에서 작업 수신, 예측, 결과 저장
├── routers/
│   ├── health.py
│   ├── predict.py        # POST /predict
│   ├── models.py
│   └── jobs.py           # POST /jobs, GET /jobs/result
├── Dockerfile
└── docker-compose.yml
```

> 위 구조는 학습 중 확인한 파일 중심의 요약이며, 전체 파일 목록을 보증하지 않습니다.

## 5. 시스템 흐름

```text
클라이언트
   │
   │ POST /jobs {"value": 10}
   ▼
FastAPI (로컬 테스트: 8001)
   │
   │ LPUSH tasks 10
   ▼
Redis 작업 큐 (tasks)
   │
   │ BRPOP tasks
   ▼
Worker (worker.py)
   │
   │ predict_model(10)
   ▼
예측 결과 20
   │
   │ SET prediction_result 20
   ▼
Redis 결과 저장
   ▲
   │ GET prediction_result
FastAPI GET /jobs/result
   │
   ▼
{"prediction": "20"}
```

### 핵심 개념

- **FastAPI:** 작업 요청을 받는 창구
- **Redis 큐:** 처리 대기 중인 작업 목록
- **Worker:** 대기열에서 작업을 꺼내 처리하는 별도 프로세스
- **모델:** 현재 실습에서는 입력 정수에 2를 곱하는 예시 함수
- **결과 저장:** Redis의 `prediction_result` 키에 마지막 결과 저장

## 6. 핵심 코드 예시

### `model.py`

```python
def predict_model(value: int) -> int:
    return value * 2
```

### `main.py`

```python
from fastapi import FastAPI
from routers import health, predict, models, jobs

app = FastAPI()
app.include_router(health.router)
app.include_router(predict.router)
app.include_router(models.router)
app.include_router(jobs.router)
```

### `routers/jobs.py` — 학습 중 완성한 기능을 정리한 예시

```python
import redis
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()

r = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
)

class JobRequest(BaseModel):
    value: int

@router.post("/jobs")
def create_job(request: JobRequest):
    r.lpush("tasks", request.value)
    return {"message": "작업 접수", "value": request.value}

@router.get("/jobs/result")
def get_job_result():
    result = r.get("prediction_result")
    return {"prediction": result}
```

### `worker.py`

```python
import redis
from model import predict_model

r = redis.Redis(
    host="127.0.0.1",
    port=6379,
    decode_responses=True,
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
```

> 예시는 대화에서 확인된 학습 코드를 기반으로 정리했습니다. 실제 Codespaces 파일을 직접 동기화하거나 수정한 것은 아닙니다.

## 7. Week 7 실행 및 테스트 기록

**전제:** Docker Compose의 Redis 서비스 `cache`가 실행 중이고, 학습용 로컬 포트 매핑 `127.0.0.1:6379:6379`이 적용되어 있어야 합니다. Python 가상환경에 `fastapi`, `uvicorn`, `redis` 등이 설치되어 있어야 합니다.

### 1) Redis 상태 확인

```bash
docker compose exec cache redis-cli PING
```

확인한 응답: `PONG`

### 2) FastAPI 실행 (터미널 A)

```bash
uvicorn main:app \
  --host 0.0.0.0 \
  --port 8001
```

### 3) Worker 실행 (터미널 B)

```bash
python worker.py
```

### 4) 작업 등록 (터미널 C)

```bash
curl -i -X POST \
  http://127.0.0.1:8001/jobs \
  -H "Content-Type: application/json" \
  -d '{"value": 10}'
```

실제 확인한 응답:

```text
HTTP/1.1 200 OK
{"message":"작업 접수","value":10}
```

Worker 출력:

```text
작업 받음: 10
예측 결과: 20
```

### 5) Redis 결과 확인

```bash
docker compose exec cache \
  redis-cli GET prediction_result
```

실제 확인한 응답: `"20"`

### 6) 결과 조회 API 확인

```bash
curl -i \
  http://127.0.0.1:8001/jobs/result
```

실제 확인한 응답:

```text
HTTP/1.1 200 OK
{"prediction":"20"}
```

### 7) 작업 큐 확인

```bash
docker compose exec cache \
  redis-cli LLEN tasks
```

실제 확인한 응답: `(integer) 0`

이후 Worker는 `Ctrl+C`로 종료했습니다.

## 8. 주요 문제와 해결 경험

| 문제 | 원인 또는 확인 사항 | 처리 |
|---|---|---|
| Python에서 Redis 접속 거부 | Redis 컨테이너 포트가 Codespaces 호스트에 노출되지 않았음 | `cache` 서비스에 로컬 포트 매핑 추가 후 재생성 |
| `Redis.__init__()` 인자 오류 | `decode_response` 오타 | `decode_responses`로 수정 후 서버 시작 성공 |
| `/jobs` 요청의 초기 404 | 이후 OpenAPI에서 `/jobs` 및 `POST` 등록 확인 | 요청 재시험에서 200 OK 확인. 초기 404의 정확한 원인은 확정하지 않음 |
| Docker API → PostgreSQL 연결 타임아웃 | `db` 이름 해석은 되지만 컨테이너 간 TCP 연결 실패 | **미해결**. Docker 브리지/방화벽 설정이 의심되나 원인 확정 전 |

## 9. 현재 구현의 한계

1. **결과가 한 개만 보관됨:** `prediction_result` 키 하나를 사용하므로 새 작업이 이전 결과를 덮어씁니다.
2. **작업별 상태 조회 없음:** 작업 ID, `queued/running/done/failed` 상태가 없습니다.
3. **실패 처리 없음:** Worker 오류 시 재시도 및 실패 작업 관리가 없습니다.
4. **컨테이너 통합 미검증:** 성공한 Week 7 테스트는 Codespaces 호스트에서 실행한 FastAPI·Worker와 Redis 컨테이너 사이의 연결입니다. Docker 내부 API↔Redis 통신까지 검증한 것은 아닙니다.
5. **PostgreSQL 연결 이슈:** Week 6에서 발생한 컨테이너 간 네트워크 문제를 해결해야 합니다.
6. **학습용 모델:** 실제 학습된 ML 모델 대신 `value * 2`를 사용합니다.

## 10. Week 8 계획

- [ ] 기존 서비스 상태 및 Docker Compose 구성 점검
- [ ] API → PostgreSQL 컨테이너 네트워크 문제 재현 및 원인 확인
- [ ] FastAPI·Redis·Worker·PostgreSQL 통합 실행
- [ ] 작업 등록부터 결과 조회까지 통합 테스트
- [ ] 로그 및 실패 상황 확인
- [ ] 필요 시 작업 ID 및 결과별 저장 구조 개선
- [ ] 전체 시스템 실행·종료 방법 문서화

---

**학습 기록 기준:** 2026-10-09  
**상태:** Week 7 핵심 실습 성공, Week 8 시작 전
