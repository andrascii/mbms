#!/bin/bash

docker buildx build \
  --platform linux/amd64 \
  -t mbms:v0.1 \
  -f Dockerfile \
  --output type=docker,dest=mbms-amd64.tar ..
