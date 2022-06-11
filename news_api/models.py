from django.db import models


class Article(models.Model):
    """Класс для хранения данных о статье"""
    article_id = models.PositiveIntegerField(verbose_name="ID новости на сайте mos.ru")
    title = models.CharField(verbose_name="Заголовок статьи", max_length=250)
    full_text = models.TextField(verbose_name="Текст статьи")
    published_at = models.DateTimeField(verbose_name="Время публикации статьи")

    def url(self):
        return f"https://www.mos.ru/news/item/{self.article_id}/"
