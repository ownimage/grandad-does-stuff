# Stable Virtual Camera on Docker

## Objective
What I want to do is to run Stable Virtual Camera on Docker.  
The repo for Stable Virtual Camera is here https://github.com/Stability-AI/stable-virtual-camera
This is because when I did this on Windows it wanted to download a .exe file that my virus guard flagged as a threat. 

## Notes
docker inspect stable-virtual-camera-buildOpen this file in PyCharm allow click to:
. run the commands for Windows
. copy and paste the commands for inside the containers


## Create the docker images
```sh
docker build -t stable-virtual-camera:build .
```

## Start/stop the container
```sh
docker compose up -d stable-virtual-camera-build
```
# Log into container
```shell
docker exec -it --user user stable-virtual-camera-build bash
```

# Next steps
'''
cd stable-virtual-camera

/home/user/.local/bin/huggingface-cli login
<ENTER_YOUR_HUGGING_FACE_ACCESS_TOKEN>
Add token as git credential? (Y/n) Y

python demo_gr.py
'''
Now wait a very long time ... 7GB+ download

You can exit out of the container ... but do not stop it.
Then we can save the container back as an image.
```shell
docker commit stable-virtual-camera-build stable-virtual-camera:1.0.0
```
Then shut down the container and start a new one up from the saved image
```shell
docker compose down
```
```shell
docker compose up stable-virtual-camera
```


