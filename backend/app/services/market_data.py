from datetime import datetime, timezone

from app.schemas.market import GoldPriceResponse


class MarketDataService:

    def get_gold_price(self) -> GoldPriceResponse:
        return GoldPriceResponse(
            symbol="XAUUSD",
            price=3350.42,
            currency="USD",
            timestamp=datetime.now(timezone.utc)
        )


market_data_service = MarketDataService()