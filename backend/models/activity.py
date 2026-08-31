from datetime import datetime, timezone

from sqlalchemy import Boolean, Column, DateTime, Float, Integer, String

from database.connection import Base


def _utc_now():
    return datetime.now(timezone.utc).replace(tzinfo=None)


class Activity(Base):
    __tablename__ = "activities"

    id = Column(Integer, primary_key=True)
    title = Column(String)
    url = Column(String)
    domain = Column(String)
    started_at = Column(DateTime)
    ended_at = Column(DateTime)
    duration = Column(Float)
    category = Column(String, default="unknown")
    subject = Column(String, nullable=True)
    topic = Column(String, nullable=True)
    confidence = Column(Float, default=0.0)
    classification_source = Column(String, default="none")
    needs_review = Column(Boolean, default=True)
    created_at = Column(DateTime, default=_utc_now)
    updated_at = Column(DateTime, default=_utc_now, onupdate=_utc_now)