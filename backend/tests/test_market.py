from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_get_gold_market_data():
    response = client.get("/market/gold")

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "XAUUSD"
    assert "price" in data
    assert "currency" in data
    assert "timestamp" in data