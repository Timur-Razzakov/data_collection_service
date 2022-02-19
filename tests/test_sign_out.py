from django import urls


def test_user_logout(client):
    """Проверяем logout"""
    logout_url = urls.reverse('logout')
    resp = client.get(logout_url)
    assert resp.status_code == 302
    assert resp.url == urls.reverse('home')
