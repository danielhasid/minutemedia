
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
import pytest

@pytest.fixture(scope="function")
def chrome_driver():
    global driver
    options = webdriver.ChromeOptions()
    options.add_experimental_option("detach", True)
    chromepath = Service("C:/ChromeDriver/chromedriver.exe")
    driver = webdriver.Chrome(service=chromepath, options=options)
    driver.implicitly_wait(15)
    driver.maximize_window()
    driver.get("https://www.90min.com")
    yield driver
    driver.close()