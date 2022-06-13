FROM python:3.9
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY .env /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN python -m spacy download ru_core_news_lg
COPY .gitignore /code/
COPY news_api /code/
COPY moscowCityHack /code/
COPY ds_module /code/
COPY manage.py /code/
