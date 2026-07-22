from app.instruments.registry import (
    get_instrument_definition,
    list_instrument_definitions,
    resolve_instrument_definition,
)
from app.models.instrument_code import InstrumentCode
from app.models.instrument_definition import InstrumentDefinition


class InstrumentService:
    """Provides access to supported financial instruments."""

    def get_definition(
        self,
        instrument_code: InstrumentCode,
    ) -> InstrumentDefinition:
        return get_instrument_definition(
            instrument_code
        )

    def resolve_definition(
        self,
        raw_code: str,
    ) -> InstrumentDefinition:
        return resolve_instrument_definition(
            raw_code
        )

    def list_instruments(
        self,
    ) -> list[InstrumentDefinition]:
        return list_instrument_definitions()

instrument_service = InstrumentService()