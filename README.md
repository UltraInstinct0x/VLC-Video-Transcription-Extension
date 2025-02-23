# VLC AI Auto-Dubbing Extension 🎙️🔄

> Automatically dub and transcribe any video in VLC using AI - powered by faster-whisper

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🎯 What it does

Transform any video played in VLC with AI-powered dubbing and transcription:
- 🤖 Automatic speech recognition and translation
- 🗣️ Natural-sounding AI voice synthesis
- 🎚️ Smart volume mixing and adjustment
- 🎬 Direct VLC integration
- 🐳 Easy setup with Docker

## Key Features

- **Zero Dependencies**: All AI models run in Docker
- **Easy Integration**: Works as a native VLC extension
- **Offline Processing**: Process videos locally on your machine
- **High Quality**: Uses state-of-the-art AI models

## Overview

This project provides a Docker-based tool that automatically creates dubbed audio tracks from videos. The process includes:

1. 🎵 Audio extraction from video
2. 🎙️ Speech-to-text transcription using faster-whisper
3. 🔊 Smart volume adjustment for spoken segments
4. 🗣️ Text-to-speech generation
5. 🎚️ Audio overlay and mixing
6. 🎼 Final audio track compilation

> **Note**: All dependencies are containerized - no local Python packages needed!

## Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/vlc-extension.git
cd vlc-extension

# Make the script executable
chmod +x run_docker.sh

# Run the dubbing pipeline
./run_docker.sh /path/to/video.mp4 /path/to/output.wav
```

## Project Structure

### Core Components

| File | Description |
|------|-------------|
| `main.py` | Core processing logic for audio extraction, transcription, and processing |
| `run_entrypoint.sh` | Docker container entrypoint script |
| `Dockerfile` | Container definition with all dependencies |
| `run_docker.sh` | Helper script for Docker operations |
| `transcribe.vlc.lua` | VLC extension for user interaction |

## Setup Guide

### Prerequisites

- **Docker Desktop**: [Download here](https://www.docker.com/products/docker-desktop)
- **VLC Media Player**: [Download here](https://www.videolan.org/vlc/)

### Installation Steps

1. **Docker Setup**
   ```bash
   # Verify Docker installation
   docker --version
   ```

2. **VLC Extension Installation**
   ```bash
   # macOS
   cp transcribe.vlc.lua ~/Library/Application\ Support/org.videolan.vlc/lua/extensions/
   ```

### Usage Instructions

#### Docker Method
```bash
./run_docker.sh <input_video> <output_audio>
```

Example:
```bash
./run_docker.sh ~/Videos/movie.mp4 ~/Music/dubbed_audio.wav
```

#### VLC Integration

1. Open VLC
2. Navigate to `View → Extensions`
3. Select the dubbing extension
4. Follow the on-screen prompts

## Advanced Configuration

### Customization Options

Edit `main.py` to adjust:
- Volume levels
- TTS voice settings
- Transcription parameters
- Audio processing options

### Development Notes

For local development:
1. Create a virtual environment
2. Install requirements
3. Run `main.py` directly

## Troubleshooting

Common issues and solutions:

- **Permission Denied**: Run `chmod +x run_docker.sh`
- **Docker Not Running**: Start Docker Desktop
- **Missing Output**: Ensure write permissions in output directory

## Contributing

Contributions welcome! Please:
1. Fork the repository
2. Create a feature branch
3. Submit a pull request

## License

MIT License

Copyright (c) 2024 VLC Video Dubbing Extension

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

---

For more information or support, please [open an issue](https://github.com/ultrainstinct0x/vlc-extension/issues).
