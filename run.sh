#!/usr/bin/env bash

docker ps -q --filter "name=processor" | grep -q . && docker stop processor
docker ps -q --filter "name=storage-connector" | grep -q . && docker stop storage-connector
docker ps -q --filter "name=api" | grep -q . && docker stop api
docker ps -q --filter "name=ui" | grep -q . && docker stop ui
docker ps -q --filter "name=processor" | grep -q . && docker rm processor
docker ps -q --filter "name=storage-connector" | grep -q . && docker rm storage-connector
docker ps -q --filter "name=api" | grep -q . && docker rm api
docker ps -q --filter "name=ui" | grep -q . && docker rm ui
docker compose -f docker-compose.yaml up -d
