#!/bin/bash

sudo apt -y update
sudo apt -y upgrade
#curl -fsSL https://get.docker.com -o get-docker.sh
#sudo sh get-docker.sh
#sudo usermod -aG docker azureuser
mkdir Dockerfile_
cd Dockerfile_
wget https://github.com/FrBonnefoy/docky/blob/main/initbook.sh
wget https://github.com/FrBonnefoy/docky/blob/main/Dockerfile
sudo docker build -t booking_url . 
sudo docker pull httpd
sudo docker pull jupyter/datascience-notebook
sudo docker pull jupyter/tensorflow-notebook

#echo 'Finished installation'

