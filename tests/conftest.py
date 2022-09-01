import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


@pytest.fixture
def create_user(request):
    request.cls.user_data = {
        'email': 'razzakov3.com',
        'password': '123',
        'specialty': 'python',
        'city': 'moskva',
    }


# fixture for Chrome
@pytest.fixture(scope='class')
def chrome_driver_init(request):
    _options = Options()
    _options.add_argument("--window-size=1920,1080")
    _options.add_argument("--proxy-bypass-list=*")
    _options.add_argument('--headless')
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=_options)
    request.cls.driver = driver

    yield
    driver.close()

