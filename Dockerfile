# Use Python 3.9 slim base image
FROM python:3.9-slim

# Install system dependencies.
RUN apt-get update && apt-get install -y \
    ffmpeg \
    ffprobe \
    espeak \
    libespeak1 \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies.
RUN pip install faster-whisper pyttsx3

WORKDIR /app
COPY . /app

RUN chmod +x run_entrypoint.sh

# Set the entrypoint to our script.
ENTRYPOINT ["./run_entrypoint.sh"]