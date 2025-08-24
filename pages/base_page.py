# pages/base_page.py
"""Базовый класс Page Object для всех страниц."""
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import allure


class BasePage:
    """
    Базовый класс для всех Page Object классов.
    
    Args:
        driver: WebDriver instance
        timeout (int): Timeout for waits in seconds (default: 10)
    """
    
    def __init__(self, driver, timeout=10):
        self.driver = driver
        self.wait = WebDriverWait(driver, timeout)
    
    @allure.step("Найти элемент по локатору: {locator}")
    def find_element(self, locator, timeout=None):
        """Найти элемент на странице с ожиданием."""
        wait = self.wait if timeout is None else WebDriverWait(self.driver, timeout)
        return wait.until(EC.presence_of_element_located(locator))
    
    # ... остальные методы ...