#!/bin/bash

#Todo - add usage + quick setup (update python packages and restart the servers)

echo "------------------------"
echo "Updating package manager"
sudo apt-get update

echo "------------------------"
echo "Configuring mail-server"
sudo debconf-set-selections <<< "postfix postfix/mailname string localhost"
sudo debconf-set-selections <<< "postfix postfix/main_mailer_type string 'Internet Site'"
sudo apt-get install --assume-yes postfix






echo "------------------------"
echo "Install python packages"

pip3 install -r requirments.txt

# QT (UI)
sudo apt-get install python3-pyqt5
sudo apt-get install pyqt5-dev-tools
sudo apt-get install qttools5-dev-tools

# Todo - create base config file.



echo "------------------------"
echo "Starting saluma"
# Todo - Create virtual env
