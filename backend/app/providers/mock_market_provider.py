from datetime import datetime, timedelta, timezone

from app.models.instrument_definition import InstrumentDefinition
from app.providers.base import MarketDataProvider
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle,
    MarketPriceResponse,
)


class MockMarketDataProvider(MarketDataProvider):
    def get_latest_price(
        self,
        instrument: InstrumentDefinition,
    ) -> MarketPriceResponse:
        return MarketPriceResponse(
            symbol=instrument.provider_symbol,
            price=3350.50,
            currency=instrument.instrument.quote_asset or "USD",
            timestamp=datetime.now(timezone.utc),
        )

    def get_historical_data(
        self,
        instrument: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        first_timestamp = request.start_time
        second_timestamp = first_timestamp + timedelta(
            minutes=5
        )

        candles = [
            MarketCandle(
                symbol=instrument.provider_symbol,
                interval=request.interval,
                timestamp=first_timestamp,
                open=4095.10,
                high=4098.40,
                low=4094.70,
                close=4097.20,
                volume=1832,
            ),
            MarketCandle(
                symbol=instrument.provider_symbol,
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
            symbol=instrument.provider_symbol,
            interval=request.interval,
            currency=instrument.instrument.quote_asset or "USD",
            candles=candles,
        )