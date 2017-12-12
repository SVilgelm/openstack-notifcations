#!/usr/bin/env bash

mkdir .tmp
for i in cli manager; do
    pb_folder=osn_$i/pb
    mkdir -p .tmp/$pb_folder
    cp protos/*.proto .tmp/$pb_folder
    sed -e "s|import \"/|import \"$pb_folder/|g" protos/service.proto > .tmp/$pb_folder/service.proto
    python -m grpc_tools.protoc -I .tmp/ --python_out=$i/ .tmp/$pb_folder/*.proto
    python -m grpc_tools.protoc -I .tmp/ --grpc_python_out=$i/ .tmp/$pb_folder/service.proto
done
rm -rf .tmp
