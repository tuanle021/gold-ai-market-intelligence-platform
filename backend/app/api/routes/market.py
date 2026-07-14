from fastapi import APIRouter, Depends

from app.api.dependencies import (
    get_gold_futures_service,
    get_gold_spot_service,
)
from app.schemas.market import GoldPriceResponse
from app.services.market_data import MarketDataService


router = APIRouter()


@router.get(
    "/gold",
    response_model=GoldPriceResponse,
    deprecated=True
)
def get_gold_price(
    service: MarketDataService = Depends(
        get_gold_futures_service
    ),
) -> GoldPriceResponse:
    """Backward-compatible gold futures endpoint."""
    return service.get_gold_price()


@router.get(
    "/gold/futures",
    response_model=GoldPriceResponse,
)
def get_gold_futures_price(
    service: MarketDataService = Depends(
        get_gold_futures_service
    ),
) -> GoldPriceResponse:
    return service.get_gold_price()


@router.get(
    "/gold/spot",
    response_model=GoldPriceResponse,
)
def get_gold_spot_price(
    service: MarketDataService = Depends(
        get_gold_spot_service
    ),
) -> GoldPriceResponse:
    return service.get_gold_price()