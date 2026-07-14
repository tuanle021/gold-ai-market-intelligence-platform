from datetime import datetime, timezone

import httpx

from app.core.config import settings
from app.providers.base import MarketDataProvider
from app.schemas.market import GoldPriceResponse


class TwelveDataMarketDataProvider(MarketDataProvider):
    """Retrieves XAU/USD spot gold data from Twelve Data."""

    GOLD_SPOT_SYMBOL = "XAU/USD"

    def __init__(
        self,
        api_key: str | None = None,
        base_url: str | None = None,
        timeout_seconds: float = 10.0,
    ):
        self.api_key = (
            settings.twelve_data_api_key
            if api_key is None
            else api_key
        )

        self.base_url = (
            settings.twelve_data_base_url
            if base_url is None
            else base_url
        )

        self.timeout_seconds = timeout_seconds

        if not self.api_key:
            raise ValueError(
                "Twelve Data API key is not configured"
            )

    def get_gold_price(self) -> GoldPriceResponse:
        response = httpx.get(
            f"{self.base_url}/price",
            params={
                "symbol": self.GOLD_SPOT_SYMBOL,
                "apikey": self.api_key,
            },
            timeout=self.timeout_seconds,
        )

        response.raise_for_status()
        payload = response.json()

        if payload.get("status") == "error":
            raise ValueError(
                payload.get(
                    "message",
                    "Twelve Data returned an unknown error",
                )
            )

        price = payload.get("price")

        if price is None:
            raise ValueError(
                "Twelve Data response did not contain a price"
            )

        return GoldPriceResponse(
            symbol=self.GOLD_SPOT_SYMBOL,
            price=round(float(price), 2),
            currency="USD",
            timestamp=datetime.now(timezone.utc),
        )