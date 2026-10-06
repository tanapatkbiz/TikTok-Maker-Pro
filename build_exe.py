import json
import os
import shutil
import subprocess
import sys
from pathlib import Path


def run(cmd):
    subprocess.run(cmd, check=True)


def load_config(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def ensure_tools():
    for tool in ["yt-dlp", "ffmpeg"]:
        if tool == "ffmpeg":
            try:
                subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
            except Exception:
                raise RuntimeError("FFmpeg ไม่พบใน PATH กรุณาติดตั้ง FFmpeg ก่อนใช้งาน")
        else:
            try:
                __import__("yt_dlp")
            except Exception:
                raise RuntimeError("yt-dlp ยังไม่ได้ติดตั้ง กรุณาติดตั้ง dependency ก่อนใช้งาน")


def download_video(url, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    video_path = os.path.join(output_dir, "input.mp4")
    if os.path.exists(video_path):
        os.remove(video_path)
    run(["yt-dlp", "-f", "best[ext=mp4]/best", "-o", video_path, url])
    return video_path


def split_video(input_file, output_dir, clip_duration):
    script_path = os.path.join("scripts", "split_video.py")
    run([sys.executable, script_path, input_file, output_dir, str(clip_duration)])


def add_subtitles(output_dir):
    script_path = os.path.join("scripts", "add_subtitles.py")
    run([sys.executable, script_path, output_dir])


def generate_tts(output_dir):
    script_path = os.path.join("scripts", "generate_tts.py")
    run([sys.executable, script_path, output_dir])


def generate_captions(output_dir):
    script_path = os.path.join("scripts", "generate_captions.py")
    run([sys.executable, script_path, output_dir])


def main():
    config_path = sys.argv[1]
    config = load_config(config_path)
    output_folder = config.get("output_folder", "output")
    clip_duration = int(config.get("clip_duration", 30))

    print("[1/5] ตรวจสอบเครื่องมือ")
    ensure_tools()

    print("[2/5] ดาวน์โหลดวิดีโอจาก YouTube")
    input_file = download_video(config["youtube_url"], output_folder)

    print("[3/5] ตัดคลิปออกเป็นวิดีโอสั้น")
    split_video(input_file, output_folder, clip_duration)

    if config.get("option_subtitle"):
        print("[4/5] เพิ่มซับไทย")
        add_subtitles(output_folder)

    if config.get("option_tts"):
        print("[5/5] สร้าง Thai TTS และ Caption")
        generate_tts(output_folder)
        generate_captions(output_folder)

    print("เสร็จสิ้น")


if __name__ == "__main__":
    main()
