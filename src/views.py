import json
import os
from datetime import datetime
from typing import Any

import pandas as pd
import requests
from dotenv import load_dotenv

load_dotenv()
API_KEY = os.getenv("API_KEY")
ALPHA_KEY = os.getenv("ALPHA_KEY")


def greeting():
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


def transactions_from_files(file_path: str, start_date: datetime, end_date: datetime):
    """Функция принимает путь до файла, формат времени по дате операции."""
    data = pd.read_excel(file_path)
    data["Дата операции"] = pd.to_datetime(
        data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce"
    )
    if start_date:
        data = data[data["Дата операции"] >= start_date]
    if end_date:
        data = data[data["Дата операции"] <= end_date]
    return data


def get_card_information(df: pd.DataFrame) -> Any:
    """Функция принимает информацию по карте: номер карты, сумму операции и кэшбек."""
    card_summary = df.groupby("Номер карты")["Сумма операции"].sum().reset_index()
    card_information = []
    for index, el in card_summary.iterrows():
        last_digit = str(el["Номер карты"])[-4:]
        total_spent = el["Сумма операции"]
        cashback = round(total_spent * 0.01, 2)
        card_information.append(
            {
                "last_digits": last_digit,
                "total_spent": total_spent,
                "cashback": cashback,
            }
        )
    return card_information


def get_date_range(date_str: str):
    """Функция делает диапозон времени."""
    date = datetime.strptime(date_str, "%Y-%m-%d %H:%M:%S")
    start_date = date.replace(day=1)
    end_date = date
    return start_date, end_date


def get_top_transactions(data):
    """Функция возвращает топ-5 транзакций."""
    data["Дата операции"] = pd.to_datetime(data["Дата операции"], format="%d.%m.%Y %H:%M:%S", errors="coerce")
    df = data.dropna(subset=["Дата операции"])
    if data.empty:
        print("DataFrame пуст после удаления некорректных дат.")
        return []
    df["Сумма платежа"] = pd.to_numeric(df["Сумма платежа"], errors="coerce")
    df = df.dropna(subset=["Сумма платежа"])
    if df.empty:
        print("DataFrame пуст после удаления некорректных значений суммы платежа.")
        return []
    top_transactions = df.nlargest(5, "Сумма платежа").to_dict("records")
    if not top_transactions:
        print("Нет транзакций, соответствующих условиям.")
        return []
    formatted_transactions = []
    for transaction in top_transactions:
        formatted_transactions.append(
            {
                "date": transaction["Дата операции"].strftime("%d.%m.%Y"),
                "amount": transaction["Сумма платежа"],
                "category": transaction["Категория"],
                "description": transaction["Описание"],
            }
        )
    return formatted_transactions


def get_user_settings():
    """Функция читает JSON-файл"""
    with open("../user_settings.json", "r") as f:
        return json.load(f)


def get_list_value(values):
    """Функция дает ответ о курсе валют по API."""
    currency_values = []
    for value in values:
        url = "https://api.apilayer.com/fixer/latest"
        params = {"base": value}
        headers = {"apikey": API_KEY}
        response = requests.get(url, headers=headers, params=params)
        if response.status_code == 200:
            data = response.json()
            currency_values.append(
                {"currency": value, "rate": data["rates"].get("RUB", "N/A")}
            )
    return currency_values


def get_list_stock(stocks):
    """Функция дает ответ о стоимости акций."""
    stock_prices = []
    for stock in stocks:
        api_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={stock}&apikey={ALPHA_KEY}"
        response = requests.get(api_url)
        if response.status_code == 200:
            data = response.json()
            last_refreshed = data["Meta Data"]["3. Last Refreshed"]
            stock_price = data["Time Series (Daily)"][last_refreshed]["4. close"]
            stock_prices.append({"stock": stock, "price": float(stock_price)})
    return stock_prices
