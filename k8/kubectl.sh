#!/bin/bash

# Update packages
sudo apt update
sleep 10

# Install curl
sudo apt install curl
sleep 10

# Download kubectl
curl -LO https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl
sleep 10

# Install kubectl
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
sleep 10

# Check kubectl version
kubectl version --client
