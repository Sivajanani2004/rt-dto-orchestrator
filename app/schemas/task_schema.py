from pydantic import BaseModel
from datetime import datetime


class TaskResponse(BaseModel):

    id: int
    job_id: int
    task_name: str
    status: str
    retry_count: int
    error_message: str | None = None
    created_at: datetime

    class Config:
        from_attributes = True