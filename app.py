import json
import os
import subprocess
import sys
import threading
import tkinter as tk
from tkinter import filedialog, messagebox, ttk


class TikTokMakerPro:
    def __init__(self, root):
        self.root = root
        self.root.title("TikTok Maker Pro v1.0")
        self.root.geometry("750x850")
        self.root.resizable(False, False)
        self.root.configure(bg="#0F1419")
        
        self.youtube_url = tk.StringVar()
        self.output_folder = tk.StringVar(value=os.path.join(os.path.expanduser("~"), "TikTokOutput"))
        self.clip_duration = tk.IntVar(value=30)
        self.add_subtitle = tk.BooleanVar(value=True)
        self.add_tts = tk.BooleanVar(value=True)
        self.add_captions = tk.BooleanVar(value=True)
        self.upload_tiktok = tk.BooleanVar(value=False)
        
        self.processing = False
        self.build_ui()
        
    def build_ui(self):
        # Header
        header_frame = tk.Frame(self.root, bg="#1a1f2e", height=80)
        header_frame.pack(fill="x", padx=0, pady=0)
        header_frame.pack_propagate(False)
        
        title = tk.Label(
            header_frame,
            text="🎬 TikTok Maker Pro",
            font=("Arial", 28, "bold"),
            bg="#1a1f2e",
            fg="#00d4ff"
        )
        title.pack(pady=(15, 5))
        
        subtitle = tk.Label(
            header_frame,
            text="แปลงวิดีโอ YouTube เป็นคลิป TikTok อัตโนมัติ",
            font=("Arial", 10),
            bg="#1a1f2e",
            fg="#a0aec0"
        )
        subtitle.pack()
        
        # Main content frame
        content_frame = tk.Frame(self.root, bg="#0F1419")
        content_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # YouTube URL Section
        url_label = tk.Label(
            content_frame,
            text="📺 YouTube URL",
            font=("Arial", 12, "bold"),
            bg="#0F1419",
            fg="#e2e8f0"
        )
        url_label.pack(anchor="w", pady=(0, 8))
        
        url_entry = tk.Entry(
            content_frame,
            textvariable=self.youtube_url,
            font=("Arial", 11),
            bg="#1a1f2e",
            fg="#e2e8f0",
            insertbackground="#00d4ff",
            relief="flat",
            bd=2
        )
        url_entry.pack(fill="x", pady=(0, 15))
        
        # Output Folder Section
        folder_label = tk.Label(
            content_frame,
            text="📁 โฟลเดอร์ผลลัพธ์",
            font=("Arial", 12, "bold"),
            bg="#0F1419",
            fg="#e2e8f0"
        )
        folder_label.pack(anchor="w", pady=(0, 8))
        
        folder_frame = tk.Frame(content_frame, bg="#0F1419")
        folder_frame.pack(fill="x", pady=(0, 15))
        
        folder_entry = tk.Entry(
            folder_frame,
            textvariable=self.output_folder,
            font=("Arial", 10),
            bg="#1a1f2e",
            fg="#e2e8f0",
            insertbackground="#00d4ff",
            relief="flat",
            bd=2
        )
        folder_entry.pack(side="left", fill="x", expand=True, padx=(0, 10))
        
        browse_btn = tk.Button(
            folder_frame,
            text="เลือก",
            command=self.select_folder,
            font=("Arial", 10, "bold"),
            bg="#00d4ff",
            fg="#0F1419",
            relief="flat",
            padx=15,
            pady=5,
            cursor="hand2"
        )
        browse_btn.pack(side="right")
        
        # Clip Duration Section
        duration_label = tk.Label(
            content_frame,
            text="⏱️ ความยาวคลิป (วินาที)",
            font=("Arial", 12, "bold"),
            bg="#0F1419",
            fg="#e2e8f0"
        )
        duration_label.pack(anchor="w", pady=(0, 8))
        
        duration_frame = tk.Frame(content_frame, bg="#0F1419")
        duration_frame.pack(anchor="w", pady=(0, 15))
        
        duration_spin = tk.Spinbox(
            duration_frame,
            from_=15,
            to=60,
            increment=5,
            textvariable=self.clip_duration,
            font=("Arial", 11),
            bg="#1a1f2e",
            fg="#00d4ff",
            width=8,
            relief="flat",
            bd=2
        )
        duration_spin.pack(side="left")
        
        # Options Section
        options_label = tk.Label(
            content_frame,
            text="⚙️ ตัวเลือก",
            font=("Arial", 12, "bold"),
            bg="#0F1419",
            fg="#e2e8f0"
        )
        options_label.pack(anchor="w", pady=(0, 10))
        
        options_frame = tk.Frame(content_frame, bg="#1a1f2e", relief="flat", bd=1)
        options_frame.pack(fill="x", pady=(0, 15), padx=0)
        
        checkbox_style = {
            "font": ("Arial", 11),
            "bg": "#1a1f2e",
            "fg": "#e2e8f0",
            "selectcolor": "#1a1f2e",
            "activebackground": "#1a1f2e",
            "activeforeground": "#00d4ff"
        }
        
        cb1 = tk.Checkbutton(
            options_frame,
            variable=self.add_subtitle,
            text="✅ เพิ่มซับไตรทล์ภาษาไทย",
            **checkbox_style
        )
        cb1.pack(anchor="w", padx=10, pady=8)
        
        cb2 = tk.Checkbutton(
            options_frame,
            variable=self.add_tts,
            text="✅ เพิ่มเสียงพูดไทย (TTS)",
            **checkbox_style
        )
        cb2.pack(anchor="w", padx=10, pady=8)
        
        cb3 = tk.Checkbutton(
            options_frame,
            variable=self.add_captions,
            text="✅ สร้าง Caption และ Hashtags",
            **checkbox_style
        )
        cb3.pack(anchor="w", padx=10, pady=8)
        
        cb4 = tk.Checkbutton(
            options_frame,
            variable=self.upload_tiktok,
            text="📤 อัปโหลดไป TikTok โดยอัตโนมัติ (ต้องมี API)",
            **checkbox_style
        )
        cb4.pack(anchor="w", padx=10, pady=8)
        
        # Progress Section
        progress_label = tk.Label(
            content_frame,
            text="📊 ความคืบหน้า",
            font=("Arial", 12, "bold"),
            bg="#0F1419",
            fg="#e2e8f0"
        )
        progress_label.pack(anchor="w", pady=(15, 8))
        
        self.progress = ttk.Progressbar(
            content_frame,
            length=400,
            mode="indeterminate",
            style="TProgressbar"
        )
        self.progress.pack(fill="x", pady=(0, 10))
        
        self.status_label = tk.Label(
            content_frame,
            text="✅ พร้อมใช้งาน",
            font=("Arial", 10),
            bg="#0F1419",
            fg="#10b981"
        )
        self.status_label.pack(anchor="w", pady=(0, 15))
        
        # Start Button
        self.start_btn = tk.Button(
            content_frame,
            text="🚀 เริ่มประมวลผล",
            command=self.start_processing,
            font=("Arial", 13, "bold"),
            bg="#00d4ff",
            fg="#0F1419",
            relief="flat",
            padx=30,
            pady=12,
            cursor="hand2",
            activebackground="#00c4e5"
        )
        self.start_btn.pack(fill="x", pady=(0, 10))
        
        # Open Folder Button
        self.folder_btn = tk.Button(
            content_frame,
            text="📂 เปิดโฟลเดอร์ผลลัพธ์",
            command=self.open_output_folder,
            font=("Arial", 11),
            bg="#1a1f2e",
            fg="#00d4ff",
            relief="flat",
            padx=20,
            pady=10,
            cursor="hand2"
        )
        self.folder_btn.pack(fill="x")
    
    def select_folder(self):
        folder = filedialog.askdirectory(title="เลือกโฟลเดอร์ผลลัพธ์")
        if folder:
            self.output_folder.set(folder)
    
    def open_output_folder(self):
        folder = self.output_folder.get()
        os.makedirs(folder, exist_ok=True)
        if sys.platform == "win32":
            os.startfile(folder)
        elif sys.platform == "darwin":
            subprocess.run(["open", folder])
        else:
            subprocess.run(["xdg-open", folder])
    
    def start_processing(self):
        url = self.youtube_url.get().strip()
        
        if not url:
            messagebox.showwarning("⚠️ คำเตือน", "กรุณาใส่ URL ของ YouTube")
            return
        
        if "youtube.com" not in url and "youtu.be" not in url:
            messagebox.showerror("❌ ข้อผิดพลาด", "URL ไม่ถูกต้อง กรุณาใส่ URL ของ YouTube")
            return
        
        if self.processing:
            messagebox.showinfo("ℹ️ ข้อมูล", "กำลังประมวลผลอยู่ กรุณารอสักครู่")
            return
        
        self.processing = True
        self.start_btn.config(state="disabled")
        self.progress.start()
        self.status_label.config(text="⏳ กำลังประมวลผล...", fg="#f59e0b")
        
        thread = threading.Thread(target=self.run_processing, daemon=True)
        thread.start()
    
    def run_processing(self):
        try:
            config = {
                "youtube_url": self.youtube_url.get().strip(),
                "output_folder": self.output_folder.get().strip() or os.path.join(os.path.expanduser("~"), "TikTokOutput"),
                "clip_duration": int(self.clip_duration.get()),
                "add_subtitle": bool(self.add_subtitle.get()),
                "add_tts": bool(self.add_tts.get()),
                "add_captions": bool(self.add_captions.get()),
                "upload_tiktok": bool(self.upload_tiktok.get()),
            }
            
            os.makedirs(config["output_folder"], exist_ok=True)
            
            config_path = os.path.join(config["output_folder"], "temp_config.json")
            with open(config_path, "w", encoding="utf-8") as f:
                json.dump(config, f, ensure_ascii=False, indent=2)
            
            # Get the directory where process.py is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            process_script = os.path.join(script_dir, "process.py")
            
            result = subprocess.run(
                [sys.executable, process_script, config_path],
                capture_output=True,
                text=True,
                cwd=script_dir
            )
            
            if result.returncode == 0:
                self.status_label.config(text="✅ ประมวลผลเสร็จสิ้นแล้ว!", fg="#10b981")
                messagebox.showinfo(
                    "✅ สำเร็จ",
                    "ประมวลผลวิดีโอเสร็จสิ้น!\n\nคลิปได้ถูกบันทึกในโฟลเดอร์:\n" + config["output_folder"]
                )
            else:
                error_msg = result.stderr or "ไม่ทราบข้อผิดพลาด"
                self.status_label.config(text=f"❌ ข้อผิดพลาด: {error_msg[:50]}", fg="#ef4444")
                messagebox.showerror(
                    "❌ ข้อผิดพลาด",
                    f"เกิดข้อผิดพลาดระหว่างประมวลผล:\n\n{error_msg}"
                )
        except Exception as exc:
            error_msg = str(exc)
            self.status_label.config(text=f"❌ ข้อผิดพลาด: {error_msg[:50]}", fg="#ef4444")
            messagebox.showerror("❌ ข้อผิดพลาด", f"เกิดข้อผิดพลาด:\n\n{error_msg}")
        finally:
            self.progress.stop()
            self.start_btn.config(state="normal")
            self.processing = False


if __name__ == "__main__":
    root = tk.Tk()
    
    # Configure style
    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TProgressbar', background='#00d4ff', troughcolor='#1a1f2e', bordercolor='#1a1f2e')
    
    app = TikTokMakerPro(root)
    root.mainloop()
