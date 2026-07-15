from datetime import datetime, timezone

from fastapi.testclient import TestClient

from app.api.dependencies import (
    get_gold_futures_service,
    get_gold_spot_service,
    get_gold_futures_historical_service
)
from app.main import app
from app.services.market_data import MarketDataService
from app.models.market_instrument import MarketInstrument
from app.models.market_interval import MarketInterval
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle,
    GoldPriceResponse
)


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
    def get_historical_data(
        self,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        return HistoricalMarketDataResponse(
            symbol=MarketInstrument.GOLD_FUTURES,
            interval=request.interval,
            currency="USD",
            candles=[
                MarketCandle(
                    symbol=MarketInstrument.GOLD_FUTURES,
                    interval=request.interval,
                    timestamp=datetime(
                        2026,
                        7,
                        14,
                        10,
                        0,
                        tzinfo=timezone.utc,
                    ),
                    open=4095.10,
                    high=4098.40,
                    low=4094.70,
                    close=4097.20,
                    volume=1832,
                )
            ],
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

def override_gold_futures_historical_service() -> MarketDataService:
    return MarketDataService(
        provider=MockFuturesMarketDataProvider()
    )

def test_get_gold_futures_historical_data():
    app.dependency_overrides[
        get_gold_futures_historical_service
    ] = override_gold_futures_historical_service

    try:
        response = client.get(
            "/market/gold/futures/history",
            params={
                "interval": "5m",
                "start_time": "2026-07-14T10:00:00Z",
                "end_time": "2026-07-14T11:00:00Z",
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_gold_futures_historical_service,
            None,
        )

    assert response.status_code == 200

    data = response.json()

    assert data["symbol"] == "GC=F"
    assert data["interval"] == "5m"
    assert data["currency"] == "USD"
    assert len(data["candles"]) == 1

    candle = data["candles"][0]

    assert candle["open"] == 4095.10
    assert candle["high"] == 4098.40
    assert candle["low"] == 4094.70
    assert candle["close"] == 4097.20
    assert candle["volume"] == 1832

def test_historical_endpoint_rejects_invalid_interval():
    response = client.get(
        "/market/gold/futures/history",
        params={
            "interval": "2h",
            "start_time": "2026-07-14T10:00:00Z",
            "end_time": "2026-07-14T11:00:00Z",
        },
    )

    assert response.status_code == 422

def test_historical_endpoint_rejects_invalid_date_range():
    app.dependency_overrides[
        get_gold_futures_historical_service
    ] = override_gold_futures_historical_service

    try:
        response = client.get(
            "/market/gold/futures/history",
            params={
                "interval": "5m",
                "start_time": "2026-07-14T12:00:00Z",
                "end_time": "2026-07-14T11:00:00Z",
            },
        )
    finally:
        app.dependency_overrides.pop(
            get_gold_futures_historical_service,
            None,
        )

    assert response.status_code == 422