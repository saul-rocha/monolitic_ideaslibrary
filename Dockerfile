FROM python:3.10-alpine3.13

LABEL maintainer="saul.rocha2001@gmail.com"

ENV PYTHONUNBUFFERED 1

COPY requirements.txt /requirements.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

RUN apk add --no-cache jpeg-dev zlib-dev musl-dev && \
    python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    /py/bin/pip install --no-cache-dir -r /requirements.txt && \
    adduser --disabled-password --no-create-home app

ENV PATH="/py/bin:$PATH"

USER app
