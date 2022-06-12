FROM python:3.8
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /code
COPY requirements.txt /code/
COPY .env /code/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
COPY .gitignore /code/
COPY news_api /code/
COPY moscowCityHack /code/
COPY manage.py /code/
