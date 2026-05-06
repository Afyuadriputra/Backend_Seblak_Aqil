def test_health_check_success(client):
    response = client.get("/health")

    assert response.status_code == 200

    body = response.json()

    assert body["success"] is True
    assert body["message"] == "Application is running"
    assert body["data"]["app"] == "Toko Online Seblak Rika API"
    assert body["data"]["version"] == "1.0.0"
    assert body["data"]["environment"] == "development"


def test_health_dependencies_should_return_safe_status(client):
    response = client.get("/health/dependencies")

    assert response.status_code == 200
    body = response.json()
    assert body["success"] is True
    assert body["data"]["status"] in {"ok", "degraded"}
    assert body["data"]["db"] in {"ok", "error"}
    assert body["data"]["redis"] in {"ok", "error"}
    assert "DATABASE_URL" not in str(body)
    assert "redis://" not in str(body)
