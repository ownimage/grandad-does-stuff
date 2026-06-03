FROM python:3.11-bookworm

SHELL ["/bin/bash", "-c"]

COPY . /app

RUN apt update \
    && apt --no-install-recommends install -y cron sudo \
    && apt clean \
    && useradd -m -s /bin/bash user \
    && echo "user:password" | chpasswd \
    && adduser user sudo \
    && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/nopasswd-user \
    && chmod 0440 /etc/sudoers.d/nopasswd-user \
    && ln -s /usr/local/bin/python /usr/bin/python \
    && chown -R 777 /app

WORKDIR /app
RUN python -m venv venv \
    && source venv/bin/activate \
    && pip install --upgrade pip \
    && pip install -r requirements.txt \
    && crontab crontab_file




