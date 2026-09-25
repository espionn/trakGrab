# trakGrab.py
# Daniel Guilbert
# 12.11.19 - 07.08.24
# v1.1

from urllib.request import urlopen, URLError, Request
from bs4 import BeautifulSoup
import json
import re
import os

#Get information
artist = input("What is the artist name? traktrain.com/")
song = '*' #input("Which song would you like to download? (* for all) ")

print("Connecting...")
#get aws server url
urlmatch = re.compile('(.)*var AWS_BASE_URL(.)*')
#print("base url: " + urlmatch)
try:
    req = Request("http://www.traktrain.com/"+artist)
    req.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36')
    html = urlopen(req).read().decode('utf-8')
except URLError:
    input("That artist cannot be found, please try again.")
    exit()

print("Connected!\n")
m = urlmatch.search(html)
baseUrl = m.group().split("'")[1]

pwd = os.path.join(os.getcwd(), "songs", artist)

if not os.path.exists(pwd):
    os.makedirs(pwd)

#if downloading single song
if song != '*':    
    #find song metadata and create full URL to mp3
    try:
        songmatch = re.compile("(.)*data-player-info='{\"name\":\""+song+"(.)*", re.I)
        s = songmatch.search(html).group()
        s = s.split("\"src\"")[1].split("\"")[1]
        songUrl = baseUrl + s
    except AttributeError:
        print("That song could not be found, please try again.")
        exit()

    print("Downloading '" + song + "'")
    #download file to $PWD\songs\{artist}\{song}.mp3
    req = Request(songUrl)
    req.add_header('Referer', 'https://traktrain.com/') #traktrain blocks access unless this is set

    song = re.sub(r'[^\w ]', '', song)
    outfile = open(os.path.join(pwd, song + ".mp3"), 'wb')
    outfile.write(urlopen(req).read())
    outfile.close()

else: #if downloading all songs
    soup = BeautifulSoup(html, 'html.parser')
    nameKeys = ['title', 'beatName', 'beat_name', 'trackName', 'track_name', 'name']
    genericNames = {'mp3 track', 'wav track', 'mp3', 'wav', 'track', 'untitled'}

    beats = []
    seen = set()
    for el in soup.select('[data-player-info]'):
        try:
            info = json.loads(el['data-player-info'])
        except ValueError:
            continue

        srcstr = info.get('src')
        if not srcstr or srcstr in seen:
            continue
        seen.add(srcstr)

        songname = None
        for key in nameKeys:
            val = info.get(key)
            if isinstance(val, str) and val.strip() and val.strip().lower() not in genericNames:
                songname = val.strip()
                break
        if not songname:
            titleEl = el.find(class_=re.compile('(title|name)', re.I))
            if titleEl and titleEl.get_text(strip=True):
                songname = titleEl.get_text(strip=True)
        if not songname:
            songname = "beat_" + str(len(beats) + 1)

        beats.append((songname, srcstr))

    if not beats:
        print("No songs found, please try again.")
        exit()

    for songname, srcstr in beats:
        songUrl = baseUrl + srcstr

        print("Downloading '" + songname + "'")
        
        #download file to $PWD\songs\{artist}\{song}.mp3
        req = Request(songUrl)
        req.add_header('Referer', 'https://traktrain.com/') #traktrain blocks access unless this is set

        songname = re.sub(r'[^\w\s\-()]', '', songname).strip() or "untitled"
        outpath = os.path.join(pwd, songname + ".mp3")
        n = 1
        while os.path.exists(outpath):
            outpath = os.path.join(pwd, songname + " (" + str(n) + ").mp3")
            n += 1

        outfile = open(outpath, 'wb')
        outfile.write(urlopen(req).read())
        outfile.close()

print("\nAll songs downloaded!")