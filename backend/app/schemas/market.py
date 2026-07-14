from datetime import datetime

from pydantic import BaseModel
from app.models.market_instrument import MarketInstrument


class GoldPriceResponse(BaseModel):
    symbol: MarketInstrument
    price: float
    currency: str
    timestamp: datetime