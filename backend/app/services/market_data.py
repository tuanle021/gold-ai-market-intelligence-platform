from app.models.instrument_definition import InstrumentDefinition
from app.providers.base import MarketDataProvider
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketPriceResponse,
)


class MarketDataService:
    def __init__(
        self,
        provider: MarketDataProvider,
        instrument: InstrumentDefinition,
    ):
        self.provider = provider
        self.instrument = instrument

    def get_latest_price(self) -> MarketPriceResponse:
        return self.provider.get_latest_price(
            self.instrument
        )

    def get_gold_price(self) -> MarketPriceResponse:
        """Temporary compatibility wrapper for existing routes."""
        return self.get_latest_price()

    def get_historical_data(
        self,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        return self.provider.get_historical_data(
            self.instrument,
            request,
        )