# trakGrab.py
# Daniel Guilbert
# 12.11.19 - 07.08.24
# v1.1

from urllib.request import urlopen, URLError, Request
from bs4 import BeautifulSoup
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

pwd = os.getcwd()
pwd = pwd + "\\songs\\" + artist + "\\"

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
    outfile = open(pwd+song+".mp3", 'wb')
    outfile.write(urlopen(req).read())
    outfile.close()

else: #if downloading all songs
    soup = BeautifulSoup(html, 'html.parser')
    #s = soup.findAll("div", {"class": 'player-track play js-player-legacy-select-track'})
    s = soup.findAll("div", {"class": 'beat-list js-player-mark-active'})
    
    for src in s:
        src = str(src)

        #exception handling because sometimes the html misformats (?)
        try:
            srcstr = src.split("\"src\"")[1].split("\"")[1]
        except IndexError:
            srcstr = src.split("&quot;src&quot;")[1].split("&quot;")[1]
        songUrl = baseUrl + srcstr
        try:
            songname = src.split("\"name\"")[1].split("\"")[1]
        except IndexError:
            songname = src.split("&quot;name&quot;")[1].split("&quot;")[1]

        print("Downloading '" + songname + "'")
        
        #download file to $PWD\songs\{artist}\{song}.mp3
        req = Request(songUrl)
        req.add_header('Referer', 'https://traktrain.com/') #traktrain blocks access unless this is set

        songname = re.sub(r'[^\w|\s]', '', songname)
        songname = re.sub('[|]', '', songname)
        outfile = open(pwd+songname+".mp3", 'wb')
        outfile.write(urlopen(req).read())
        outfile.close()

print("\nAll songs downloaded!")       
