import spotify_fetch
import yt_api
import csv
import os
import dataclean

playlist = input("Enter a playlist link:\n")
print("")

#get playlist as csv and store in cwd/temp
spotify_fetch.getCSV(playlist, "temp")
read_content=list()
path = os.getcwd()

#read csv and download using yt_api
total = 0
processed = 0
r = 1
with open(path + "\\temp.csv", 'r') as playlist_csv:
    read_content = csv.reader(playlist_csv, delimiter=',', quotechar='|')
    #loop that calls SpotifyDownloader.findStream() and SpotifyDownloader.downloadVideo() for each track
    for row in read_content:
        if len(row) != 0:
            total += 1
            title = row[0]
            artist = row[1]
            length = row[2]
            print("attempting to download " + title + " - " + artist)
            title = dataclean.scrub_string(title)
            artist = dataclean.scrub_string(artist)
            if title.isascii() == True and artist.isascii() == True:
                try:
                    video_link = yt_api.findStream(title, artist, length)
                    yt_api.downloadVideo(link=video_link, trackTitle=title, num=r)
                    processed += 1
                    r += 1
                except:
                    print(title + " could not be downloaded")
            else:
                print(title + " contains non-ascii characters! Could not be downloaded.\n")
print(processed, "of", total, "downloads complete!")

#remove the csv file
csv = path + "\\temp.csv"
os.remove(csv)
print("Cleanup complete.")