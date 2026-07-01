# ▶ YT Downloader

A fast, modern desktop app for downloading YouTube videos and audio — built with Python, yt-dlp, and Tkinter.

![Python](https://img.shields.io/badge/Python-3.10+-blue?style=flat-square)
![yt-dlp](https://img.shields.io/badge/yt--dlp-latest-red?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows-lightgrey?style=flat-square)

---

## Features

- **Video downloads** — MP4 at your choice of resolution: 360p, 480p, 720p, 1080p, 1440p, 4K, or Best
- **Audio downloads** — MP3, M4A, AAC, OPUS, or WAV at 64 – 320 kbps
- **No file conflicts** — filenames are automatically tagged with resolution / quality (e.g. `My Video [720p].mp4`)
- **Live progress** — real-time size, speed, and ETA displayed while downloading
- **Text-to-speech** — voice feedback on success and error via pyttsx3
- **Auto-retry** — automatically retries on network timeout (up to 10 attempts)
- **Dark modern UI** — clean professional interface with a segmented type selector

---

## Screenshots

> _Coming soon_

---

## Requirements

| Dependency | Purpose |
|---|---|
| Python 3.10+ | Runtime |
| [yt-dlp](https://github.com/yt-dlp/yt-dlp) | YouTube downloading engine |
| [FFmpeg](https://ffmpeg.org/) | Merging video + audio / converting to MP3 |
| [pyttsx3](https://pypi.org/project/pyttsx3/) | Text-to-speech notifications |

---

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/tokayasurecah-stack/yt_download.git
cd yt_download
```

### 2. Install Python dependencies

```bash
pip install yt-dlp pyttsx3
```

### 3. Install FFmpeg (Windows)

```powershell
winget install Gyan.FFmpeg
```

> After installation, close and reopen your terminal so the PATH update takes effect.

---

## Usage

```bash
python app.py
```

1. Paste a YouTube URL into the **VIDEO URL** field
2. Choose **Video (MP4)** or **Audio Only**
3. Select your preferred resolution or audio quality
4. Pick a save folder (defaults to `~/Downloads`)
5. Hit **DOWNLOAD**

---

## Project Structure

```
yt_download/
├── app.py          # UI — Tkinter frontend
├── function.py     # Backend — yt-dlp download logic
└── README.md
```

---

## Developer

**Tony Bbosa** — Full-Stack Developer  
GitHub: [github.com/tonybbosa](https://github.com/tonybbosa)

---

## License

This project is open source and available under the [MIT License](LICENSE).
