#!/usr/bin/env bash

# Generate Python from gRPC definitions
python -m grpc_tools.protoc --proto_path=./protobuf --python_out=./protobuf --pyi_out=./protobuf --grpc_python_out=./protobuf ./protobuf/proto/*.proto && \
# Copy code to all components
find ./storage-connector/proto ./api/proto ./processor/proto -maxdepth 0 -exec cp ./protobuf/proto/*.{py,pyi} {} \;
