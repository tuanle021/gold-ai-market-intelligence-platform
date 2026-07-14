from app.providers.base import MarketDataProvider
from app.schemas.market import (
    GoldPriceResponse,
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
)


class MarketDataService:
    def __init__(
        self,
        provider: MarketDataProvider,
    ):
        self.provider = provider

    def get_gold_price(self) -> GoldPriceResponse:
        return self.provider.get_gold_price()

    def get_historical_data(
        self,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        return self.provider.get_historical_data(
            request
        )