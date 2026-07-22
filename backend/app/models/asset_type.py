from enum import StrEnum


class AssetType(StrEnum):
    COMMODITY = "commodity"
    FOREX = "forex"
    EQUITY = "equity"
    FUTURES = "futures"
    CRYPTO = "crypto"