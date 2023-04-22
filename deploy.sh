#!/usr/bin/env bash

docker pull localhost:5000/ole-ya/processor
docker pull localhost:5000/ole-ya/api
docker pull localhost:5000/ole-ya/ui
docker ps -q --filter "name=processor" | grep -q . && docker stop processor
docker ps -q --filter "name=api" | grep -q . && docker stop api
docker ps -q --filter "name=ui" | grep -q . && docker stop ui
docker ps -q --filter "name=processor" | grep -q . && docker rm processor
docker ps -q --filter "name=api" | grep -q . && docker rm api
docker ps -q --filter "name=ui" | grep -q . && docker rm ui
docker compose -f docker-compose.yaml up -d
