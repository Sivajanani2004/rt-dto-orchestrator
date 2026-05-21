# Architecture Overview

The system uses FastAPI as the dispatcher service.
Redis acts as the distributed task queue.
Celery workers consume tasks asynchronously from Redis.
PostgreSQL stores persistent job and task states.
Tasks execute sequentially:
Validation → Ledger Update → Notification