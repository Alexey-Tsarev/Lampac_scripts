# Lampac scripts (Windows)
# See [English version](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/README_EN.md)
## Проблемы
Я сделал этот проект, чтобы решить несколько проблем:
1. Изменение ссылки на поток. Например, [Lampac](https://github.com/immisterio/Lampac) выдаёт ссылку в виде  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=1&preload  
которую мне нужно поменять на  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=1&play
2. Для проигрывания потоков я использую [Kodi](https://kodi.tv/download/windows/).
При старте потока, окно Kodi остаётся позади окна браузера.
3. Просмотр сериалов. Пример, при проигрывании раздач, в которых есть множество файлов, 
плеер стартует с файла со смещением `index=x`, пример `index=3`:  
http://127.0.0.1:9118/ts/stream/FILE_NAME?link=LINK_ID&index=3&preload  
После окончания серии 3, следующая серия не начинается автоматически!

## Решения
### Решение 2
Для решения 2, я выбрал [AutoIt](https://www.autoitscript.com).
```
WinWait("Kodi", "", 10)
WinActivate("Kodi")
```

Поскольку запуск скрипта AutoIt в Windows - это запуск `AutoIt3.exe script.au3`,
то задание параметра `playerInner` не работает, так как нужно дополнительно передать имя скрипта `au3` как аргумент.  
Поэтому сделана настройка [Lampac\init.conf](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/Lampac/init.conf)
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

Для запуска плеера изменён скрипт [Lampac\plugins\player-inner.js](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/Lampac/plugins/player-inner.js)
```
$.get('{localhost}/cmd/player/' + element.url);
```

### Решение 3
Для решения 3, скачивается `m3u` плейлист в котором удалятся все ссылки до `index`.  
Из-за того, что Lampac стартует [TorrServer](https://github.com/YouROK/TorrServer) и проксирует его через URL
http://127.0.0.1:9118/ts/ (добавляя `ts`), то ссылки внутри `m3u` получаются неверными.  
Для решения этой проблемы я установил [TorrServer-windows-amd64.exe](https://github.com/YouROK/TorrServer/releases)
и настроил Lampac на использование TorrServer по ссылке [http://127.0.0.1:8090](http://127.0.0.1:8090).

### Решение 1
Разрешилось автоматически, переходом на `m3u`.

## Скрипт
Таким образом всю основную работу делает скрипт [run_player.au3](https://github.com/Alexey-Tsarev/Lampac_scripts/blob/master/run_player.au3):
- преобразовывает полученный URL, таким образом, чтобы скачать `m3u` плейлист
- скачивает `m3u` плейлист
- удаляет из `m3u` плейлиста все ссылки до `index`
- запускает Kodi с полученным `m3u` плейлистом

## Итоговый пример
В данном примере `index=3`.  
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

Good luck, Tsarev.Alexey at gmail.com.
