from pydantic import BaseModel, ConfigDict

from app.models.instrument import Instrument


class InstrumentDefinition(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    instrument: Instrument
    market_data_provider: str
    provider_symbol: str

    supports_latest: bool = True
    supports_history: bool = True
    supports_sentiment: bool = False