from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, model_validator
from app.models.market_instrument import MarketInstrument
from app.models.market_interval import MarketInterval


class GoldPriceResponse(BaseModel):
    symbol: MarketInstrument
    price: float
    currency: str
    timestamp: datetime

class MarketCandle(BaseModel):
    model_config = ConfigDict(
        extra="forbid",
    )

    symbol: MarketInstrument
    interval: MarketInterval
    timestamp: datetime

    open: float = Field(gt=0)
    high: float = Field(gt=0)
    low: float = Field(gt=0)
    close: float = Field(gt=0)

    volume: float | None = Field(
        default=None,
        ge=0,
    )

    @model_validator(mode="after")
    def validate_candle_prices(self) -> "MarketCandle":
        if self.high < self.low:
            raise ValueError(
                "Candle high must be greater than or equal to candle low"
            )

        if not self.low <= self.open <= self.high:
            raise ValueError(
                "Candle open must be between candle low and high"
            )

        if not self.low <= self.close <= self.high:
            raise ValueError(
                "Candle close must be between candle low and high"
            )

        if self.timestamp.tzinfo is None:
            raise ValueError(
                "Candle timestamp must be timezone-aware"
            )

        return self

class HistoricalMarketDataResponse(BaseModel):
    symbol: MarketInstrument
    interval: MarketInterval
    currency: str
    candles: list[MarketCandle]

class HistoricalMarketDataRequest(BaseModel):
    symbol: MarketInstrument
    interval: MarketInterval
    start_time: datetime
    end_time: datetime

    @model_validator(mode="after")
    def validate_time_range(
        self,
    ) -> "HistoricalMarketDataRequest":
        if self.start_time.tzinfo is None:
            raise ValueError(
                "Start time must be timezone-aware"
            )

        if self.end_time.tzinfo is None:
            raise ValueError(
                "End time must be timezone-aware"
            )

        if self.start_time >= self.end_time:
            raise ValueError(
                "Start time must be before end time"
            )

        return self