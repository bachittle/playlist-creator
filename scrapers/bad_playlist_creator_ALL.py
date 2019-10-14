### This scraper is used for adding each item to a playlist (using selenium)
# WARNING: this is really inefficient. Use insert_video.py as it uses the youtube api and is much faster,
# only use this if your google api quota runs out

# this goes through ALL your links, even if they are in the playlist_ids.dat file already
# this program is even worse. Use this as your last resort

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options           
import requests
from bs4 import BeautifulSoup


import json
import time
import datetime
import os.path

start = datetime.datetime.now()
my_playlist = input("please enter the playlist url: ")
if not my_playlist: my_playlist = "https://www.youtube.com/playlist?list=PLM5ZrANa_78gHjjpuBknrx86fQbQT1kTL"
response = requests.get(my_playlist)
soup = BeautifulSoup(response.text, "html.parser")
my_playlist = soup.title.string
my_playlist = my_playlist[:my_playlist.find(" - YouTube")]
print(my_playlist + ".")

# load required files
file_in = open("songs.json", "r")
songs = file_in.read()
file_in.close()
songs = json.loads(songs)
song_links = songs["links"]

# setup
print("setting up web drivers")
options = Options()
options.add_argument("--headless")               
# add where your local data is if youre already signed in to discord
options.add_argument(r"--user-data-dir=C:\Users\Bailey\AppData\Local\Google\Chrome\User Data") 

# use this if your drivers are in your PATH directory
browser = webdriver.Chrome(options=options)      # for chrome

# use this if you have your drivers in this git repo "playlist-creator/drivers" or anywhere else other than path (type it manually)
# browser = webdriver.Chrome(r"../drivers/chromedriver.exe", options=options)    
print("performing actions in youtube")
i = 0
filename = input("Please enter what filename to save to (default: new_playlist_ids.dat): ")
if not filename: filename = "new_playlist_ids.dat"
file_out = open("../" + filename, "w")
for song_name in song_links:
    try:
        i += 1
        url = song_links[song_name]["youtube"]
        if not url or "playlist" in url:
            continue
        
        x = url.find('=')
        if x == -1: x = url.find('be/') + 2
        y = url.find('&')
        if y == -1: y = len(url)
        current_id = url[x+1:y]
        print("%d: %s" %(i, url))
        file_out.write(current_id + "\n")
        print("%d: %s" %(i, current_id))
        browser.get(url) # navigate to the page
        time.sleep(2)
        # button = browser.find_element_by_xpath('//yt-formatted-string[@class="style-scope ytd-button-renderer style-default size-default"]')
        button = browser.find_element_by_xpath("//yt-formatted-string[contains(text(), 'Save')]")
        button.click()
        time.sleep(2)
        # playlists = browser.find_elements_by_css_selector("yt-formatted-string#label.checkbox-height.style-scope.ytd-playlist-add-to-option-renderer")
        playlists = browser.find_elements_by_css_selector("paper-checkbox#checkbox.style-scope.ytd-playlist-add-to-option-renderer")

        for playlist in playlists:
            if my_playlist in playlist.text:
                if playlist.get_attribute("aria-checked") == 'false':
                    playlist.find_element_by_xpath('.//div[@id="checkboxContainer"]').click()
                    time.sleep(2)
    except Exception as e:
        continue

file_out.close()
browser.quit()