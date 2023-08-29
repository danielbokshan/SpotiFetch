


#+---------------------------------------+
#|                                       |
#|              DEPRECATED               |
#|                                       |
#+---------------------------------------+



"""Get song titles and artists from Spotify playlist"""

#import stuff
import csv
import re
import base64
import spotipy
from pytube import YouTube
import os
import urllib.request
from requests import post
import json

#load credentials from system env var
client_id = os.environ.get('SPOTIFY_CLIENT_ID')
client_secret = os.environ.get('SPOTIFY_CLIENT_SECRET')
print(client_id)
print(client_secret)

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
    #session = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
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
    with open("csv/" + OUTPUT_FILE_NAME, "w", encoding="utf-8") as file:
        writer = csv.writer(file)

        # extract name and artist
        print("writing to", OUTPUT_FILE_NAME)
        for track in tracks:
            name = track["track"]["name"]
            artists = " ".join([artist["name"] for artist in track["track"]["artists"]])
            length = track['track']['duration_ms']
            print(track)
            print('')

            # write to csv
            writer.writerow([name, artists, length])
        print("file written to csv folder")
        print("done!")
        


def downloadVideo(link, folderName, trackTitle):
    '''saves a youtube audio stream from a link, destination folder name, and title
    
    link = link to youtube stream
    
    folderName = name of destination folder within Downloaded Files path
    
    trackTitle = name of finished mp3, should be taken from Spotify csv'''

    yt = YouTube(link)
    print(yt)

    #extract only audio
    video = yt.streams.filter(only_audio=True).first()

    #save destination
    destination = 'C:\\Users\\DanBo\\Documents\\Projects\\Spotify Downloader\\Downloaded Files\\test'

    #download file
    out_file = video.download(output_path=destination)

    #rename file to match song title provided by spotify
    base = trackTitle
    new_file = base + '.mp3'
    os.rename(out_file, new_file)

    print('successfully saved' + new_file)


def findStream(trackTitle, artist, length_ms):
    '''locates a lyric video stream on youtube using parameter trackTitle and returns its link'''

    #convert length_ms to seconds
    spotify_length_sec = int(length_ms) // 1000

    #create search query link and scrape video ids from first page of results
    artist = artist.replace(" ", "+")
    trackTitle = trackTitle.replace(" ", "+")
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + trackTitle + "+" + artist + "+lyrics")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    #get info from captured video ids and compare to length of spotify track
    current_vid = ''
    for video in video_ids:
        current_vid = "https://www.youtube.com/watch?v=" + video
        yt_obj = YouTube(current_vid)
        try:
            video_length = yt_obj.length
            if video_length == spotify_length_sec:
            #return matched video link
                print("CURRENT VID:" + current_vid)
                return current_vid
        except:
            #return first vid in id list if time can't be matched
            print("failed to match time...")
            print("CURRENT VID: " + current_vid)
            return current_vid