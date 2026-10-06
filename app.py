import json
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import messagebox, ttk


def ensure_pip_dependencies():
    required = [
        "yt-dlp",
        "pyttsx3",
        "requests",
        "whisper",
        "pyinstaller",
    ]
    for package in required:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])


def ensure_ffmpeg():
    ffmpeg_path = os.environ.get("FFMPEG_PATH") or "ffmpeg"
    try:
        subprocess.run([ffmpeg_path, "-version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
        return True
    except Exception:
        messagebox.showwarning(
            "FFmpeg ไม่พบ",
            "กรุณาติดตั้ง FFmpeg หรือเพิ่ม path ของ ffmpeg ลงใน PATH ก่อนใช้งาน\n"
            "หากใช้ Windows เราขอแนะนำให้ติดตั้งจาก https://www.ffmpeg.org/download.html"
        )
        return False


class App:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Maker Pro")
        self.root.geometry("680x700")
        self.root.resizable(False, False)
        self.root.configure(bg="#111827")

        self.youtube_url = tk.StringVar()
        self.output_folder = tk.StringVar(value=os.path.join(os.getcwd(), "output"))
        self.clip_duration = tk.IntVar(value=30)
        self.option_subtitle = tk.BooleanVar(value=True)
        self.option_tts = tk.BooleanVar(value=True)
        self.option_caption = tk.BooleanVar(value=True)

        self.build_ui()

    def build_ui(self):
        title = tk.Label(
            self.root,
            text="TikTok Maker Pro",
            font=("Tahoma", 24, "bold"),
            bg="#111827",
            fg="#F9FAFB",
        )
        title.pack(pady=(24, 18))

        frame = tk.Frame(self.root, bg="#1F2937", padx=20, pady=18)
        frame.pack(fill="both", expand=True, padx=18, pady=8)

        tk.Label(frame, text="YouTube URL", font=("Tahoma", 12, "bold"), bg="#1F2937", fg="#F9FAFB").pack(anchor="w")
        url_entry = tk.Entry(frame, textvariable=self.youtube_url, font=("Tahoma", 11), width=68)
        url_entry.pack(fill="x", pady=(8, 16))

        tk.Label(frame, text="Folder ผลลัพธ์", font=("Tahoma", 12, "bold"), bg="#1F2937", fg="#F9FAFB").pack(anchor="w")
        folder_row = tk.Frame(frame, bg="#1F2937")
        folder_row.pack(fill="x", pady=(8, 18))
        folder_entry = tk.Entry(folder_row, textvariable=self.output_folder, width=58, font=("Tahoma", 11))
        folder_entry.pack(side="left")
        browse_btn = tk.Button(folder_row, text="เลือกโฟลเดอร์", command=self.select_folder, bg="#06B6D4", fg="#111827", font=("Tahoma", 10, "bold"))
        browse_btn.pack(side="left", padx=(10, 0))

        tk.Label(frame, text="ความยาวคลิป (วินาที)", font=("Tahoma", 12, "bold"), bg="#1F2937", fg="#F9FAFB").pack(anchor="w")
        duration_spin = tk.Spinbox(frame, from_=15, to=60, textvariable=self.clip_duration, width=8, font=("Tahoma", 11))
        duration_spin.pack(anchor="w", pady=(8, 18))

        options = tk.Frame(frame, bg="#1F2937")
        options.pack(anchor="w")
        tk.Checkbutton(options, variable=self.option_subtitle, text="เพิ่มซับไทย", bg="#1F2937", fg="#F9FAFB", font=("Tahoma", 11), selectcolor="#111827").pack(anchor="w")
        tk.Checkbutton(options, variable=self.option_tts, text="เพิ่มเสียงไทย (Thai TTS)", bg="#1F2937", fg="#F9FAFB", font=("Tahoma", 11), selectcolor="#111827").pack(anchor="w")
        tk.Checkbutton(options, variable=self.option_caption, text="สร้าง Caption และ Hashtags", bg="#1F2937", fg="#F9FAFB", font=("Tahoma", 11), selectcolor="#111827").pack(anchor="w")

        self.progress = ttk.Progressbar(self.root, orient="horizontal", length=520, mode="indeterminate")
        self.progress.pack(pady=(10, 10))

        self.status = tk.Label(self.root, text="พร้อมใช้งาน", fg="#34D399", bg="#111827", font=("Tahoma", 10))
        self.status.pack()

        self.start_btn = tk.Button(
            self.root,
            text="เริ่มประมวลผล",
            command=self.start_processing,
            bg="#10B981",
            fg="#111827",
            font=("Tahoma", 12, "bold"),
            width=20,
            height=2,
        )
        self.start_btn.pack(pady=(20, 8))

    def select_folder(self):
        folder = tk.filedialog.askdirectory(title="เลือกโฟลเดอร์ผลลัพธ์")
        if folder:
            self.output_folder.set(folder)

    def start_processing(self):
        if not self.youtube_url.get().strip():
            messagebox.showwarning("คำเตือน", "กรุณาใส่ URL ของ YouTube")
            return

        if not ensure_ffmpeg():
            return

        self.start_btn.config(state="disabled")
        self.progress.start(12)
        self.status.config(text="กำลังเริ่มประมวลผล...", fg="#FBBF24")

        thread = threading.Thread(target=self.run_process, daemon=True)
        thread.start()

    def run_process(self):
        try:
            config = {
                "youtube_url": self.youtube_url.get().strip(),
                "output_folder": self.output_folder.get().strip() or os.path.join(os.getcwd(), "output"),
                "clip_duration": int(self.clip_duration.get()),
                "option_subtitle": bool(self.option_subtitle.get()),
                "option_tts": bool(self.option_tts.get()),
                "option_caption": bool(self.option_caption.get()),
            }
            os.makedirs(config["output_folder"], exist_ok=True)
            with open("temp_config.json", "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)

            result = subprocess.run([sys.executable, "process.py", "temp_config.json"], capture_output=True, text=True)

            if result.returncode != 0:
                self.status.config(text=f"เกิดข้อผิดพลาด: {result.stderr[:200]}", fg="#F87171")
                messagebox.showerror("เกิดข้อผิดพลาด", result.stderr or "ไม่ทราบสาเหตุ")
            else:
                self.status.config(text="ประมวลผลเสร็จสิ้น", fg="#34D399")
                messagebox.showinfo("สำเร็จ", "สร้างคลิป TikTok เสร็จสิ้นแล้ว\nกรุณาเปิดโฟลเดอร์ผลลัพธ์เพื่อตรวจสอบ")
        except Exception as exc:
            self.status.config(text=f"ข้อผิดพลาด: {exc}", fg="#F87171")
            messagebox.showerror("ข้อผิดพลาด", str(exc))
        finally:
            self.progress.stop()
            self.start_btn.config(state="normal")


if __name__ == "__main__":
    ensure_pip_dependencies()
    root = tk.Tk()
    App(root)
    root.mainloop()
