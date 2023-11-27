#import external modules
from pytube import YouTube
import os
import urllib.request
import re


def downloadVideo(link, trackTitle, num):
    '''saves a youtube audio stream from a link, destination folder name, and title
    
    link = link to youtube stream
    
    trackTitle = name of finished mp3, should be taken from Spotify csv
    
    num = enumeration variable for ordering'''

    yt = YouTube(link)

    #extract only audio
    video = yt.streams.filter(only_audio=True).first()

    #save destination
    save_location = os.getcwd() + "\\Downloads\\"

    #download file
    out_file = video.download(save_location)

    #rename file to match song title provided by spotify
    new_file = save_location + f"{num:02} " + trackTitle + ".mp3"
    os.rename(out_file, new_file)
    print("Successfully saved to " + new_file + "\n")

def findStream(trackTitle, artist, length_ms):
    '''locates a lyric video stream on youtube using parameter trackTitle and returns its link'''

    #convert length_ms to seconds and add buffer times
    spotify_length_sec = int(length_ms) // 1000
    spotify_length_plus = spotify_length_sec +3
    spotify_length_minus = spotify_length_sec -3

    #create search query link and scrape video ids from first page of results
    artist = artist.replace(" ", "+")
    trackTitle = trackTitle.replace(" ", "+")
    html = urllib.request.urlopen('https://www.youtube.com/results?search_query=' + trackTitle + "+" + artist + "+lyrics")
    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())

    #get info from captured video ids and compare to length of spotify track
    current_vid = ''
    for video in video_ids:
        try:
            current_vid = "https://www.youtube.com/watch?v=" + video
            yt_obj = YouTube(current_vid)
            try:
                video_length = yt_obj.length
                #edit this
                if video_length > spotify_length_minus and video_length < spotify_length_plus:
                    #return matched video link
                    return current_vid
            except:
                #return first vid in id list if time can't be matched
                print("failed to match time...")
                return current_vid
        except:
            print("Could not create Youtube Object for " + trackTitle)
        