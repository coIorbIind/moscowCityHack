FROM python:3
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
WORKDIR /parsers
COPY requirements.txt /parsers/
RUN pip install -r requirements.txt
COPY main.py /parsers/
COPY parserClasses.py /parsers/