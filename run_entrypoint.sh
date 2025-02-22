#!/bin/bash
# This entrypoint script is run inside the Docker container.
# It reads environment variables VIDEO_PATH and OUTPUT_AUDIO and calls main.py
if [ -z "$VIDEO_PATH" ] || [ -z "$OUTPUT_AUDIO" ]; then
  echo "Error: Environment variables VIDEO_PATH and OUTPUT_AUDIO must be set."
  exit 1
fi
python main.py "$VIDEO_PATH" "$OUTPUT_AUDIO"