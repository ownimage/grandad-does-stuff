FROM python:3.11-bookworm

SHELL ["/bin/bash", "-c"]

COPY . /app
WORKDIR /app

RUN apt update \
    && apt --no-install-recommends install -y cron sudo \
    && apt clean \
    && python -m venv venv \
    && source venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && crontab crontab_file




