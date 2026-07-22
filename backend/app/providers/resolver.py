from app.core.config import settings
from app.models.instrument_definition import InstrumentDefinition
from app.providers.base import MarketDataProvider
from app.providers.mock_market_provider import MockMarketDataProvider
from app.providers.twelve_data_provider import TwelveDataMarketDataProvider
from app.providers.yahoo_finance_provider import YahooFinanceMarketDataProvider


def resolve_market_data_provider(
    instrument: InstrumentDefinition,
) -> MarketDataProvider:
    provider_name = instrument.market_data_provider

    if provider_name == "yahoo":
        return YahooFinanceMarketDataProvider()

    if provider_name == "twelve_data":
        return TwelveDataMarketDataProvider(
            api_key=settings.twelve_data_api_key,
            base_url=settings.twelve_data_base_url,
        )

    if provider_name == "mock":
        return MockMarketDataProvider()

    raise ValueError(
        f"Unsupported market data provider: {provider_name}"
    )