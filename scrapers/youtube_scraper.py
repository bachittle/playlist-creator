# takes links, and finds song names based on their html title

import json
import requests
from bs4 import BeautifulSoup
import time

default_song_filename = "songs.dat"
song_filename = input(
    "Please enter the name of the song file" + 
    " you would like to load. (Default is " + default_song_filename + "): "
)
if not song_filename: song_filename = default_song_filename
file_in = open(song_filename, "r")
song_urls = file_in.read().split("\n")
file_in.close()

linktype = input("Which type of link would you like to save? \n"+
    "('y' for youtube, 'e' for everything other than youtube, (default all links):")
if not linktype: linktype = "o"
song_stuff = []
song_titles = []
i = 0
valid_url_types = ["youtu", "spotify.com", "apple.com", "soundcloud.com"]

for url in song_urls[:]:
    # remove link if it is not of the correct type

    # empty link
    if url == "": continue 

    # remove link based on linktype
    if linktype[0] == "y":
        if "youtu" not in url: 
            song_urls.remove(url)
            continue 
    elif linktype[0] == "e":
        if "youtu" in url: 
            song_urls.remove(url)
            continue 
    else:     # no need for else as any other option takes the whole thing
        if False: continue

    # checks if link is of valid url type. Also assigns a type to each link 
    valid_url_type = False 
    j = 0
    for url_type in valid_url_types:
        if url_type in url:
            valid_url_type = True
            if url_type == "youtu":
                url_type = "youtube.com"
            url_type = url_type[:len(url_type) - 4]
            song_stuff.append({url_type: url})
            break 
        j += 1
    if not valid_url_type: 
        song_urls.remove(url)
        continue

    # link is valid. Continue...
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "lxml")
    title = soup.title.string
    if title == "YouTube":
        print("Invalid link. Trying again...")
        response = requests.get(url)
        time.sleep(10)
        soup = BeautifulSoup(response.text, "lxml")
        title = soup.title.string
    trail_array = ["- YouTube", "| Free Listening on SoundCloud", "on Spotify", "on Apple Music"]
    for trail in trail_array:
        trail = title.find(trail)
        if trail != -1:
            title = title[0: trail]
    song_titles.append(title)
    # print(song_stuff[len(song_stuff) - 1])
    print(str(i + 1) + ": " + title)
    i += 1

### create json format of dict
# an unexpected yet welcome side effect is dictionaries remove duplicate links, so if anyone posts the same link it will remove the dupes
song_dict = dict(zip(song_titles, song_stuff))
song_dict = {
    "length": len(song_dict),
    "links": song_dict
}
song_json = json.dumps(song_dict, sort_keys=True, separators=(',', ':'), indent=4)

# save to json file
default_song_json_filename = "songs3.json"
song_json_filename = input("Please enter what filename you would like to save to. Default is ("+default_song_json_filename+"): ")
if not song_json_filename: song_json_filename = default_song_json_filename 
file_out = open(song_json_filename, "w")
file_out.write(song_json)
file_out.close()
print("Done! Check out " + song_json_filename)