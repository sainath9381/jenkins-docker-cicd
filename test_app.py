from app import app


def test_home():
    client = app.test_client()

    response = client.get("/")

    assert response.status_code == 200
    assert b"CI/CD Application is running successfully!" in response.data


def test_health():
    client = app.test_client()

    response = client.get("/health")

    assert response.status_code == 200
    assert response.json["status"] == "healthy"