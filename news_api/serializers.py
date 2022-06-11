from rest_framework.fields import DateTimeField

from .models import Article

from rest_framework import serializers


class ArticleSerializer(serializers.ModelSerializer):
    """Сериализатор для новостей"""
    published_at = DateTimeField(format="%Y-%m-%d %H:%M:%S", input_formats=("%Y-%m-%d %H:%M:%S",))

    class Meta:
        model = Article
        fields = ("article_id", "title", "full_text", "url", "published_at")
        read_only_fields = ("url", )
