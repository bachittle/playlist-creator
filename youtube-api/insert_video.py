# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlistItems.insert
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
from get_song_ids import get_song_ids

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
    song_ids = get_song_ids()
    print(song_ids)
    for song_id in song_ids:
      try:
        print("Adding song id: " + song_id)
        request = youtube.playlistItems().insert(
            part="snippet",
            body={
              "snippet": {
                "playlistId": "PLM5ZrANa_78hVN5Nzr5QfKOtK6FJO5vKk",
                "resourceId": {
                  "videoId": song_id,
                  "kind": "youtube#video"
                }
              }
            }
        )
        response = request.execute()
      except:
        print("Error adding song id: " + song_id)
        continue

    print(response)

if __name__ == "__main__":
    main()