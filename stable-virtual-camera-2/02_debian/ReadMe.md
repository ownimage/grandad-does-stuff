# Introduction

I want to use a debian base image for python, (I'm planning a few Raspberry Pi projects and the default OS is debian 
based.)

## Create the docker images
```sh
docker build -t stable-virtual-camera:build-debian .
```

## Start the container
```sh
docker compose up -d stable-virtual-camera-build-debian
```
# Log into container
```shell
docker exec -it --user user stable-virtual-camera-build-debian bash
```

# Next steps
```
cd stable-virtual-camera

/home/user/.local/bin/huggingface-cli login
<ENTER_YOUR_HUGGING_FACE_ACCESS_TOKEN>
Add token as git credential? (Y/n) n

python demo_gr.py --no-share
```
Now wait a very long time ... 11GB+ download

You will see something like this 
```
* Running on local URL:  http://0.0.0.0:7860
INFO:httpx:HTTP Request: GET http://localhost:7860/gradio_api/startup-events "HTTP/1.1 200 OK"
INFO:httpx:HTTP Request: HEAD http://localhost:7860/ "HTTP/1.1 200 OK"

To create a public link, set `share=True` in `launch()`.
INFO:httpx:HTTP Request: GET https://api.gradio.app/pkg-version "HTTP/1.1 200 OK"
```

You can exit out of the container ... but do not stop it.  
Ctrl-C to stop the running process, `exit` to exit out of the bash shell and return to the host machine.

Then we can save the container back as an image.
```shell
docker commit stable-virtual-camera-build-debian stable-virtual-camera:2.0.0
```
Then shut down the container and start a new one up from the saved image
```shell
docker compose down
```
```shell
docker compose up stable-virtual-camera-debian
```

You should then be able to access the UI on http://localhost:7860/

## Problems

## container name already in use
You will see an error such as this ...

`Error response from daemon: Conflict. The container name "/stable-virtual-camera" is already in use by container 
"463faa86b320cc9a6de476f8bd1b67c001d486b775bf77b218c323c67e2b5799". You have to remove (or rename) that container to be 
able to reuse that name.`

This can happen if you stop your machine without terminating the running docker image.

Unless you want to keep the container for some reason, the easiest solution is to delete it, replace the container id 
with the one in your message

```shell
docker container rm 463faa86b320cc9a6de476f8bd1b67c001d486b775bf77b218c323c67e2b5799
```