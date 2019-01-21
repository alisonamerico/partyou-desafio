import pytest
from django.urls import reverse

from partyou.django_assertions import assert_contains


@pytest.fixture
def resp(client):
    resp = client.get(reverse('base:home'))
    return resp


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, '<title>PartyouDesafio</title>')


def test_home_link(resp):
    assert_contains(resp, f'href="{reverse("base:home")}">PartyouDesafio</a>')


@pytest.mark.parametrize(
    'content', [
        'One Page Wonder',
        'Will Rock Your Socks Off',
        'For those about to rock...',
        'We salute you!',
        'Let there be rock!',
    ]
)
def test_home_content(resp, content):
    assert_contains(resp, content)
