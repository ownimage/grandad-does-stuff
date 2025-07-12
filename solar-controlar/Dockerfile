FROM python:3.11-bookworm

SHELL ["/bin/bash", "-c"]

RUN apt update \
    && apt install -y cron sudo \
    && useradd -m -s /bin/bash user \
    && echo "user:password" | chpasswd \
    && adduser user sudo \
    && echo "user ALL=(ALL) NOPASSWD:ALL" > /etc/sudoers.d/nopasswd-user \
    && chmod 0440 /etc/sudoers.d/nopasswd-user \
    && pip install --upgrade pip \
    && ln -s /usr/local/bin/python /usr/bin/python
