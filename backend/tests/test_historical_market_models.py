from datetime import datetime, timezone

import pytest
from pydantic import ValidationError

from app.models.market_instrument import MarketInstrument
from app.models.market_interval import MarketInterval
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle,
)


def create_valid_candle() -> MarketCandle:
    return MarketCandle(
        symbol=MarketInstrument.GOLD_FUTURES,
        interval=MarketInterval.FIVE_MINUTES,
        timestamp=datetime.now(timezone.utc),
        open=4095.10,
        high=4098.40,
        low=4094.70,
        close=4097.20,
        volume=1832,
    )


def test_market_interval_values():
    assert MarketInterval.FIVE_MINUTES == "5m"
    assert MarketInterval.ONE_DAY == "1d"


def test_market_candle_accepts_valid_ohlcv_data():
    candle = create_valid_candle()

    assert candle.symbol == MarketInstrument.GOLD_FUTURES
    assert candle.interval == MarketInterval.FIVE_MINUTES
    assert candle.close == 4097.20


def test_market_candle_allows_missing_volume():
    candle = MarketCandle(
        symbol=MarketInstrument.GOLD_SPOT,
        interval=MarketInterval.FIVE_MINUTES,
        timestamp=datetime.now(timezone.utc),
        open=4055.10,
        high=4057.40,
        low=4054.70,
        close=4056.20,
        volume=None,
    )

    assert candle.volume is None


def test_market_candle_rejects_high_below_low():
    with pytest.raises(
        ValidationError,
        match="Candle high must be greater than or equal",
    ):
        MarketCandle(
            symbol=MarketInstrument.GOLD_FUTURES,
            interval=MarketInterval.FIVE_MINUTES,
            timestamp=datetime.now(timezone.utc),
            open=4095.10,
            high=4090.00,
            low=4094.70,
            close=4093.20,
            volume=100,
        )


def test_market_candle_rejects_close_outside_range():
    with pytest.raises(
        ValidationError,
        match="Candle close must be between",
    ):
        MarketCandle(
            symbol=MarketInstrument.GOLD_FUTURES,
            interval=MarketInterval.FIVE_MINUTES,
            timestamp=datetime.now(timezone.utc),
            open=4095.10,
            high=4098.40,
            low=4094.70,
            close=4100.00,
            volume=100,
        )


def test_market_candle_rejects_naive_timestamp():
    with pytest.raises(
        ValidationError,
        match="Candle timestamp must be timezone-aware",
    ):
        MarketCandle(
            symbol=MarketInstrument.GOLD_FUTURES,
            interval=MarketInterval.FIVE_MINUTES,
            timestamp=datetime.now(),
            open=4095.10,
            high=4098.40,
            low=4094.70,
            close=4097.20,
            volume=100,
        )


def test_historical_request_accepts_valid_range():
    request = HistoricalMarketDataRequest(
        symbol=MarketInstrument.GOLD_FUTURES,
        interval=MarketInterval.ONE_DAY,
        start_time=datetime(
            2026,
            7,
            1,
            tzinfo=timezone.utc,
        ),
        end_time=datetime(
            2026,
            7,
            14,
            tzinfo=timezone.utc,
        ),
    )

    assert request.start_time < request.end_time


def test_historical_request_rejects_invalid_range():
    with pytest.raises(
        ValidationError,
        match="Start time must be before end time",
    ):
        HistoricalMarketDataRequest(
            symbol=MarketInstrument.GOLD_FUTURES,
            interval=MarketInterval.ONE_DAY,
            start_time=datetime(
                2026,
                7,
                14,
                tzinfo=timezone.utc,
            ),
            end_time=datetime(
                2026,
                7,
                1,
                tzinfo=timezone.utc,
            ),
        )


def test_historical_response_accepts_candle_collection():
    candle = create_valid_candle()

    response = HistoricalMarketDataResponse(
        symbol=MarketInstrument.GOLD_FUTURES,
        interval=MarketInterval.FIVE_MINUTES,
        currency="USD",
        candles=[candle],
    )

    assert len(response.candles) == 1
    assert response.candles[0].close == 4097.20