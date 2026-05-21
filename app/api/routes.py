from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.db.session import get_db
from app.services.job_services import create_job
from app.services.job_services import (create_job,get_job_details)


router = APIRouter()

@router.post("/jobs")
def create_new_job(db: Session = Depends(get_db)):
    job = create_job(db)
    return {
        "message": "Job Created Successfully",
        "job_id": job.id
        }


@router.get("/jobs/{job_id}")
def get_job(job_id: int, db: Session = Depends(get_db)):
    job = get_job_details(job_id, db)
    if not job:
        return {"message": "Job not found"}
    return job