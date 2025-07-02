#!/bin/bash

docker buildx build \
  --platform linux/arm64 \
  -t vpn-telegram-bot:v1.0 \
  -f Dockerfile \
  --output type=docker,dest=vpn-telegram-bot-arm64.tar ../..
