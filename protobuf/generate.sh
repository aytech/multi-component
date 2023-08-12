#!/usr/bin/env bash

python -m grpc_tools.protoc --proto_path=. --python_out=. --pyi_out=. --grpc_python_out=. ./proto/*.proto
mv proto/*.py generated
mv proto/*.pyi generated
cp -r generated/*.py ../storage-connector/proto
cp -r generated/*.pyi ../storage-connector/proto
cp -r generated/*.py ../api/proto
cp -r generated/*.pyi ../api/proto