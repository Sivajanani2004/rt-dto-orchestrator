from sqlalchemy.orm import Session
from app.models.job import Job
from app.models.task import Task
from app.workers.tasks import validation_task

def create_job(db: Session):

    job = Job(status="SCHEDULED")
    db.add(job)
    db.commit()
    db.refresh(job)
    task_names = [
        "Validation",
        "Ledger Update",
        "Notification"]

    for name in task_names:
        task = Task(
            job_id=job.id,
            task_name=name,
            status="SCHEDULED")
        db.add(task)
    db.commit()
    validation_task.delay(job.id)
    return job


def get_job_details(job_id: int, db: Session):

    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        return None
    tasks = db.query(Task).filter(Task.job_id == job_id).all()

    return {
        "job_id": job.id,
        "job_status": job.status,
        "tasks": [
            {
                "task_id": task.id,
                "task_name": task.task_name,
                "status": task.status,
                "retry_count": task.retry_count
            }
            for task in tasks
                 ]
            }
