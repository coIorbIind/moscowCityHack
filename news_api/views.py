from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Article
from .serializers import ArticleSerializer
from moscowCityHack.wsgi import model


class NewsView(APIView):

    def get(self, request, format=None):
        data = request.data

        text = data.get("text")
        title = data.get("title")

        print(text)

        if model is None:
            print("Модель не работает")
            return Response({"error": "Error during creating model"})

        print("OK!")

        result = model.predict(text)

        orig_article = Article.objects.get(article_id=int(result.pop("origId")))
        orig_article_url = orig_article.url()
        orig_article_title = orig_article.title

        result["originalUrl"] = orig_article_url
        result["originalTitle"] = orig_article_title

        # result = {
        #     "rating": "",
        #     "distortionCount": "",
        #     "stuffingCount": "",
        #     "directQuotesCount": "",
        #     "originalUrl": "",
        #     "originalTitle": "",
        #     "similarity": "",
        #     "sentences": [
        #         {
        #             "userSentence": "",
        #             "originalSentence": "",
        #         },
        #         {
        #             "userSentence": "",
        #             "originalSentence": "",
        #         }
        #     ]
        # }

        return Response(result)
