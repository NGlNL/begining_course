from unittest.mock import patch

from src.services import get_month, get_services, get_year, info_from_excel


def test_info_from_excel():
    data = info_from_excel("data/operations.xlsx")
    assert isinstance(data, list)
    for transaction in data:
        assert isinstance(transaction, dict)
        assert "Дата операции" in transaction
        assert "Категория" in transaction
        assert "Бонусы (включая кэшбэк)" in transaction


def test_get_year():
    user_input = "2022"
    with patch("builtins.input", return_value=user_input):
        year = get_year()
        assert year == "2022"


def test_get_month():
    user_input = "12"
    with patch("builtins.input", return_value=user_input):
        month = get_month()
        assert month == "12"


def test_get_services():
    data = [
        {"Дата операции": "01.01.2022 12:49:53", "Категория": "Переводы", "Бонусы (включая кэшбэк)": "100"},
        {"Дата операции": "01.01.2022 12:49:53", "Категория": "Красота", "Бонусы (включая кэшбэк)": "200"},
        {"Дата операции": "01.01.2022 12:49:53", "Категория": "Супермаркеты", "Бонусы (включая кэшбэк)": "300"},
    ]
    year = "2022"
    month = "01"
    services = get_services(data, int(year), int(month))
    assert isinstance(services, str)
    assert '{\n    "Супермаркеты": 300.0,\n    "Красота": 200.0,\n    "Переводы": 100.0\n}' in services
