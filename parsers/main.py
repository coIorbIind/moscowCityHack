from datetime import datetime
import schedule

from parserClasses import MosRuParser


def main():
    date_from = datetime(2021, 9, 1, 0, 0, 0)  # дата, начиная с которой нужно собрать новости

    date_to = datetime.today()  # текущая дата = дата окончания сборки новостей

    fields = ["id", "full_text", "title", "published_at"]  # поля, которые нужно получить в json объекте

    sort = "-date"  # параметры сортировки

    per_page = 50  # количество записей на одной странице, не может превысить 50

    mp = MosRuParser(date_from=date_from, date_to=date_to, fields=fields, sort=sort, per_page=per_page,
                     url="https://www.mos.ru/api/newsfeed/v4/frontend/json/ru/articles?")

    schedule.every().day.at('23:59').do(mp.get_updates)

    while True:
        schedule.run_pending()


if __name__ == '__main__':
    main()
