from fastapi import APIRouter

from app.schemas.market import GoldPriceResponse
from app.services.market_data import MarketDataService

router = APIRouter()

market_service = MarketDataService()

@router.get(
    "/gold",
    response_model=GoldPriceResponse
)
def get_gold_price():
    return market_service.get_gold_price()