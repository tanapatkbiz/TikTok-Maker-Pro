import os
import sys
from pathlib import Path


def generate_captions(output_dir):
    files = sorted(Path(output_dir).glob("*.mp4"))
    for video in files:
        caption_file = video.with_suffix(".txt")
        if not caption_file.exists():
            caption_file.write_text("#TikTok #คลิปสั้น #ทำเงิน #AI #สบาย", encoding="utf-8")
        else:
            content = caption_file.read_text(encoding="utf-8")
            if "#" not in content:
                caption_file.write_text(content + " #TikTok #คลิปสั้น #AI", encoding="utf-8")
    print(f"สร้าง caption สำหรับ {len(files)} คลิป")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: generate_captions.py <output_dir>")
        sys.exit(1)
    generate_captions(sys.argv[1])
