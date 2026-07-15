from datetime import datetime

from fastapi import HTTPException, Query, status
from pydantic import ValidationError
from app.core.config import settings
from app.providers.factory import create_market_data_provider
from app.providers.twelve_data_provider import TwelveDataMarketDataProvider
from app.services.market_data import MarketDataService
from app.providers.yahoo_finance_provider import (
    YahooFinanceMarketDataProvider,
)
from app.models.market_instrument import MarketInstrument
from app.models.market_interval import MarketInterval
from app.schemas.market import HistoricalMarketDataRequest


def get_gold_futures_service() -> MarketDataService:
    provider = create_market_data_provider(
        settings.market_provider
    )

    return MarketDataService(
        provider=provider
    )

def get_gold_futures_historical_service() -> MarketDataService:
    return MarketDataService(
        provider=YahooFinanceMarketDataProvider()
    )


def get_gold_spot_service() -> MarketDataService:
    provider = TwelveDataMarketDataProvider(
        api_key=settings.twelve_data_api_key,
        base_url=settings.twelve_data_base_url,
    )

    return MarketDataService(
        provider=provider
    )

def get_gold_futures_historical_request(
    interval: MarketInterval = Query(
        default=MarketInterval.FIVE_MINUTES,
        description="Historical candle interval",
    ),
    start_time: datetime = Query(
        ...,
        description="UTC start time in ISO 8601 format",
    ),
    end_time: datetime = Query(
        ...,
        description="UTC end time in ISO 8601 format",
    ),
) -> HistoricalMarketDataRequest:
    try:
        return HistoricalMarketDataRequest(
            symbol=MarketInstrument.GOLD_FUTURES,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=error.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            ),
        ) from error
    
def get_gold_spot_historical_service() -> MarketDataService:
    return MarketDataService(
        provider=TwelveDataMarketDataProvider(
            api_key=settings.twelve_data_api_key,
            base_url=settings.twelve_data_base_url,
        )
    )

def get_gold_spot_historical_request(
    interval: MarketInterval = Query(
        default=MarketInterval.FIVE_MINUTES,
        description="Historical candle interval",
    ),
    start_time: datetime = Query(
        ...,
        description="UTC start time in ISO 8601 format",
    ),
    end_time: datetime = Query(
        ...,
        description="UTC end time in ISO 8601 format",
    ),
) -> HistoricalMarketDataRequest:
    try:
        return HistoricalMarketDataRequest(
            symbol=MarketInstrument.GOLD_SPOT,
            interval=interval,
            start_time=start_time,
            end_time=end_time,
        )
    except ValidationError as error:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
            detail=error.errors(
                include_url=False,
                include_input=False,
                include_context=False,
            ),
        ) from error