#!/bin/bash

# Wait for internet connectivity
while ! /usr/bin/curl -s http://google.com &> /dev/null; do
  echo "Waiting for internet..."
  /bin/sleep 2
done


echo "$(date): Internet is available"

# Update the package list and upgrade all packages
sudo apt update && sudo apt upgrade -y


#Check if pip is installed, if not, install it
if ! command -v pip3 &> /dev/null; then
  echo "$(date): pip not found, installing..."
  sudo apt install -y python3-pip
fi


# Pull or Clone the repo for the Raspberry code
REPO_URL="https://github.com/cs-23-pt-9-01/BenchManagementRaspbPI.git"
DIR="BenchManagementRaspbPI"

sudo /usr/bin/git -C $HOME/$DIR pull || cd $HOME/ & /usr/bin/git clone $REPO_URL


# Install python dependencies
cd $HOME/$DIR && pip3 install -r requirements.txt