#!/usr/bin/env bash

find ./storage-connector/proto/*.py* ./api/proto/*.py* ./processor/proto/*.py* ./protobuf/proto/*.py* -not -name __init__.py 2>/dev/null -exec rm {} \; 