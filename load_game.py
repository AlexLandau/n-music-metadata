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

# Looks like I don't really need this info? Except maybe for the localized names, but I can get those from the whole lists

def download_game_info(game_id: str, locale: str):
    country = locale[3:]
    print(f"Loading game {game_id} ({locale})...")
    time.sleep(1.1) # run less than one request per second
    outcome = subprocess.run([
            "curl",
            f"https://api.m.nintendo.com/catalog/games/{game_id}?country={country}&lang={locale}&sdkVersion=android-1.4.0_3e8b373-1&membership=BASIC&packageType=dash_cbcs"
        ], capture_output=True)
    outcome.check_returncode()
    json_result = json.loads(outcome.stdout.decode(encoding="utf-8"))
    json_text = json.dumps(json_result, sort_keys=True, indent=2)
    # print(json_text)
    with open(f'games/{game_id}-{locale}.json', mode='w') as file:
        file.write(json_text)
