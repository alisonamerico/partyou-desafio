# import pytest
# from django.test import Client
# from django.urls import reverse
#
# from partyou.django_assertions import assert_contains
#
#
# @pytest.fixture
# def resp_without_user(client):
#     return client.get(reverse('moveis:new'))
#
#
# @pytest.fixture
# def user(django_user_model):
#     usr = django_user_model(name='Alison')
#     usr.save()
#     return usr
#
#
# @pytest.fixture
# def resp(user, client: Client):
#     client.force_login(user)
#     return resp_without_user(client)
#
#
# def test_status_code_user_not_logged(resp_without_user):
#     assert 302 == resp_without_user.status_code
#
#
# def test_status_code_user_logged(resp):
#     assert 200 == resp.status_code
#
#
# @pytest.mark.parametrize(
#     'content', [
#         '<input type="text" name="titulo"',
#         '<input type="number" name="preco"',
#         '<textarea name="descricao"',
#         '<button type="submit"',
#         'csrfmiddlewaretoken',
#     ]
# )
# def test_form_inputs(resp, content):
#     assert_contains(resp, content)
#
#
# def test_form_action(resp):
#     assert_contains(resp, f'''<form method="post" action="{reverse('produtos:create')}"''')
