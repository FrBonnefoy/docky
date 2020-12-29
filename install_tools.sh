#!/bin/bash

sudo apt -y update
sudo apt -y upgrade
#curl -fsSL https://get.docker.com -o get-docker.sh
#sudo sh get-docker.sh
#sudo usermod -aG docker azureuser
mkdir booking_urls_docker
mkdir luminati_docker
mkdir booking_info_docker
cd booking_urls_docker
https://github.com/FrBonnefoy/docky/blob/main/urls/initbook.sh
https://github.com/FrBonnefoy/docky/blob/main/urls/Dockerfile
cd ..
cd luminati_docker
sudo docker build -t booking_url . 
sudo docker pull httpd
sudo docker pull jupyter/datascience-notebook
sudo docker pull jupyter/tensorflow-notebook
mkdir data_science
mkdir booking_url
mkdir tensorflow
mkdir booking
#echo 'Finished installation'

