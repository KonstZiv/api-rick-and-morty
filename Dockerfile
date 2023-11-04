FROM python:3.11.6-alpine3.18
LABEL maintainer="kos.zivenko@gmail.com"

ENV PYTHOUNNBUFFERED 1

WORKDIR app/

COPY requirements/dev.txt requirements/dev.txt
RUN pip install -r requirements/dev.txt

COPY . .
