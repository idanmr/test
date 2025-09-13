import pytest

from wallets.coins_factory import CoinsFactory
from wallets.enums import Coins
from wallets.models import LilA2BThroughput


@pytest.fixture
def mock_coin():
    return LilA2BThroughput()


def test_create_coin(mock_coin):
    coin = CoinsFactory.create_coin(Coins.LilA2BThroughput)
    assert coin == mock_coin
