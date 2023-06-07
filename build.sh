#!/usr/bin/env bash

docker build -f processor/Dockerfile -t ole-ya/processor processor
docker build -f storage-connector/Dockerfile -t ole-ya/storage-connector . 
docker build -f api/Dockerfile -t ole-ya/api .
docker build -f ui/Dockerfile -t ole-ya/ui ui