from abc import ABC, abstractmethod

from app.models.instrument_definition import InstrumentDefinition
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketPriceResponse,
)


class MarketDataProvider(ABC):
    """Contract implemented by market-data providers."""

    @abstractmethod
    def get_latest_price(
        self,
        instrument: InstrumentDefinition,
    ) -> MarketPriceResponse:
        """Retrieve the latest price for an instrument."""
        raise NotImplementedError

    @abstractmethod
    def get_historical_data(
        self,
        instrument: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        """Retrieve historical candles for an instrument."""
        raise NotImplementedError