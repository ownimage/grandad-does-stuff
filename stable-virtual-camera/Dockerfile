# Start with a lightweight Linux base image
FROM ubuntu:20.04

# Set environment variables to suppress interactive prompts
ENV DEBIAN_FRONTEND=noninteractive

# Set up a user
RUN useradd -m -s /bin/bash user
RUN echo "user:password" | chpasswd

# Start loop
CMD ["sleep", "infinite"]

# Prerequisites
RUN apt update
RUN apt upgrade -y
RUN apt remove python3-pip
RUN apt install -y curl
RUN apt install -y software-properties-common
RUN add-apt-repository ppa:deadsnakes/ppa
RUN apt install -y git python3.10 python3.10-distutils
RUN ln -sf /usr/bin/python3.10 /usr/bin/python
RUN ln -sf /usr/bin/python3.10 /usr/bin/python3
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python
RUN python3 -m pip install --upgrade pip
RUN apt install -y libgl1


USER user
WORKDIR /home/user
RUN git config --global credential.helper store

## Install Stable Virtual Camera
RUN git clone --recursive https://github.com/Stability-AI/stable-virtual-camera \
    && cd /home/user/stable-virtual-camera \
    && pip install -e .

RUN pip install pydantic==2.10.6




