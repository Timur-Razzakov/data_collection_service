# import pytest
# import requests
# from django import urls
#
# base_url = 'http://localhost:8000'
#
#
# @pytest.mark.parametrize('param', ['registration',
#                                    'login',
#                                    'home',
#                                    'vacant_list'])
# def test_render_views(param):
#     """проверяем статус страниц"""
#     temp_url = urls.reverse(param)  # возвращает относительный адрес (uri)
#     response = requests.get(base_url + temp_url)
#     assert response.status_code == 200
#
