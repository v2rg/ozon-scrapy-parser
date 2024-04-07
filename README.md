# Парсер ozon.ru
- собирает информацию о версиях операционных систем в топ-100 смартфонах (с самым высоким рейтингом пользователей)

## Особенности
- работает на python3.11, scrapy, selenium, pandas
- для обхода антибота — undetected-chromedriver, scrapy-rotating-proxies

## Запуск
- клонировать проект `git clone https://github.com/v2rg/ozon-scrapy-parser.git`
- установить зависимости `pip install -r requirements.txt`
- заменить код в файле `.venv\Lib\site-packages\scrapy_selenium\middlewares.py` на [исправленный](https://gist.github.com/v2rg/d288575f1523d983a683ff9864f8ec56) (с модулем undetected_chromedriver)
- добавить прокси в файл `proxies.txt`
- в `SELECTOR_URL` поместить актуальный селектор (в файле `ozon_smartphone_parser/spiders/ozon_spider.py`), который отвечает за ссылку на товар (страница каталога ozon.ru). Этот селектор может изменяться каждый день

![ozon_selector.png](https://s8d6.turboimg.net/sp/3659becf0a18a8f3d54915c086097d90/ozon_selector.png)

- запустить парсер через `main.py`

## Требования
- python 3.11
- Scrapy
- scrapy-selenium
- undetected-chromedriver
- webdriver-manager
- scrapy-rotating-proxies
- pandas
