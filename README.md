# Lampac scripts (Windows)
# Read [English version](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/README_EN.md)
## Проблемы
Я сделал этот проект, чтобы решить проблемы:
1. Для проигрывания потоков я использую [Kodi](https://kodi.tv/download/windows/). При старте потока, окно Kodi остаётся позади окна браузера.
2. Изменение ссылки на поток. Например, [Lampac](https://github.com/immisterio/Lampac) выдаёт ссылку в виде  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=1&preload  
которую мне нужно поменять так, чтобы скачать плейлист файл (`.m3u`)  
http://127.0.0.1:8090/stream/?link=LINK_ID&m3u
3. Просмотр сериалов. Пример, при проигрывании раздач, в которых есть множество файлов, 
плеер стартует с файла со смещением `index=x`, пример `index=3`:  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=3&preload  
После окончания серии 3, следующая серия не начинается автоматически!

## Решения
### Решение 1
Используется Python библиотека `pygetwindow`.

### Решение 2 
Поскольку запуск Python скрипта в Windows - это запуск `python.exe kodi.py`,
то задание параметра `playerInner` не работает, так как нужно дополнительно передать имя скрипта `py` как аргумент.  
Поэтому сделана настройка [Lampac\init.conf](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/Lampac/init.conf)
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

Для запуска плеера изменён скрипт [Lampac\plugins\player-inner.js](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/Lampac/plugins/player-inner.js)
```
$.get('{localhost}/cmd/player/' + element.url);
```

### Решение 3
Из-за того, что Lampac стартует [TorrServer](https://github.com/YouROK/TorrServer) и проксирует его через URL
http://127.0.0.1:9118/ts/ (добавляя `ts`), то ссылки внутри `m3u` получаются неверными.  
Для решения этой проблемы я установил [TorrServer-windows-amd64.exe](https://github.com/YouROK/TorrServer/releases)
и настроил Lampac на использование TorrServer по ссылке [http://127.0.0.1:8090](http://127.0.0.1:8090).

Таким образом, скачивается `m3u` плейлист. Этот плейлист отрывается в Kodi, используя следующие [JSON-RPC API](https://kodi.wiki/view/JSON-RPC_API):
- [Playlist.Clear](https://kodi.wiki/view/JSON-RPC_API/v13#Playlist.Clear) (`"params": {"playlistid": 1}`)
- [Playlist.Add](https://kodi.wiki/view/JSON-RPC_API/v13#Playlist.Add) (`"params": {"playlistid": 1, "item": {"file": playlist.m3u}}`)
- [Player.Open](https://kodi.wiki/view/JSON-RPC_API/v13#Player.Open) (`"params": {"item": {"playlistid": 1}}`)
- если `index >= 2`, то [Player.GoTo](https://kodi.wiki/view/JSON-RPC_API/v13#Player.GoTo) (`"params": {"playerid": 1, "to": index-1}`)

## Скрипт
Таким образом всю основную работу делает скрипт [kodi.py](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/kodi.py):
- преобразовывает полученный URL, таким образом, чтобы скачать `m3u` плейлист
- скачивает `m3u` плейлист
- запускает Kodi со скаченным `m3u` плейлистом
- производит перемотку до нужного файла через Player.GoTo

## Python virtualenv
```
python -m venv .virtualenv
.virtualenv\Scripts\activate.bat
.virtualenv\Scripts\pip install -r requirements.txt
.virtualenv\Scripts\python.exe kodi.py --help
```


## Управление
Для управления Lampac и Kodi я использую пульт [UGOOS UR02](https://ugoos.com/ugoos-bt-remote-control-ur02).  
Для биндинга кнопок и остальной логики [EventGhost](https://github.com/EventGhost/EventGhost/releases).  
Файл конфигурации для EventGhost [UGOOS_UR02.xml](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/UGOOS_UR02.xml).

####
Good luck, Tsarev.Alexey at gmail.com.
