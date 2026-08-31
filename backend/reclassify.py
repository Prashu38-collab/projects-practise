"""Re-run classification on previously unclassified activities.

Used after the rule hints change: past activities stored as
category="unknown" with classification_source="none" are re-evaluated
with the current rules. User decisions are never touched.

Run from backend/:  .venv/bin/python reclassify.py
"""

from database.connection import SessionLocal
from models.activity import Activity
from services import classification_service


def main() -> None:
    db = SessionLocal()
    rows = db.query(Activity).filter(
        Activity.classification_source == "none",
        Activity.needs_review.is_(True),
    ).all()

    changed = 0
    for activity in rows:
        result = classification_service.classify(
            db, activity.title, activity.url, activity.domain
        )
        if result["classification_source"] == "rule":
            activity.category = result["category"]
            activity.confidence = result["confidence"]
            activity.classification_source = "rule"
            activity.needs_review = False
            changed += 1

    db.commit()
    db.close()
    print(f"Reclassified {changed} of {len(rows)} previously unknown activities.")


if __name__ == "__main__":
    main()