#!/usr/bin/env bash

docker build -f processor/Dockerfile -t ole-ya/processor processor
docker build -f api/Dockerfile -t ole-ya/api api
docker build -f ui/Dockerfile -t ole-ya/ui ui

docker tag ole-ya/processor 10.0.1.22:5000/ole-ya/processor
docker tag ole-ya/api 10.0.1.22:5000/ole-ya/api
docker tag ole-ya/ui 10.0.1.22:5000/ole-ya/ui

docker push 10.0.1.22:5000/ole-ya/processor
docker push 10.0.1.22:5000/ole-ya/api
docker push 10.0.1.22:5000/ole-ya/ui