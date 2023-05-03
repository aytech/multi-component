#!/usr/bin/env bash

docker build -f processor/Dockerfile -t ole-ya/processor processor
docker build -f api/Dockerfile -t ole-ya/api api
docker build -f ui/Dockerfile -t ole-ya/ui ui