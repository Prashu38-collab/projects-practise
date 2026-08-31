from datetime import datetime, timedelta, timezone


def test_analytics_today_and_categories(client):
    now = datetime.now(timezone.utc)

    # Add 1 hour study
    client.post("/api/v1/activities", json={
        "title": "FastAPI Masterclass Tutorial",
        "url": "https://youtube.com/watch?v=fastapi",
        "started_at": now.isoformat(),
        "ended_at": (now + timedelta(hours=1)).isoformat(),
    })

    # Add 30 mins entertainment
    client.post("/api/v1/activities", json={
        "title": "Funny Cats Compilation",
        "url": "https://youtube.com/watch?v=cats",
        "started_at": now.isoformat(),
        "ended_at": (now + timedelta(minutes=30)).isoformat(),
    })

    today_res = client.get("/api/v1/analytics/today")
    assert today_res.status_code == 200
    today_data = today_res.json()
    assert today_data["total_seconds"] == 5400.0

    cat_res = client.get("/api/v1/analytics/categories")
    assert cat_res.status_code == 200
    cat_map = {item["category"]: item["seconds"] for item in cat_res.json()}
    assert cat_map["study"] == 3600.0
    assert cat_map["entertainment"] == 1800.0


def test_top_websites_and_daily(client):
    now = datetime.now(timezone.utc)

    client.post("/api/v1/activities", json={
        "title": "LeetCode Two Sum Solution",
        "url": "https://leetcode.com/problems/two-sum",
        "started_at": now.isoformat(),
        "ended_at": (now + timedelta(minutes=20)).isoformat(),
    })

    web_res = client.get("/api/v1/analytics/websites")
    assert web_res.status_code == 200
    websites = web_res.json()
    assert len(websites) >= 1
    assert websites[0]["domain"] == "leetcode.com"
    assert websites[0]["seconds"] == 1200.0

    daily_res = client.get("/api/v1/analytics/daily?days=7")
    assert daily_res.status_code == 200
    daily_data = daily_res.json()
    assert len(daily_data) == 7
