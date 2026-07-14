from app.services.market_data import MarketDataService


def test_market_service_returns_gold_price():

    service = MarketDataService()

    result = service.get_gold_price()

    assert result["symbol"] == "XAUUSD"
    assert result["currency"] == "USD"
    assert result["price"] > 0