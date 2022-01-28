from datetime import datetime

from celery import Celery
from celery.utils.log import get_task_logger
from requests import get
from sqlalchemy.orm import Session

from config import settings
from data import models
from utils.database import SessionLocal

celery = Celery("tasks", broker=settings.RABBITMQ_URL)
logger = get_task_logger(__name__)


# Pings the server and measures the response time.
# Then, stores an entry with the relevant data.
@celery.task
def probe_server(server_id, server_url, init_time: str):
    db: Session = SessionLocal()

    start_time = datetime.now()
    try:
        get(url="http://" + server_url, headers={'Cache-Control': 'no-cache'})
        elapsed = (datetime.now() - start_time).microseconds / 1000
    except Exception:
        logger.warning(f"couldn't ping {server_url}.")
        elapsed = -1

    celery_log = get_task_logger(__name__)
    celery_log.info(f"{server_url} - took {elapsed} ms")

    print(datetime.now())
    new_entry = models.Entry(date=datetime.strptime(init_time, "%Y-%m-%dT%H:%M:%S.%f"),
                             response_time=elapsed,
                             server_id=server_id)
    db.add(new_entry)
    db.commit()
    db.refresh(new_entry)
