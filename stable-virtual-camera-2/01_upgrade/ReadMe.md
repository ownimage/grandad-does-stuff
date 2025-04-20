# Introduction

This folder updates the Docker image built in the stable-virtual-camera directory.

Specifically it removes the public url and allows access to the local port.

## Upgrade

To upgrade the image built in stable-virtual camera

```shell
docker build -t stable-virtual-camera:1.0.1 .
```
```shell
docker compose up
```

You should then be able to access the UI on http://localhost:7860/

## Problems

## container name already in use
You will see an error such as this ...

`Error response from daemon: Conflict. The container name "/stable-virtual-camera" is already in use by container 
"a2962b3aa02f092d3483459994d4ab03960b8d3d72150da75e725d348393e292". You have to remove (or rename) that container to be 
able to reuse that name.`

This can happen if you stop your machine without terminating the running docker image.

Unless you want to keep the container for some reason, the easiest solution is to delete it, replace the container id 
with the one in your message

```shell
docker container rm a2962b3aa02f092d3483459994d4ab03960b8d3d72150da75e725d348393e292
```