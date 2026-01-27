# Lampac scripts (Windows)
# Read [Russian version](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/README.md)

## Problems
This project is for resolving the following problems:
1. I use [Kodi](https://kodi.tv/download/windows/) as a player. When it starts, Kodi's window stays behind the browser's window.
2. Change a link to a stream. For instance, [Lampac](https://github.com/immisterio/Lampac) outputs a link:
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=1&preload  
and I need it to convert to a playlist file (`.m3u`):  
http://127.0.0.1:8090/stream/?link=LINK_ID&m3u
3. Watch series. For example, for torrent files with many files inside, 
a player starts from a file with `index=x`, for example, with `index=3`:  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=3&preload  
However, after an episode 3 ended, the next episode (4) does not start automatically!

## Solutions
### Solution 1
The Python lib `pygetwindow` is used.

### Solution 2
Because to run a Python script in Windows, you need to run `python.exe kodi.py`,
then `playerInner` setting does not work because it's needed to provide an additional `py` parameter as an argument.
That's why the following lines in [Lampac\init.conf](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/Lampac/init.conf) are added:
```
{
  "playerInner": "notNull",
  "cmd": {
    "player": {
      "path": "C:\\PF\\Lampac_scripts\\.virtualenv\\Scripts\\python.exe",
      "arguments": "C:\\PF\\Lampac_scripts\\kodi.py --kodi-play \"{value}\""
    }
  }
}
```

To run a player, this script [Lampac\plugins\player-inner.js](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/Lampac/plugins/player-inner.js) is changed:
```
$.get('{localhost}/cmd/player/' + element.url);
```

### Solution 3 
Because Lampac starts [TorrServer](https://github.com/YouROK/TorrServer) and proxies it through the URL
http://127.0.0.1:9118/ts/ (add `ts`), then links inside `m3u` become invalid.  
To resolve this, I install [TorrServer-windows-amd64.exe](https://github.com/YouROK/TorrServer/releases)
and configure Lampac to use the link [http://127.0.0.1:8090](http://127.0.0.1:8090).

So, after an `m3u` playlist is downloaded. This playlist is opened by Kodi, using the following [JSON-RPC API](https://kodi.wiki/view/JSON-RPC_API):
- [Playlist.Clear](https://kodi.wiki/view/JSON-RPC_API/v13#Playlist.Clear) (`"params": {"playlistid": 1}`)
- [Playlist.Add](https://kodi.wiki/view/JSON-RPC_API/v13#Playlist.Add) (`"params": {"playlistid": 1, "item": {"file": playlist.m3u}}`)
- [Player.Open](https://kodi.wiki/view/JSON-RPC_API/v13#Player.Open) (`"params": {"item": {"playlistid": 1}}`)
- if `index >= 2`, then [Player.GoTo](https://kodi.wiki/view/JSON-RPC_API/v13#Player.GoTo) (`"params": {"playerid": 1, "to": index-1}`)

## Script
Thus, the [kodi.py](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/kodi.py) script does all main work:
- convert URL to download an `m3u` playlist
- download an `m3u` playlist
- run Kodi with the downloaded `m3u` playlist
- rewinds to the desired file using Player.GoTo

## Python virtualenv
```
python -m venv .virtualenv
.virtualenv\Scripts\activate.bat
.virtualenv\Scripts\pip install -r requirements.txt
.virtualenv\Scripts\python.exe kodi.py --help
```

## Remote control
To control Lampac and Kodi, I use the [UGOOS UR02](https://ugoos.com/ugoos-bt-remote-control-ur02) remote.  
For button bindings and other logic, I use [EventGhost](https://github.com/EventGhost/EventGhost/releases).  
The EventGhost configuration file: [UGOOS_UR02.xml](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/UGOOS_UR02.xml).

####
Thanks a lot and good luck,  
Alexey Tsarev, Tsarev.Alexey at gmail.com.
