### This scraper is used for adding each item to a playlist (using selenium)
# WARNING: this is really inefficient. Use insert_video.py as it uses the youtube api and is much faster,
# only use this if your google api quota runs out

from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options           


import json
import time
import datetime
import os.path

start = datetime.datetime.now()
my_playlist = input("please enter the name of the playlist you would like to add to (case_sensitive): ")
if not my_playlist: my_playlist = "uWin Discord CS music"

# load required files
file_in = open("songs.json", "r")
songs = file_in.read()
file_in.close()
file_in = open("../playlist_ids.dat", "r")
current_song_ids = file_in.read().split("\n")
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
file_out = open("../playlist_ids.dat", "a")
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
        breaker = 0
        for id in current_song_ids:
            if id == current_id:
                breaker = 1
                break
        if breaker == 1: 
            continue
        print("%d: %s" %(i, url))
        file_out.write(current_id + "\n")
        print("%d: %s" %(i, current_id))
        browser.get(url) # navigate to the page
        time.sleep(1)
        # button = browser.find_element_by_xpath('//yt-formatted-string[@class="style-scope ytd-button-renderer style-default size-default"]')
        button = browser.find_element_by_xpath("//yt-formatted-string[contains(text(), 'Save')]")
        button.click()
        time.sleep(1)
        # playlists = browser.find_elements_by_css_selector("yt-formatted-string#label.checkbox-height.style-scope.ytd-playlist-add-to-option-renderer")
        playlists = browser.find_elements_by_css_selector("paper-checkbox#checkbox.style-scope.ytd-playlist-add-to-option-renderer")

        for playlist in playlists:
            if my_playlist in playlist.text:
                if playlist.get_attribute("aria-checked") == 'false':
                    playlist.find_element_by_xpath('.//div[@id="checkboxContainer"]').click()
    except Exception as e:
        print(e)
        file_out.close()
        file_out = open("../playlist_ids.dat", "a")
        continue

file_out.close()
browser.quit()