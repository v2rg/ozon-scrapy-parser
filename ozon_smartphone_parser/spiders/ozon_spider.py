import logging
import random

import scrapy
from scrapy import exceptions
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from scrapy_selenium import SeleniumRequest


class OzonSpider(scrapy.Spider):  # парсим версии ОС смартфонов
    name = 'ozon'

    HOST = 'https://ozon.ru'
    LIMIT = 100  # кол-во смартфонов
    PER_PAGE = 36  # кол-во товаров на странице (для подсчета кол-ва страниц)
    SELECTOR_URL = 'ix3'  # селектор для поиска ссылки на товар: <div class="xi3"><a href="/product/apple-smartfon-iphon...></a></div>

    count = 0

    def start_requests(self):  # получаем кол-во страниц с товарами
        pages = self.LIMIT // self.PER_PAGE + 1  # подсчет страниц

        urls = [f'{self.HOST}/category/smartfony-15502/?page={x}&sorting=rating' for x in range(1, pages + 1)]

        for url in urls:
            yield SeleniumRequest(url=url, callback=self.parse)

    def parse(self, response, **kwargs):  # парсим ссылки на товары
        if self.count >= self.LIMIT:  # остановка, если достигнут лимит
            logging.info(f'CloseSpider because COUNT == {self.count}')
            raise exceptions.CloseSpider(f'CloseSpider because COUNT == {self.count}')
        else:
            urls = [f'{self.HOST}' + x for x in response.css(f'div.{self.SELECTOR_URL} a ::attr(href)').getall()]

            with open('urls.txt', 'a+', encoding='UTF-8') as f:  # сохранение ссылок в файл urls.txt
                f.write(str(urls) + '\n')

            for url in urls:
                yield SeleniumRequest(
                    url=url,
                    callback=self.os_parse,
                    script=f"window.scrollBy(0, {random.randint(200, 1000)})"
                )

    def os_parse(self, response, **kwargs):  # парсим версию ОС
        characteristics = response.css('dl ::text').getall()

        if self.count >= self.LIMIT:  # остановка, если достигнут лимит
            # logging.info(f'CloseSpider because COUNT == {self.count}')
            raise exceptions.CloseSpider(f'CloseSpider because COUNT == {self.count}')
        else:
            if 'Операционная система' in characteristics:
                self.count += 1
                for ind, value in enumerate(characteristics):
                    if value == 'Операционная система':
                        try:
                            characteristics[ind + 1]
                        except IndexError:
                            with open('os.txt', 'a+', encoding='UTF-8') as f:
                                f.write('index error OS\n')
                        else:
                            if characteristics[ind + 1] == 'iOS':
                                try:
                                    os_ind = characteristics.index('Версия iOS')
                                except ValueError:
                                    with open('os.txt', 'a+', encoding='UTF-8') as f:
                                        f.write('Index error iOS\n')
                                else:
                                    with open('os.txt', 'a+', encoding='UTF-8') as f:
                                        f.write(f'{characteristics[os_ind + 1]}\n')
                            else:
                                if 'Версия Android' in characteristics:
                                    try:
                                        characteristics[ind + 3]
                                    except IndexError:
                                        with open('os.txt', 'a+', encoding='UTF-8') as f:
                                            f.write('Index error OS Other\n')
                                    else:
                                        with open('os.txt', 'a+', encoding='UTF-8') as f:
                                            f.write(f'{characteristics[ind + 3]}\n')
                                else:
                                    with open('os.txt', 'a+', encoding='UTF-8') as f:
                                        f.write('Android\n')

            # else:
            #     logging.info(f'- Повтор os_parse - | {response.request.url}')
            #     yield SeleniumRequest(url=response.request.url,
            #                           callback=self.os_parse)  # повтор os_parse, если 'Операционная система' не в characteristics


def start_ozon_spider():  # для запуска из main.py
    process = CrawlerProcess(get_project_settings())
    process.crawl(OzonSpider)
    process.start()
