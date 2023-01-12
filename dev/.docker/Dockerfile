FROM python:3.7

ENV PYTHONUNBUFFERED 1

RUN mkdir /app

EXPOSE 8000
VOLUME /app
WORKDIR /app

COPY requirements.txt /app/requirements.txt

RUN pip install -r requirements.txt

COPY . /app

CMD  [ "python3", "manage.py", "runserver", "0:8000" ]
