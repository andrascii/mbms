#!/bin/bash

docker buildx build \
  --platform linux/arm64 \
  -t mbms:v0.1 \
  -f Dockerfile \
  --output type=docker,dest=mbms-arm64.tar ..
