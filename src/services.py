import json
from datetime import datetime
from typing import Hashable, Any

import pandas as pd


def info_from_excel(filepath: str = "../data/operations.xlsx") -> list[dict[Hashable, Any]]:
    """Читает информацию из excel"""
    df = pd.read_excel(filepath)
    data = df.to_dict("records")
    return data


def get_year() -> str:
    """Запрос года"""
    while True:
        user_input = input("Введите год: ")
        if user_input.isdigit() and len(user_input) == 4:
            return user_input
        else:
            print("Неверный формат года")


def get_month() -> str:
    """Запросить месяц"""
    while True:
        user_input = input("Введите месяц: ")
        if user_input.isdigit() and 1 <= int(user_input) <= 12:
            return user_input.zfill(2)
        else:
            print("Неверный формат месяца")


def get_services(data: list[dict[Hashable, Any]], year: int, month: int) -> str:
    """Анализ выгодности категорий повышенного кешбэка"""
    analysis = {}
    for transaction in data:
        date = datetime.strptime(transaction.get("Дата операции", ""), "%d.%m.%Y %H:%M:%S")
        if date.year == year and date.month == month:
            category = transaction.get("Категория", "")
            if float(transaction.get("Бонусы (включая кэшбэк)", "")) > 0:
                if category not in analysis:
                    analysis[category] = 0.0
                analysis[category] += float(transaction.get("Бонусы (включая кэшбэк)", ""))
    sorted_analysis = dict(sorted(analysis.items(), key=lambda item: item[1], reverse=True))
    return json.dumps(sorted_analysis, indent=4, ensure_ascii=False)
