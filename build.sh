#!/bin/bash
# Build script for macOS/Linux

echo "🔨 Building for macOS/Linux..."
echo

echo "📦 Installing PyInstaller..."
pip install --upgrade pyinstaller

echo "⏳ Building executable..."
echo

pyinstaller --onefile \\
    --windowed \\
    --name TikTokMakerPro \\
    --add-data scripts:scripts \\
    --add-data config:config \\
    --hidden-import=tkinter \\
    --hidden-import=yt_dlp \\
    --hidden-import=whisper \\
    --hidden-import=pyttsx3 \\
    app.py

echo
echo "✅ Build complete!"
echo "📍 Executable: dist/TikTokMakerPro.app/Contents/MacOS/TikTokMakerPro"
