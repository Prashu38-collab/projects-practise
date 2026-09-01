from collections import defaultdict
from datetime import datetime, time, timedelta, timezone

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.activity import Activity
from services.classification_service import CATEGORIES


def _utc_naive(aware: datetime) -> datetime:
    return aware.astimezone(timezone.utc).replace(tzinfo=None)


def _local_tz():
    return datetime.now().astimezone().tzinfo


def _today_bounds():
    local_now = datetime.now().astimezone()
    start_local = datetime.combine(local_now.date(), time.min, tzinfo=local_now.tzinfo)
    end_local = start_local + timedelta(days=1)
    return _utc_naive(start_local), _utc_naive(end_local)


def _zeroed_categories() -> dict[str, float]:
    return {category: 0.0 for category in CATEGORIES}


def _as_category_totals(by_category: dict[str, float]) -> list[dict]:
    return [
        {"category": category, "seconds": seconds}
        for category, seconds in by_category.items()
    ]


def today_summary(db: Session) -> dict:
    start, end = _today_bounds()
    rows = (
        db.query(Activity.category, func.sum(Activity.duration))
        .filter(Activity.started_at >= start, Activity.started_at < end)
        .group_by(Activity.category)
        .all()
    )

    by_category = _zeroed_categories()
    for category, seconds in rows:
        by_category[category] = float(seconds or 0)

    review_seconds = (
        db.query(func.sum(Activity.duration))
        .filter(
            Activity.started_at >= start,
            Activity.started_at < end,
            Activity.needs_review.is_(True),
        )
        .scalar()
        or 0
    )

    return {
        "date": datetime.now().astimezone().date().isoformat(),
        "total_seconds": round(sum(by_category.values()), 2),
        "review_seconds": round(float(review_seconds), 2),
        "by_category": _as_category_totals(by_category),
    }


def category_totals(db: Session) -> list[dict]:
    rows = (
        db.query(Activity.category, func.sum(Activity.duration))
        .group_by(Activity.category)
        .all()
    )
    by_category = _zeroed_categories()
    for category, seconds in rows:
        by_category[category] = float(seconds or 0)
    return _as_category_totals(by_category)


def top_websites(db: Session, limit: int = 10) -> list[dict]:
    duration_sum = func.sum(Activity.duration).label("total")
    rows = (
        db.query(Activity.domain, duration_sum)
        .group_by(Activity.domain)
        .order_by(duration_sum.desc())
        .limit(limit)
        .all()
    )
    return [
        {"domain": domain, "seconds": round(float(seconds or 0), 2)}
        for domain, seconds in rows
    ]


def daily_breakdown(db: Session, days: int = 7) -> list[dict]:
    local_tz = _local_tz()
    local_start = datetime.now().astimezone() - timedelta(days=days - 1)
    start_utc = _utc_naive(datetime.combine(local_start.date(), time.min, tzinfo=local_start.tzinfo))

    rows = (
        db.query(Activity.started_at, Activity.duration, Activity.category)
        .filter(Activity.started_at >= start_utc)
        .all()
    )

    buckets: dict[str, dict[str, float]] = defaultdict(_zeroed_categories)
    for started_at, duration, category in rows:
        day = started_at.replace(tzinfo=timezone.utc).astimezone(local_tz).date().isoformat()
        buckets[day][category] += float(duration or 0)
        buckets[day][category] = round(buckets[day][category], 2)

    result = []
    today = datetime.now().astimezone().date()
    for offset in range(days - 1, -1, -1):
        day = (today - timedelta(days=offset)).isoformat()
        result.append({"date": day, "by_category": buckets.get(day, _zeroed_categories())})
    return result