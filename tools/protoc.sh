#!/usr/bin/env bash

python -m grpc_tools.protoc -Iprotos --python_out=cli/cli/pb --grpc_python_out=cli/cli/pb protos/event.proto protos/service.proto
python -m grpc_tools.protoc -Iprotos --python_out=manager/manager/pb --grpc_python_out=manager/manager/pb protos/event.proto protos/service.proto
