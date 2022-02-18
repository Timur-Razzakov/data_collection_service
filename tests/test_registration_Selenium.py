import pytest
from django import urls
from django.test import LiveServerTestCase
from icecream import ic

base_url = 'http://localhost:8000'

"""Проверяем работоспособность регистрационной формы"""
@pytest.mark.usefixtures('chrome_driver_init')
class TestBrowser(LiveServerTestCase):
    def test_check_registration(self):
        temp_url = urls.reverse('registration')  # возвращает относительный адрес (uri)
        self.driver.get(base_url + temp_url)

        """
        Находим поля для заполнения формы

        """
        input_email = self.driver.find_element('xpath',
                                               '//*[@id="id_email"]')

        input_password = self.driver.find_element('xpath',
                                                  '//*[@id="id_password"]')
        repeat_password = self.driver.find_element('xpath',
                                                   '//*[@id="id_password2"]')

        '''
           заполнение тестовыми данными и отправляем
        '''
        input_email.clear()
        input_email.send_keys('razzakov3@gmail.com')
        input_password.send_keys('123')
        repeat_password.send_keys('123')

        select_city = self.driver.find_element('xpath',
                                               '//option[@value="moskva"]').click()
        select_specialty = self.driver.find_element('xpath',
                                                    '//option[@value="java"]').click()

        registr = self.driver.find_element('xpath',
                                           '//button[@type="submit"]').click()

        """Проверяем зарегистрировался ли пользователь"""

        resoult = self.driver.find_element('xpath',
                                           '//h4[@class="my-2"]').text

        assert 'Приветствуем' in resoult
