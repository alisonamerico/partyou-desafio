# import pytest
# from django.urls import reverse
#
# from partyou.django_assertions import assert_contains
#
#
# @pytest.fixture
# def resp(client):
#     resp = client.get(reverse('base:contact'))
#     return resp
#
#
# def test_status_code(resp):
#     assert resp.status_code == 200
#
#
# def test_title(resp):
#     assert_contains(resp, 'Contato | PartyouDesafio')
#
#
# def test_home_link(resp):
#     assert_contains(resp, f'href="{reverse("base:contact")}">Contato</a>')
#
#
# @pytest.mark.parametrize(
#     'content', [
#         'Fale conosco',
#         'Nome',
#         'E-mail',
#         'Mensagem',
#     ]
# )
# def test_contact_content(resp, content):
#     assert_contains(resp, content)
