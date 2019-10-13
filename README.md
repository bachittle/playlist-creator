# My Playlist Creator
Web scrapes discord using your own account, and converts each link into a youtube playlist

First, you must encode a valid password. You can do that by running encode.py
The password is only used in selenium. If you want to be safe use a dummy discord account that is not 
your main account. 

### setup
install the required dependencies

```sh
pip install -r requirements.txt
```

Run the python file of your choice by using
```sh
cd scrapers
python discord_scraper.py
```

### Which python files do I use?
##### scrapers/discord_scraper.py
```sh
cd scrapers
python discord_scraper.py
```
use this scraper to update the songs.dat file with new links from any discord channel 
you must have an encrypted AES file and key already set up. To set one up use encode.py first:

```sh
python crypto/encode.py
```
##### scrapers/youtube_scraper.py
