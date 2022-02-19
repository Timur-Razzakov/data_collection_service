import pytest
from django import urls
from django.test import LiveServerTestCase
from icecream import ic
from validate_email import validate_email

base_url = 'http://localhost:8000'

"""Проверяем работоспособность регистрационной формы"""


@pytest.mark.usefixtures('chrome_driver_init', 'create_user')
class TestBrowser(LiveServerTestCase):
    def test_check_registration(self):
        temp_url = urls.reverse('registration')  # возвращает относительный адрес (uri)
        self.driver.get(base_url + temp_url)
        is_valid = validate_email(self.user_data['email'])

        if not is_valid:
            ic(f'Указанная почта неверного формата!! {self.user_data["email"]}')
        else:
            assert True
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

        input_email.send_keys(self.user_data['email'])
        input_password.send_keys(self.user_data['password'])
        repeat_password.send_keys(self.user_data['password'])

        select_city = self.driver.find_element('xpath',
                                               f'//option[@value="{self.user_data["city"]}"]').click()
        select_specialty = self.driver.find_element('xpath',
                                                    f'//option[@value="{self.user_data["specialty"]}"]').click()

        registr = self.driver.find_element('xpath',
                                           '//button[@type="submit"]').click()

        """Проверяем зарегистрировался ли пользователь"""

        resoult = self.driver.find_element('xpath',
                                           '//h4[@class="my-2"]').text
        if 'Приветствуем' in resoult:
            assert 'Регистрация удалась'
        else:
            ic('Пользователь с такой почтой уже существует')
