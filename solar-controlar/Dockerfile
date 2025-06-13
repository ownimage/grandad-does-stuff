FROM python:3.11-bookworm

# Create a link so python appears in the same place as the RPi
RUN ln -s /usr/local/bin/python /usr/bin/python

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
COPY pyproject.toml /app/pyproject.toml
# Create user and Prerequisites
RUN useradd -m -s /bin/bash user \
    && echo "user:password" | chpasswd

RUN pip install --upgrade pip

RUN pip install -r /app/requirements.txt

RUN apt update \
    && apt install -y cron

