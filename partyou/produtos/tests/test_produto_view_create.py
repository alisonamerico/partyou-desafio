# import pytest
# from django.test import Client
# from django.urls import reverse
#
# from partyou.produtos.forms import ProdutoForm
# from partyou.produtos.models import Produto
#
#
# @pytest.fixture
# def resp_without_user(client: Client):
#     return client.post(
#         reverse('produtos:create'),
#         data={
#             'titulo': 'Camisa Amarela',
#             'preco': '100',
#             'descricao': 'Camisa amarela de linho',
#         }
#     )
#
#
# # @pytest.fixture
# # def user(django_user_model):
# #     usr = django_user_model(name='admin')
# #     usr.save()
# #     return usr
# #
# #
# # @pytest.fixture
# # def resp(user, client: Client):
# #     client.force_login(user)
# #     return resp_without_user(client)
# #
# #
# # @pytest.fixture
# # def resp_no_data(user, client: Client):
# #     client.force_login(user)
# #     return client.post(
# #         reverse('produtos:create'),
# #         data={
# #             'titulo': '',
# #             'preco': '',
# #             'descricao': '',
# #         }
# #     )
#
#
# def test_status_code_user_not_logged(resp_without_user):
#     assert resp_without_user.url.startswith(reverse('login'))
#
#
# def test_status_code_user_logged(resp):
#     assert resp.url.startswith(reverse('produtos:index'))
#
#
# def test_produto_salvo(resp):
#     assert Produto.objects.exists()
#
#
# def test_status_code_for_error(resp_no_data):
#     assert 400 == resp_no_data.status_code
#
#
# def test_status_invalid_data_in_context(resp_no_data):
#     assert isinstance(resp_no_data.context['form'], ProdutoForm)
