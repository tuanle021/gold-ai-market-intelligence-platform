from pydantic import BaseModel, ConfigDict

from app.models.asset_type import AssetType
from app.models.instrument_code import InstrumentCode


class Instrument(BaseModel):
    model_config = ConfigDict(
        frozen=True,
        extra="forbid",
    )

    code: InstrumentCode
    display_symbol: str
    name: str
    asset_type: AssetType
    base_asset: str | None = None
    quote_asset: str | None = None