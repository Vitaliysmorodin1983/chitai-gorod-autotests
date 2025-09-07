import allure
import pytest
import requests
from config import BASE_URL


@allure.epic("API Тесты")
@allure.feature("Читай Город - API Проверки")
class TestChitaiGorodAPI:

    @allure.title("TC-API-001: Проверка доступности главной страницы")
    @allure.severity(allure.severity_level.BLOCKER)
    @pytest.mark.api
    def test_main_page_status(self):
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(BASE_URL, headers=headers, timeout=10)

        with allure.step("Проверить статус-код ответа"):
            assert response.status_code in [200, 403], f"Неверный статус: {response.status_code}"

        with allure.step("Проверить, что это не защита DDOS"):
            if "ddos-guard" in response.text.lower():
                pytest.skip("Ответ от DDOS Guard — контент недоступен")

        with allure.step("Проверить наличие ключевых слов в HTML"):
            assert any(word in response.text.lower() for word in ["книга", "акция", "читай"]), "Контент не соответствует ожиданиям"

    @allure.title("TC-API-002: Проверка редиректа при переходе на /login")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_login_redirect(self):
        url = BASE_URL.rstrip("/") + "/login"
        response = requests.get(url, allow_redirects=False, timeout=10)

        with allure.step("Проверить статус-код"):
            if response.status_code == 403:
                pytest.skip("DDOS Guard блокирует редирект")

            assert response.status_code in [301, 302], f"Ожидался редирект, но статус: {response.status_code}"

        with allure.step("Проверить заголовок Location"):
            assert "Location" in response.headers
            assert "/auth" in response.headers["Location"] or "login" in response.headers["Location"]

    @allure.title("TC-API-003: Проверка заголовков ответа")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_response_headers(self):
        response = requests.get(BASE_URL, timeout=10)

        with allure.step("Проверить наличие стандартных заголовков"):
            assert "Server" in response.headers
            assert "Content-Type" in response.headers
            assert response.headers["Content-Type"].startswith("text/html")

    @allure.title("TC-API-004: Проверка времени ответа и размера контента")
    @allure.severity(allure.severity_level.NORMAL)
    @pytest.mark.api
    def test_response_time_and_size(self):
        response = requests.get(BASE_URL, timeout=10)

        with allure.step("Проверить, что ответ пришёл менее чем за 5 секунд"):
            assert response.elapsed.total_seconds() < 5, f"Медленный ответ: {response.elapsed.total_seconds()} сек"

        with allure.step("Проверить, что это не защита DDOS"):
            if "ddos-guard" in response.text.lower():
                pytest.skip("Контент от DDOS Guard — размер невалиден")

        with allure.step("Проверить, что контент не пустой"):
            assert len(response.content) > 1000, f"Контент слишком мал: {len(response.content)} байт"

    @allure.title("TC-API-005: Проверка доступности страницы каталога")
    @allure.severity(allure.severity_level.CRITICAL)
    @pytest.mark.api
    def test_catalog_page(self):
        url = BASE_URL.rstrip("/") + "/catalog"
        response = requests.get(url, timeout=10)

        with allure.step("Проверить статус-код"):
            assert response.status_code in [200, 403, 404], f"Неверный статус: {response.status_code}"

        with allure.step("Проверить, что это не защита DDOS"):
            if "ddos-guard" in response.text.lower():
                pytest.skip("Страница каталога недоступна — DDOS Guard")

        with allure.step("Проверить наличие ключевых элементов в HTML"):
            assert any(word in response.text.lower() for word in ["жанр", "каталог", "книги"]), "Страница каталога не содержит ожидаемых элементов"

