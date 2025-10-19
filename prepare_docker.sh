#!/bin/bash
set -e

IMAGE_NAME="robot-framework-custom:latest"

# Automatic Architecture Detection
HOST_ARCH=$(uname -m)
PLATFORM="linux/amd64" # Base image ppodgorsek/robot-framework is amd64 only

echo "Host architecture detected: ${HOST_ARCH}"
if [[ "${HOST_ARCH}" != "x86_64" ]]; then
    echo "Host is not x86_64. Forcing platform to ${PLATFORM} for compatibility."
else
    echo "Host is x86_64. Building for native platform: ${PLATFORM}."
fi

echo "Building Docker image ${IMAGE_NAME} for platform ${PLATFORM}..."
docker build --platform "${PLATFORM}" -t "${IMAGE_NAME}" .
echo "Build complete."
