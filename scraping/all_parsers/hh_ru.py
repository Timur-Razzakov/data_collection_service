import json
import sys
import time

from pyppeteer.errors import PageError
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as ES
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


def get_data(
        page_count: int,
        city: str,
        speciality: str):
    _options = Options()
    # _options.add_argument("--window-size=1920,1080")
    # _options.add_argument("--proxy-bypass-list=*")
    # _options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(),chrome_options=_options)
    st = time.time()
    driver.get('https://hh.uz')
    results = []
    errors = []
    '''
        Самодельная универсальная функция для ожидания
    '''

    def Wait(time, what_by, second_param):
        return WebDriverWait(driver, time).until(
            ES.presence_of_element_located((what_by, second_param))
        )

    """   
        Поиск нужного поля
    """
    try:
        input_prof = driver.find_element('xpath',
                                         '//input[@placeholder="Профессия, должность или компания"]')
        submit_button = driver.find_element('xpath',
                                            '//button[@data-qa="search-button"]')
    except TimeoutError:
        # {f'{DARK_PURPLE}Could not
        # locate {ENDE}{INBOX}{LIGHT_BLUE}"xpath=//input[@placeholder="Профессия, должность или компания"]'})
        errors.append({f'Could not locate "//input[@placeholder="Профессия, должность или компания"]'})

    '''
       заполнение ДАННЫМИ! и отправка
    '''
    input_prof.clear()
    input_prof.send_keys('{0}  {1}'.format(speciality, city))
    submit_button.click()

    """
        Проверяем не пустая ли страница
    """
    try:
        vacancies = Wait(10, By.CSS_SELECTOR, f'.bloko-column_m-9.bloko-column_l-13')
    except Exception:
        errors.append({f'vacancies is EMPTY'})

    i = 0
    while i < page_count:
        # получаем все вакансии
        try:
            vacancies = WebDriverWait(driver, 10) \
                .until(ES.presence_of_all_elements_located((By.CSS_SELECTOR, "div.vacancy-serp-item")))
        except Exception:
            data = {
                "errors": 'vacancies is EMPTY',
                "city": city,
                'speciality': speciality,
            }
            errors.append(data)
        try:
            for vacancy in vacancies:
                title = vacancy.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-serp__vacancy-title"]')
                company_name = vacancy.find_element(By.CSS_SELECTOR, 'a[data-qa="vacancy-serp__vacancy-employer"]')
                city = vacancy.find_element(By.CSS_SELECTOR, 'div[data-qa="vacancy-serp__vacancy-address"]')
                url = title.get_attribute('href')

                driver.execute_script("window.open('about:blank', 'tab2');")
                driver.switch_to.window("tab2")
                driver.get(url)

                try:
                    salary = driver.find_element(By.CSS_SELECTOR, 'div[data-qa^="vacancy-salary"]').text
                    description = driver.find_element(By.CSS_SELECTOR,
                                                      'div[data-qa="vacancy-description"]').text
                except Exception:
                    errors.append({f'description and salary is EMPTY'})

                driver.switch_to.window(driver.window_handles[0])

                data = {
                    "url": url,
                    "title": title.text,
                    "description": description,
                    "company_name": company_name.text,
                    "salary": salary,
                    "city": city.text,
                    'speciality': speciality,
                }
                results.append(data)

            i += 1
        except (TimeoutError, PageError):
            errors.append({'url': url, 'title': title})
        try:
            next_page_btn = Wait(10, By.CSS_SELECTOR, f'a[data-qa="pager-next"]')
            next_page_btn.click()
        except Exception:
            continue

    #
    with open("results_hh.json", "w", encoding="utf=8") as file:
        json.dump(results, file, indent=4, ensure_ascii=False)

    return results, errors

#
# if __name__ == '__main__':
#     get_data(1, 'Сочи', 'Python')