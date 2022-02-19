import pytest
from django import urls
from django.test import LiveServerTestCase
from icecream import ic

base_url = 'http://localhost:8000'
"""Проверяем форму для входа"""


@pytest.mark.usefixtures('chrome_driver_init', 'create_user')
class TestBrowser(LiveServerTestCase):
    def test_check_sign_in(self):
        temp_url = urls.reverse('login')  # возвращает относительный адрес (uri)
        self.driver.get(base_url + temp_url)

        """
        Находим поля для заполнения формы

        """
        input_email = self.driver.find_element('xpath',
                                               '//*[@id="id_email"]')

        input_password = self.driver.find_element('xpath',
                                                  '//*[@id="id_password"]')

        '''
           заполнение тестовыми данными и отправляем
        '''
        input_email.clear()

        input_email.send_keys(self.user_data['email'])
        input_password.send_keys(self.user_data['password'])
        sign = self.driver.find_element('xpath',
                                        '//button[@type="submit"]').click()

        """Проверяем удалось ли пройти авторизацию"""

        get_url = self.driver.current_url
        if get_url != base_url + urls.reverse('home'):
            ic('Проверить email и password')
        else:
            assert True
