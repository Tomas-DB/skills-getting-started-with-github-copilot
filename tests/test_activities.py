import urllib.parse

import src.app as app_module


def quote(s: str) -> str:
    return urllib.parse.quote(s, safe="")


def test_get_activities(client):
    r = client.get("/activities")
    assert r.status_code == 200
    data = r.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data


def test_signup_success(client):
    activity = "Chess Club"
    email = "newstudent@example.com"
    r = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r.status_code == 200

    data = client.get("/activities").json()
    assert email in data[activity]["participants"]


def test_signup_duplicate(client):
    activity = "Chess Club"
    email = "duplicate@example.com"
    r1 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r1.status_code == 200

    r2 = client.post(f"/activities/{quote(activity)}/signup", params={"email": email})
    assert r2.status_code == 400
    assert "already" in r2.json().get("detail", "").lower()


def test_unregister_success(client):
    activity = "Chess Club"
    email = "toremove@example.com"
    # sign up first
    client.post(f"/activities/{quote(activity)}/signup", params={"email": email})

    r = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r.status_code == 200

    data = client.get("/activities").json()
    assert email not in data[activity]["participants"]


def test_unregister_not_found(client):
    activity = "Chess Club"
    email = "noone@example.com"
    r = client.delete(f"/activities/{quote(activity)}/participants", params={"email": email})
    assert r.status_code == 404
