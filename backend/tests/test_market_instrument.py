import pytest
from pydantic import ValidationError

from app.models.market_instrument import MarketInstrument
from app.schemas.market import GoldPriceResponse


def test_gold_futures_instrument_value():
    assert MarketInstrument.GOLD_FUTURES == "GC=F"


def test_gold_spot_instrument_value():
    assert MarketInstrument.GOLD_SPOT == "XAU/USD"


def test_gold_price_response_accepts_supported_instrument():
    response = GoldPriceResponse(
        symbol=MarketInstrument.GOLD_FUTURES,
        price=4097.20,
        currency="USD",
        timestamp="2026-07-14T15:20:00Z",
    )

    assert response.symbol == MarketInstrument.GOLD_FUTURES


def test_gold_price_response_rejects_unsupported_instrument():
    with pytest.raises(ValidationError):
        GoldPriceResponse(
            symbol="INVALID",
            price=100.00,
            currency="USD",
            timestamp="2026-07-14T15:20:00Z",
        )