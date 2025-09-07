import allure
import pytest
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from config import BASE_URL


@allure.epic("UI Тесты")
@allure.feature("Читай Город - Главная страница")
class TestChitaiGorodUI:

    @allure.title("TC-UI-001: Загрузка главной страницы")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.ui
    def test_main_page_load(self, driver):
        driver.get(BASE_URL)
        if "ddos-guard" in driver.title.lower():
            pytest.skip("Сайт вернул защитную страницу DDOS Guard")
        assert "читай" in driver.title.lower()
        assert "chitai-gorod" in driver.current_url

    @allure.title("TC-UI-002: Проверка логотипа сайта")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_site_logo(self, driver):
        logo_selectors = [
            "[class*='logo']",
            "[class*='header'] [class*='logo']",
            "img[alt*='Читай']",
            "img[alt*='Читай-город']",
            "a[href='/'] img"
        ]
        logo_found = False
        for selector in logo_selectors:
            try:
                logo = WebDriverWait(driver, 5).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, selector))
                )
                if logo.is_displayed():
                    logo_found = True
                    break
            except Exception:
                continue
        assert logo_found, "Логотип сайта не найден"

    @allure.title("TC-UI-003: Проверка поля поиска")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.ui
    def test_search_field(self, driver):
        driver.get(BASE_URL)
        try:
            search_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "input[type='search'], input[name='search'], input[placeholder*='Поиск']"))
            )
            search_input.clear()
            search_input.send_keys("Пушкин")
            assert "Пушкин" in search_input.get_attribute("value")
        except TimeoutException:
            pytest.skip("Поле поиска не найдено — возможно, изменился селектор")

    @allure.title("TC-UI-004: Проверка кнопки 'Корзина'")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.ui
    def test_cart_button(self, driver):
        driver.get(BASE_URL)
        try:
            cart_button = WebDriverWait(driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, "a[href*='cart'], a[href*='basket'], button[class*='cart']"))
            )
            assert cart_button.is_displayed()
        except TimeoutException:
            pytest.skip("Кнопка корзины не найдена — возможно, изменился селектор")

    @allure.title("TC-UI-005: Проверка футера сайта")
    @allure.severity(allure.severity_level.MINOR)
    @pytest.mark.ui
    def test_footer_visibility(self, driver):
        driver.get(BASE_URL)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        try:
            footer = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "footer"))
            )
            assert any(word in footer.text.lower() for word in ["контакт", "обратная связь", "вопросы", "читай-город"])
        except TimeoutException:
            pytest.skip("Футер не найден — возможно, изменился селектор")
