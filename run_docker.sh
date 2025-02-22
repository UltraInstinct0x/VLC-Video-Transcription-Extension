#!/bin/bash
# This shell script checks for Docker installation, builds the Docker image if needed,
# and then runs the container with the current working directory mounted.
# Usage: ./run_docker.sh <video_path> <output_audio>
if ! command -v docker &> /dev/null
then
    echo "Error: Docker is not installed. Please install Docker and try again."
    exit 1
fi

if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <video_path> <output_audio>"
    exit 1
fi

VIDEO_PATH=$(realpath "$1")
OUTPUT_AUDIO=$(realpath "$2")

echo "[INFO] Building Docker image (if not already built)..."
docker build -t vlc-extension .

echo "[INFO] Running Docker container..."
docker run --rm -v "$(pwd):/app" -e VIDEO_PATH="$VIDEO_PATH" -e OUTPUT_AUDIO="$OUTPUT_AUDIO" vlc-extension