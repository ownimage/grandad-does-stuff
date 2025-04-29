FROM python:3.10.17-slim-bookworm

RUN mkdir /app
COPY requirements.txt /app/requirements.txt
# Create user and Prerequisites
RUN useradd -m -s /bin/bash user \
    && echo "user:password" | chpasswd

RUN pip install --upgrade pip
RUN pip install -r /app/requirements.txt
#
#USER user
