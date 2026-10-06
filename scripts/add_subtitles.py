import os
import sys
from pathlib import Path


def add_placeholder_subtitles(output_dir):
    files = sorted(Path(output_dir).glob("*.mp4"))
    for video in files:
        srt_path = video.with_suffix(".srt")
        with open(srt_path, "w", encoding="utf-8") as f:
            f.write("1\n00:00:00,000 --> 00:00:03,000\nThai Subtitle Demo\n")
    print(f"สร้างไฟล์ subtitle placeholder สำหรับ {len(files)} คลิป")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: add_subtitles.py <output_dir>")
        sys.exit(1)
    output_dir = sys.argv[1]
    add_placeholder_subtitles(output_dir)
