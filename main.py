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
from load_announcements import load_announcements
from load_games_list import load_games_list
from load_playlist import load_playlist
from load_related_playlists import load_related_playlists

NON_US_LOCALES = ['ja-JP', 'en-GB', 'fr-FR', 'fr-CA', 'de-DE', 'nl-NL', 'it-IT', 'pt-PT', 'pt-BR', 'es-ES', 'es-MX', 'ru-RU', 'ko-KR', 'zh-CN', 'zh-TW']

def main():
    print("Running...")
    # Currently assuming en-US is all we need here...? Will there be e.g. Japan-only releases?
    announcements = load_announcements('en-US')
    last_timestamp = max([x['publishAt'] for x in announcements])
    print(f'last timestamp: {last_timestamp}')
    games_list = load_games_list('en-US', last_timestamp)
    timestamps_by_game_id = load_last_announcement_times_per_game_id(announcements, games_list)
    language_counts_list = []
    for game in games_list:
        print(game)
        if (game['isGameLink']):
            print("Skipping game entry that is a game link (i.e. duplicate entry)...")
            continue
        timestamp = timestamps_by_game_id[game['id']]
        our_data = {}
        our_data['nameEnUS'] = game['name']
        our_data['id'] = game['id']
        our_data['hardware'] = game['formalHardware']
        our_data['timestamp'] = timestamp
        our_data['name'] = {}
        related_playlists = load_related_playlists(game['id'], 'en-US', timestamp)
        all_playlist_id = related_playlists['allPlaylist']['id']
        our_data['allTracksPlaylistId'] = all_playlist_id
        us_playlist = load_playlist(all_playlist_id, 'en-US', timestamp)
        our_data['name']['en-US'] = us_playlist['game']['name']
        our_data['tracks'] = []
        for track in us_playlist['tracks']:
            trackData = {}
            trackData['id'] = track['id']
            trackData['name'] = {}
            trackData['name']['en-US'] = track['name']
            our_data['tracks'].append(trackData)
        for locale in NON_US_LOCALES:
            playlist = load_playlist(all_playlist_id, locale, timestamp)
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
        our_data['localesWithDistinctTrackNames'] = sorted(locales_with_distinct_track_names)
        our_data['localesWithDistinctTrackNamesCount'] = len(locales_with_distinct_track_names)
        language_counts_list.append([-len(locales_with_distinct_track_names), game['name']])
        filename = f'processed/{game['name']}.json'
        our_data_text = json.dumps(our_data, indent=2, ensure_ascii=False)
        print(f"Collected all data for game {game['name']}")
        with open(filename, mode="w") as file:
            file.write(our_data_text)
    # To make this sort "natural", we store the languages count as a negative value
    language_counts_list.sort()
    with open("games-by-locales-with-distinct-track-names.txt", mode='w') as file:
        for [negNum, gameName] in language_counts_list:
            file.write(str(-negNum) + ": " + gameName + "\n")

def load_last_announcement_times_per_game_id(announcements, games_list):
    results = {}
    # Start by making sure all games have entries
    default_start_time = 1730325600 # time of the earliest announcement, when Nintendo Music launched
    for game in games_list:
        if (game['isGameLink']):
            continue
        results[game['id']] = default_start_time
    for announcement in announcements:
        if 'game' in announcement['summary']:
            game_id = announcement['summary']['game']['id']
            results[game_id] = max(results[game_id], announcement['publishAt'])
        if 'officialPlaylist' in announcement['summary'] and 'game' in announcement['summary']['officialPlaylist']:
            game_id = announcement['summary']['officialPlaylist']['game']['id']
            results[game_id] = max(results[game_id], announcement['publishAt'])
    return results

# print(json.dumps(load_last_announcement_times_per_game_id(), indent=2))
main()
