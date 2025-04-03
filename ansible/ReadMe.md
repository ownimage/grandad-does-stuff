# Ansible and GPU

## Objective
What I want to do is to set up the framework for using ansible to commission new images on either a docker container or 
later on a RaspberryPi.

## Notes
When I open this file in PyCharm allows me to:
. run the commands for Windows
. copy and paste the commands for inside the containers


## Overview of files
Dockerfile-ansible-controller defines an image with ansible installed \
It installs ansbile and the nvidia role we will use later 

Dockerfile-ansible-node defines an ubuntu image with a user, password, ssh configured

docker-compose-ansible.yml allows these two images to start up with docker-compose \
and mount the controller directory into the controller

controller/inventory.ini is the ansible list of all the hosts (only the ansible-node in this case)

controller/playbook.yml are the packages to be installed, the interesting one here is the role nvidia.nvidia_driver

docker-compose-gpu.yml allows the image that we will build to be started with docker-compose \
note that the gpu is mapped through to the image


## Create the docker images
```sh
docker build -f Dockerfile-ansible-controller -t ansible-controller:1.0.0 .
```

```sh
docker build -f Dockerfile-ansible-node -t ansible-node:1.0.0 .
```

## Start the containers
```sh
docker compose -f docker-compose-ansible.yml up -d
```

## Log into the ansible containers and run ansbile to configure node
```shell
docker exec -it ansible_controller bash
```
Paste the command below into the bash shell, ignore the error message that ansible also ignores.  
There is also a failure message at the end where it cant reboot the container, but again we are going to restart a copy \
of this container soon.
```sh
cd /controller 
ansible-playbook playbook.yml -i inventory.ini
exit
```

## Commit the changes
We have made changes to the ansible-node which we want to be able to save as an image to start a new container from.
```sh
docker commit ansible_node ansible-gpu-node:1.0.0
```

## Start the gpu node and log into the container and check it workd
```sh
docker compose -f docker-compose-gpu.yml up -d
```
```sh
docker exec -it ansible_gpu_node bash
```
```sh
nvidia-smi
```
