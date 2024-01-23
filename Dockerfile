FROM python:3.11-slim-buster as base

RUN apt-get update

ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

WORKDIR /app

RUN pip install --upgrade pip

COPY requirements.txt .
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

COPY src ./src

RUN python ./src/manage.py migrate

CMD ["python", "./src/manage.py", "runserver", "0.0.0.0:8000"] 