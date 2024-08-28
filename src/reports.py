import logging
from datetime import datetime, timedelta
from typing import Any, Optional, Union

import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def save_to_file(filename: str = "reports.log") -> Any:
    """Декоратор для сохранения результатов функций-отчетов в файл"""

    def decorator(func: Any) -> Any:
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            result = func(*args, **kwargs)
            with open(filename, "w") as file:
                file.write(str(result))
            return result

        return wrapper

    return decorator


# Функция для получения трат по заданной категории за последние три месяца
def spending_by_category(
    transactions: pd.DataFrame, category: str, date: Optional[Union[datetime, str, pd.Timestamp]] = None
) -> pd.DataFrame:
    if date is None:
        date = datetime.now()
    elif isinstance(date, str):
        date = pd.to_datetime(date)

    start_date = date - timedelta(days=90)

    filtered_transactions: pd.DataFrame = transactions[
        (transactions["Категория"] == category)
        & (transactions["Дата операции"] >= start_date)
        & (transactions["Дата операции"] <= date)
    ]

    result: pd.DataFrame = (
        filtered_transactions.groupby(pd.Grouper(key="Дата операции", freq="ME"))["Сумма операции"]
        .apply(lambda x: x.abs().sum())
        .reset_index()
    )

    return result


def category_spending(df: pd.DataFrame) -> Any:
    """Поиск категории из DataFrame"""
    logging.info("Начало поиска категории")

    categories_data = df["Категория"].unique()
    logging.debug(f"Доступные категории: {categories_data}")

    print("Доступные категории:")
    for category in categories_data:
        if not pd.isnull(category):
            print(category)

    user_input = input("Введите название категории: ").lower()
    logging.debug(f"Пользователь ввел: {user_input}")

    categories_lower = [cat.lower() for cat in categories_data if not pd.isnull(cat)]

    if user_input in categories_lower:
        category_found = next(cat for cat in categories_data if not pd.isnull(cat) and cat.lower() == user_input)
        logging.info(f"Категория найдена: {category_found}")
        return category_found
    else:
        logging.warning("Нет такой категории.")
        print("Нет такой категории.")
        return None
