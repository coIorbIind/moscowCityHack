# Fake detection service(backend)

## Installation guide
1) Cloning repository
```
git clone https://github.com/coIorbIind/moscowCityHack
```
2) Than we should configure .env file
  * Rename .env_template -> .env
  * Modify it

3) Dowload  word embeddings from: http://docs.deeppavlov.ai/en/master/features/pretrained_vectors.html (fastText first link) to **/ds_module/**

4) Configuring docker:
```
docker-compose build
docker-compose up
```
Than it takes ~30 minutes to vectorize 5000 texts from .json file

## API
Send GET request on http://127.0.0.1:8000/api/v1/get-assessment/

*Request BODY:*
```
{
  'title': titleOfTheArticle,
  'text': textOfTheArticle,
}
```
*Response BODY:*
```
{
  {
    "rating": article assesment,
    "distortionCount": number of distortions,
    "stuffingCount": number of unknown sentences,
    "directQuotesCount": number of citates,
    "originalUrl": source link,
    "originalTitle": source title, 
    "similarity": texts cosine similarity,
    "sentences": [
        {
            "userSentence": sentence from user's enter with marked fake,
            "originalSentence": source sentence for user sentence,
        }
    ]
  }
}
```

## Parsers

You can create custom classes for parsing by extending base parser class **BaseParser**. We created only one parser for https://www.mos.ru/
