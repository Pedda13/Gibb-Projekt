#!/bin/bash

# Prompt the user to enter the IP address of the remote server
read -p "Enter the IP address of the remote server: " ip_address

# Check if the IP address is empty
if [[ -z "$ip_address" ]]; then
  echo "IP address cannot be empty"
  exit 1
fi

# Prompt the user to enter the username of the remote server
read -p "Enter the username of the remote server (default is root): " username

# Use "root" as the default username if none is provided
if [[ -z "$username" ]]; then
  username="root"
fi

# Generate an SSH key
ssh-keygen -t rsa

# Copy the SSH key to the remote server's user account
ssh-copy-id $username@$ip_address
