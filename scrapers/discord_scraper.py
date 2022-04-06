### main scraper for discord. Gets links from a channel
# this version does not require you use crypto to save your password on your pc.
# it uses your local data for chrome, so make sure you are logged in on chrome
# works as long as the channel does not get deleted
# ONLY USES CHROME: firefox support is in the old discord scraper (old branch)
# use the old discord scraper if you have any issues

from webdrivermanager import ChromeDriverManager
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options           


import time
import datetime
import os.path

start = datetime.datetime.now()

driver_manager = ChromeDriverManager()
driver_manager.download_and_install()

# setup
print("setting up web drivers")
options = Options()

# headless doesn't seem to work...
# options.add_argument("--headless")               

# add where your local data is if youre already signed in to discord
#options.add_argument(r"--user-data-dir=C:\Users\Bailey\AppData\Local\Google\Chrome\User Data")

# use this if your drivers are in your PATH directory
browser = webdriver.Chrome(options=options)      # for chrome

# use this if you have your drivers in this git repo "playlist-creator/drivers" or anywhere else other than path (type it manually)
# browser = webdriver.Chrome(r"../drivers", options=options)

#######################################################
# Change channel url to the channel of your choice    #
#######################################################
url = "https://discord.com/channels/667734565309382657/781945075948978197"

browser.get(url) # navigate to the page

time.sleep(10)

# do stuff on the main discord page
print("performing actions in discord")

# filter used when looking only for links
def my_filter(x):
    return "https://" in x

action = ActionChains(browser)
old_links = None
filename = "songs.dat"
is_file = os.path.isfile(filename) 
if is_file:
    file_in = open(filename, "r")
    old_links = file_in.read().split("\n")
    file_in.close()
links = []
j = 0 
error_amount = 0 # shouldn't surpass 3
freq = 30        # the frequency of link scraping
call_amount = 7  # amount of times you call the link scraper
for i in range(freq * call_amount + 1):
    try:
        action.send_keys(Keys.PAGE_UP).perform()
        breaker = 0
        if j % freq == 0:
            # scrape links
            sub_links = browser.find_elements_by_xpath("//a")
            sub_links = [x.text for x in sub_links]    # convert to array
            # print(str(links) + "\n\n\n" + str(sub_links))
            links.extend(sub_links)
            links = list(set(links))
            print(links)
            if is_file:
                for old_link in old_links:
                    if old_link in links:
                        print("found link")
                        links.extend(old_links)
                        links = list(set(links))
                        breaker = 1
                        break
        if breaker == 1:
            break
        j += 1
        time.sleep(0.1 / i)
    except Exception as e:
        print("Error: trying again...")
        error_amount += 1
        if error_amount >= 3: 
            print("too many errors. Exiting...")
            print(e)
            quit(2)
    
links = list(filter(None, links))      # filter empty
links = list(filter(my_filter, links)) # filter only containing https://

end = datetime.datetime.now()
delta = end - start

# save to file
if is_file:
    old_size = str(len(old_links))
    new_size = str(len(links))
    print("old file size: " + old_size)
    print("new file size: " + new_size)
    if new_size < old_size:
        print("Warning: new size is less than the old size.")
        print("Either someone deleted a song or the program messed up")


def save(filename, io_type):
    file_out = open(filename, io_type)
    for x in links:
        file_out.write(x + "\n")
    file_out.close()

print("Please enter the song filename. (Type in 'a' to abort) (Press enter for default: songs.dat): ")
new_filename = input()
if new_filename == "a": 
    print("aborting...")
    browser.quit()
    quit(3)
if not new_filename: new_filename = filename
save(new_filename, "w")


print("********************************")
print("Done reading songs")
print("********************************")
print("total time: " + str(delta.total_seconds()))
print("press enter to exit: ")
exit = input()
browser.quit()