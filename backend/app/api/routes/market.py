from fastapi import APIRouter

from app.services.market_data import MarketDataService

router = APIRouter()

market_service = MarketDataService()

@router.get("/gold")
def get_gold_price():
    return market_service.get_gold_price()