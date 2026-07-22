from datetime import datetime, timezone

import httpx

from app.core.config import settings
from app.providers.base import MarketDataProvider
from app.models.market_interval import MarketInterval
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle,
)
from app.instruments.definitions import GOLD_SPOT
from app.models.instrument_definition import InstrumentDefinition
from app.schemas.market import MarketPriceResponse

class TwelveDataMarketDataProvider(MarketDataProvider):

    INTERVAL_MAPPING: dict[MarketInterval, str] = {
        MarketInterval.ONE_MINUTE: "1min",
        MarketInterval.FIVE_MINUTES: "5min",
        MarketInterval.FIFTEEN_MINUTES: "15min",
        MarketInterval.THIRTY_MINUTES: "30min",
        MarketInterval.ONE_HOUR: "1h",
        MarketInterval.FOUR_HOURS: "4h",
        MarketInterval.ONE_DAY: "1day",
    }

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

    def get_latest_price(
        self,
        instrument: InstrumentDefinition,
    ) -> MarketPriceResponse:
        response = httpx.get(
            f"{self.base_url}/price",
            params={
                "symbol": instrument.provider_symbol,
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

        return MarketPriceResponse(
            symbol=instrument.provider_symbol,
            price=round(float(price), 2),
            currency=instrument.instrument.quote_asset or "USD",
            timestamp=datetime.now(timezone.utc),
        )
    
    def get_historical_data(
        self,
        instrument: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:

        provider_interval = self._get_provider_interval(
            request.interval
        )

        response = httpx.get(
            f"{self.base_url}/time_series",
            params={
                "symbol": instrument.provider_symbol,
                "interval": provider_interval,
                "start_date": request.start_time.isoformat(),
                "end_date": request.end_time.isoformat(),
                "timezone": "UTC",
                "order": "ASC",
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

        values = payload.get("values")

        if not values:
            raise ValueError(
                "Twelve Data returned no historical spot data"
            )

        candles: list[MarketCandle] = []

        for item in values:
            timestamp = datetime.fromisoformat(
                item["datetime"]
            )

            if timestamp.tzinfo is None:
                timestamp = timestamp.replace(
                    tzinfo=timezone.utc
                )
            else:
                timestamp = timestamp.astimezone(
                    timezone.utc
                )

            volume = item.get("volume")

            candles.append(
                MarketCandle(
                    symbol=instrument.provider_symbol,
                    interval=request.interval,
                    timestamp=timestamp,
                    open=float(item["open"]),
                    high=float(item["high"]),
                    low=float(item["low"]),
                    close=float(item["close"]),
                    volume=(
                        None
                        if volume in (None, "")
                        else float(volume)
                    ),
                )
            )

        candles.sort(
            key=lambda candle: candle.timestamp
        )

        return HistoricalMarketDataResponse(
            symbol=instrument.provider_symbol,
            interval=request.interval,
            currency="USD",
            candles=candles,
        )
    
    @classmethod
    def _get_provider_interval(
        cls,
        interval: MarketInterval,
    ) -> str:
        try:
            return cls.INTERVAL_MAPPING[interval]
        except KeyError as error:
            raise ValueError(
                f"Twelve Data does not support interval: {interval}"
            ) from error
        
    def get_gold_price(self) -> MarketPriceResponse:
        return self.get_latest_price(GOLD_SPOT)