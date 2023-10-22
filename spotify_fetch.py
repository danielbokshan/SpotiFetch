#import external modules
import os
import base64
from requests import post
import json
import spotipy
import re
import csv
import dataclean
from pathlib import Path

#load credentials from system env var
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')

def get_token():
    '''automatically asks for spotify token to authenticate'''
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode('utf-8')
    auth_base64 = str(base64.b64encode(auth_bytes), 'utf-8')

    url = 'https://accounts.spotify.com/api/token'
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result['access_token']
    return token


def getCSV(playlist_link, outfile_name):

    #user input
    OUTPUT_FILE_NAME = str(outfile_name) + ".csv"

    # change for your target playlist
    PLAYLIST_LINK = playlist_link

    #authenticate
    token = get_token()

    # create spotify session object
    session = spotipy.Spotify(auth=token)
    print("auth successful")

    # get uri from https link
    if match := re.match(r"https://open.spotify.com/playlist/(.*)\?", PLAYLIST_LINK):
        playlist_uri = match.groups()[0]
        print("got uri match")
    else:
        raise ValueError("Expected format: https://open.spotify.com/playlist/...")

    # get list of tracks in a given playlist (note: max playlist length 100, api limitation)
    print("getting track info...")
    tracks = session.playlist_tracks(playlist_uri)["items"]
    print("fetched tracks!")

    # create csv file
    csvname = os.getcwd() + "\\temp.csv"
    csvpath = Path(csvname)
    if csvpath.is_file():
        os.remove(csvname)
    creation = open(OUTPUT_FILE_NAME, "x")
    creation.close()
    with open(OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        # extract name and artist
        print("writing to", OUTPUT_FILE_NAME + "...")
        for track in tracks:
            name = track["track"]["name"]
            name = dataclean.scrub_string(name)
            artists = " ".join([artist["name"] for artist in track["track"]["artists"]])
            artists = dataclean.scrub_string(artists)
            length = track['track']['duration_ms']
            print(name)
            print('')

            # write to csv
            writer.writerow([name, artists, length])
        print("tracks written to csv file")
        print("done!")