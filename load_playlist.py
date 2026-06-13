#!/bin/python3

from datetime import datetime, UTC
import html
import io
import json
import math
import os
import os.path
import re
import subprocess
import time
import yaml

def load_playlist(playlist_id: str, locale: str, force_refresh: bool):
    filename = f'playlists/{playlist_id}-{locale}.json'
    if force_refresh or not os.path.exists(filename):
        download_playlist(playlist_id, locale)
    with open(filename) as file:
        return json.load(file)


def download_playlist(playlist_id: str, locale: str):
    country = locale[3:]
    print(f"Loading playlist {playlist_id} ({locale})...")
    time.sleep(1.1) # run less than one request per second
    outcome = subprocess.run([
            "curl",
            # "--user-agent",
            # "JustSomeRandomScripting/0.0.0 ( oporaca@gmail.com )",
            f"https://api.m.nintendo.com/catalog/officialPlaylists/{playlist_id}?country={country}&lang={locale}&sdkVersion=android-1.4.0_3e8b373-1&membership=BASIC&packageType=dash_cbcs"
        ], capture_output=True)
    outcome.check_returncode()
    json_result = json.loads(outcome.stdout.decode(encoding="utf-8"))
    json_result['lastRetrieved'] = math.floor(datetime.now().timestamp())
    json_text = json.dumps(json_result, sort_keys=True, indent=2)
    # print(json_text)
    with open(f'playlists/{playlist_id}-{locale}.json', mode='w') as file:
        file.write(json_text)

# download_playlist("18ddd82c-d01c-4a99-9b05-a4c6f940dc70", locale='en-US')
# download_playlist("18ddd82c-d01c-4a99-9b05-a4c6f940dc70", locale='es-MX')

# https://music.nintendo.com/shared/en-US/US/tracks/33460fd7-c7eb-4f06-bac3-9eb8c04860a3/
# Track ID is: 33460fd7-c7eb-4f06-bac3-9eb8c04860a3

# print(datetime.now().timestamp())
# ts = math.floor(datetime.now().timestamp())
# print(ts)
# print(datetime.fromtimestamp(ts).strftime('%Y-%m-%d %H:%M:%S'))
# print(datetime.fromtimestamp(ts))
# print(datetime.fromtimestamp(ts, tz=UTC))
