from celery import Celery
import sys
sys.path.insert(0, '/app/app')
from config import settings
from database import SessionLocal
from services.aggregation import update_device_aggregates

celery_app = Celery(
    "device_stats",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)

@celery_app.task(name="update_aggregates")
def update_aggregates_task(device_id: int):
    db = SessionLocal()
    try:
        update_device_aggregates(db, device_id)
    finally:
        db.close()
