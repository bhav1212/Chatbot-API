from fastapi.testclient import TestClient

from app import app


client = TestClient(app)


def test_rejects_missing_uid():
    response = client.post("/chat", json={"uid": "", "session_id": "s1", "query": "hi"})
    assert response.status_code == 401


def test_chat_and_clear_session():
    payload = {"uid": "u1", "session_id": "s1", "query": "hello"}

    chat_response = client.post("/chat", json=payload)
    assert chat_response.status_code == 200
    body = chat_response.json()
    assert body["uid"] == "u1"
    assert body["session_id"] == "s1"
    assert "hello" in body["answer"]

    health = client.get("/health")
    assert health.status_code == 200
    assert health.json()["active_sessions"] >= 1

    end_response = client.post("/session/end", json={"uid": "u1", "session_id": "s1"})
    assert end_response.status_code == 200
    assert end_response.json()["status"] == "session_cleared"
