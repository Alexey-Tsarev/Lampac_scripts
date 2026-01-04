#include <Array.au3>

Local $url = $CmdLine[1]
;MsgBox(0, "Source URL", $url)

Local $index = ""
Local $aMatch = StringRegExp($url, "&index=(\d+)", 1)
If Not @error Then $index = $aMatch[0]
;MsgBox(0, "index in URL", $index)

$url = StringReplace($url, "?link=", ".m3u?link=")
$url = StringRegExpReplace($url, "&index=\d+", "")
$url = StringReplace($url, "&preload", "&m3u")
;MsgBox(0, "M3U URL", $url)

Local $m3uSavePath = @ScriptDir & '\in.m3u'
InetGet($url, $m3uSavePath, 1, 0)

Local $hFile = FileOpen($m3uSavePath, 0)
If $hFile = -1 Then Exit MsgBox(16, "Error", "Cannot open file")

Local $m3uLines = StringSplit(StringStripCR(FileRead($hFile)), @LF)
FileClose($hFile)

Local $result = $m3uLines[1] & @LF ; always keep the first line (#EXTM3U)

Local $iSkipLines = ($index - 1) * 2
For $i = 2 + $iSkipLines To $m3uLines[0] Step 1
    If $m3uLines[$i] <> "" Then
        $result &= $m3uLines[$i] & @LF
    EndIf
Next

Local $outFile = @ScriptDir & '\out.m3u'
FileDelete($outFile)
FileWrite($outFile, $result)

Run('"C:\Program Files\Kodi\kodi.exe" "' & $outFile & '"')
WinWait("Kodi", "", 10)
WinActivate("Kodi")
