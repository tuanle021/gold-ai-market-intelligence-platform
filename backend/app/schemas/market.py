from datetime import datetime

from pydantic import BaseModel


class GoldPriceResponse(BaseModel):
    symbol: str
    price: float
    currency: str
    timestamp: datetime