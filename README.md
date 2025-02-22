```markdown
# VLC Video Dubbing with Docker Integration

This project provides a Docker‑based tool that processes a video file to produce a dubbed audio track. The tool:
  • Extracts audio from the video.
  • Transcribes the audio (using faster‑whisper) to obtain spoken segments with timestamps.
  • Dampens the volume in spoken segments.
  • Generates Text-to-Speech (TTS) overlay for the spoken text.
  • Overlays the TTS audio onto the dampened original audio.
  • Concatenates processed audio segments and any non-spoken parts to produce the final dubbed audio file.

All dependencies are containerized so **no local Python package installations are needed**.

## Files

- **main.py**  
  Contains the Python code for audio extraction, transcription, processing, and concatenation.

- **run_entrypoint.sh**  
  An entrypoint script used by the Docker container to run main.py with environment variables.

- **Dockerfile**  
  Builds the Docker image with all necessary dependencies (ffmpeg, ffprobe, espeak, faster‑whisper, pyttsx3).

- **run_docker.sh**  
  A helper shell script that checks for Docker installation, builds the image if needed, and runs the container with proper volume mounts and environment variables.

- **transcribe.vlc.lua**  
  The VLC Lua extension that provides a dialog prompt for the user to enter a target language (if needed) and triggers the Docker container. In our case, it calls `run_docker.sh` with the video path and desired output audio filename.

## Installation & Usage

### Prerequisites

1. **Install Docker**  
   Download and install Docker Desktop from [docker.com](https://www.docker.com/products/docker-desktop) if not already installed.

2. **VLC**  
   Ensure VLC is installed. The Lua extension will be placed in VLC’s extensions folder.

### Running the Tool via Docker

1. **Clone the Repository**  
   Clone this repository to your local machine.

2. **Make Scripts Executable**  
   In your terminal, navigate to the repository directory and run:
   ```bash
   chmod +x run_docker.sh
   ```

3. **Run the Docker-based Dubbing Pipeline**  
   Use the provided shell script to process a video. For example:
   ```bash
   ./run_docker.sh /path/to/sample_video.mp4 /path/to/output_dubbed.wav
   ```
   This script will:
      - Check that Docker is installed.
      - Build the Docker image (if not already built).
      - Run the container with the current directory mounted so that output files are available locally.

### VLC Integration

To integrate with VLC:

1. **Place the Lua Extension**  
   Copy `transcribe.vlc.lua` into your VLC extensions directory. For macOS:
   ```
   ~/Library/Application\ Support/org.videolan.vlc/lua/extensions/
   ```
2. **Usage in VLC**  
   When you play a video in VLC, the extension will check if the dubbed audio exists. If not, it will prompt (or automatically call our helper script) to process the video via Docker. The extension uses `run_docker.sh` to build and run the Docker container so that the processing is fully containerized. The final dubbed audio file will be output back into your local folder, and VLC can stream it accordingly.

### Developer Notes

- **Local Development and Testing**  
  You can also run the Python tool locally in a virtual environment if needed. However, the Docker solution is recommended for a smooth, package-free experience.
  
- **Customization**  
  Adjust volume levels, TTS settings, and transcription parameters in `main.py` as needed.

Happy dubbing!