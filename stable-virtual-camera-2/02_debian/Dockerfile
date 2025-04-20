FROM python:3.10.17-slim-bookworm

# Set environment variables to suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Start loop
CMD ["sleep", "infinite"]

# Create user and Prerequisites
RUN useradd -m -s /bin/bash user \
    && echo "user:password" | chpasswd \
    && apt update \
    && apt upgrade -y \
    && apt install -y git libgl1 libglib2.0-dev

USER user
WORKDIR /home/user

## Install Stable Virtual Camera
RUN git clone --recursive https://github.com/Stability-AI/stable-virtual-camera \
    && cd /home/user/stable-virtual-camera \
    && pip install -e . \
    && pip install pydantic==2.10.6 hf_xet

EXPOSE 7860
ENV GRADIO_SERVER_NAME=0.0.0.0