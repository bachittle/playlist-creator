# has extra functions for getting my song ids to add to playlist,
# also removes duplicates from the main playlist

import json

def get_song_ids():
    json_filename = input('Enter song json file (Default: songs.json): ')
    if not json_filename: json_filename = "songs.json"
    json_filename = "../scrapers/" + json_filename
    file_in = open(json_filename, "r")
    json_data = file_in.read()
    file_in.close()

    songs = json.loads(json_data)
    song_links = songs["links"]
    i = 0
    song_link = "" 
    song_link_ids = []
    for song_name in song_links:
        if 'youtube' in song_links[song_name]:
            song_link = song_links[song_name]['youtube']
            if "playlist" in song_link:
                # might convert playlists to links later in convert_playlist_to_youtube.py
                continue
            x = song_link.find('=')
            if x == -1: x = song_link.find('e/') + 1
            if x == 0: 
                print("Erorr: youtube link invalid. Aborting. ")
                quit(2)
            y = song_link.find('&list')
            if y == -1:
                y = len(song_link)
            song_link_ids.append(song_link[x + 1:y])
        else:
            print("Error! You must have all youtube links. Please run convert_to_youtube.py.")
            quit(1)
        i += 1
    return song_link_ids

# remove_duplicates: makes sure there are no duplicates between playlist_ids.dat and the song_ids array inputted.
# outputs the new song_ids array. 
def remove_duplicates(song_ids, song_ids_filename):
    file_in = open(song_ids_filename, "r")
    old_song_ids = file_in.read().split("\n")
    new_song_ids = []
    for song_id in song_ids:
        if not song_id: continue
        if song_id not in old_song_ids:
            new_song_ids.append(song_id)
    return new_song_ids

# my_song_ids = get_song_ids()
# print(len(my_song_ids))
# my_song_ids = remove_duplicates(my_song_ids, "../playlist_ids.dat")
# print(len(my_song_ids))