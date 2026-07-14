from app.providers.mock_market_provider import MockMarketDataProvider
from app.services.market_data import MarketDataService


def test_market_service_returns_gold_price():
    provider = MockMarketDataProvider()
    service = MarketDataService(provider=provider)

    result = service.get_gold_price()

    assert result.symbol == "GC=F"
    assert result.currency == "USD"
    assert result.price > 0