import pytest
import requests
from django import urls
from icecream import ic


def test_user_logout(client):
    """Проверяем выход"""
    logout_url = urls.reverse('logout')
    resp = client.get(logout_url)
    ic(resp.status_code)

    assert resp.status_code == 302
    assert resp.url == urls.reverse('home')
