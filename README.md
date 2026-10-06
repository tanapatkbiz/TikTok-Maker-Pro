# TikTok Maker Pro

TikTok Maker Pro เป็นโปรเจกต์สำหรับ Windows ที่ช่วยแปลงวิดีโอ YouTube เป็นวิดีโอสั้น TikTok แบบอัตโนมัติ

ฟีเจอร์หลัก:
- GUI ภาษาไทยสำหรับผู้ใช้กรอก URL เอง
- ดาวน์โหลดวิดีโอจาก YouTube
- ตัดวิดีโอเป็นคลิปสั้นแบบหลายคลิป
- เพิ่มซับไทยอัตโนมัติ
- เพิ่มเสียงอ่านบทความแบบ Thai TTS
- สร้าง Caption และ Hashtags สำหรับ TikTok
- รันได้ผ่านไฟล์ `.exe` สำหรับ Windows

โครงสร้างโปรเจกต์:

```text
TikTok-Maker-Pro/
├── app.py
├── process.py
├── build_exe.py
├── requirements.txt
├── README.md
├── .gitignore
├── config/
│   └── settings.json
├── scripts/
│   ├── __init__.py
│   ├── split_video.py
│   ├── add_subtitles.py
│   ├── generate_tts.py
│   └── generate_captions.py
├── output/
│   └── (ไฟล์คลิปที่สร้างเสร็จ)
└── dist/
    └── (ผลลัพธ์จาก PyInstaller)
```

วิธีสร้างไฟล์ EXE สำหรับ Windows:

```bash
pip install -r requirements.txt
python build_exe.py
```

ผลลัพธ์จะอยู่ที่:

```text
dist/TikTokMakerPro.exe
```

คำแนะนำ:
- เปิดโปรแกรมแล้วกรอก URL ของวิดีโอ YouTube ทีต้องการ
- กำหนดความยาวคลิป (เช่น 30 วินาที)
- เลือกการเพิ่มซับไทย, Thai TTS และ Caption
- คลิก Start Processing

หมายเหตุ:
- สคริปต์นี้ออกแบบมาเพื่อใช้งานบน Windows
- สำหรับการสร้าง `.exe` แบบเต็มจำเป็นต้องติดตั้ง PyInstaller และมี FFmpeg ใน PATH
- หาก FFmpeg ไม่พร้อม โปรแกรมจะแจ้งให้ติดตั้งอัตโนมัติจากลิงก์ดาวน์โหลดที่กำหนด

