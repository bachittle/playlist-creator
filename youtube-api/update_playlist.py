# -*- coding: utf-8 -*-

# Sample Python code for youtube.playlists.update
# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import os
import json

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

    request = youtube.playlists().update(
        part="id, snippet",
        body={
          "id": "PLM5ZrANa_78hVN5Nzr5QfKOtK6FJO5vKk",
          "snippet": {
            "title": "uWin Discord CS music",
            "description": "Good morning gamers"
          }
        }
    )
    response = request.execute()

    print(response)
    playlist = "playlist.json"
    file_in = open(playlist, "w+")
    file_in.write(json.dumps(response, indent=4, separators=(',', ': ')))
    file_in.close()
    print("Playlist successfully created. Data is in the file: " + playlist)

if __name__ == "__main__":
    main()