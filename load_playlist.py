#!/bin/python3

from datetime import datetime
import io
import json
import math
import os
import os.path
import re
import subprocess
import time

def load_playlist(playlist_id: str, locale: str, timestamp: int):
    filename = f'playlists/{playlist_id}-{locale}.json'
    if not os.path.exists(filename):
        download_playlist(playlist_id, locale, timestamp)
    with open(filename) as file:
        loaded = json.load(file)
        if 'timestamp' in loaded and loaded['timestamp'] == timestamp:
            return loaded
    # We've downloaded it, but it's out-of-date
    download_playlist(playlist_id, locale, timestamp)
    with open(filename) as file:
        return json.load(file)

def download_playlist(playlist_id: str, locale: str, timestamp: int):
    country = locale[3:]
    print(f"Loading playlist {playlist_id} ({locale})...")
    time.sleep(1.1) # run less than one request per second
    outcome = subprocess.run([
            "curl",
            f"https://api.m.nintendo.com/catalog/officialPlaylists/{playlist_id}?country={country}&lang={locale}&sdkVersion=android-1.4.0_3e8b373-1&membership=BASIC&packageType=dash_cbcs"
        ], capture_output=True)
    outcome.check_returncode()
    json_result = json.loads(outcome.stdout.decode(encoding="utf-8"))
    json_result['timestamp'] = timestamp
    json_text = json.dumps(json_result, sort_keys=True, indent=2)
    with open(f'playlists/{playlist_id}-{locale}.json', mode='w') as file:
        file.write(json_text)
