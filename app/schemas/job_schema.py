from pydantic import BaseModel
from datetime import datetime


class JobCreate(BaseModel):
    pass


class JobResponse(BaseModel):

    id: int
    status: str
    created_at: datetime

    class Config:
        from_attributes = True