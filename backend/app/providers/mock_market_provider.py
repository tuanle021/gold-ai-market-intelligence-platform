from datetime import datetime, timezone, timedelta

from app.providers.base import MarketDataProvider
from app.models.market_instrument import MarketInstrument
from app.models.market_interval import MarketInterval
from app.schemas.market import (
    GoldPriceResponse,
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle,
)


class MockMarketDataProvider(MarketDataProvider):
    """Development provider returning predictable gold market data."""

    def get_gold_price(self) -> GoldPriceResponse:
        return GoldPriceResponse(
            symbol=MarketInstrument.GOLD_FUTURES,
            price=3350.50,
            currency="USD",
            timestamp=datetime.now(timezone.utc),
        )

    def get_historical_data(
        self,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        first_timestamp = request.start_time

        second_timestamp = first_timestamp + timedelta(
            minutes=5
        )

        candles = [
            MarketCandle(
                symbol=request.symbol,
                interval=request.interval,
                timestamp=first_timestamp,
                open=4095.10,
                high=4098.40,
                low=4094.70,
                close=4097.20,
                volume=1832,
            ),
            MarketCandle(
                symbol=request.symbol,
                interval=request.interval,
                timestamp=second_timestamp,
                open=4097.20,
                high=4100.10,
                low=4096.80,
                close=4099.60,
                volume=1950,
            ),
        ]

        return HistoricalMarketDataResponse(
            symbol=request.symbol,
            interval=request.interval,
            currency="USD",
            candles=candles,
        )