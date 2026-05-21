import time
from app.core.celery_app import celery
from app.db.database import SessionLocal
from app.models.task import Task
from app.models.job import Job
from app.utils.logger import logger

@celery.task(time_limit=30)
def validation_task(job_id):

    db = SessionLocal()
    task = db.query(Task).filter(
        Task.job_id == job_id,
        Task.task_name == "Validation"
    ).first()

    try:
        task.status = "RUNNING"
        db.commit()
        logger.info(f"Validation started for Job {job_id}")
        time.sleep(5)
        task.status = "COMPLETED"
        db.commit()
        logger.info("Validation completed")
        ledger_task.delay(job_id)

    except Exception as e:
        task.status = "FAILED"
        task.error_message = str(e)
        db.commit()
        logger.info("Validation timeout failed")

    finally:
        db.close()


@celery.task
def ledger_task(job_id):

    db = SessionLocal()
    task = db.query(Task).filter(
        Task.job_id == job_id,
        Task.task_name == "Ledger Update"
    ).first()
    task.status = "RUNNING"
    db.commit()
    logger.info(f"Ledger Update started for Job {job_id}")
    time.sleep(5)
    task.status = "COMPLETED"
    db.commit()
    logger.info("Ledger Update completed")
    notification_task.delay(job_id)
    db.close()


@celery.task(bind=True, max_retries=3)
def notification_task(self, job_id):

    db = SessionLocal()
    task = db.query(Task).filter(
        Task.job_id == job_id,
        Task.task_name == "Notification"
    ).first()

    try:
        task.status = "RUNNING"
        db.commit()
        logger.info(f"Notification started for Job {job_id}")
        time.sleep(5)
        # Simulated failure
        raise Exception("Notification API Failed")
    
    except Exception as e:
        task.retry_count += 1
        task.error_message = str(e)
        db.commit()
        logger.info(f"Retry Attempt: {task.retry_count}")
        if task.retry_count >= 3:
            task.status = "FAILED"
            job = db.query(Job).filter(Job.id == job_id).first()
            job.status = "FAILED"
            db.commit()
            logger.info("Moved to DLQ")
            
        else:
            raise self.retry(exc=e, countdown=5)

    finally:
        db.close()