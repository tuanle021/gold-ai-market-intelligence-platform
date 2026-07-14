from datetime import datetime, timezone
from unittest.mock import MagicMock, patch

import pandas as pd
import pytest

from app.providers.yahoo_finance_provider import (
    YahooFinanceMarketDataProvider,
)


def test_yahoo_provider_returns_normalised_gold_price():
    mock_history = pd.DataFrame(
        {
            "Close": [4097.2001953125],
        },
        index=[
            pd.Timestamp(
                datetime(2026, 7, 14, 15, 20, tzinfo=timezone.utc)
            )
        ],
    )

    with patch(
        "app.providers.yahoo_finance_provider.yf.Ticker"
    ) as mock_ticker_class:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = mock_history
        mock_ticker_class.return_value = mock_ticker

        provider = YahooFinanceMarketDataProvider()
        result = provider.get_gold_price()

    assert result.symbol == "GC=F"
    assert result.price == 4097.20
    assert result.currency == "USD"
    assert result.timestamp.tzinfo is not None

    mock_ticker.history.assert_called_once_with(
        period="1d",
        interval="5m",
    )

def test_yahoo_provider_raises_error_when_no_data_returned():
    empty_history = pd.DataFrame()

    with patch(
        "app.providers.yahoo_finance_provider.yf.Ticker"
    ) as mock_ticker_class:
        mock_ticker = MagicMock()
        mock_ticker.history.return_value = empty_history
        mock_ticker_class.return_value = mock_ticker

        provider = YahooFinanceMarketDataProvider()

        with pytest.raises(
            ValueError,
            match="Yahoo Finance returned no gold price data",
        ):
            provider.get_gold_price()