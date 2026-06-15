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

# 1 hour refresh for this list that updates once or twice a week
OUT_OF_DATE_SECONDS = 3600

def load_announcements(locale: str):
    last_announcement_check_time = 0
    if os.path.exists('last_announcement_check_time.txt'):
        with open('last_announcement_check_time.txt') as file:
            last_announcement_check_time = int(file.read())
    if datetime.now().timestamp() - last_announcement_check_time > OUT_OF_DATE_SECONDS:
        download_announcements(locale, download_all=(last_announcement_check_time == 0))
        with open('last_announcement_check_time.txt', mode='w') as file:
            file.write(str(int(datetime.now().timestamp())))
    announcements = []
    for filename in os.listdir('announcements'):
        if not filename.endswith('.json'):
            continue
        with open(f'announcements/{filename}') as file:
            announcements.append(json.load(file))
    return announcements

def download_announcements(locale: str, download_all: bool):
    country = locale[3:]
    limit = 10
    if download_all:
        limit = 999
    print(f"Downloading announcements ({locale}, limit {limit})...")
    time.sleep(1.1) # run less than one request per second
    outcome = subprocess.run([
            "curl",
            f"https://api.m.nintendo.com/catalog/contentNotices?country={country}&lang={locale}&limit={limit}"
        ], capture_output=True)
    outcome.check_returncode()
    json_result = json.loads(outcome.stdout.decode(encoding="utf-8"))
    for json_item in json_result['items']:
        publish_time = json_item['publishAt']
        id = json_item['id']
        json_text = json.dumps(json_item, sort_keys=True, indent=2, ensure_ascii=False)
        filename = f'announcements/{publish_time}_{id}.json'
        if not os.path.exists(filename):
            print(f"New announcement {id}:")
            print(json_text)
            with open(filename, mode='w') as file:
                file.write(json_text)
        else:
            with open(filename, mode='r') as file:
                existing_text = file.read()
                if existing_text != json_text:
                    print(f"Modified announcement?: {id}")
                    print("Stored:")
                    print(existing_text)
                    print("Newly loaded:")
                    print(json_text)
                    file.close()
                    with open(filename, mode='w') as file2:
                        file2.write(json_text)
    return json_result
