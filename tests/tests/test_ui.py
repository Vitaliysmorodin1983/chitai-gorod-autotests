"""UI тесты для сайта Читай Город.

Тесты проверяют основные функциональные элементы главной страницы:
- Загрузка страницы
- Наличие ключевых элементов интерфейса
- Базовая функциональность
"""
import allure
import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL


@allure.epic("UI Тесты")
@allure.feature("Читай Город - Главная страница")
@allure.story("Проверка базовой функциональности главной страницы")
class TestChitaiGorodUI:
    """Test class for Chitai Gorod main page UI tests."""
    
    @allure.title("TC-UI-001: Загрузка главной страницы")
    @allure.severity(allure.severity_level.BLOCKER)
    @allure.description("""
    **Цель:** Проверить корректную загрузку главной страницы сайта.
    
    **Шаги:**
    1. Открыть главную страницу
    2. Проверить заголовок страницы
    3. Проверить URL страницы
    
    **Ожидаемый результат:**
    - Страница загружается без ошибок
    - Заголовок содержит название сайта
    - URL соответствует ожидаемому
    """)
    def test_main_page_load(self, driver):
        """Проверить загрузку главной страницы."""
        with allure.step("Открыть главную страницу сайта"):
            driver.get(BASE_URL)
        
        with allure.step("Проверить заголовок страницы содержит 'читай'"):
            assert "читай" in driver.title.lower()
        
        with allure.step("Проверить URL страницы содержит 'chitai-gorod'"):
            assert "chitai-gorod" in driver.current_url
    
    @allure.title("TC-UI-002: Проверка логотипа сайта")
    @allure.severity(allure.severity_level.CRITICAL)
    @allure.description("""
    **Цель:** Проверить наличие и видимость логотипа сайта.
    
    **Шаги:**
    1. Найти логотип по различным селекторам
    2. Проверить что логотип отображается
    
    **Ожидаемый результат:**
    - Логотип сайта присутствует на странице
    - Логотип видим пользователю
    """)
    def test_site_logo(self, driver):
        """Проверить наличие логотипа сайта."""
        logo_selectors = [
            "[class*='logo']",
            "[class*='header'] [class*='logo']", 
            "img[alt*='Читай']",
            "img[alt*='Читай-город']",
            "a[href='/'] img"
        ]
        
        logo_found = False
        for selector in logo_selectors:
            with allure.step(f"Поиск логотипа по селектору: {selector}"):
                try:
                    wait = WebDriverWait(driver, 3)
                    logo = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, selector)))
                    if logo.is_displayed():
                        logo_found = True
                        allure.attach(
                            f"Логотип найден по селектору: {selector}",
                            name="logo_found",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        break
                except Exception as e:
                    continue
        
        with allure.step("Проверить что логотип найден и отображается"):
            assert logo_found, "Логотип сайта не найден"

    # ... остальные тесты с аналогичной документацией ...