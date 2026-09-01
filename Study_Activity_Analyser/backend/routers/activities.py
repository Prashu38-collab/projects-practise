from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.activity import ActivityCreate, ActivityResponse, ClassificationUpdate
from services import activity_service


router = APIRouter(tags=["Activities"])


@router.post("/activities", response_model=ActivityResponse, status_code=status.HTTP_201_CREATED)
def create_activity(payload: ActivityCreate, db: Session = Depends(get_db)):
    return activity_service.create_activity(db, payload)


@router.get("/activities", response_model=list[ActivityResponse])
def list_activities(db: Session = Depends(get_db)):
    return activity_service.list_activities(db)


@router.get("/activities/review", response_model=list[ActivityResponse])
def list_review(db: Session = Depends(get_db)):
    return activity_service.list_review(db)


@router.patch("/activities/{activity_id}/classification", response_model=ActivityResponse)
@router.patch("/activities/{activity_id}/category", response_model=ActivityResponse)
def classify_activity(activity_id: int, payload: ClassificationUpdate, db: Session = Depends(get_db)):
    return activity_service.update_category(
        db,
        activity_id,
        category=payload.category,
        subject=payload.subject,
        topic=payload.topic,
    )



@router.delete("/activities/{activity_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_activity(activity_id: int, db: Session = Depends(get_db)):
    activity_service.delete_activity(db, activity_id)