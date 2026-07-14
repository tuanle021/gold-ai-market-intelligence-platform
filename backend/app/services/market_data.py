from app.services.market_client import MockMarketClient


class MarketDataService:

    def __init__(self):
        self.client = MockMarketClient()


    def get_gold_price(self):
        return self.client.get_gold_price()