from urllib.parse import urlparse

from fastapi import HTTPException
from sqlalchemy.orm import Session

from models.activity import Activity
from schemas.activity import ActivityCreate
from services import classification_service


def extract_domain(url: str) -> str:
    parsed = urlparse(url)
    if parsed.netloc:
        return parsed.netloc
    return parsed.scheme or "unknown"


def create_activity(db: Session, payload: ActivityCreate) -> Activity:
    domain = extract_domain(payload.url)
    result = classification_service.classify(db, payload.title, payload.url, domain)
    activity = Activity(
        title=payload.title.strip(),
        url=payload.url,
        domain=domain,
        started_at=payload.started_at,
        ended_at=payload.ended_at,
        duration=classification_service.recompute_duration(
            payload.started_at, payload.ended_at
        ),
        **result,
    )
    db.add(activity)
    db.commit()
    db.refresh(activity)
    return activity


def list_activities(db: Session) -> list[Activity]:
    return db.query(Activity).order_by(Activity.started_at.desc()).all()


def list_review(db: Session) -> list[Activity]:
    return (
        db.query(Activity)
        .filter(Activity.needs_review.is_(True))
        .order_by(Activity.started_at.desc())
        .all()
    )


def update_category(
    db: Session,
    activity_id: int,
    category: str,
    subject: str | None = None,
    topic: str | None = None,
) -> Activity:
    if category not in classification_service.CATEGORIES:
        raise HTTPException(status_code=422, detail=f"Invalid category: {category}")

    activity = db.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    activity.category = category
    if subject is not None:
        activity.subject = subject
    if topic is not None:
        activity.topic = topic
    activity.confidence = 1.0
    activity.classification_source = "user"
    activity.needs_review = False
    db.commit()
    db.refresh(activity)
    return activity



def delete_activity(db: Session, activity_id: int) -> None:
    activity = db.get(Activity, activity_id)
    if activity is None:
        raise HTTPException(status_code=404, detail="Activity not found")

    db.delete(activity)
    db.commit()