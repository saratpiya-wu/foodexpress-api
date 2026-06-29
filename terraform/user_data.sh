#!/bin/bash
set -e

# Update and install Docker
apt-get update -y
apt-get install -y docker.io
systemctl enable docker
systemctl start docker

# Pull and run the FoodExpress container
# (Jenkins will also push new versions to this same instance on later builds)
docker pull ${docker_image}
docker run -d --restart unless-stopped -p 80:5000 --name foodexpress ${docker_image}
