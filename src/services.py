import json
import logging
from datetime import datetime
from typing import Any, Hashable

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


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
    logging.info("Начало анализа данных")

    analysis = {}
    for transaction in data:
        try:
            date_str = transaction.get("Дата операции", "")
            date = datetime.strptime(date_str, "%d.%m.%Y %H:%M:%S")
            logging.debug(f"Обрабатывается дата: {date_str}")

            if date.year == year and date.month == month:
                category = transaction.get("Категория", "")
                bonus_str = transaction.get("Бонусы (включая кэшбэк)", "")
                bonus = float(bonus_str) if bonus_str else 0.0

                logging.debug(f"Категория: {category}, Бонус: {bonus}")

                if bonus > 0:
                    if category not in analysis:
                        analysis[category] = 0.0
                    analysis[category] += bonus

        except ValueError as e:
            logging.error(f"Ошибка обработки транзакции: {transaction}. Ошибка: {e}")

    sorted_analysis = dict(sorted(analysis.items(), key=lambda item: item[1], reverse=True))
    logging.info("Анализ завершен")
    logging.debug(f"Результат анализа: {sorted_analysis}")

    return json.dumps(sorted_analysis, indent=4, ensure_ascii=False)
