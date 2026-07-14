from app.providers.base import MarketDataProvider
from app.schemas.market import GoldPriceResponse


class MarketDataService:
    def __init__(self, provider: MarketDataProvider):
        self.provider = provider

    def get_gold_price(self) -> GoldPriceResponse:
        return self.provider.get_gold_price()