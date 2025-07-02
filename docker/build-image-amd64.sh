#!/bin/bash

docker buildx build \
  --platform linux/amd64 \
  -t vpn-telegram-bot:v1.0 \
  -f Dockerfile \
  --output type=docker,dest=vpn-telegram-bot-amd64.tar ../..
