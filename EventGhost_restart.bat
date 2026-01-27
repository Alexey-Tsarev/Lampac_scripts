taskkill /IM EventGhost.exe
timeout /t 1
taskkill /IM EventGhost.exe /F >nul 2>&1

timeout /t 1

cd "C:\Program Files (x86)\EventGhost"
start /MIN EventGhost.exe

rem pause
