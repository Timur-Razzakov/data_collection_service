import json
import sys

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def main_scraping_part(
        page_count: int,
        city: str,
        speciality: str):
    _options = Options()
    # _options.add_argument("--window-size=1920,1080")
    # _options.add_argument("--proxy-bypass-list=*")
    # _options.add_argument('--headless')

    driver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=_options)

    errors = []
    all_href = set()
    results = []

    '''
        Самодельная универсальная функция для ожидания
    '''

    def Wait(time, what_by, second_param):
        return WebDriverWait(driver, time).until(
            ES.presence_of_element_located((what_by, second_param))
        )

    driver.get('https://remote-job.ru')  # Получение страницы !

    """   
    Поиск нужного поля
    """
    try:
        input_prof = driver.find_element('xpath',
                                         '//*[@id="search_query"]')
        submit_button = driver.find_element('xpath',
                                            '//*[@class="btn btn-success btn-toggle"]')
    except TimeoutError:
        # {f'{DARK_PURPLE}Could not locate {ENDE}{INBOX}{LIGHT_BLUE}"xpath=//*[@id="search_query"]'})
        errors.append({f'Could not locate "xpath=//*[@id="search_query"]'})
    '''
       заполнение ДАННЫМИ! и отправка
    '''
    input_prof.clear()
    input_prof.send_keys('{0}  {1}'.format(city, speciality))
    submit_button.click()

    """ Кнопка для выбора вакансий сегодняшнего дня"""

    date_button = Wait(10, By.CSS_SELECTOR,
                       '.col-md-12.min-width > button:nth-child(2)')
    date_button.click()
    '''
    циклы для получения ссылок на вакансии для подробного парсинга
    '''

    try:
        all_jobs = Wait(10, By.CSS_SELECTOR, '.contentContainer > div:nth-child(3) > div')
    except Exception:
        errors.append({f'vacancies is EMPTY'})
    # получаем все вакансии
    try:

        all_jobs = driver.find_elements('xpath', '//*[@class="vacancy_item"]')
        for job in all_jobs:
            # получение WebElement-ты ссылок
            urls = job.find_elements('xpath', '//h3/a[@target="_blank"]')
            for item in urls:
                # получаем чисты ссылки на вакансии
                href = item.get_attribute('href')
                all_href.add(href)
    except Exception:
        data = {
            "errors": 'vacancies is EMPTY',
            "city": city,
            'speciality': speciality,
        }
        errors.append(data)
    # проходимся по всем ссылкам из списка и берём нужные данные
    for url_job in all_href:
        # открываем новую вкладку
        driver.execute_script("window.open('about:blank', 'tab2');")
        driver.switch_to.window("tab2")
        driver.get(url_job)
        '''
        Locate Fields
        '''
        try:
            url = url_job
            title = driver.find_element('xpath', '//div[@class="col-md-12"]/h1').text
            description = driver.find_element('xpath',
                                              '//div/div[@class="row p-y-3"]/div[@class="col-md-12"]').text
            salary = driver.find_element('xpath', '//div/div[@class="row m-y-1"]/div[@class="col-md-4"]').text
            company_name = driver.find_element('xpath', '//div[@class="col-md-12"]/h4').text
        except TimeoutError:
            # ({DARK_PURPLE: {'url': url, 'title': "Div does not exists"},
            # f'{ENDE}{INBOX}{LIGHT_BLUE} Functions not found': None})
            errors.append({'url': url, 'title': "Div does not exists"})

        results.append({
            'url': url,
            'title': title,
            'description': description,
            'company_name': company_name,
            'salary': salary,
            'city': city,
            'speciality': speciality
        })

    """
    scroll
    """
    # переходим на первую вкладку
    parent_handle = driver.window_handles[0]
    driver.switch_to.window(parent_handle)
    # Scroll down to bottom
    driver.execute_script(
        "window.scrollTo(0, document.body.scrollHeight/1.2);")
    # ожидаем загрузки страницы
    try:
        progress_bar = WebDriverWait(driver, 3).until(
            ES.presence_of_element_located((By.LINK_TEXT, '2'))
        )
        progress_bar.click()
    except Exception:
        pass

    with open("results.json", "w", encoding="utf=8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)
    # with open("errors.json", "w", encoding="utf=8") as file:
    #     json.dump(errors, file, indent=4, ensure_ascii=False)

    return results, errors

#
# '''
# Очень важно иметь точку входа.
# '''
#
#
# def entry(
#         city: str,
#         speciality: str) -> None:
#     start_t = time.time()
#     main_scraping_part( city, speciality)
#     print(f'Time taken => {time.time() - start_t}')
#
#
# if __name__ == '__main__':
#     main_scraping_part(1, 'Москва', 'Python')
