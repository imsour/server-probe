from datetime import datetime
from typing import List

from pydantic import BaseModel

from data.consts import ProbeStatus


class BaseEntry(BaseModel):
    date: datetime
    response_time: int
    server_id: int


class EntryCreate(BaseEntry):
    pass


class Entry(BaseEntry):
    id: int

    class Config:
        orm_mode = True


class ServerBase(BaseModel):
    url: str


class ServerCreate(ServerBase):
    pass


class Server(ServerBase):
    id: int
    probe_status: ProbeStatus

    class Config:
        orm_mode = True
