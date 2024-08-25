import json
from datetime import datetime
from typing import Any

import pandas as pd


def greeting() -> str:
    """Функция приветствия по времени суток."""
    hour = datetime.now().hour
    if 6 <= hour < 12:
        return "Доброе утро"
    elif 12 <= hour < 18:
        return "Добрый день"
    elif 18 <= hour < 24:
        return "Добрый вечер"
    else:
        return "Доброй ночи"


def transactions_from_files(file_path: str, start_date: datetime, end_date: datetime) -> pd.DataFrame:
    """Функция принимает путь до файла, формат времени по дате операции."""
    data = pd.read_excel(file_path)
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    if start_date:
        data = data[data["Дата операции"] >= start_date]
    if end_date:
        data = data[data["Дата операции"] <= end_date]
    return data


def get_date_range(date_str: str) -> tuple:
    """Функция делает диапозон времени."""
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date = date.replace(day=1)
    end_date = date
    return start_date, end_date


def get_user_settings() -> Any:
    """Функция читает JSON-файл"""
    with open("../user_settings.json", "r") as f:
        return json.load(f)
