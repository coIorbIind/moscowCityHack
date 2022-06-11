from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer


class NewsView(APIView):

    def get(self, request, format=None):

        data = request.data

        text = data.get("text")
        title = data.get("title")

        result = {
            "original_id": 101279073,
            "new_original_text": "новый текст оригинал",
            "new_user_text": "новый текст для пользователя"
        }

        article_id = result.get("original_id")
        new_original_text = result.get("new_original_text")
        new_user_text = result.get("new_user_text")
        article = Article.objects.get(article_id=article_id)
        serialized_data = ArticleSerializer(article).data

        serialized_data["full_text"] = new_original_text

        response = {
            "original": serialized_data,
            "new_user_text": new_user_text,
            "fake": True
        }

        return Response(response)
        # article_text

