#!/usr/bin/env python3
"""
This script processes a video file as follows:
  1. Extracts the audio track from the video.
  2. Transcribes the audio using faster-whisper to obtain spoken segments (with timestamps).
  3. For each spoken segment:
       - Extracts the corresponding audio.
       - Lowers its volume to dampen the human voice.
       - Generates TTS audio for the spoken text.
       - Overlays the TTS audio on the lowered segment.
  4. Splits the entire audio into chunks (non-spoken and processed spoken segments)
     and concatenates them into a final dubbed audio file.
Usage:
  python main.py <video_path> <output_audio>
Example:
  python main.py /app/sample_video.mp4 /app/output_dubbed.wav
"""

import os
import sys
import subprocess
import argparse
from datetime import timedelta
from faster_whisper import WhisperModel
import pyttsx3

def format_timestamp(seconds: float) -> str:
    td = timedelta(seconds=seconds)
    total_seconds = int(td.total_seconds())
    hours = total_seconds // 3600
    minutes = (total_seconds % 3600) // 60
    secs = total_seconds % 60
    milliseconds = int((td.total_seconds() - total_seconds) * 1000)
    return f"{hours:02}:{minutes:02}:{secs:02},{milliseconds:03}"

def extract_audio(video_path: str, audio_filename: str):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", video_path,
        "-vn",
        "-acodec", "pcm_s16le",
        "-ar", "44100",
        "-ac", "2",
        audio_filename
    ]
    print("[INFO] Extracting audio...")
    subprocess.run(cmd, check=True)
    print(f"[INFO] Audio extracted to {audio_filename}")

def get_audio_duration(audio_filename: str) -> float:
    cmd = [
        "ffprobe",
        "-v", "error",
        "-show_entries", "format=duration",
        "-of", "default=noprint_wrappers=1:nokey=1",
        audio_filename
    ]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
    return float(result.stdout.strip())

def extract_audio_segment(input_audio: str, start: float, duration: float, output_audio: str):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_audio,
        "-ss", str(start),
        "-t", str(duration),
        output_audio
    ]
    subprocess.run(cmd, check=True)

def lower_audio_volume(input_audio: str, output_audio: str, volume: float=0.2):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", input_audio,
        "-af", f"volume={volume}",
        output_audio
    ]
    subprocess.run(cmd, check=True)

def generate_tts(text: str, output_audio: str):
    engine = pyttsx3.init()
    engine.save_to_file(text, output_audio)
    engine.runAndWait()

def overlay_audio(fg_audio: str, bg_audio: str, output_audio: str):
    cmd = [
        "ffmpeg",
        "-y",
        "-i", bg_audio,
        "-i", fg_audio,
        "-filter_complex", "[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=2",
        output_audio
    ]
    subprocess.run(cmd, check=True)

def concatenate_audios(audio_files: list, output_audio: str):
    list_filename = "concat_list.txt"
    with open(list_filename, "w") as f:
        for audio in audio_files:
            f.write(f"file '{os.path.abspath(audio)}'\n")
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", list_filename,
        "-c", "copy",
        output_audio
    ]
    subprocess.run(cmd, check=True)
    os.remove(list_filename)

def process_spoken_segment(full_audio: str, segment, index: int) -> str:
    seg_start = segment.start
    seg_duration = segment.end - segment.start

    seg_orig = f"seg_{index}_orig.wav"
    seg_lower = f"seg_{index}_lower.wav"
    seg_tts = f"seg_{index}_tts.wav"
    seg_final = f"seg_{index}_final.wav"

    print(f"[INFO] Processing spoken segment {index}: start={seg_start:.2f}, duration={seg_duration:.2f}")

    extract_audio_segment(full_audio, seg_start, seg_duration, seg_orig)
    lower_audio_volume(seg_orig, seg_lower, volume=0.2)
    generate_tts(segment.text, seg_tts)
    overlay_audio(seg_tts, seg_lower, seg_final)

    for fname in [seg_orig, seg_lower, seg_tts]:
        if os.path.exists(fname):
            os.remove(fname)

    return seg_final

def transcribe_and_dub(video_path: str, output_audio: str):
    base, _ = os.path.splitext(video_path)
    full_audio = base + "_full.wav"
    extract_audio(video_path, full_audio)
    total_duration = get_audio_duration(full_audio)
    print(f"[INFO] Audio duration: {total_duration:.2f} seconds")

    print("[INFO] Running transcription with faster-whisper...")
    model_size = "base"
    model = WhisperModel(model_size, device="cpu")
    segments, info = model.transcribe(video_path, beam_size=5)
    print("[INFO] Transcription complete.")

    processed_chunks = []
    current_time = 0.0
    seg_index = 0

    for segment in segments:
        if segment.start > current_time:
            non_speech = f"chunk_{seg_index}_nonspeech.wav"
            duration = segment.start - current_time
            extract_audio_segment(full_audio, current_time, duration, non_speech)
            processed_chunks.append(non_speech)
            seg_index += 1

        processed_segment = process_spoken_segment(full_audio, segment, seg_index)
        processed_chunks.append(processed_segment)
        seg_index += 1

        current_time = segment.end

    if current_time < total_duration:
        non_speech = f"chunk_{seg_index}_nonspeech.wav"
        duration = total_duration - current_time
        extract_audio_segment(full_audio, current_time, duration, non_speech)
        processed_chunks.append(non_speech)

    print("[INFO] Concatenating audio chunks...")
    concatenate_audios(processed_chunks, output_audio)
    print(f"[INFO] Final dubbed audio saved as {output_audio}")

    for chunk in processed_chunks:
        if os.path.exists(chunk):
            os.remove(chunk)
    if os.path.exists(full_audio):
        os.remove(full_audio)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Extract audio, dampen spoken segments, and overlay TTS dubbing.")
    parser.add_argument("video", help="Path to the video file")
    parser.add_argument("output", help="Filename for the final dubbed audio output (e.g., /app/output_dubbed.wav)")
    args = parser.parse_args()

    transcribe_and_dub(args.video, args.output)