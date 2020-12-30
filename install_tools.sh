#!/bin/bash

sudo apt -y update
sudo apt -y upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker azureuser
mkdir booking_small_urls_docker
mkdir booking_info_docker
mkdir apache
cd booking_urls_docker
wget https://github.com/FrBonnefoy/docky/blob/main/small_urls/Dockerfile
wget https://github.com/FrBonnefoy/docky/blob/main/small_urls/initbook.sh
sudo docker build -t booking_url . 
cd ..
sudo docker pull luminati/luminati-proxy
sudo docker run -d --name luminati --network host luminati/luminati-proxy luminati --daemon
sudo docker pull httpd
sudo docker run -d -p 80:80/tcp -v /home/azureuser/apache:/usr/local/apache2/htdocs --name apache httpd
sudo docker pull jupyter/datascience-notebook
sudo docker pull jupyter/tensorflow-notebook
mkdir /home/azureuser/apache/data_science
mkdir /home/azureuser/apache/booking_small_url
mkdir /home/azureuser/apache/tensorflow
mkdir /home/azureuser/apache/booking_info
mkdir /home/azureuser/apache/booking_big_url
#echo 'Finished installation'

