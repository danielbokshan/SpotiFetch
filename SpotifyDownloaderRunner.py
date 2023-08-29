import spotify_fetch
import yt_api
import csv

playlist = input("Enter a playlist link:\n")
print("")

#phase this out to just use a temp file
filename = input("Enter a file name for the csv output (no extension):\n")

#outfolder = input("Enter the name of the destination folder (within Downloaded Files):\n")

spotify_fetch.getCSV(playlist, filename)

#write something that reads info from the CSV here

read_content=list()
path = 'C:\\Users\\DanBo\\Documents\\Projects\\Spotify Downloader\\csv\\' + filename + ".csv"
total = 0
processed = 0
with open(path, 'r') as playlist_csv:
    read_content = csv.reader(playlist_csv, delimiter=',', quotechar='|')
    #loop that calls SpotifyDownloader.findStream() and SpotifyDownloader.downloadVideo() for each track
    for row in read_content:
        if len(row) != 0:
            total += 1
            title = row[0]
            artist = row[1]
            length = row[2]
            video_link = yt_api.findStream(title, artist, length)
            if title.isascii() and artist.isascii():
                try:
                    yt_api.downloadVideo(link=video_link, folderName=filename, trackTitle=title)
                    processed += 1
                except:
                    print(title + " could not be downloaded")
            else:
                print(title + " contains non-ascii characters!")
print(processed, "of", total, "downloads complete!")