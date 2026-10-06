#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import os
import subprocess
import sys
from pathlib import Path


def log_message(step, message):
    print(f"[{step}] {message}")
    sys.stdout.flush()


def ensure_dependencies():
    """ตรวจสอบและติดตั้ง dependencies ที่จำเป็น"""
    try:
        import yt_dlp
    except ImportError:
        log_message("SETUP", "ติดตั้ง yt-dlp...")
        subprocess.run([sys.executable, "-m", "pip", "install", "yt-dlp"], check=True)
    
    try:
        import whisper
    except ImportError:
        log_message("SETUP", "ติดตั้ง openai-whisper...")
        subprocess.run([sys.executable, "-m", "pip", "install", "openai-whisper"], check=True)
    
    try:
        import pyttsx3
    except ImportError:
        log_message("SETUP", "ติดตั้ง pyttsx3...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyttsx3"], check=True)


def check_ffmpeg():
    """ตรวจสอบว่า FFmpeg อยู่ใน PATH"""
    try:
        subprocess.run(["ffmpeg", "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        log_message("ERROR", "FFmpeg ไม่พบ กรุณาติดตั้ง FFmpeg จาก https://www.ffmpeg.org/download.html")
        return False


def download_youtube(url, output_path):
    """ดาวน์โหลดวิดีโอจาก YouTube"""
    log_message("1/5", "📥 ดาวน์โหลดวิดีโอจาก YouTube...")
    video_file = os.path.join(output_path, "input.mp4")
    
    if os.path.exists(video_file):
        os.remove(video_file)
    
    try:
        import yt_dlp
        ydl_opts = {
            'format': 'best[ext=mp4]/best',
            'outtmpl': video_file.replace('.mp4', ''),
            'quiet': False,
            'no_warnings': False,
        }
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        if not os.path.exists(video_file):
            # ค้นหาไฟล์ที่ดาวน์โหลด
            for file in os.listdir(output_path):
                if file.startswith("input") and file.endswith(".mp4"):
                    video_file = os.path.join(output_path, file)
                    break
        
        log_message("1/5", f"✅ ดาวน์โหลดเสร็จ: {video_file}")
        return video_file
    except Exception as e:
        raise RuntimeError(f"ไม่สามารถดาวน์โหลดวิดีโอได้: {str(e)}")


def split_video(input_file, output_path, clip_duration):
    """ตัดวิดีโอเป็นคลิปสั้น"""
    log_message("2/5", f"✂️ ตัดวิดีโอเป็นคลิป {clip_duration} วินาที...")
    
    output_pattern = os.path.join(output_path, "clip_%03d.mp4")
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-f", "segment",
        "-segment_time", str(clip_duration),
        "-c:v", "libx264",
        "-preset", "fast",
        "-c:a", "aac",
        "-movflags", "+faststart",
        output_pattern
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        clips = sorted([f for f in os.listdir(output_path) if f.startswith("clip_") and f.endswith(".mp4")])
        log_message("2/5", f"✅ สร้างคลิปเสร็จ: {len(clips)} คลิป")
        return clips
    except Exception as e:
        raise RuntimeError(f"ไม่สามารถตัดวิดีโอได้: {str(e)}")


def extract_subtitles(input_file, output_path):
    """แยกซับไตรทล์จากวิดีโอ"""
    log_message("3/5", "📝 สร้างซับไตรทล์ภาษาไทย...")
    
    try:
        import whisper
        model = whisper.load_model("base", device="cpu")
        result = model.transcribe(input_file, language="th", verbose=False)
        
        srt_file = os.path.join(output_path, "subtitles.srt")
        with open(srt_file, "w", encoding="utf-8") as f:
            for i, segment in enumerate(result["segments"], 1):
                start = int(segment["start"])
                end = int(segment["end"])
                text = segment["text"].strip()
                f.write(f"{i}\n{start:02d}:{start%60:02d}:{int((start%1)*1000):03d} --> {end:02d}:{end%60:02d}:{int((end%1)*1000):03d}\n{text}\n\n")
        
        log_message("3/5", f"✅ สร้างซับไตรทล์เสร็จ: {srt_file}")
        return srt_file
    except Exception as e:
        log_message("3/5", f"⚠️ ไม่สามารถสร้างซับไตรทล์ได้: {str(e)}")
        return None


def generate_tts(text, output_path):
    """สร้างเสียงพูดไทย"""
    log_message("4/5", "🎙️ สร้างเสียงพูดไทย (TTS)...")
    
    try:
        import pyttsx3
        engine = pyttsx3.init()
        
        # ตั้งค่า Thai voice
        engine.setProperty('rate', 150)
        engine.setProperty('volume', 1.0)
        
        audio_file = os.path.join(output_path, "voiceover.mp3")
        engine.save_to_file(text, audio_file)
        engine.runAndWait()
        
        log_message("4/5", f"✅ สร้างเสียงเสร็จ: {audio_file}")
        return audio_file
    except Exception as e:
        log_message("4/5", f"⚠️ ไม่สามารถสร้างเสียงได้: {str(e)}")
        return None


def generate_captions(output_path, clip_count):
    """สร้าง Caption และ Hashtags สำหรับ TikTok"""
    log_message("5/5", "📋 สร้าง Caption และ Hashtags...")
    
    thai_hashtags = [
        "#TikTok", "#คลิปสั้น", "#ทำเงิน", "#AI",
        "#สร้างเนื้อหา", "#มันได้เงิน", "#ทำเงินออนไลน์",
        "#Thailand", "#สำเร็จ", "#ยอดนิยม"
    ]
    
    captions_data = []
    for i in range(1, clip_count + 1):
        caption = {
            "clip": f"clip_{i:03d}.mp4",
            "caption": f"🎬 คลิปที่ {i}\n\nสร้างจากวิดีโอ YouTube เป็นคลิป TikTok\nพร้อมซับไตรทล์และเสียงพูด\n\n" + " ".join(thai_hashtags[:5]),
            "hashtags": thai_hashtags
        }
        captions_data.append(caption)
    
    captions_file = os.path.join(output_path, "captions.json")
    with open(captions_file, "w", encoding="utf-8") as f:
        json.dump(captions_data, f, ensure_ascii=False, indent=2)
    
    log_message("5/5", f"✅ สร้าง Caption เสร็จ: {captions_file}")
    return captions_file


def main():
    if len(sys.argv) < 2:
        print("Usage: process.py <config_file>")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            config = json.load(f)
    except Exception as e:
        log_message("ERROR", f"ไม่สามารถอ่านไฟล์การตั้งค่าได้: {str(e)}")
        sys.exit(1)
    
    log_message("SETUP", "ตรวจสอบ dependencies...")
    ensure_dependencies()
    
    if not check_ffmpeg():
        sys.exit(1)
    
    output_folder = config.get("output_folder", os.path.expanduser("~/TikTokOutput"))
    os.makedirs(output_folder, exist_ok=True)
    
    try:
        # Step 1: Download YouTube video
        video_file = download_youtube(config["youtube_url"], output_folder)
        
        # Step 2: Split video into clips
        clips = split_video(video_file, output_folder, config.get("clip_duration", 30))
        
        # Step 3: Add subtitles
        if config.get("add_subtitle"):
            extract_subtitles(video_file, output_folder)
        
        # Step 4: Generate TTS
        if config.get("add_tts"):
            generate_tts("สวัสดี นี่คือเสียงพูดไทยจากโปรแกรม TikTok Maker Pro", output_folder)
        
        # Step 5: Generate captions
        if config.get("add_captions"):
            generate_captions(output_folder, len(clips))
        
        log_message("✅", "การประมวลผลเสร็จสิ้นแล้ว!")
        log_message("ℹ️", f"ผลลัพธ์ถูกบันทึกไว้ใน: {output_folder}")
        
    except Exception as e:
        log_message("ERROR", str(e))
        sys.exit(1)


if __name__ == "__main__":
    main()
