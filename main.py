from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from pprint import pprint
import os

URL = "https://www.billboard.com/charts/hot-100/2008-01-05/"
CLIENT_ID = os.getenv("CLIENT_ID")
CLIENT_SECRET = os.getenv("CLIENT_SECRET")
SCOPE = "playlist-modify-private"
REDIRECT_URI = "https://example.com"
SPOTIFY_ENDPOINT = "https://api.spotify.com/v1/search"
SPOTIFY_API_TOKEN = os.getenv("SPOTIFY_API_TOKEN")

headers = {
"Authorization": f"Bearer {SPOTIFY_API_TOKEN}",
"Content-Type": "application/json"
}


def get_year(date_input):
    year = date_input.split("-")[0]
    return year


class_element = "c-title  a-no-trucate a-font-primary-bold-s u-letter-spacing-0021 u-font-size-23@tablet lrv-u-font-size-16 u-line-height-125 u-line-height-normal@mobile-max a-truncate-ellipsis u-max-width-245 u-max-width-230@tablet-only u-letter-spacing-0028@tablet"
music_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")
search_year = get_year(music_date)

response = requests.get(url=URL)

billboard_response = response.text

billboard_tag = BeautifulSoup(billboard_response, "html.parser")

song_title = billboard_tag.find_all(name="li", class_="lrv-u-width-100p")
song_list = []
song_uri = []


for song in song_title:
    find_song_title = song.find(name="h3", id="title-of-a-story")
    if find_song_title is not None:
        title = (find_song_title.getText()).strip()
        song_list.append(title)


sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(client_id=CLIENT_ID, client_secret=CLIENT_SECRET, scope=SCOPE, redirect_uri=REDIRECT_URI, show_dialog=True, username="Minh Le", cache_path="token.txt"))

user_id = sp.current_user()["id"]
print(user_id)


for song in song_list:
    try:
        q = {
            "q": song,
            "type":"track",
            "year": search_year
        }
        song_search = requests.get(url=SPOTIFY_ENDPOINT, params=q, headers=headers)
        uri = song_search.json()["tracks"]["items"][0]["uri"]
        song_uri.append(uri)
        print(song)
        print(uri)

    except IndexError:
        print("Song don't exist")
        pass

create_playlist = sp.user_playlist_create(user=user_id, name=f"{music_date} Top 100 Billboard", public=False, description="My First Spotify Project")

playlist_id=create_playlist["id"]

for song in song_uri:

    json = {
        "uris": [song],
        "position":0
    }
    add_songs = requests.post(url=f"https://api.spotify.com/v1/playlists/{playlist_id}/tracks", json=json, headers=headers)
    print(add_songs.status_code)
