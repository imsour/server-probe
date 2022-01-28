from datetime import datetime, timedelta
from typing import List, Any

from data import schemas, models
from data.consts import ProbeStatus
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

from .validation import is_valid_url


def server_id_exists(db: Session, server_id: int) -> bool:
    return db.query(models.Server).filter(models.Server.id == server_id).all()


def server_url_exists(db: Session, server_url: str) -> bool:
    return db.query(models.Server).filter(models.Server.url == server_url).all()


def create_server(db: Session, server: schemas.ServerCreate):
    if not is_valid_url(server.url):
        return JSONResponse(status_code=422, content={"message": f"Server has an invalid URL!"})
    elif not server_url_exists(db, server.url):
        db_entry = models.Server(**server.dict())
        db.add(db_entry)
        db.commit()
        db.refresh(db_entry)
        return db_entry
    else:
        return JSONResponse(status_code=409, content={"message": f"Server {server.url} already exists!"})


def get_servers(db: Session, skip: int = 0, limit: int = 20) -> List[models.Server]:
    return db.query(models.Server).offset(skip).limit(limit).all()


def get_servers_latest_entries(db: Session, entry_count: int = 20) -> list[dict[str, Any]]:
    ret = []
    time_ago = datetime.now() - timedelta(seconds=2)  # Max entry date is 1 second ago.
    for server in get_active_probe_servers(db):
        entries = server.entries.order_by(models.Entry.date.desc()).filter(models.Entry.date < time_ago).limit(
            entry_count)[::-1]

        ret.append({'name': server.url,
                    'data': [{'x': entry.date, 'y': entry.response_time}
                             for entry in entries]})

    return ret


def get_active_probe_servers(db: Session) -> List[models.Server]:
    return db.query(models.Server).filter(models.Server.probe_status == ProbeStatus.ENABLED).all()


def set_server_probe_status(db: Session, server_id: int, status: ProbeStatus):
    server_object: models.Server = db.query(models.Server).filter(models.Server.id == server_id).first()
    server_object.probe_status = status
    db.commit()


def get_general_probe_status(db: Session) -> bool:
    return db.query(models.Server).first().probe_status == ProbeStatus.ENABLED
