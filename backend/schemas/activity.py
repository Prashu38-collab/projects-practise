from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ActivityCreate(BaseModel):
    title: str
    url: str
    started_at: datetime
    ended_at: datetime


class ActivityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    title: str
    url: str
    domain: str
    started_at: datetime
    ended_at: datetime
    duration: float
    category: str
    subject: str | None = None
    topic: str | None = None
    confidence: float
    classification_source: str
    needs_review: bool
    created_at: datetime


class ClassificationUpdate(BaseModel):
    category: str
    subject: str | None = None
    topic: str | None = None


# Backwards compatibility alias
CategoryUpdate = ClassificationUpdate