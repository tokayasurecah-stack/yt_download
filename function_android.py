"""
function_android.py — cross-platform download logic.
Works on Windows (desktop) and Android (APK via Buildozer).
"""

import os
import sys

import yt_dlp

# ── Platform detection ────────────────────────────────────────────────────────
IS_ANDROID = hasattr(sys, "getandroidapilevel")

# ── Options exposed to the UI ─────────────────────────────────────────────────
VIDEO_RESOLUTIONS = ["Best", "4K (2160p)", "1440p", "1080p", "720p", "480p", "360p"]
AUDIO_FORMATS = ["mp3", "m4a", "aac", "opus", "wav"]
AUDIO_QUALITIES = ["320 kbps", "256 kbps", "192 kbps", "128 kbps", "96 kbps", "64 kbps"]

# ── Windows FFmpeg path ───────────────────────────────────────────────────────
_FFMPEG_WIN = (
    r"C:\Users\SAMUEL PRO\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.2-full_build\bin"
)

# ── Video format strings ──────────────────────────────────────────────────────
# Use mp4+m4a combos — avoids FFmpeg merging on Android
_RES_FORMAT = {
    "Best": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
    "4K (2160p)": "bestvideo[ext=mp4][height<=2160]+bestaudio[ext=m4a]/best[ext=mp4][height<=2160]/best",
    "1440p": "bestvideo[ext=mp4][height<=1440]+bestaudio[ext=m4a]/best[ext=mp4][height<=1440]/best",
    "1080p": "bestvideo[ext=mp4][height<=1080]+bestaudio[ext=m4a]/best[ext=mp4][height<=1080]/best",
    "720p": "bestvideo[ext=mp4][height<=720]+bestaudio[ext=m4a]/best[ext=mp4][height<=720]/best",
    "480p": "bestvideo[ext=mp4][height<=480]+bestaudio[ext=m4a]/best[ext=mp4][height<=480]/best",
    "360p": "bestvideo[ext=mp4][height<=360]+bestaudio[ext=m4a]/best[ext=mp4][height<=360]/best",
}


def download_media(
    url: str,
    media_type: str,
    output_path: str = ".",
    resolution: str = "720p",
    audio_format: str = "mp3",
    audio_quality: str = "192 kbps",
    progress_hook=None,
):
    """
    Download video (mp4) or audio from a YouTube URL.

    On Android  → no FFmpeg; downloads m4a audio / pre-muxed mp4 video directly.
    On Windows  → full FFmpeg pipeline; converts audio & merges video+audio.
    """
    os.makedirs(output_path, exist_ok=True)
    bitrate = audio_quality.replace(" kbps", "")

    # ── Shared base options ───────────────────────────────────────────────────
    base = {
        "socket_timeout": 30,
        "retries": 10,
        "fragment_retries": 10,
        "retry_sleep_functions": {"http": lambda n: min(4 * n, 30)},
    }
    if not IS_ANDROID:
        base["ffmpeg_location"] = _FFMPEG_WIN
    if progress_hook:
        base["progress_hooks"] = [progress_hook]

    # ── Audio ─────────────────────────────────────────────────────────────────
    if media_type == "audio":
        tag = f"{audio_format.upper()} {bitrate}kbps"
        base["outtmpl"] = os.path.join(output_path, f"%(title)s [{tag}].%(ext)s")

        if IS_ANDROID:
            # Download best m4a directly — no conversion needed
            opts = {
                **base,
                "format": "bestaudio[ext=m4a]/bestaudio/best",
            }
        else:
            # Windows: convert to chosen format via FFmpeg
            opts = {
                **base,
                "format": "bestaudio/best",
                "postprocessors": [
                    {
                        "key": "FFmpegExtractAudio",
                        "preferredcodec": audio_format,
                        "preferredquality": bitrate,
                    }
                ],
            }

    # ── Video ─────────────────────────────────────────────────────────────────
    else:
        base["outtmpl"] = os.path.join(output_path, f"%(title)s [{resolution}].%(ext)s")
        fmt = _RES_FORMAT.get(resolution, _RES_FORMAT["720p"])

        if IS_ANDROID:
            # No FFmpeg — rely on pre-muxed mp4 format
            opts = {
                **base,
                "format": fmt,
                "merge_output_format": "mp4",
            }
        else:
            # Windows: re-encode audio to AAC for compatibility
            opts = {
                **base,
                "format": fmt,
                "merge_output_format": "mp4",
                "postprocessor_args": {
                    "merger+ffmpeg_o": ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"],
                },
            }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
