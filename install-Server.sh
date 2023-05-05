#!/bin/bash

# Update the package list
sudo apt-get update

# Install openssh-server package
sudo apt-get install openssh-server -y

# Modify sshd_config file
sudo sed -i 's/#Port 22/Port 22/g' /etc/ssh/sshd_config
sudo sed -i 's/#AddressFamily any/AddressFamily any/g' /etc/ssh/sshd_config
sudo sed -i 's/#ListenAddress 0.0.0.0/ListenAddress 0.0.0.0/g' /etc/ssh/sshd_config
sudo sed -i 's/#ListenAddress ::/ListenAddress ::/g' /etc/ssh/sshd_config
sudo sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/g' /etc/ssh/sshd_config
sudo sed -i 's/#MaxAuthTries 6/MaxAuthTries 6/g' /etc/ssh/sshd_config
sudo sed -i 's/#PubkeyAuthentication yes/PubkeyAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/#AuthorizedKeysFile/AuthorizedKeysFile/g' /etc/ssh/sshd_config
sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication yes/g' /etc/ssh/sshd_config
sudo sed -i 's/#KbdInteractiveAuthentication no/KbdInteractiveAuthentication no/g' /etc/ssh/sshd_config
sudo sed -i 's/#UsePAM yes/UsePAM yes/g' /etc/ssh/sshd_config
sudo sed -i 's/#X11Forwarding no/X11Forwarding yes/g' /etc/ssh/sshd_config
