from fastapi import APIRouter

from app.schemas.market import GoldPriceResponse
from app.services.market_data import market_data_service

router = APIRouter(
    prefix="/market",
    tags=["Market"]
)


@router.get(
    "/gold",
    response_model=GoldPriceResponse
)
def get_gold_price():
    return market_data_service.get_gold_price()