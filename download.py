import bs4
from bs4 import BeautifulSoup
from requests_html import HTMLSession
from pathlib import Path
import yt_dlp
import requests
import pandas
import os

ydl_opts = {
    "format": "bestaudio/best",
    "outtmpl": str(os.path.join(Path.home(), "Downloads/songs/%(title)s.%(ext)s")),
    "timeout": None,
}

file_name = ""

def DownloadVideosFromTitles(los):
    for index, item in enumerate(los):
        # Define the file name
        file_name = f"{item}.webm"

        if os.path.exists(file_name):
            print(f"{item} already exists, skipping...")
            continue
        print("Downloading song", index + 1, ":", item)
        vid_id = ScrapeVidId(item)
        DownloadVideosFromIds([vid_id])

def DownloadVideosFromIds(lov):
    SAVE_PATH = str(os.path.join(Path.home(), "Downloads/songs"))
    try:
        os.mkdir(SAVE_PATH)
    except:
        print("download folder exists")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for video_id in lov:
            # Check if the file exists before downloading
            if not os.path.exists(file_name):
                print("Downloading video with ID:", video_id)
                ydl.download(["https://www.youtube.com/watch?v=" + video_id])

def ScrapeVidId(query):
    print ("Getting video id for: ", query)
    BASIC="http://www.youtube.com/results?search_query="
    URL = (BASIC + query)
    URL = URL.replace(" ", "+")
    print("URL: ", URL)
    page = requests.get(URL)
    session = HTMLSession()
    response = session.get(URL)
    response.html.render(sleep=100)
    soup = BeautifulSoup(response.html.html, "html.parser")

    results = soup.find('a', id="video-title")
    return results['href'].split('/watch?v=')[1]

def __main__():

    data = pandas.read_csv('songs.csv')
    data = data['song names'].tolist()
    print("Found ", len(data), " songs!")
    DownloadVideosFromTitles(data)

__main__()
