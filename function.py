import os

import yt_dlp

FFMPEG_LOCATION = (
    r"C:\Users\SAMUEL PRO\AppData\Local\Microsoft\WinGet\Packages"
    r"\Gyan.FFmpeg_Microsoft.Winget.Source_8wekyb3d8bbwe"
    r"\ffmpeg-8.1.2-full_build\bin"
)

# ── Options exposed to the UI ─────────────────────────────────────────────────
VIDEO_RESOLUTIONS = ["Best", "4K (2160p)", "1440p", "1080p", "720p", "480p", "360p"]
AUDIO_FORMATS = ["mp3", "m4a", "aac", "opus", "wav"]
AUDIO_QUALITIES = ["320 kbps", "256 kbps", "192 kbps", "128 kbps", "96 kbps", "64 kbps"]

_RES_FORMAT = {
    "Best": "bestvideo+bestaudio/best",
    "4K (2160p)": "bestvideo[height<=2160]+bestaudio/best",
    "1440p": "bestvideo[height<=1440]+bestaudio/best",
    "1080p": "bestvideo[height<=1080]+bestaudio/best",
    "720p": "bestvideo[height<=720]+bestaudio/best",
    "480p": "bestvideo[height<=480]+bestaudio/best",
    "360p": "bestvideo[height<=360]+bestaudio/best",
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
    Download video (MP4) or audio from a YouTube URL.

    Filenames include the chosen resolution / quality tag so that the same
    video downloaded at different settings never overwrites each other:
        My Video [720p].mp4
        My Video [1080p].mp4
        My Video [MP3 192kbps].mp3
    """
    bitrate = audio_quality.replace(" kbps", "")

    # ── Shared yt-dlp options ─────────────────────────────────────────────────
    base = {
        "ffmpeg_location": FFMPEG_LOCATION,
        "socket_timeout": 30,
        "retries": 10,
        "fragment_retries": 10,
        "retry_sleep_functions": {"http": lambda n: min(4 * n, 30)},
    }
    if progress_hook:
        base["progress_hooks"] = [progress_hook]

    # ── Audio ─────────────────────────────────────────────────────────────────
    if media_type == "audio":
        tag = f"{audio_format.upper()} {bitrate}kbps"
        opts = {
            **base,
            "outtmpl": os.path.join(output_path, f"%(title)s [{tag}].%(ext)s"),
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
        opts = {
            **base,
            "outtmpl": os.path.join(output_path, f"%(title)s [{resolution}].%(ext)s"),
            "format": _RES_FORMAT.get(resolution, _RES_FORMAT["720p"]),
            "merge_output_format": "mp4",
            # Re-encode audio → AAC so the mp4 plays everywhere
            "postprocessor_args": {
                "merger+ffmpeg_o": ["-c:v", "copy", "-c:a", "aac", "-b:a", "192k"],
            },
        }

    with yt_dlp.YoutubeDL(opts) as ydl:
        ydl.download([url])
