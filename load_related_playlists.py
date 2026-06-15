#!/bin/python3

from datetime import datetime
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

def load_related_playlists(game_id: str, locale: str, force_refresh: bool):
    filename = f'related_playlists/{game_id}-{locale}.json'
    if force_refresh or not os.path.exists(filename):
        download_related_playlists(game_id, locale)
    with open(filename) as file:
        return json.load(file)

def download_related_playlists(game_id: str, locale: str):
    country = locale[3:]
    print(f"Loading related playlists for {game_id} ({locale})...")
    time.sleep(1.1) # run less than one request per second
    outcome = subprocess.run([
            "curl",
            f"https://api.m.nintendo.com/catalog/games/{game_id}/relatedPlaylists?country={country}&lang={locale}&sdkVersion=android-1.4.0_3e8b373-1&membership=BASIC&packageType=dash_cbcs"
        ], capture_output=True)
    outcome.check_returncode()
    json_result = json.loads(outcome.stdout.decode(encoding="utf-8"))
    json_result['lastRetrieved'] = math.floor(datetime.now().timestamp())
    json_text = json.dumps(json_result, sort_keys=True, indent=2)
    with open(f'related_playlists/{game_id}-{locale}.json', mode='w') as file:
        file.write(json_text)
