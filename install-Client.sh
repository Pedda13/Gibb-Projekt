#!/bin/bash

 

# prompt the user for the desired username
read -p "Enter the username for the remote server: " user

 

# prompt the user for the IP address of the remote server
read -p "Enter the IP address of the remote server: " ip_address

 

# generate a new SSH key pair (if you don't already have one)
ssh-keygen -t rsa

 

# copy the public key to the remote server
ssh-copy-id $user@$ip_address