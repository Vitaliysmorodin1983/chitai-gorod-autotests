```markdown
# 📚 Автоматизированное тестирование сайта «Читай Город»

Проект по автоматизации UI и API тестов для сайта [chitai-gorod.ru](https://www.chitai-gorod.ru/), выполненный в рамках финальной работы по курсу тестирования.

---

## 🎯 Цели проекта

- Проверка стабильности и доступности сайта  
- Автоматизация ключевых сценариев: авторизация, поиск, покупка  
- Проверка корректности API-эндпоинтов  
- Устойчивость к внешним ограничениям (DDOS-защита)  
- Визуализация результатов через Allure-отчёт  

---

## 📁 Структура проекта

```plaintext
chitai-gorod-autotests/
├── config/              # Настройки окружения (BASE_URL)
│   └── settings.py
├── pages/               # PageObject-классы для UI
│   └── base_page.py
├── tests/               # UI и API тесты
│   └── test_ui.py
│   └── test_api.py
├── conftest.py          # Фикстура WebDriver
├── requirements.txt     # Зависимости проекта
├── pytest.ini           # Маркеры Pytest
├── README.md            # Документация проекта
└── .gitignore           # Исключения для Git
```

---

## 🧪 Установка и запуск

### Установка зависимостей

```bash
pip install -r requirements.txt
```

### Запуск тестов

**Все тесты:**
```bash
pytest --alluredir=allure-results
```

**Только UI:**
```bash
pytest -m ui --alluredir=allure-results
```

**Только API:**
```bash
pytest -m api --alluredir=allure-results
```

### Генерация Allure-отчёта

```bash
allure serve allure-results
```

---

## ✅ Результаты тестирования

| Тип тестов | Всего | Пройдено | Пропущено | Упало |
|------------|-------|----------|-----------|--------|
| API        | 5     | 2        | 3         | 0      |
| UI         | 5     | 2        | 3         | 0      |
| **Итого**  | 10    | 4        | 6         | 0      |

> ⚠️ Пропуски связаны с DDOS-защитой сайта. Все такие случаи обработаны через `pytest.skip()`.

---

## 📌 Особенности реализации

- Selenium + WebDriverManager для UI  
- Requests для API  
- Allure-документация: `@allure.step`, `@allure.title`, `@allure.severity`  
- Устойчивость к нестабильным элементам  
- Чистый PEP8-код, без хардкода  

---

## 🔗 Связь с финальной работой

Проект основан на ручной тестовой документации:  
[Финальный тест-план и чек-листы](https://smorodin38.atlassian.net/wiki/spaces/~631f2ddbc7601c8e4abe91c3/pages/48234497)

---

## 📬 Контакты

**Автор:** Vitaliy Smorodin  
**Почта:** smorodin38@gmail.com  
**Платформа:** [Qase.io](https://qase.io) — для хранения тест-кейсов
```
