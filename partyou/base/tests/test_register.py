# import pytest
# from django.urls import reverse
#
# from partyou.django_assertions import assert_contains
#
#
# @pytest.fixture
# def register_get_resp(client, db):
#     return client.get(reverse('login'), secure=True)
#
#
# def test_page_status(login_get_resp):
#     register_get_resp.status = 200
#
#
# @pytest.mark.parametrize(
#     'content',
#     [
#         '<form',
#         '<input type="text" name="username"',
#         '<input type="password" name="password"',
#         'type="submit"',
#     ]
# )
# def test_page_content(content, login_get_resp):
#     assert_contains(login_get_resp, content)
