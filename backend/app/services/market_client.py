from datetime import datetime, timezone


class MockMarketClient:

    def get_gold_price(self):
        return {
            "symbol": "XAUUSD",
            "price": 3350.50,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }