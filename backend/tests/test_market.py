from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.api.dependencies import (
    get_gold_futures_service,
    get_gold_spot_service,
)
from app.main import app
from app.schemas.market import GoldPriceResponse
from app.services.market_data import MarketDataService
from app.models.market_instrument import MarketInstrument


client = TestClient(app)


class MockSpotMarketDataProvider:
    def get_gold_price(self) -> GoldPriceResponse:
        return GoldPriceResponse(
            symbol=MarketInstrument.GOLD_SPOT,
            price=4056.80,
            currency="USD",
            timestamp=datetime.now(timezone.utc),
        )


class MockFuturesMarketDataProvider:
    def get_gold_price(self) -> GoldPriceResponse:
        return GoldPriceResponse(
            symbol=MarketInstrument.GOLD_FUTURES,
            price=4097.20,
            currency="USD",
            timestamp=datetime.now(timezone.utc),
        )


def override_gold_spot_service() -> MarketDataService:
    return MarketDataService(
        provider=MockSpotMarketDataProvider()
    )


def override_gold_futures_service() -> MarketDataService:
    return MarketDataService(
        provider=MockFuturesMarketDataProvider()
    )


def test_get_gold_spot_market_data():
    app.dependency_overrides[
        get_gold_spot_service
    ] = override_gold_spot_service

    try:
        response = client.get("/market/gold/spot")
    finally:
        app.dependency_overrides.pop(
            get_gold_spot_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "XAU/USD"
    assert data["price"] == 4056.80
    assert data["currency"] == "USD"
    assert "timestamp" in data


def test_get_gold_futures_market_data():
    app.dependency_overrides[
        get_gold_futures_service
    ] = override_gold_futures_service

    try:
        response = client.get("/market/gold/futures")
    finally:
        app.dependency_overrides.pop(
            get_gold_futures_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "GC=F"
    assert data["price"] == 4097.20
    assert data["currency"] == "USD"
    assert "timestamp" in data