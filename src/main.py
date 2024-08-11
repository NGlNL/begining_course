import json

from src.views import (
    get_card_information,
    get_date_range,
    get_list_stock,
    get_list_value,
    get_top_transactions,
    get_user_settings,
    greeting,
    transactions_from_files,
)


def main():
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


if __name__ == "__main__":
    result = main()
    print(result)
