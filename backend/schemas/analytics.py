from pydantic import BaseModel


class CategoryTotal(BaseModel):
    category: str
    seconds: float


class TodaySummary(BaseModel):
    date: str
    total_seconds: float
    review_seconds: float
    by_category: list[CategoryTotal]


class WebsiteTotal(BaseModel):
    domain: str
    seconds: float


class DailyBreakdown(BaseModel):
    date: str
    by_category: dict[str, float]