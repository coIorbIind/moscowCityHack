from datetime import datetime

from django.test import TestCase

from news_api.models import Article
from news_api.serializers import ArticleSerializer


class ArticleSerializerTestCase(TestCase):

    def setUp(self):
        self.article = Article.objects.create(
            article_id=12345,
            title="Заголовок",
            full_text="Текст тестовой статьи",
            published_at=datetime(2022, 6,  12, 12, 12, 12)
        )

    def test_serializing(self):
        serialized_data = ArticleSerializer(self.article).data
        expected_data = {
            "article_id": 12345,
            "title": "Заголовок",
            "full_text": "Текст тестовой статьи",
            "published_at": datetime(2022, 6,  12, 12, 12, 12).strftime("%Y-%m-%d %H:%M:%S"),
            "url": self.article.url()
        }

        self.assertEqual(expected_data, serialized_data)

    def test_deserializing(self):
        data = {
            "article_id": 123456,
            "title": "Новый заголовок",
            "full_text": "Текст новой статьи",
            "published_at": datetime(2022, 6,  12, 12, 12, 12).strftime("%Y-%m-%d %H:%M:%S"),
        }

        serializer = ArticleSerializer(data=data)

        self.assertEqual(True, serializer.is_valid())

        serializer.save()

        self.assertEqual(2, Article.objects.count())
