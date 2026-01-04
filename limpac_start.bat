cd C:\PF\TorrServer
start /MIN TorrServer-windows-amd64.exe

cd C:\PF\Lampac
start /MIN Lampac.exe

rem "C:\Program Files\Google\Chrome\Application\chrome.exe" --start-fullscreen http://127.0.0.1:9118
"C:\Program Files\Mozilla Firefox\firefox.exe" --kiosk http://127.0.0.1:9118
