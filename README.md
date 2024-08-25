# Описание проекта
## Программа анализирует транзакции, которые находятся в Excel-файле. Приложение будет генерировать JSON-данные для веб-страниц.
# Установка
## Для использования модуля, клонируйте репозиторий и убедитесь, что у вас установлен Python версии 3.6 или выше.
```bash
git clone <URL вашего репозитория>
cd <директория вашего проекта>
```
# Зависимости
## В проекте используется poetry.
## Для того чтобы подтянуть зависимости используйте:
```bash
poetry install
# Для первичной установки
poetry update
# В случае, если poetry уже был
```
# Тестирование
## В проекте используется тестирование pytest, для того чтобы запустить тесты, нужно запустить виртуальное окружение и выполнить команду:
```bash
pytest
```
## Если установлен poetry:
```bash
poetry run pytest
```
# API
## Перед использованием программы нужно создать файл '.env'
## API - перейти на сайт "https://apilayer.com/" и найти там "FIXER API" и получить свой апи ключь и записать его в переменную файла .env
## AlPHA_API - перейти на сайт "https://www.alphavantage.co/" и получить свой апи и записать его в другую переменную .env
# Использование 
## В проекте есть функции: 1. Приветствия, которая приветствует в зависимости от текущего времени суток, 2. Функция, котрая выдаёт информацию о  карте(последние 4 цифры карты, общую сумму расходов, кешбэк (1 рубль на каждые 100 рублей), 3. Функция, которая показывает Топ-5 транзакций по сумме платежа, 4. Курс валют, 5. Стоимость акций из S&P500.
## Также есть основная функция, которая объединяет все вышеперечисленные и выдаёт JSON-строку.
## Есть функция события: выгодные категории повышенного кэшбека, функия принимает на вход данные для анализа, год и месяц и возвращает JSON с анализом, сколько на каждой категории можно заработать кешбэка.
## Добавлен сервис траты по категориям, который принимает на вход датафрейм с транзакциями, название категории, опцинальную дату. Функция возвращает траты по заданной категории за последние три месяца (от переданной даты).
# Запуск программы
## Запустите модуль main.py.
