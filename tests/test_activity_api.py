import pytest
from fastapi.testclient import TestClient
from src.app import app, activities


@pytest.fixture
def client():
    return TestClient(app)


@pytest.fixture
def reset_activities():
    original_activities = {
        "Chess Club": {
            "description": "Learn strategies and compete in chess tournaments",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["michael@mergington.edu", "daniel@mergington.edu"]
        },
        "Programming Class": {
            "description": "Learn programming fundamentals and build software projects",
            "schedule": "Tuesdays and Thursdays, 3:30 PM - 4:30 PM",
            "max_participants": 20,
            "participants": ["emma@mergington.edu", "sophia@mergington.edu"]
        },
        "Gym Class": {
            "description": "Physical education and sports activities",
            "schedule": "Mondays, Wednesdays, Fridays, 2:00 PM - 3:00 PM",
            "max_participants": 30,
            "participants": ["john@mergington.edu", "olivia@mergington.edu"]
        },
        "Basketball Team": {
            "description": "Competitive basketball team and practice drills",
            "schedule": "Tuesdays and Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 15,
            "participants": ["james@mergington.edu", "marcus@mergington.edu"]
        },
        "Tennis Club": {
            "description": "Learn tennis skills and compete in matches",
            "schedule": "Mondays and Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 12,
            "participants": ["alex@mergington.edu"]
        },
        "Art Studio": {
            "description": "Painting, drawing, and sculpture techniques",
            "schedule": "Wednesdays, 3:30 PM - 5:00 PM",
            "max_participants": 18,
            "participants": ["isabella@mergington.edu", "lucas@mergington.edu"]
        },
        "Drama Club": {
            "description": "Theater performances and acting workshops",
            "schedule": "Thursdays, 4:00 PM - 5:30 PM",
            "max_participants": 25,
            "participants": ["grace@mergington.edu", "joshua@mergington.edu"]
        },
        "Science Club": {
            "description": "Hands-on experiments and scientific exploration",
            "schedule": "Fridays, 3:30 PM - 5:00 PM",
            "max_participants": 16,
            "participants": ["ryan@mergington.edu", "aiden@mergington.edu"]
        },
        "Debate Team": {
            "description": "Competitive debate and public speaking",
            "schedule": "Tuesdays, 4:00 PM - 5:30 PM",
            "max_participants": 14,
            "participants": ["chloe@mergington.edu"]
        }
    }

    activities.clear()
    activities.update(original_activities)

    yield

    activities.clear()
    activities.update(original_activities)


class TestActivityAPI:
    def test_get_activities(self, client, reset_activities):
        response = client.get("/activities")
        assert response.status_code == 200
        data = response.json()
        assert "Chess Club" in data
        assert "Programming Class" in data
        assert len(data) == 9

    def test_signup_success(self, client, reset_activities):
        response = client.post("/activities/Chess Club/signup", params={"email": "newstudent@mergington.edu"})
        assert response.status_code == 200
        assert response.json()["message"] == "Signed up newstudent@mergington.edu for Chess Club"

        verify_response = client.get("/activities")
        assert "newstudent@mergington.edu" in verify_response.json()["Chess Club"]["participants"]

    def test_signup_duplicate(self, client, reset_activities):
        response = client.post("/activities/Chess Club/signup", params={"email": "michael@mergington.edu"})
        assert response.status_code == 400

    def test_signup_unknown_activity(self, client, reset_activities):
        response = client.post("/activities/Unknown/signup", params={"email": "x@x.com"})
        assert response.status_code == 404

    def test_delete_participant_success(self, client, reset_activities):
        response = client.delete("/activities/Chess Club/participants/michael@mergington.edu")
        assert response.status_code == 200

        verify_response = client.get("/activities")
        assert "michael@mergington.edu" not in verify_response.json()["Chess Club"]["participants"]

    def test_delete_unknown_activity(self, client, reset_activities):
        response = client.delete("/activities/Unknown/participants/x@x.com")
        assert response.status_code == 404

    def test_delete_unknown_participant(self, client, reset_activities):
        response = client.delete("/activities/Chess Club/participants/unknown@x.com")
        assert response.status_code == 404
