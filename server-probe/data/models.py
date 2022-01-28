from sqlalchemy import Column, ForeignKey, Integer, String, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy_utils.types.choice import ChoiceType
from .consts import ProbeStatus
from utils.database import Base


class Server(Base):
    __tablename__ = "servers"

    id = Column(Integer, primary_key=True, index=True)
    url = Column(String, unique=True, index=True)
    probe_status = Column(ChoiceType(ProbeStatus, impl=Integer()), nullable=False, default=ProbeStatus.DISABLED)

    entries = relationship("Entry", back_populates="server", lazy='dynamic')


class Entry(Base):
    __tablename__ = "entries"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, index=True)
    response_time = Column(Integer, index=True)
    server_id = Column(Integer, ForeignKey("servers.id"))

    server = relationship("Server", back_populates="entries")
