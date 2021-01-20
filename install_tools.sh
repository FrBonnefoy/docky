#!/bin/bash

sudo apt -y update
sudo apt -y upgrade
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker azureuser
mkdir apache
cd apache
sudo docker build -t booking_url . 
cd ..
sudo docker pull luminati/luminati-proxy
sudo docker run -dit --name luminati --network host luminati/luminati-proxy luminati
sudo docker pull httpd
sudo docker run -d -p 80:80/tcp -v /home/azureuser/apache:/usr/local/apache2/htdocs --name apache httpd
sudo docker pull jupyter/datascience-notebook
sudo docker pull jupyter/tensorflow-notebook
#echo 'Finished installation'
sudo docker run -it -v "$PWD":/home/jovyan/work --network host --cpus="1.0" -e GRANT_SUDO=yes --user root jupyter/datascience-notebook
sudo docker run -dit --name booking_big --network host --memory="4g" --memory-swap="6g" --cpus="2.5" --shm-size="4g" -v /home/azureuser/docky/big_urls:/Bookinfo  booking
sudo docker run -dit --name booking_info --network host --memory="4g" --memory-swap="6g" --cpus="0.625" --shm-size="4g" -v /home/azureuser/docky/info:/Bookinfo  booking_info
