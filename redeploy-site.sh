#!/bin/bash

cd ~/logan-portfolio

git fetch && git reset origin/main --hard

docker compose -f docker-compose.prod.yml down
docker compose -f docker-compose.prod.yml up -d --build

chmod +x redeploy-site.sh
