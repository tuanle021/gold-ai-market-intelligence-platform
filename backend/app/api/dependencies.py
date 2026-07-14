from app.core.config import settings
from app.providers.factory import create_market_data_provider
from app.providers.twelve_data_provider import TwelveDataMarketDataProvider
from app.services.market_data import MarketDataService


def get_gold_futures_service() -> MarketDataService:
    provider = create_market_data_provider(
        settings.market_provider
    )

    return MarketDataService(
        provider=provider
    )


def get_gold_spot_service() -> MarketDataService:
    provider = TwelveDataMarketDataProvider(
        api_key=settings.twelve_data_api_key,
        base_url=settings.twelve_data_base_url,
    )

    return MarketDataService(
        provider=provider
    )