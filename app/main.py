from fastapi import FastAPI
from app.db.database import Base, engine
from app.models.job import Job
from app.models.task import Task
from app.api.routes import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="RT-DTO")
app.include_router(router)

@app.get("/")
def home():
    return {"message": "RT-DTO Running Successfully"}