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
                continue
            x = song_link.find('=')
            if x == -1: x = song_link.find('e/') + 1
            if x == 0: 
                print("Erorr: youtube link invalid. Aborting. ")
                quit(2)
            song_link_ids.append(song_link[x + 1:])
        else:
            print("Error! You must have all youtube links. Please run convert_to_youtube.py.")
            quit(1)
        i += 1
    return song_link_ids