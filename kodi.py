import argparse
import base64
import json
import logging.handlers
import os
import pyautogui
import pygetwindow
import re
import socket
import subprocess
import sys
import time
import urllib.parse
import urllib.request


def is_port_open(host, port):
    try:
        log.info(f"Check '{host}:{port}' is open")
        with socket.create_connection((host, port), timeout=0.1):
            return True
    except OSError:
        return False


def wait_for_port(host, port, timeout=5):
    end_time = time.time() + timeout
    while time.time() < end_time:
        if is_port_open(host, port):
            return True

        time.sleep(0.05)
    return False


def kodi_quit():
    payload = {
        "jsonrpc": "2.0",
        "method": "Application.Quit",
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_playlist_clear():
    payload = {
        "jsonrpc": "2.0",
        "method": "Playlist.Clear",
        "params": {"playlistid": 1},
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_playlist_add(file):
    payload = {
        "jsonrpc": "2.0",
        "method": "Playlist.Add",
        "params": {"playlistid": 1, "item": {"file": file}},
        "id": 2
    }

    return kodi_rpc(payload)


def kodi_open_playlist():
    payload = {
        "jsonrpc": "2.0",
        "method": "Player.Open",
        "params": {"item": {"playlistid": 1}},
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_goto(to):
    payload = {
        "jsonrpc": "2.0",
        "method": "Player.GoTo",
        "params": {"playerid": 1, "to": to},
        "id": 3
    }

    return kodi_rpc(payload)


def kodi_stop_playerid(player_id):
    payload = {
        "jsonrpc": "2.0",
        "method": "Player.Stop",
        "params": {"playerid": player_id},
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_get_active_players():
    payload = {
        "jsonrpc": "2.0",
        "method": "Player.GetActivePlayers",
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_stop():
    r = kodi_get_active_players()
    log.info(f"Active players: {r}")

    result = json.loads(r.decode())
    active_players = result.get("result", [])

    resp = None
    if active_players:
        for player in active_players:
            resp = kodi_stop_playerid(player["playerid"])

    return resp


def kodi_play_pause(play_pause):
    payload = {
        "jsonrpc": "2.0",
        "method": "Player.PlayPause",
        "params": {"playerid": 1, "play": play_pause},
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_play():
    return kodi_play_pause(True)


def kodi_pause():
    return kodi_play_pause(False)


def kodi_execute_action_back():
    payload = {
        "jsonrpc": "2.0",
        "method": "Input.ExecuteAction",
        "params": {"action": "back"},
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_get_properties_currentwindow():
    payload = {
        "jsonrpc": "2.0",
        "method": "GUI.GetProperties",
        "params": {"properties": ["currentwindow"]},
        "id": 1
    }

    return kodi_rpc(payload)


def kodi_rpc(payload):
    data = json.dumps(payload).encode()
    headers = {"Content-Type": "application/json"}

    if args.kodi_user and args.kodi_pass:
        token = f"{args.kodi_user}:{args.kodi_pass}".encode()
        headers["Authorization"] = "Basic " + base64.b64encode(token).decode()

    log.info(f"Send request to Kodi: {data}")
    req = urllib.request.Request(f"http://{args.kodi_host}:{args.kodi_port}/jsonrpc", data=data, headers=headers)

    with urllib.request.urlopen(req, timeout=5) as resp:
        return resp.read()


def show_window(window_title):
    all_windows = pygetwindow.getAllWindows()
    log.debug(f"Got windows: {all_windows}")

    for window in all_windows:
        log.debug(f"Window: {window}")

        if re.match(window_title, window.title, re.IGNORECASE):
            log.debug(f"Found window: {window}")

            try:
                if window.isMinimized:
                    window.restore()

                pyautogui.press('alt')
                window.activate()
                log.info(f"Window activated: {window}")
                return True
            except Exception as e:
                log.warning(f"Window '{window}' was not activated: {e}")
                return False

    print(f"Window with title '{window_title}' was not found")
    return False


def show_kodi_window():
    return show_window("^Kodi$")


def show_lampa_window():
    return show_window("^Lampa - ")


def get_log_level(log_level):
    log_levels = {
        'DEBUG': logging.DEBUG,
        'INFO': logging.INFO,
        'WARNING': logging.WARNING,
        'ERROR': logging.ERROR,
        'CRITICAL': logging.CRITICAL
    }

    if log_level is None:
        log_level = 'INFO'

    return log_levels.get(log_level.strip().upper(), logging.INFO)


script_dir = os.path.dirname(os.path.realpath(__file__))

parser = argparse.ArgumentParser()
# parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "info"))
parser.add_argument("--log-level", default=os.getenv("LOG_LEVEL", "debug"))
parser.add_argument("--log-file", default=os.getenv("LOG_FILE", os.path.join(script_dir, "log", "main.log")))
parser.add_argument("--kodi-bin", default=os.getenv("KODI_BIN", r"C:\Program Files\Kodi\kodi.exe"))
parser.add_argument("--kodi-host", default=os.getenv("KODI_HOST", "127.0.0.1"))
parser.add_argument("--kodi-port", default=os.getenv("KODI_PORT", 8080), type=int)
parser.add_argument("--kodi-user", default=os.getenv("KODI_USER", "kodi"))
parser.add_argument("--kodi-pass", default=os.getenv("KODI_PASS", "kodi"))
parser.add_argument("--kodi-do")
parser.add_argument("--kodi-play")
parser.add_argument("--playlist-file", default=os.getenv("PLAYLIST_FILE", os.path.join(script_dir, "playlist.m3u")))
parser.add_argument("--show-kodi", action="store_true")
parser.add_argument("--show-lampa", action="store_true")
args = parser.parse_args()

# Log setup
log = logging.getLogger()
log.setLevel(get_log_level(args.log_level))

logging_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

log_handler_stream = logging.StreamHandler()
log_handler_stream.setFormatter(logging_formatter)
log_handler_stream.setLevel(get_log_level(args.log_level))
log.addHandler(log_handler_stream)

log_handler_file = logging.handlers.TimedRotatingFileHandler(
    encoding='utf-8',
    filename=str(os.path.join(script_dir, args.log_file)),
    when='midnight')
log_handler_file.setFormatter(logging_formatter)
log_handler_file.setLevel(get_log_level(args.log_level))
log.addHandler(log_handler_file)
# End Log setup

try:
    log.info(f"Start script with arguments: {sys.argv}")

    if args.show_kodi:
        show_kodi_window()
        sys.exit(0)

    if args.show_lampa:
        show_lampa_window()
        sys.exit(0)

    log.info("Check Kodi is already started")
    if is_port_open(args.kodi_host, args.kodi_port):
        log.info("Kodi is already started")
    else:
        log.info("Start Kodi")
        subprocess.Popen(args.kodi_bin, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if wait_for_port(args.kodi_host, args.kodi_port):
            log.info(f"Port is open: {args.kodi_host}:{args.kodi_port}")
        else:
            log.error(f"Connection failed: {args.kodi_host}:{args.kodi_port}")
            exit(1)

    if args.kodi_do == "play":
        log.info(kodi_play())

    if args.kodi_do == "pause":
        log.info(kodi_pause())

    if args.kodi_do == "stop":
        kodi_stop()

    if args.kodi_do == "quit" or args.kodi_do == "exit":
        log.info(kodi_quit())

    if args.kodi_play:
        url = args.kodi_play
        log.debug(f"URL: {url}")

        url_parsed = urllib.parse.urlparse(url)
        log.debug(f"URL parsed: {url_parsed}")

        url_query = urllib.parse.parse_qs(url_parsed.query, keep_blank_values=True)
        log.debug(f"URL query: {url_query}")

        url_index = url_query["index"][0]
        log.debug(f"URL index: {url_index}")

        new_url_query = urllib.parse.urlencode({
            "link": url_query["link"][0],
            "m3u": ""})

        m3u_url = urllib.parse.urlunparse(
            [url_parsed.scheme,
             url_parsed.netloc,
             "stream/",
             url_parsed.params,
             new_url_query,
             url_parsed.fragment])

        log.debug(f"Get M3U URL content: {m3u_url}")
        with urllib.request.urlopen(m3u_url) as response:
            m3u_content = response.read()
        log.debug(f"Got M3U URL content:\n{m3u_content.decode()}")

        log.debug(f"Save M3U URL content in file: {args.playlist_file}")
        with open(args.playlist_file, "wb") as f:
            f.write(m3u_content)

        log.info(kodi_playlist_clear())
        log.info(kodi_playlist_add(args.playlist_file))
        log.info(kodi_open_playlist())
        show_kodi_window()

        if int(url_index) >= 2:
            log.info(kodi_goto(int(url_index) - 1))

            end = time.time() + 30
            while time.time() < end:
                current_window = kodi_get_properties_currentwindow()
                label = json.loads(current_window.decode()).get("result", {}).get("currentwindow", {}).get("label", "")
                log.debug(f"Label: {label}")

                if label == "Home":
                    log.info(f"Do Back, because found Label: {label}")
                    kodi_execute_action_back()
                    break

                time.sleep(1)

except Exception as e:
    log.exception(f"An unhandled exception occurred: {e}")
