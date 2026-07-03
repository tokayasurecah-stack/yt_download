@echo off
echo Clearing Windows icon cache...

:: Kill Explorer
taskkill /f /im explorer.exe >nul 2>&1

:: Delete all icon cache files
del /f /q "%LocalAppData%\IconCache.db" >nul 2>&1
del /f /q "%LocalAppData%\Microsoft\Windows\Explorer\iconcache_*.db" >nul 2>&1
del /f /q "%LocalAppData%\Microsoft\Windows\Explorer\thumbcache_*.db" >nul 2>&1

:: Small pause then restart Explorer
ping 127.0.0.1 -n 3 >nul
start explorer.exe

echo Done! Icon cache cleared.
