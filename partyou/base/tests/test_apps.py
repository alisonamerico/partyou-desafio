
from partyou.base.apps import BaseConfig


def test_home():
    assert BaseConfig.name == 'base'
