## trakGrab

trakGrab is a Python3 script designed for use on Windows.
It downloads beats from a specified artists traktrain.com
profile.

__DEPENDENCIES__

-BeautifulSoup
--install via `python -m pip install beautifulsoup4`

__USAGE__

Simply run the script from the command line with `py trakGrab.py`
The script prompts the user for an artist (their traktrain URL)
and for a beat to download. The wildcard character (*) can be 
used to download all of an artists available beats. 

Beats are downloaded to `$PWD\songs\artistName\songName.mp3` where `$PWD`
is the location of the script.


No rights reserved.

##### -dg 12.11.19
