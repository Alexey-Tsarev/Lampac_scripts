# Lampac scripts (Windows)

## Problems
This project is for resolving the following problems:
1. Change a link to a stream. For instance, [Lampac](https://github.com/immisterio/Lampac) outputs a link:
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=1&preload  
I need to convert it to:  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=1&play
2. I use [Kodi](https://kodi.tv/download/windows/) as a player.
When it starts, Kodi's window stays behind the browser's window.
3. Watch series. For example, for torrent files with many files inside, 
a player starts from a file with `index=x`, for example, with `index=3`:  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=3&preload  
After episode 3 ended, the next episode (4?) does not start automatically!

## Solutions
### Solution 2
To resolve 2, I select [AutoIt](https://www.autoitscript.com).
```
WinWait("Kodi", "", 10)
WinActivate("Kodi")
```

Because to run an AutoIt script in Windows, you need to run `AutoIt3.exe script.au3`,
then `playerInner` setting does not work because it's needed to provide an additional `au3` parameter as an argument.
That's why the following lines in [Lampac\init.conf](http://example.com/Lampac/init.conf) are added:
```
{
  "cmd": {
    "player": {
      "path": "C:\\PF\\AutoIt\\AutoIt3_x64.exe",
      "arguments": "C:\\PF\\Lampac_scripts\\run_player.au3 \"{value}\""
    }
  }
}
```

To run a player, this script [Lampac\plugins\player-inner.js](http://example.com/Lampac/plugins/player-inner.js) is changed:
```
$.get('{localhost}/cmd/player/' + element.url);
```

### Solution 3
To resolve 3: download an `m3u` playlist and remove all links before the `index` parameter.  
Because Lampac starts [TorrServer](https://github.com/YouROK/TorrServer) and proxies it through the URL
http://127.0.0.1:9118/ts/ (add `ts`), then links inside `m3u` become invalid.  
To resolve this, I install [TorrServer-windows-amd64.exe](https://github.com/YouROK/TorrServer/releases)
and configure Lampac to use the link [http://127.0.0.1:8090](http://127.0.0.1:8090).

### Solution 1
Resolved automatically by using `m3u`.

## Script
In this way all needed work is happening in [run_player.au3](http://example.com/run_player.au3) script:
- convert URL to download `m3u` playlist
- download `m3u` playlist
- remove in `m3u` playlist all links before `index`
- run Kodi with the resulted `m3u` playlist

## Example
In this example, `index=3`.  
__in.m3u__
```
#EXTM3U
#EXTINF:0,NameOfSeriesS03x01.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x01.mkv?link=LINK_ID&index=1&play
#EXTINF:0,NameOfSeriesS03x02.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x02.mkv?link=LINK_ID&index=2&play
#EXTINF:0,NameOfSeriesS03x03.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x03.mkv?link=LINK_ID&index=3&play
#EXTINF:0,NameOfSeriesS03x04.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x04.mkv?link=LINK_ID&index=4&play
#EXTINF:0,NameOfSeriesS03x05.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x05.mkv?link=LINK_ID&index=5&play
#EXTINF:0,NameOfSeriesS03x06.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x06.mkv?link=LINK_ID&index=6&play
#EXTINF:0,NameOfSeriesS03x07.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x07.mkv?link=LINK_ID&index=7&play
#EXTINF:0,NameOfSeriesS03x08.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x08.mkv?link=LINK_ID&index=8&play
```

__out.m3u__
```
#EXTM3U
#EXTINF:0,NameOfSeriesS03x03.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x03.mkv?link=LINK_ID&index=3&play
#EXTINF:0,NameOfSeriesS03x04.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x04.mkv?link=LINK_ID&index=4&play
#EXTINF:0,NameOfSeriesS03x05.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x05.mkv?link=LINK_ID&index=5&play
#EXTINF:0,NameOfSeriesS03x06.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x06.mkv?link=LINK_ID&index=6&play
#EXTINF:0,NameOfSeriesS03x07.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x07.mkv?link=LINK_ID&index=7&play
#EXTINF:0,NameOfSeriesS03x08.mkv
http://127.0.0.1:8090/stream/NameOfSeriesS03x08.mkv?link=LINK_ID&index=8&play
```

####
Thanks a lot and good luck,  
Alexey Tsarev, Tsarev.Alexey at gmail.com
