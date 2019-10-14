####################################################
#   this is used for creating a brand new playlist #
#   it adds all songs from the songs.json file     #
#   if you already have a playlist you're going to #
#   want to use update_insert_video.py             #
####################################################

# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import os.path
if not os.path.isfile("playlist_helper.py"):
  print("Error! Please run this script while in the youtube-api directory!")
  quit(1)
from playlist_helper import get_song_ids
from playlist_helper import remove_duplicates

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
  # Disable OAuthlib's HTTPS verification when running locally.
  # *DO NOT* leave this option enabled in production.
  os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

  api_service_name = "youtube"
  api_version = "v3"
  client_secrets_file = "client_secret.json"

  # Get credentials and create an API client
  flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
      client_secrets_file, scopes)
  credentials = flow.run_console()
  youtube = googleapiclient.discovery.build(
      api_service_name, api_version, credentials=credentials)

  #### my code
  song_ids_filename = "../playlist_ids.dat"
  song_ids = get_song_ids()
  # save tremendous amount of quota data if you only add what playlists are new
  if os.path.isfile(song_ids_filename):
    song_ids = remove_duplicates(song_ids, song_ids_filename)
  if not song_ids:
    print("Your playlist is already up to date!")
    quit(2)
  print("Size of link list to add:" + str(len(song_ids)))
  print(song_ids)
  file_out = open(song_ids_filename, "a")
  response = None 
  for song_id in song_ids:
    try:
      print("Adding song id: " + song_id)
      request = youtube.playlistItems().insert(
          part="snippet",
          body={
            "snippet": {
              "playlistId": "PLM5ZrANa_78gHjjpuBknrx86fQbQT1kTL",   
              "resourceId": {
                "videoId": "EWUHoKNs_o0",
                "kind": "youtube#video"
              }
            }
          }
      )
      response = request.execute()
      file_out.write(song_id + "\n")
    except Exception as e:
      print("Error adding song id: %s\n" % song_id)
      print(str(e) + "\n")
      continue

  file_out.close()
  print(response)

if __name__ == "__main__":
    main()