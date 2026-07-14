from datetime import timezone
from unittest.mock import MagicMock, patch

import httpx
import pytest

from app.providers.twelve_data_provider import (
    TwelveDataMarketDataProvider,
)


def test_twelve_data_provider_returns_normalised_spot_price():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "price": "4056.79513",
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ) as mock_get:
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        result = provider.get_gold_price()

    assert result.symbol == "XAU/USD"
    assert result.price == 4056.80
    assert result.currency == "USD"
    assert result.timestamp.tzinfo == timezone.utc

    mock_get.assert_called_once_with(
        "https://test.twelvedata.com/price",
        params={
            "symbol": "XAU/USD",
            "apikey": "test-api-key",
        },
        timeout=10.0,
    )

def test_twelve_data_provider_requires_api_key():
    with pytest.raises(
        ValueError,
        match="Twelve Data API key is not configured",
    ):
        TwelveDataMarketDataProvider(
            api_key="",
            base_url="https://test.twelvedata.com",
        )

def test_twelve_data_provider_raises_error_for_provider_error_response():
    mock_response = MagicMock()
    mock_response.json.return_value = {
        "status": "error",
        "code": 401,
        "message": "Invalid API key",
    }
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="invalid-key",
            base_url="https://test.twelvedata.com",
        )

        with pytest.raises(
            ValueError,
            match="Invalid API key",
        ):
            provider.get_gold_price()

def test_twelve_data_provider_raises_error_when_price_is_missing():
    mock_response = MagicMock()
    mock_response.json.return_value = {}
    mock_response.raise_for_status.return_value = None

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        with pytest.raises(
            ValueError,
            match="Twelve Data response did not contain a price",
        ):
            provider.get_gold_price()
            
def test_twelve_data_provider_propagates_http_error():
    mock_request = httpx.Request(
        "GET",
        "https://test.twelvedata.com/price",
    )

    mock_response = httpx.Response(
        status_code=500,
        request=mock_request,
    )

    with patch(
        "app.providers.twelve_data_provider.httpx.get",
        return_value=mock_response,
    ):
        provider = TwelveDataMarketDataProvider(
            api_key="test-api-key",
            base_url="https://test.twelvedata.com",
        )

        with pytest.raises(httpx.HTTPStatusError):
            provider.get_gold_price()