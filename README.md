# My Playlist Creator
Web scrapes discord using your own account, and converts each link into a youtube playlist

## setup
install the required dependencies

```sh
pip install -r requirements.txt
```

you must also install chromedriver.exe to use the python files: discord_scraper.py, bad_playlist_creator.py, bad_playlist_creator_ALL.py
Get it from here: https://chromedriver.storage.googleapis.com/index.html?path=77.0.3865.40/
if that doesn't work try different versions: https://chromedriver.chromium.org/downloads
Put it in your PATH directory if you don't know how to do this, comment out the code that looks like this:
```python
browser = webdriver.Chrome(options=options)      # for chrome
```
and uncomment out the code that looks like this: 
```python
browser = webdriver.Chrome(r"../drivers/chromedriver.exe", options=options)    
```
if you would prefer using firefox, change the branch to old and use that scraper instead

Run scraper package:
```sh
cd scrapers
python scraper_package.py
```

If the scraper package fails, read the below documentation and try running each python program separately. Worse case scenario submit an issue and I'll see what I can do. 

## What if I want to run each python file separately? What order do I go in?
This is the order:
### scrapers/discord_scraper.py
```sh
cd scrapers
python discord_scraper.py
```
use this scraper to update the songs.dat file with new links from any discord channel 

### scrapers/youtube_scraper.py
```sh
python youtube_scraper.py
```
use this scraper once you already have a bunch of links in a songs.dat file. It will turn it into a json file with the names of each song added as well. These names are used if you need to turn any other link into a youtube link

### scrapers/convert_to_youtube.py
```sh
python convert_to_youtube.py
```
once you have a songs.json file, this program will make sure every song has a youtube link. It does this by querying youtube search and picking the first result. Will resave in the same songs.json format

### You can choose between any of these playlist creators. They are in order from most to least efficient
#### scrapers/bad_playlist_creator_ALL.py
```sh
python bad_playlist_creator_ALL.py
```
this playlist creator will always go through every link and make sure they are added to the playlist. It uses selenium headless mode if you do not want GUI. This one is good if you want to initialize the playlist, but after that I would recommend using bad_playlist_creator.py as it skips unneccesary links. 

#### scrapers/bad_playlist_creator.py
```sh
python bad_playlist_creator.py
```
this playlist creator is similar to the bad_playlist_creator_ALL.py, however it skips unneccesary files by making use of playlist_ids.dat. If you don't see a song in the playlist after using this, try using bad_playlist_creator_ALL as it thouroughly checks that the playlist has been added, even if  going through unnecessary files

#### youtube-api/insert_video.py
```sh
cd ../youtube-api
python insert_video.py
```
this is the fastest method as it has no overhead from loading web-pages. It uses the youtube data api. The link can be found here: https://developers.google.com/youtube/v3

To use this api, you must create a client_secret.json file. You have to set up an account with google cloud by going to: https://console.developers.google.com. Then, go to credentials and create a credential. The website will walk you through setting it up. If you need more help getting it set up, go to this link (although it is a little old): https://www.geeksforgeeks.org/youtube-data-api-playlist-set-1/

