from abc import ABC, abstractmethod

from app.schemas.market import GoldPriceResponse


class MarketDataProvider(ABC):
    """Contract implemented by all market-data providers."""

    @abstractmethod
    def get_gold_price(self) -> GoldPriceResponse:
        """Retrieve the latest available gold market price."""
        raise NotImplementedError