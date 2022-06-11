import json
import time
from datetime import datetime
from random import random
from typing import Optional

import requests
from bs4 import BeautifulSoup
from urllib3.exceptions import ProtocolError

from news_api.models import Article
from news_api.serializers import ArticleSerializer


class BaseParser:
    """Базовый класс для парсеров различных сайтов"""

    def __init__(self, url: str):
        """
        Конструктор класса BaseParser.
        :param url: адрес сайта для парсинга.
        """
        self.__url = url

    def parse(self) -> None:
        """
        Метод для парсинга сайта и сохранения данных в файл, название которого передано.
        """
        pass

    def get_updates(self) -> None:
        """
        Метод, для получения новостей за последний день.
        """
        pass

    @property
    def url(self):
        """Getter для url"""
        return self.__url

    @url.setter
    def url(self, new_url):
        """Setter для url"""
        self.__url = new_url


class MosRuParser(BaseParser):
    """Парсер для сайта mos.ru."""

    def __init__(self, date_from: datetime, date_to: datetime, fields: list, sort: str, per_page: int, url: str):
        """
        Конструктор для класса MosRuParser.
        :param date_from: дата, начиная с которой нужно начинать парсинг.
        :param date_to: дата, до которой нужно совершать парсинг.
        :param fields: поля, которые нужно извлечь для каждой статьи
        :param sort: параметры сортировки
        :param per_page: количество статей на одной странице
        :param url: url адрес сайта
        """

        # Создаем параметры для запроса
        params = {
            "from": date_from.strftime("%Y-%m-%d+%H:%M:%S"),
            "to": date_to.strftime("%Y-%m-%d+%H:%M:%S"),
            "fields": ",".join(fields),
            "per-page": per_page,
            "sort": sort
        }
        self.__clear_url = url

        url = self._create_url(url, params)

        super().__init__(url)

    @staticmethod
    def _create_url(url: str, params: dict) -> str:
        """
        Метод для создания ссылки
        :param params: параметры запроса
        :return: готовый url
        """
        for k, v in params.items():
            url += f"{k}={v}&"

        url = url[:-1]

        return url

    def parse(self) -> None:
        page_count = self._get_page_count()  # получаем число страниц с данными

        for page_num in range(1, page_count + 1):
            items = self._collect_data(page_num=page_num, url=self.url)  # собираем данные с каждой страницы

            if items is None:
                pass
            else:
                self._save_data(items=items)  # сохраняем записи в БД

            time.sleep(random() * 1.5 + 0.5)  # немного ждем, чтобы не нагружать сервер запросами

    def _collect_data(self, url: str, page_num: int) -> Optional[list]:
        """
        Метод для извлечения информации о статьях.
        :param url: url адрес сайта
        :param page_num: номер страницы.
        :return: None
        """
        page_url = url + f"&page={page_num}"  # подставляем номер страницы в параметры запроса

        # Отправляем запрос на сайт, если нет ответа, ждем в течение 15 секунд
        try:
            response = requests.get(page_url)

        except ProtocolError:
            time.sleep(15)
            response = requests.get(page_url)

        if response.ok:
            data = response.json()  # если данные успешно получены, собираем информацию с ответа сервера

            items = data.get("items")  # забираем все новости

            # Извлекаем текст из всех тегов статьи
            for item in items:
                item["full_text"] = BeautifulSoup(item["full_text"], "lxml").text
                item["article_id"] = item.pop("id")

            return items

        return None
        # # Если это первая страница, создаем новый файл и записываем в него данные
        # if page_num == 1:
        #     with open(self.filename, "w", encoding="utf8") as file:
        #         json.dump(items, file, indent=4, ensure_ascii=False)
        #
        # # Если страница не первая, то дописываем данные к уже существующему файлу
        # else:
        #     with open(self.filename, "r+", encoding='utf8') as file:
        #         try:
        #             data = json.load(file)
        #             data += items
        #             file.seek(0)
        #             json.dump(data, file, indent=4, ensure_ascii=False)
        #         except json.decoder.JSONDecodeError:
        #             data = items
        #             json.dump(data, file, indent=4, ensure_ascii=False)

    def _save_data(self, items: list):
        """
        Функция для записи новостей в БД
        :param items: список новостей
        """
        for item in items:
            serializer = ArticleSerializer(item)

            if serializer.is_valid():
                serializer.save()

    def _get_page_count(self) -> int:
        """
        Метод для получения количества всех страниц.
        :return: количество страниц с записями
        """
        response = requests.get(self.url)  # отправляем запрос на сайт

        if response.ok:
            data = response.json()  # если ответ успешно получен, извлекаем из него данные

            meta = data.get("_meta")  # находим метаданные

            page_count = meta.get("pageCount")  # извлекаем число страниц

            return page_count

        return 0

    def get_updates(self) -> None:
        """Функция для получения новостей за день"""
        params = dict([item.split("=") for item in self.url.split("?")[-1].split("&")])  # получаем старые параметры url

        date_from_str = datetime.today().strftime("%Y-%m-%d+00:00:00")  # генерируем начало текущего дня

        date_to_str = datetime.today().strftime("%Y-%m-%d+23:59:59")  # генерируем конец текущего дня

        params["from"] = date_from_str  # изменяем дату для начала парсинга

        params["to"] = date_to_str  # изменяем дату для конца парсинга

        url = self._create_url(self.__clear_url, params)  # генерируем url для поиска

        items = self._collect_data(url=url, page_num=1)  # собираем и дописываем данные за день

        if items is None:
            pass
        else:
            self._save_data(items=items)  # сохраняем записи в БД
