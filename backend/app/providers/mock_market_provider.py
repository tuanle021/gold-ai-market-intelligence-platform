from datetime import datetime, timezone

from app.providers.base import MarketDataProvider
from app.schemas.market import GoldPriceResponse


class MockMarketDataProvider(MarketDataProvider):
    """Development provider returning predictable gold market data."""

    def get_gold_price(self) -> GoldPriceResponse:
        return GoldPriceResponse(
            symbol="GC=F",
            price=3350.50,
            currency="USD",
            timestamp=datetime.now(timezone.utc),
        )