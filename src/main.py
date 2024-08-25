import json

import pandas as pd

from src.reports import category_spending, spending_by_category
from src.services import get_month, get_services, get_year, info_from_excel
from src.utils import get_date_range, get_user_settings, greeting, transactions_from_files
from src.views import get_card_information, get_list_stock, get_list_value, get_top_transactions


def main() -> str:
    """Основная функция."""
    greet = greeting()
    start_date, end_date = get_date_range("2021-04-12 17:54:00")
    df = transactions_from_files("../data/operations.xlsx", start_date, end_date)
    card_info = get_card_information(df)
    top_transaction = get_top_transactions(df)
    user_settings = get_user_settings()
    values = user_settings.get("user_currencies", [])
    stocks = user_settings.get("user_stocks", [])
    currency_rates = get_list_value(values)
    stock_price = get_list_stock(stocks)
    dic_lst = {
        "greeting": greet,
        "cards": card_info,
        "top_transactions": top_transaction,
        "currency_rates": currency_rates,
        "stock_prices": stock_price,
    }
    json_response = json.dumps(dic_lst, ensure_ascii=False, indent=4)
    return json_response


def service_main() -> str:
    """Основная функция по сервису."""
    data = info_from_excel()
    print("Категории повышенного кэшбека")
    year = get_year()
    month = get_month()
    cashback = get_services(data, int(year), int(month))
    return cashback


def handle_reports() -> None:
    print("Выбрано траты по категории")
    data = info_from_excel()
    df = pd.DataFrame(data)
    df["Дата операции"] = pd.to_datetime(df["Дата операции"], dayfirst=True)
    date_option = input("Выбрать текущую дату для анализа? (Да/Нет): ")

    if date_option == "да":
        found = category_spending(df)
        result_nov = spending_by_category(df, found)
        print(result_nov)
    else:
        print("Введите дату для анализа данных")
        year = get_year()
        month = get_month()
        day = input("Введите день: ")
        date_str = f"{year}-{month}-{day}"
        found = category_spending(df)
        result_date = spending_by_category(df, found, date_str)
        print(result_date)


if __name__ == "__main__":
    while True:
        print("1. Страница «Главная»")
        print("2. Выгодные категории повышенного кешбэка")
        print("3. Траты по категории")
        print("4. Выход")
        user_input = input("Введите команду: ")
        if user_input == "1":
            result = main()
            print(result)
        elif user_input == "2":
            result = service_main()
            print(result)
        elif user_input == "3":
            handle_reports()
        elif user_input == "4":
            break
        else:
            print("Неверный ввод")
