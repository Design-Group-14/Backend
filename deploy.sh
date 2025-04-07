#!/bin/bash

cd /home/ubuntu/Backend

echo "Pulling latest code..."
git pull origin master

echo "Rebuilding docker containers..."
docker-compose down
docker-compose build --no-cache
docker-compose up -d

echo "Deployment complete."