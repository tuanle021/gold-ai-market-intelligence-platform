from datetime import datetime

from app.schemas.market import GoldPriceResponse


def test_gold_price_schema():

    response = GoldPriceResponse(
        symbol="XAUUSD",
        price=3350.50,
        currency="USD",
        timestamp=datetime.now()
    )

    assert response.symbol == "XAUUSD"
    assert response.price > 0
    assert response.currency == "USD"