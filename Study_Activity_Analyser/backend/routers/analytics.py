from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database.connection import get_db
from schemas.analytics import CategoryTotal, DailyBreakdown, TodaySummary, WebsiteTotal
from services import analytics_service

router = APIRouter(tags=["Analytics"])



@router.get("/analytics/today", response_model=TodaySummary)
def today(db: Session = Depends(get_db)):
    return analytics_service.today_summary(db)


@router.get("/analytics/categories", response_model=list[CategoryTotal])
def categories(db: Session = Depends(get_db)):
    return analytics_service.category_totals(db)


@router.get("/analytics/websites", response_model=list[WebsiteTotal])
def websites(limit: int = 10, db: Session = Depends(get_db)):
    return analytics_service.top_websites(db, limit)


@router.get("/analytics/daily", response_model=list[DailyBreakdown])
def daily(days: int = 7, db: Session = Depends(get_db)):
    return analytics_service.daily_breakdown(db, days)