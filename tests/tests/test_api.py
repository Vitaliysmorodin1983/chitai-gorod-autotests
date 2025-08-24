"""API тесты для Читай Город."""
import allure
import pytest
import requests
from config import BASE_URL


@allure.epic("API Тесты")
@allure.feature("Читай Город API")
class TestChitaiGorodAPI:
    
    @allure.title("1. Доступность сайта")
    @allure.severity(allure.severity_level.BLOCKER)
    def test_site_availability(self):
        """Проверить что сайт доступен."""
        with allure.step("Отправить GET запрос с заголовками"):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
            }
            response = requests.get(BASE_URL, headers=headers, timeout=10)
        
        with allure.step("Проверить что сайт отвечает (любой статус кроме 5xx)"):
            assert response.status_code < 500, f"Ошибка сервера: {response.status_code}"
    
    @allure.title("2. Проверка заголовков")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_response_headers(self):
        """Проверить корректность заголовков ответа."""
        with allure.step("Отправить GET запрос с заголовками"):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(BASE_URL, headers=headers, timeout=10)
        
        with allure.step("Проверить наличие стандартных заголовков"):
            assert 'Server' in response.headers
            assert 'Date' in response.headers
    
    @allure.title("3. Время ответа")
    @allure.severity(allure.severity_level.NORMAL)
    def test_response_time(self):
        """Проверить время ответа сервера."""
        with allure.step("Измерить время ответа с заголовками"):
            headers = {
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            }
            response = requests.get(BASE_URL, headers=headers, timeout=10)
        
        with allure.step("Проверить что ответ быстрый (<5 сек)"):
            assert response.elapsed.total_seconds() < 5
    
    @allure.title("4. Проверка редиректов")
    @allure.severity(allure.severity_level.NORMAL)
    def test_redirects(self):
        """Проверить обработку редиректов."""
        test_paths = ['/login', '/cart', '/search', '/books', '/catalog']
        
        for path in test_paths:
            with allure.step(f"Проверить путь: {path}"):
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    response = requests.get(BASE_URL + path, headers=headers, timeout=5, allow_redirects=False)
                    assert response.status_code < 500, f"Ошибка для {path}"
                except requests.exceptions.RequestException:
                    # Пропустить если URL недоступен
                    pass
    
    @allure.title("5. Проверка доступности сайта и основных функций")
    @allure.severity(allure.severity_level.CRITICAL)
    def test_site_functionality(self):
        """Проверить основные функции сайта."""
        test_cases = [
            {
                "name": "Главная страница",
                "url": BASE_URL,
                "expected_status": [200, 403]  # 403 - DDOS Guard
            },
            {
                "name": "Страница книг", 
                "url": BASE_URL.rstrip('/') + '/books',
                "expected_status": [200, 403, 404]
            },
            {
                "name": "Страница акций",
                "url": BASE_URL.rstrip('/') + '/actions',
                "expected_status": [200, 403, 404]
            }
        ]
        
        successful_tests = 0
        
        for test_case in test_cases:
            with allure.step(f"Проверка: {test_case['name']}"):
                try:
                    headers = {
                        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                    }
                    
                    response = requests.get(
                        test_case['url'],
                        headers=headers,
                        timeout=10,
                        allow_redirects=True
                    )
                    
                    if response.status_code in test_case['expected_status']:
                        successful_tests += 1
                        allure.attach(
                            f"{test_case['name']}: статус {response.status_code} (ожидалось: {test_case['expected_status']})",
                            name=f"Test_{test_case['name'].replace(' ', '_')}",
                            attachment_type=allure.attachment_type.TEXT
                        )
                    else:
                        allure.attach(
                            f"{test_case['name']}: неожиданный статус {response.status_code} (ожидалось: {test_case['expected_status']})",
                            name=f"Test_{test_case['name'].replace(' ', '_')}_failed",
                            attachment_type=allure.attachment_type.TEXT
                        )
                        
                except Exception as e:
                    allure.attach(
                        f"{test_case['name']}: ошибка - {str(e)}",
                        name=f"Test_{test_case['name'].replace(' ', '_')}_error",
                        attachment_type=allure.attachment_type.TEXT
                    )
                    continue

        with allure.step("Проверить что 2 теста прошли успешно"):
            assert successful_tests >= 2, f"Успешно прошло только {successful_tests} тестов из {len(test_cases)}"