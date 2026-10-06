#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
import shutil
import subprocess
import sys
from pathlib import Path


def build_exe_windows():
    """
    สร้าง EXE สำหรับ Windows โดยใช้ PyInstaller
    """
    print("🔨 กำลังสร้าง EXE สำหรับ Windows...")
    print()
    
    # ตรวจสอบว่า PyInstaller ได้รับการติดตั้ง
    try:
        import PyInstaller
    except ImportError:
        print("📦 ติดตั้ง PyInstaller...")
        subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller>=6.0.0"], check=True)
    
    # สร้าง spec file สำหรับ PyInstaller
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-
import sys
from PyInstaller.utils.hooks import collect_submodules, get_module_file_attribute

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[('scripts', 'scripts'), ('config', 'config')],
    hiddenimports=[
        'tkinter',
        'yt_dlp',
        'whisper',
        'pyttsx3',
        'PIL',
        'requests',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludedimports=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='TikTokMakerPro',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='TikTokMakerPro'
)
'''
    
    spec_file = "TikTokMakerPro.spec"
    with open(spec_file, "w", encoding="utf-8") as f:
        f.write(spec_content)
    
    print(f"✅ สร้าง spec file: {spec_file}")
    print()
    
    # รัน PyInstaller
    print("⏳ กำลังสร้าง EXE (อาจใช้เวลาสักครู่)...")
    print()
    
    result = subprocess.run(
        [sys.executable, "-m", "PyInstaller", "--clean", spec_file],
        capture_output=False,
        text=True
    )
    
    if result.returncode == 0:
        exe_path = os.path.join("dist", "TikTokMakerPro", "TikTokMakerPro.exe")
        print()
        print("="*60)
        print("✅ สร้าง EXE เสร็จสิ้นแล้ว!")
        print("="*60)
        print()
        print(f"📍 ตำแหน่ง: {os.path.abspath(exe_path)}")
        print()
        print("วิธีใช้งาน:")
        print("1. ไปที่โฟลเดอร์ dist/TikTokMakerPro/")
        print("2. คลิก TikTokMakerPro.exe")
        print("3. โปรแกรมจะติดตั้ง dependencies ต่าง ๆ โดยอัตโนมัติ (ครั้งแรก)")
        print("4. ใส่ YouTube URL และเลือกตัวเลือกที่ต้องการ")
        print("5. คลิก 'เริ่มประมวลผล'")
        print()
        return True
    else:
        print()
        print("❌ ไม่สามารถสร้าง EXE ได้")
        return False


if __name__ == "__main__":
    success = build_exe_windows()
    sys.exit(0 if success else 1)
