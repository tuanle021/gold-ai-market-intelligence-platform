from datetime import timezone

import pandas as pd
import yfinance as yf

from app.providers.base import MarketDataProvider
from app.schemas.market import (
    HistoricalMarketDataRequest,
    HistoricalMarketDataResponse,
    MarketCandle,
)
from app.instruments.definitions import GOLD_FUTURES
from app.models.instrument_definition import InstrumentDefinition
from app.schemas.market import MarketPriceResponse
from app.models.market_interval import MarketInterval

class YahooFinanceMarketDataProvider(MarketDataProvider):

    INTERVAL_MAPPING: dict[MarketInterval, str] = {
        MarketInterval.ONE_MINUTE: "1m",
        MarketInterval.FIVE_MINUTES: "5m",
        MarketInterval.FIFTEEN_MINUTES: "15m",
        MarketInterval.THIRTY_MINUTES: "30m",
        MarketInterval.ONE_HOUR: "1h",
        MarketInterval.ONE_DAY: "1d",
    }

    def get_latest_price(
        self,
        instrument: InstrumentDefinition,
    ) -> MarketPriceResponse:
        
        ticker = yf.Ticker(instrument.provider_symbol)

        history = ticker.history(
            period="1d",
            interval="5m",
        )

        if history.empty:
            raise ValueError("Yahoo Finance returned no gold price data")

        latest_row = history.iloc[-1]
        latest_timestamp = history.index[-1]

        return MarketPriceResponse(
            symbol=instrument.provider_symbol,
            price=round(float(latest_row["Close"]), 2),
            currency=instrument.instrument.quote_asset or "USD",
            timestamp=latest_timestamp.astimezone(timezone.utc),
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
                f"Yahoo Finance does not support interval: {interval}"
            ) from error
        
    @staticmethod
    def _validate_historical_range(
        request: HistoricalMarketDataRequest,
    ) -> None:
        intraday_intervals = {
            MarketInterval.ONE_MINUTE,
            MarketInterval.FIVE_MINUTES,
            MarketInterval.FIFTEEN_MINUTES,
            MarketInterval.THIRTY_MINUTES,
            MarketInterval.ONE_HOUR,
        }

        requested_range = (
            request.end_time - request.start_time
        )

        if (
            request.interval in intraday_intervals
            and requested_range.days > 60
        ):
            raise ValueError(
                "Yahoo Finance intraday requests cannot exceed 60 days"
            )    
    
    def get_historical_data(
        self,
        instrument: InstrumentDefinition,
        request: HistoricalMarketDataRequest,
    ) -> HistoricalMarketDataResponse:
        self._validate_historical_range(request)

        provider_interval = self._get_provider_interval(
            request.interval
        )

        ticker = yf.Ticker(
            instrument.provider_symbol
        )

        history = ticker.history(
            start=request.start_time,
            end=request.end_time,
            interval=provider_interval,
            auto_adjust=False,
        )

        if history.empty:
            raise ValueError(
                "Yahoo Finance returned no historical gold data"
            )

        candles: list[MarketCandle] = []

        for timestamp, row in history.iterrows():
            required_values = [
                row["Open"],
                row["High"],
                row["Low"],
                row["Close"],
            ]

            if any(pd.isna(value) for value in required_values):
                continue

            volume = row.get("Volume")

            normalised_volume = (
                None
                if volume is None or pd.isna(volume)
                else float(volume)
            )

            candle_timestamp = (
                timestamp.to_pydatetime()
                .astimezone(timezone.utc)
            )

            candles.append(
                MarketCandle(
                    symbol=instrument.provider_symbol,
                    interval=request.interval,
                    timestamp=candle_timestamp,
                    open=float(row["Open"]),
                    high=float(row["High"]),
                    low=float(row["Low"]),
                    close=float(row["Close"]),
                    volume=normalised_volume,
                )
            )

        if not candles:
            raise ValueError(
                "Yahoo Finance returned no valid historical candles"
            )

        return HistoricalMarketDataResponse(
            symbol=instrument.provider_symbol,
            interval=request.interval,
            currency="USD",
            candles=candles,
        )

    def get_gold_price(self) -> MarketPriceResponse:
        return self.get_latest_price(GOLD_FUTURES)
