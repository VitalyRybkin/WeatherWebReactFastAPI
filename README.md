
# 🚀 FastAPI Microservice Template

A production-ready FastAPI weather microservice template featuring:

* ✅ FastAPI with Pydantic for validation
* 🐘 PostgreSQL + SQLAlchemy ORM
* 🔄 Alembic migrations
* 🧪 Locust for load testing
* 📊 Prometheus + Grafana + Loki for monitoring and observability
* 🧠 Redis for caching and task queuing
* 📦 Docker for containerization
* 🔐 FastAPI Limiter for rate limiting
* 🧵 Celery with retry logic for background tasks
* 📘 Structured logging
* 📚 Poetry for dependency management and packaging

---

## 📁 Project Structure

```
.
├── app/
│   └── api_v1/             # FastAPI main routes
│       └── views/
│   ├── celery_tasks/       # Celery configuration, start and tasks
│   ├── logger/             # Logger configuration and handker
│   ├── logs/               # Logging directory
│   ├── models/             # Database models
│   ├── schemas/            # Pydentic schemas
│   ├── users/              # Users routes
│   ├── utils/              # User authentication, settings, exeption handlers, API limiter, retry logic, database connection
│   ├── main.py             # FastAPI entrypoint
│   ├── README.md
│   └── .env 
├── alembic/                # DB migrations
├── alembic.ini             # ALembic configuration
├── compose.locust.yaml     # Services orchestration for load testing
├── docker-compose.yml      # Services orchestration
├── Dockerfile              # App Dockerfile
├── poetry.lock             # Project depencies
├── pyproject.toml          # Project metadata
└── README.md
```

---

## ⚙️ Tech Stack

| Tool                | Purpose                       |
| ------------------- |-------------------------------|
| **FastAPI**         | Web framework                 |
| **Pydantic**        | Data validation and settings  |
| **PostgreSQL**      | Relational database           |
| **SQLAlchemy**      | ORM for PostgreSQL            |
| **Alembic**         | Database migrations           |
| **Celery**          | Background task processing    |
| **Redis**           | Broker for Celery and caching |
| **Locust**          | Load testing                  |
| **Prometheus**      | Metrics scraping              |
| **Grafana**         | Metrics dashboards            |
| **Loki**            | Log aggregation               |
| **Docker**          | Containerization              |
| **FastAPI Limiter** | IP-based rate limiting        |

---

## 🛠️ Setup & Development

### 1. Clone the Repository

```bash
git clone https://github.com/VitalyRybkin/WeatherWebReactFastAPI.git
cd WeatherWebReactFastAPI
```

### 2. Environment Configuration

Create a `.env` file:

```env
DB_NAME=
DB_USERNAME=
DB_PASSWORD=
DB_HOST=
API_TOKEN=
```
### 5. Install Poetry & Dependencies
Set localhost or docker host option for:

* Redis - app/main/__init__.py
```aiignore
redis_client: Redis = redis.Redis(host=settings.REDIS_LOCALHOST)
```
* Redis - app/main.py
```aiignore
redis_connection = redis.from_url(
        settings.REDIS_LOCAL_CONN, encoding="utf-8", decode_responses=True
    )
```
* Celery - app/celery_tasks/run_celery.py
```aiignore
broker=settings.REDIS_LOCAL_CONN,
backend=settings.REDIS_LOCAL_CONN,
```

### 4. Install Poetry & Dependencies

```bash
curl -sSL https://install.python-poetry.org | python3 -
poetry install
```

### 5. Start with Docker

```bash
docker compose build
docker compose --env-file .env up
```

---
## 📦 Dependency Management
To add a new package:
```bash
poetry add fastapi
poetry add --dev black
```
To export for other formats:
```bash
poetry export --format requirements.txt --output requirements.txt
```
---
## 🔄 Database Migrations (Alembic)

```bash
# Generate migration
alembic revision --autogenerate -m "Add user table"

# Apply migration
alembic upgrade head
```

---

## 🧵 Background Tasks (Celery)

Run the Celery worker for local running:

```bash
cd app/
celery -A celery_tasks.run_celery worker -E --loglevel INFO
```

---

## 🚦 Rate Limiting (FastAPI Limiter)

Example usage:

```python
@location_router.get(
    "/name/{location_name}/",
    summary="Get location / list of locations by name.",
    dependencies=[
        Depends(
            RateLimiter(
                times=settings.limiter.REQUEST_LIMIT,
                seconds=settings.limiter.DURATION_LIMIT_SEC,
            )
        )
    ],
    response_model=List[LocationPublic],
)
def get_location_by_name(location_name: str) -> list[LocationPublic] | None:
    locations_found: List[LocationPublic] = get_locations(location_name)
    return locations_found
```

---

## 📈 Monitoring

Prometheus scrapes `/metrics`. Grafana visualizes Prometheus + Loki logs.


* Grafana: `http://localhost:3000`
* Prometheus: `http://localhost:9090`
* Loki: `http://localhost:3100`

---

## 📊 Load Testing with Locust

```bash
LOCUSTFILE={file_name} docker compose -f compose.locust.yaml up --build 
```

Open: `http://localhost:8089`

---

## 📦 Logging

Structured logging with timestamps, level, and source:

```python

import logging.config

def get_logger(name) -> logging.Logger:
    """
    Function. Creates a logger instance.
    :return: logger instance
    """
    logger = logging.getLogger(name)
    """ logic """
    return logger
```

Logs are streamed to Loki for centralized access.

---

## 🧪 Example API Call

```bash
curl http://localhost:8000/
curl -X 'GET' 'http://127.0.0.1:8000/app/api_v1/name/NY/' -H 'accept: application/json'
```

---

## 📚 Useful Commands

| Action                      | Command                                                                   |
|-----------------------------|---------------------------------------------------------------------------|
| Run migrations              | `alembic upgrade head`                                                    |
| Create new migration        | `alembic revision --autogenerate -m ""`                                   |
| Start Celery worker locally | `celery -A celery_tasks.run_celery worker -E --loglevel INFO`             |
| Run app locally (no Docker) | `uvicorn app.main:app --host 0.0.0.0 --port 8000`                         |
| Run app in Docker           | `docker compose --env-file .env up`                                       |
| Run app load test in Docker | `LOCUSTFILE={file_name} docker compose -f compose.locust.yaml up --build` |

---

## 🧼 Lint & Format

```bash
black .
pylint .
```

---

## ✅ Todo / Extensible Features

* ✅ User registration Email notification
* ✅ Email confirmation
* ⏳ CI/CD Actions

---
