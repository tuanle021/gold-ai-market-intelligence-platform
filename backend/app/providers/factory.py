from app.providers.base import MarketDataProvider
from app.providers.mock_market_provider import MockMarketDataProvider
from app.providers.yahoo_finance_provider import (
    YahooFinanceMarketDataProvider,
)


def create_market_data_provider(
    provider_name: str,
) -> MarketDataProvider:
    normalised_name = provider_name.strip().lower()

    if normalised_name == "mock":
        return MockMarketDataProvider()

    if normalised_name == "yahoo":
        return YahooFinanceMarketDataProvider()

    raise ValueError(
        f"Unsupported market provider: {provider_name}"
    )