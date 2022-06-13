"""
WSGI config for moscowCityHack project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

from ds_module.model import SimilarityModel
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'moscowCityHack.settings')

try:
    model = SimilarityModel("ds_module/ft_native_300_ru_wiki_lenta_lemmatize.vec")
    print("Created model")
    texts = pd.read_json("ds_module/mos_ru.json", encoding="utf8")
    print("Text reading finished")
    model.train(texts)
    print("Model training finished")

except Exception as e:
    model = None
    print(e)

application = get_wsgi_application()
