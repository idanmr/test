from wallets.enums import Coins
from wallets.models import LilA2BThroughput, BaseCoin


class CoinsFactory:
    @staticmethod
    def create_coin(coin: str) -> BaseCoin:
        if coin == Coins.LilA2BThroughput:
            return LilA2BThroughput()
        else:
            raise ValueError(f"Unsupported coin: {coin}")
