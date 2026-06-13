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
from load_games_list import load_games_list
from load_playlist import load_playlist
from load_related_playlists import load_related_playlists

NON_US_LOCALES = ['ja-JP', 'en-GB', 'fr-FR', 'fr-CA', 'de-DE', 'nl-NL', 'it-IT', 'pt-PT', 'pt-BR', 'es-ES', 'es-MX', 'ru-RU', 'ko-KR', 'zh-CN', 'zh-TW']

def main():
    print("Running...")
    # Currently assuming this is all we need...? Will there be e.g. Japan-only releases?
    games_list = load_games_list('en-US')
    for game in games_list:
        print(game)
        if (game['isGameLink']):
            print("Skipping game entry that is a game link (i.e. duplicate entry)...")
            continue
        our_data = {}
        our_data['nameEnUS'] = game['name']
        our_data['id'] = game['id']
        our_data['hardware'] = game['formalHardware']
        our_data['lastRetrieved'] = game['lastRetrieved']
        our_data['name'] = {}
        related_playlists = load_related_playlists(game['id'], 'en-US', False)
        all_playlist_id = related_playlists['allPlaylist']['id']
        our_data['allTracksPlaylistId'] = all_playlist_id
        us_playlist = load_playlist(all_playlist_id, 'en-US', False)
        our_data['lastRetrieved'] = min(our_data['lastRetrieved'], us_playlist['lastRetrieved'])
        our_data['name']['en-US'] = us_playlist['game']['name']
        our_data['tracks'] = []
        for track in us_playlist['tracks']:
            trackData = {}
            trackData['id'] = track['id']
            trackData['name'] = {}
            trackData['name']['en-US'] = track['name']
            our_data['tracks'].append(trackData)
        for locale in NON_US_LOCALES:
            playlist = load_playlist(all_playlist_id, locale, False)
            our_data['lastRetrieved'] = min(our_data['lastRetrieved'], playlist['lastRetrieved'])
            our_data['name'][locale] = playlist['game']['name']
            for trackData, track in zip(our_data['tracks'], playlist['tracks']):
                trackData['name'][locale] = track['name']
        locales_with_distinct_track_names = set()
        for track in our_data['tracks']:
            seen_names = set()
            for locale in track['name']:
                name = track['name'][locale]
                if name not in seen_names:
                    seen_names.add(name)
                    locales_with_distinct_track_names.add(locale)
        our_data['localesWithDistinctTrackNames'] = list(locales_with_distinct_track_names)
        our_data['localesWithDistinctTrackNamesCount'] = len(locales_with_distinct_track_names)
        filename = f'processed/{game['name']}.json'
        our_data_text = json.dumps(our_data, indent=2, ensure_ascii=False)
        # print(our_data_text)
        print(f"Collected all data for game {game['name']}")
        with open(filename, mode="w") as file:
            file.write(our_data_text)


main()
