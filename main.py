import os

import pandas

from ozon_smartphone_parser.spiders.ozon_spider import start_ozon_spider


def pandas_count():
    data = pandas.read_csv('os.txt', header=None, engine='python').value_counts().rename_axis('OS')

    return data


def main():
    start_ozon_spider()  # запускаем парсер

    if os.path.exists('os.txt'):
        return pandas_count()  # запускаем pandas
    else:
        return 'Файл os.txt не найден'


print(main())  # запуск
