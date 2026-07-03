#!/bin/bash
# ── YT Downloader APK Builder ─────────────────────────────────────────────────
echo "======================================"
echo "  YT Downloader APK Builder"
echo "======================================"

# System dependencies
echo ""
echo "[1/4] Installing system dependencies..."
sudo apt-get update -qq
sudo apt-get install -y git zip unzip openjdk-17-jdk \
    autoconf libtool pkg-config zlib1g-dev \
    libncurses5-dev libffi-dev libssl-dev build-essential

# Python dependencies
echo ""
echo "[2/4] Installing Python dependencies..."
source ~/my_kivy_project/venv/bin/activate
pip install --upgrade cython==0.29.33 buildozer

# Copy latest project files
echo ""
echo "[3/4] Copying project files..."
cp "/mnt/c/Users/SAMUEL PRO/Desktop/yt dowload/main.py" ~/my_kivy_project/
cp "/mnt/c/Users/SAMUEL PRO/Desktop/yt dowload/function_android.py" ~/my_kivy_project/
cp "/mnt/c/Users/SAMUEL PRO/Desktop/yt dowload/buildozer.spec" ~/my_kivy_project/
cp "/mnt/c/Users/SAMUEL PRO/Desktop/yt dowload/icon.png" ~/my_kivy_project/

# Build APK
echo ""
echo "[4/4] Building APK (20-40 mins first time)..."
cd ~/my_kivy_project
buildozer android debug

# Copy APK to Windows Desktop when done
echo ""
echo "Copying APK to Windows Desktop..."
cp bin/*.apk "/mnt/c/Users/SAMUEL PRO/Desktop/" 2>/dev/null && \
echo "✅ APK copied to your Windows Desktop!" || \
echo "⚠️  Find APK at: ~/my_kivy_project/bin/"

echo ""
echo "======================================"
echo "  DONE!"
echo "======================================"
