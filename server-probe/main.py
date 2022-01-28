from datetime import datetime, time
import logging
from typing import List

from fastapi import FastAPI, Depends, BackgroundTasks
from fastapi_utils.tasks import repeat_every
from sqlalchemy.orm import Session
from starlette.middleware.cors import CORSMiddleware
from starlette.responses import RedirectResponse

from config import settings
from data import schemas, models
from data.consts import ProbeStatus
from celery_worker import probe_server
from utils import crud
from utils.database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)
app = FastAPI(debug=True)
logger = logging.getLogger(__name__)


# Dependency
def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/server", response_model=schemas.Server)
def add_server(server: schemas.ServerCreate, db: Session = Depends(get_db)):
    return crud.create_server(db, server)


@app.post("/start")
async def start_probe_all_servers(tasks: BackgroundTasks, db: Session = Depends(get_db)):
    for server in crud.get_servers(db):
        crud.set_server_probe_status(db, server.id, ProbeStatus.ENABLED)


@app.post("/stop")
def stop_probe_all_servers(db: Session = Depends(get_db)):
    for server in crud.get_servers(db):
        crud.set_server_probe_status(db, server.id, ProbeStatus.DISABLED)


@app.get("/probe_status")
def get_probe_status(db: Session = Depends(get_db)):
    return {"running": crud.get_general_probe_status(db)}


@app.get("/probe_data")
def get_probe_data(db: Session = Depends(get_db)):
    return crud.get_servers_latest_entries(db)


@app.get('/')
def root():
    return RedirectResponse('/docs')


@app.on_event('startup')
@repeat_every(seconds=settings.PROBE_INTERVAL, logger=logger)
async def probe(db: Session = SessionLocal()):
    for server in crud.get_active_probe_servers(db):
        probe_server.delay(server.id, server.url, datetime.now())


@app.on_event("shutdown")
def shutdown(db: Session = SessionLocal()):
    logger.info("Shutdown - disabling all probes")
    stop_probe_all_servers(db)
