import pytest

from app.models.instrument_code import InstrumentCode
from app.services.instrument_service import (
    InstrumentService,
)
from app.instruments.definitions import GOLD_FUTURES, GOLD_SPOT
from app.instruments.registry import list_instrument_definitions, INSTRUMENT_REGISTRY

service = InstrumentService()


def test_service_resolves_definition():
    service = InstrumentService()

    result = service.resolve_definition("XAUUSD")

    assert result == GOLD_SPOT


def test_service_lists_instruments():
    service = InstrumentService()

    assert service.list_instruments() == [
        GOLD_SPOT,
        GOLD_FUTURES,
    ]

def test_list_instruments_returns_registered_definitions():
    definitions = list_instrument_definitions()

    codes = {
        definition.instrument.code
        for definition in definitions
    }

    assert InstrumentCode.GOLD_SPOT in codes
    assert InstrumentCode.GOLD_FUTURES in codes