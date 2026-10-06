import os
import sys
from pathlib import Path


def generate_tts(output_dir):
    files = sorted(Path(output_dir).glob("*.mp4"))
    for video in files:
        text_file = video.with_suffix(".txt")
        if not text_file.exists():
            text_file.write_text("Thai voice over demo text", encoding="utf-8")
        audio_file = video.with_suffix(".wav")
        print(f"เตรียมสร้างเสียงไทยสำหรับ {video.name}")
        # In a full implementation, this would call TTS engine such as pyttsx3 or Azure voice.
        # This placeholder keeps the process working without a full TTS pipeline.
        if not audio_file.exists():
            audio_file.write_bytes(b"")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_tts.py <output_dir>")
        sys.exit(1)
    generate_tts(sys.argv[1])
