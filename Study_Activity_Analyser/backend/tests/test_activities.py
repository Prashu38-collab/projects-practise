from datetime import datetime, timedelta, timezone


def test_create_activity_study_rule(client):
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=45)

    payload = {
        "title": "Calculus Integration by Parts Lecture",
        "url": "https://youtube.com/watch?v=12345",
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
    }

    response = client.post("/api/v1/activities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["title"] == "Calculus Integration by Parts Lecture"
    assert data["domain"] == "youtube.com"
    assert data["duration"] == 2700.0
    assert data["category"] == "study"
    assert data["confidence"] == 0.8
    assert data["classification_source"] == "rule"
    assert data["needs_review"] is False


def test_create_activity_unknown(client):
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=10)

    payload = {
        "title": "Random Personal Blog Post",
        "url": "https://random-site.example.com/blog/1",
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
    }

    response = client.post("/api/v1/activities", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["category"] == "unknown"
    assert data["confidence"] == 0.0
    assert data["needs_review"] is True


def test_user_override_and_learning(client):
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=15)

    payload = {
        "title": "How to Build a Custom Desk",
        "url": "https://youtube.com/watch?v=desk123",
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
    }

    # 1. First creation is study because of "how to" hint in title
    res1 = client.post("/api/v1/activities", json=payload)
    assert res1.status_code == 201
    act_id = res1.json()["id"]

    # 2. User manual override to 'work' with subject 'Woodworking'
    patch_payload = {
        "category": "work",
        "subject": "Woodworking",
        "topic": "Desk Assembly",
    }
    patch_res = client.patch(f"/api/v1/activities/{act_id}/classification", json=patch_payload)
    assert patch_res.status_code == 200
    patched_data = patch_res.json()
    assert patched_data["category"] == "work"
    assert patched_data["subject"] == "Woodworking"
    assert patched_data["topic"] == "Desk Assembly"
    assert patched_data["classification_source"] == "user"
    assert patched_data["confidence"] == 1.0

    # 3. Next activity with exact same title must use user override
    res2 = client.post("/api/v1/activities", json=payload)
    assert res2.status_code == 201
    data2 = res2.json()
    assert data2["category"] == "work"
    assert data2["subject"] == "Woodworking"
    assert data2["topic"] == "Desk Assembly"
    assert data2["classification_source"] == "user"


def test_list_activities_and_review(client):
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=5)

    # Unknown item (needs review)
    client.post("/api/v1/activities", json={
        "title": "Unclassified Page",
        "url": "https://unknown.com/page",
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
    })

    # Direct study item
    client.post("/api/v1/activities", json={
        "title": "Python Documentation",
        "url": "https://coursera.org/learn/python",
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
    })

    list_res = client.get("/api/v1/activities")
    assert list_res.status_code == 200
    assert len(list_res.json()) == 2

    review_res = client.get("/api/v1/activities/review")
    assert review_res.status_code == 200
    review_items = review_res.json()
    assert len(review_items) == 1
    assert review_items[0]["title"] == "Unclassified Page"


def test_delete_activity(client):
    start = datetime.now(timezone.utc)
    end = start + timedelta(minutes=5)

    res = client.post("/api/v1/activities", json={
        "title": "To Delete",
        "url": "https://example.com",
        "started_at": start.isoformat(),
        "ended_at": end.isoformat(),
    })
    act_id = res.json()["id"]

    del_res = client.delete(f"/api/v1/activities/{act_id}")
    assert del_res.status_code == 204

    get_res = client.get("/api/v1/activities")
    assert len(get_res.json()) == 0
