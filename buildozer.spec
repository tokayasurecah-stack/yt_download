[app]
title = YT Downloader
package.name = ytdownloader
package.domain = com.tonybbosa
source.dir = .
source.include_exts = py,png,jpg,ico,kv,atlas
source.exclude_dirs = dist,build,__pycache__,.git
source.exclude_patterns = app.py,fix_*.ps1,ffpath.txt,push*.bat,deploy*.bat,make_icon.py,.github
version = 2.0.0

requirements = python3==3.11.9,kivy==2.3.0,yt_dlp,certifi,requests,mutagen,pycryptodomex,websockets,brotli

orientation = portrait
fullscreen = 0

android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.api = 33
android.minapi = 21
android.ndk = 25b
android.ndk_api = 21
android.private_storage = True
android.accept_sdk_license = True
android.arch = arm64-v8a

p4a.branch = master

icon.filename = %(source.dir)s/icon.png
presplash.filename = %(source.dir)s/icon.png

log_level = 2
warn_on_root = 1

[buildozer]
log_level = 2
warn_on_root = 1
