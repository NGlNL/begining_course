import json
from datetime import datetime
from unittest.mock import Mock, patch

import pandas as pd
import pytest

from src.views import (get_card_information, get_date_range, get_list_stock,
                       get_list_value, get_top_transactions, get_user_settings,
                       greeting, transactions_from_files)


def test_greeting_morning():
    with patch("src.views.datetime") as mock_datetime:
        mock_datetime.now.return_value = datetime(2024, 8, 11, 9, 0, 0)
        assert greeting() == "Доброе утро"


start = datetime(2022, 1, 1, 12, 0, 0)
end = datetime(2022, 1, 1, 12, 0, 0)


def test_transactions_from_files():
    with pytest.raises(FileNotFoundError):
        transactions_from_files("not_existing_file", start, end)


def test_get_card_information():
    df = pd.DataFrame(
        {
            "Номер карты": ["1234567812345678", "1234567812345678", "1234567812345678"],
            "Сумма операции": [100, 200, 300],
        }
    )

    card_information = get_card_information(df)
    assert card_information == [
        {"last_digits": "5678", "total_spent": 600, "cashback": 6.0},
    ]


def test_get_date_range():
    start_date, end_date = get_date_range("2022-01-01 12:00:00")
    assert start_date == datetime(2022, 1, 1, 12, 0, 0)
    assert end_date == datetime(2022, 1, 1, 12, 0, 0)

    start_date, end_date = get_date_range("2022-12-31 23:59:59")
    assert start_date == datetime(2022, 12, 1, 23, 59, 59)
    assert end_date == datetime(2022, 12, 31, 23, 59, 59)

    start_date, end_date = get_date_range("2022-02-01 00:00:00")
    assert start_date == datetime(2022, 2, 1)
    assert end_date == datetime(2022, 2, 1, 0, 0, 0)

    start_date, end_date = get_date_range("2022-12-31 23:59:59")
    assert start_date == datetime(2022, 12, 1, 23, 59, 59)
    assert end_date == datetime(2022, 12, 31, 23, 59, 59)

    start_date, end_date = get_date_range("2023-01-01 00:00:00")
    assert start_date == datetime(2023, 1, 1)
    assert end_date == datetime(2023, 1, 1, 0, 0, 0)


def test_get_top_transactions():
    df = pd.DataFrame(
        {
            "Дата операции": [
                "01.08.2023 12:00:00",
                "02.08.2023 14:00:00",
                "03.08.2023 10:00:00",
                "04.08.2023 16:00:00",
                "05.08.2023 18:00:00",
                "06.08.2023 20:00:00",
            ],
            "Сумма платежа": [5000, 7000, 2000, 8000, 1000, 9000],
            "Категория": [
                "Продукты",
                "Развлечения",
                "Транспорт",
                "Рестораны",
                "Продукты",
                "Путешествия",
            ],
            "Описание": [
                "Покупка в магазине",
                "Поход в кино",
                "Проезд",
                "Ужин в ресторане",
                "Покупка еды",
                "Билеты на самолет",
            ],
        }
    )

    top_transactions = get_top_transactions(df)
    assert top_transactions == [
        {
            "date": "06.08.2023",
            "amount": 9000,
            "category": "Путешествия",
            "description": "Билеты на самолет",
        },
        {
            "date": "04.08.2023",
            "amount": 8000,
            "category": "Рестораны",
            "description": "Ужин в ресторане",
        },
        {
            "date": "02.08.2023",
            "amount": 7000,
            "category": "Развлечения",
            "description": "Поход в кино",
        },
        {
            "date": "01.08.2023",
            "amount": 5000,
            "category": "Продукты",
            "description": "Покупка в магазине",
        },
        {
            "date": "03.08.2023",
            "amount": 2000,
            "category": "Транспорт",
            "description": "Проезд",
        },
    ]


def test_get_user_settings():
    with open("../user_settings.json", "w") as f:
        json.dump({"key": "value"}, f)

    user_settings = get_user_settings()
    assert user_settings == {"key": "value"}

    with open("../user_settings.json", "w") as f:
        json.dump({}, f)

    user_settings = get_user_settings()
    assert user_settings == {}


def test_get_list_value():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {"rates": {"RUB": 70}}
        mock_get.return_value = mock_response

        list_value = get_list_value(["USD"])
        assert list_value == [{"currency": "USD", "rate": 70}]


def test_get_list_stock():
    with patch("requests.get") as mock_get:
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "Meta Data": {"3. Last Refreshed": "2022-01-01"},
            "Time Series (Daily)": {"2022-01-01": {"4. close": "100.0"}},
        }
        mock_get.return_value = mock_response

        list_stock = get_list_stock(["AAPL"])
        assert list_stock == [{"stock": "AAPL", "price": 100.0}]
