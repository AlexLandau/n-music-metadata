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

# 1 hour for this list that updates frequently
OUT_OF_DATE_SECONDS = 3600

def load_games_list(locale: str):
    if not os.path.exists(f'games-{locale}.json'):
        return download_games_list(locale)
    with open(f'games-{locale}.json') as file:
        contents = json.load(file)
        if datetime.now().timestamp() - contents[0]['lastRetrieved'] > OUT_OF_DATE_SECONDS:
            return download_games_list(locale)
        else:
            return contents

def download_games_list(locale: str):
    country = locale[3:]
    print(f"Downloading games list ({locale})...")
    time.sleep(1.1) # run less than one request per second
    outcome = subprocess.run([
            "curl",
            # "--user-agent",
            # "JustSomeRandomScripting/0.0.0 ( oporaca@gmail.com )",
            f"https://api.m.nintendo.com/catalog/games:all?lang={locale}&country={country}&sortRule=RECENT"
        ], capture_output=True)
    outcome.check_returncode()
    json_result = json.loads(outcome.stdout.decode(encoding="utf-8"))
    for json_item in json_result:
        json_item['lastRetrieved'] = math.floor(datetime.now().timestamp())
    json_text = json.dumps(json_result, sort_keys=True, indent=2)
    # print(json_text)
    with open(f'games-{locale}.json', mode='w') as file:
        file.write(json_text)
    return json_result

# load_games_list('en-US')
