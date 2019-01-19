import pytest
from django.urls import reverse

from partyou.django_assertions import assert_contains


@pytest.fixture
def resp(client):
    resp = client.get(reverse('base:contato'))
    return resp


def test_status_code(resp):
    assert resp.status_code == 200


def test_title(resp):
    assert_contains(resp, '<title>Contato</title>')


def test_home_link(resp):
    assert_contains(resp, f'href="{reverse("base:contato")}">Contato</a>')


@pytest.mark.parametrize(
    'content', [
        'Brasil, Pernambuco',
        'Areias',
        '+55(081) 9 8888 7777',
        'Seg. à Sext. - 09:00 às 18:00hs',
        'suporte@suporte.com',
        'Envie-nos sua mensagem a qualquer momento!',
    ]
)
def test_contact_content(resp, content):
    assert_contains(resp, content)
