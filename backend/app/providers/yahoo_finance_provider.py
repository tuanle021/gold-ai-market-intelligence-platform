from datetime import timezone

import yfinance as yf

from app.providers.base import MarketDataProvider
from app.schemas.market import GoldPriceResponse
from app.models.market_instrument import MarketInstrument


class YahooFinanceMarketDataProvider(MarketDataProvider):
    """Retrieves gold futures market data from Yahoo Finance."""

    GOLD_TICKER = MarketInstrument.GOLD_FUTURES

    def get_gold_price(self) -> GoldPriceResponse:
        ticker = yf.Ticker(self.GOLD_TICKER)

        history = ticker.history(
            period="1d",
            interval="5m",
        )

        if history.empty:
            raise ValueError("Yahoo Finance returned no gold price data")

        latest_row = history.iloc[-1]
        latest_timestamp = history.index[-1]

        return GoldPriceResponse(
            symbol=self.GOLD_TICKER,
            price=round(float(latest_row["Close"]), 2),
            currency="USD",
            timestamp=latest_timestamp.astimezone(timezone.utc),
        )