# Real-Time Distributed Task Orchestrator (RT-DTO)

## Overview

This project is a high-performance backend orchestration engine built using FastAPI, Celery, Redis, and PostgreSQL.

The system processes multi-step financial transaction jobs in a distributed environment. Each job contains sequential tasks:

1. Validation
2. Ledger Update
3. Notification

The orchestrator ensures:
- Sequential task execution
- Persistent task tracking
- Retry handling
- Failure management
- Dead Letter Queue (DLQ) simulation
- Distributed worker processing

---

# Tech Stack

| Technology | Purpose |
|---|---|
| FastAPI | REST API Framework |
| PostgreSQL | Persistent Database |
| Redis | Message Broker / Queue |
| Celery | Distributed Task Workers |
| SQLAlchemy | ORM |
| Docker | Containerization |
| Docker Compose | Multi-container orchestration |

---

# Architecture

```text
Client
   ↓
FastAPI Dispatcher
   ↓
PostgreSQL (Stores Jobs & Tasks)
   ↓
Redis Queue
   ↓
Celery Workers
   ↓
Task Execution
```

---

# Workflow

```text
POST /jobs
     ↓
Create Job
     ↓
Create Tasks
     ↓
Validation Task Starts
     ↓
Ledger Update Starts
     ↓
Notification Starts
     ↓
Retry Logic if Failure
     ↓
Move to DLQ after 3 retries
```

---

# Features

## 1. Distributed Task Orchestration

Tasks are executed sequentially:

```text
Validation → Ledger Update → Notification
```

---

## 2. Retry Logic

If Notification task fails:

```text
Retry 1
Retry 2
Retry 3
```

After 3 failures:

```text
Task marked as FAILED
Moved to DLQ simulation
```

---

## 3. Persistent State Tracking

Each task state is stored in PostgreSQL.

Supported states:

```text
SCHEDULED
RUNNING
COMPLETED
FAILED
```

---

## 4. Failure Handling

Failures are stored permanently in database.

Example:

```text
Notification API Failed
```

---

## 5. Dead Letter Queue (DLQ)

Tasks that fail after maximum retries are marked as failed for manual inspection.

---

# Project Structure

```text
Rt-dto/
│
├── app/
│   ├── core/
│   │   └── celery_app.py
│   │
│   ├── db/
│   │   └── database.py
│   │
│   ├── models/
│   │   ├── job.py
│   │   └── task.py
│   │
│   ├── routes/
│   │   └── endpoint.py
│   │
│   ├── schemas/
│   │   └── schema.py
│   │
│   ├── services/
│   │   └── job_services.py
│   │
│   ├── utils/
│   │   └── logger.py
│   │
│   ├── workers/
│   │   └── tasks.py
│   │
│   └── main.py
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── .env
└── README.md
```

---

# API Endpoints

## Create Job

```http
POST /jobs
```

Creates:
- Job
- Validation Task
- Ledger Task
- Notification Task

---

## Get Job Details

```http
GET /jobs/{job_id}
```

Returns:
- Job status
- Task statuses
- Retry counts
- Error messages

---

# Running Locally

## 1. Clone Repository

```bash
git clone <repo-url>
cd Rt-dto
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

---

## 3. Activate Virtual Environment

### Windows

```bash
.venv\Scripts\activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Start Redis

```bash
docker run -d -p 6379:6379 --name redis redis
```

---

## 6. Start FastAPI Server

```bash
uvicorn app.main:app --reload
```

---

## 7. Start Celery Worker

```bash
python -m celery -A app.core.celery_app worker --pool=solo --loglevel=info
```

---

# Running with Docker Compose

## Build and Start Containers

```bash
docker-compose up --build
```

---

## Run Again Later

```bash
docker-compose up
```

---

## Stop Containers

```bash
docker-compose down
```

---

# Database Schema

## Jobs Table

| Column | Description |
|---|---|
| id | Job ID |
| status | Overall Job Status |

---

## Tasks Table

| Column | Description |
|---|---|
| id | Task ID |
| job_id | Linked Job |
| task_name | Task Type |
| status | Task Status |
| retry_count | Retry Counter |
| error_message | Failure Reason |

---

# Retry & DLQ Strategy

## Notification Task

- Maximum retries: 3
- Retry delay: 5 seconds

After exceeding retry limit:

```text
FAILED
```

and moved to DLQ simulation.

---

# Concurrency Strategy

Celery workers consume tasks asynchronously from Redis queue.

This prevents:
- API blocking
- slow request handling
- task execution bottlenecks

---

# Fault Tolerance

If a worker fails:
- task state remains stored in PostgreSQL
- retry mechanism handles transient failures
- failed tasks remain persisted for inspection

---

# Logging

Structured logging implemented using Python logging module.

Example:

```text
INFO - Validation started for Job 5
INFO - Retry Attempt: 2
INFO - Moved to DLQ
```

---

# Future Improvements

- Kubernetes deployment
- Prometheus & Grafana monitoring
- Worker auto scaling
- Real Dead Letter Queue implementation

---

# Author

Siva Janani R