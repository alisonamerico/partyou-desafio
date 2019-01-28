import pytest
from django.urls import reverse

from partyou.django_assertions import assert_contains


@pytest.fixture
def resp(client, db):
    resp = client.get(reverse('catalog:product_list'))
    return resp


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, '| PartyouDesafio')
