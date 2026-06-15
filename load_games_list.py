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

def load_games_list(locale: str, timestamp: int):
    last_games_list_load_time = 0
    load_time_filename = f'last_games_list_load_time-{locale}.txt'
    if os.path.exists(load_time_filename):
        with open(load_time_filename) as file:
            last_games_list_load_time = int(file.read())
    if timestamp != last_games_list_load_time or not os.path.exists(f'games-{locale}.json'):
        download_games_list(locale)
        with open(load_time_filename, mode='w') as file:
            file.write(str(timestamp))
    with open(f'games-{locale}.json') as file:
        return json.load(file)

def download_games_list(locale: str):
    country = locale[3:]
    print(f"Downloading games list ({locale})...")
    time.sleep(1.1) # run less than one request per second
    outcome = subprocess.run([
            "curl",
            f"https://api.m.nintendo.com/catalog/games:all?lang={locale}&country={country}&sortRule=RECENT"
        ], capture_output=True)
    outcome.check_returncode()
    json_result = json.loads(outcome.stdout.decode(encoding="utf-8"))
    json_text = json.dumps(json_result, sort_keys=True, indent=2)
    with open(f'games-{locale}.json', mode='w') as file:
        file.write(json_text)
    return json_result
