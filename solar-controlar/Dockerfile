FROM python:3.11-bookworm

SHELL ["/bin/bash", "-c"]
COPY . /app
WORKDIR /app
RUN    useradd -m -s /bin/bash user \
    && echo "user:password" | chpasswd \
    && apt update \
    && apt install -y cron \
    && pip install --upgrade pip \
    && python -m venv venv \
    && source /app/venv/bin/activate \
    && pip install -r /app/requirements.txt \
    && ln -s /usr/local/bin/python /usr/bin/python
