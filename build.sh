#!/usr/bin/env bash

docker build -f processor/Dockerfile -t ole-ya/processor processor
docker build -f api/Dockerfile -t ole-ya/api api
