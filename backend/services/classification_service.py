import re

from sqlalchemy import func
from sqlalchemy.orm import Session

from models.activity import Activity

CATEGORIES = ["study", "work", "social", "entertainment", "other", "unknown"]

# Domains almost always used for one purpose. Matched on the base domain.
DIRECT_DOMAIN = {
    "coursera.org": "study",
    "udemy.com": "study",
    "khanacademy.org": "study",
    "edx.org": "study",
    "w3schools.com": "study",
    "geeksforgeeks.org": "study",
    "leetcode.com": "study",
    "stackoverflow.com": "work",
    "github.com": "work",
    "gitlab.com": "work",
    "notion.so": "work",
    "slack.com": "work",
    "linkedin.com": "work",
    "mail.google.com": "work",
    "confluence.atlassian.com": "work",
    "netflix.com": "entertainment",
    "primevideo.com": "entertainment",
    "spotify.com": "entertainment",
    "twitch.tv": "entertainment",
    "instagram.com": "social",
    "facebook.com": "social",
    "twitter.com": "social",
    "x.com": "social",
    "tiktok.com": "social",
    "reddit.com": "social",
    "discord.com": "social",
    "whatsapp.com": "social",
    "telegram.org": "social",
}

# Content platforms: the site is used for all kinds of things, so the title
# must hint at the purpose before we call it study/entertainment.
AMBIGUOUS_DOMAINS = {
    "youtube.com",
    "google.com",
    "bing.com",
    "duckduckgo.com",
}

STUDY_TITLE_HINTS = [
    # general learning signals
    "how to", "learn", "learning", "guide", "explained", "explain", "basics",
    "beginner", "advanced", "crash course", "course", "tutorial", "lesson",
    "lecture", "class", "study", "revision", "notes", "syllabus", "curriculum",
    "textbook", "mock test", "exam", "entrance", "preparation", "prep",
    "homework", "assignment", "semester",
    # academic shorthand / entrance exams
    "mbbs", "neet", "jee", "gate", "upsc", "gre", "ielts", "toefl", "sat",
    "school", "college", "university", "professor",
    # subjects
    "math", "maths", "mathematics", "calculus", "algebra", "geometry",
    "physics", "chemistry", "biology", "science", "history", "geography",
    "economics", "accounting", "english", "nepali",
    # programming and CS
    "programming", "coding", "code", "python", "javascript", "java", "c++",
    "sql", "html", "css", "react", "django", "fastapi", "flask", "algorithm",
    "data structure", "documentation",
    # AI / ML
    "ai", "machine learning", "deep learning", "neural network", "artificial intelligence",
]

ENTERTAINMENT_TITLE_HINTS = [
    # humor
    "funny", "joke", "jokes", "meme", "memes", "comedy", "skit", "prank",
    "fail", "fails", "satisfying", "asmr", "compilation",
    # films, series, anime
    "movie", "trailer", "film", "anime", "series", "episode", "cartoon",
    # music
    "music", "song", "lyrics", "remix", "playlist", "official video",
    "official audio", "official music",
    # gaming
    "game", "gaming", "gameplay", "playthrough", "walkthrough", "lets play",
    "letsplay", "gta", "minecraft",
    # creator/viral content
    "vlog", "vlogs", "reaction", "unboxing", "challenge", "top 10", "top10",
    "ranking", "viral", "trending", "highlights",
]


def _base_domain(domain: str) -> str:
    parts = [p for p in (domain or "").lower().strip().split(".") if p]
    return ".".join(parts[-2:]) if len(parts) > 2 else domain.lower()


def _has_hint(title: str, hint: str) -> bool:
    title = title.lower()
    # Single tokens match only on word boundaries so short hints like "ai",
    # "sat" or "gre" never match inside unrelated words ("main", "saturday").
    if re.fullmatch(r"[a-z0-9 ]+", hint):
        return re.search(rf"\b{re.escape(hint)}\b", title) is not None
    # Phrases and hints with symbols ("c++", "top 10") match as substrings.
    return hint in title


def _user_decision_for_title(db: Session, title: str) -> tuple[str, str | None, str | None] | None:
    row = (
        db.query(Activity.category, Activity.subject, Activity.topic)
        .filter(
            func.lower(Activity.title) == title.strip().lower(),
            Activity.classification_source == "user",
            Activity.category != "unknown",
        )
        .order_by(Activity.updated_at.desc())
        .first()
    )
    return (row[0], row[1], row[2]) if row else None


def classify(db: Session, title: str, url: str, domain: str) -> dict:
    # 1. Prior user decision for the same activity title outranks every rule.
    user_decision = _user_decision_for_title(db, title)
    if user_decision:
        user_category, user_subject, user_topic = user_decision
        return {
            "category": user_category,
            "subject": user_subject,
            "topic": user_topic,
            "confidence": 0.9,
            "classification_source": "user",
            "needs_review": False,
        }

    # 2. Deterministic rules.
    base = _base_domain(domain)
    title_lower = title.lower()

    if base in AMBIGUOUS_DOMAINS or base in DIRECT_DOMAIN:
        if any(_has_hint(title_lower, hint) for hint in STUDY_TITLE_HINTS):
            return {
                "category": "study",
                "subject": None,
                "topic": None,
                "confidence": 0.8,
                "classification_source": "rule",
                "needs_review": False,
            }
        if any(_has_hint(title_lower, hint) for hint in ENTERTAINMENT_TITLE_HINTS):
            return {
                "category": "entertainment",
                "subject": None,
                "topic": None,
                "confidence": 0.8,
                "classification_source": "rule",
                "needs_review": False,
            }

    if base in DIRECT_DOMAIN:
        return {
            "category": DIRECT_DOMAIN[base],
            "subject": None,
            "topic": None,
            "confidence": 0.9,
            "classification_source": "rule",
            "needs_review": False,
        }

    # 3. We do not know. Honest uncertainty beats a wrong guess.
    return {
        "category": "unknown",
        "subject": None,
        "topic": None,
        "confidence": 0.0,
        "classification_source": "none",
        "needs_review": True,
    }



def recompute_duration(started_at, ended_at) -> float:
    delta = (ended_at - started_at).total_seconds()
    return max(0.0, delta)