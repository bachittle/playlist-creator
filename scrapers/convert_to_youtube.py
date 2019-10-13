# converts a song name to a youtube video by searching on youtube
# NOTE: may not always work, especially if youtube takes down the video. Will fix that later

import json
import requests
from bs4 import BeautifulSoup

json_filename = input('Enter song json file (Default: songs.json): ')
if not json_filename: json_filename = "songs.json"
file_in = open(json_filename, "r")
json_data = file_in.read()
file_in.close()

songs = json.loads(json_data)
song_links = songs["links"]
for song_name in song_links:
    if "youtube" not in song_links[song_name]:
        url = 'https://www.youtube.com/results?search_query=' + song_name
        response = requests.get(url)
        soup = BeautifulSoup(response.text, 'html.parser')
        link = soup.find("a", {"class": "yt-uix-tile-link"}).get("href")
        song_links[song_name].update({"youtube": "https://www.youtube.com" + link})
        print(song_links[song_name])

new_json_filename = input("Please enter new json filename (Default: songs.json): ")
if not new_json_filename: new_json_filename = "songs.json"
file_out = open(new_json_filename, "w")
file_out.write(json.dumps(songs, sort_keys=True, separators=(',', ': '), indent=4))
file_out.close()