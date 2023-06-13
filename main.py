from bs4 import BeautifulSoup
import requests
import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth

SPOTIFY_ID_CLIENT = os.environ.get("SPOTIFY_ID_CLIENT")
SPOTIFY_CLIENT_SECRET = os.environ.get("SPOTIFY_CLIENT_SECRET")
date_time_travel = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD?")
URL = f"https://www.billboard.com/charts/hot-100/{date_time_travel}/"
year = date_time_travel[0:4:1]
response = requests.get(URL)
data = response.text

soup = BeautifulSoup(data, "html.parser")
songs = soup.find_all(id="title-of-a-story")

billboard_songs_list = []
billboard_new_list = []
for song in songs:
    text = song.getText()
    billboard_songs_list.append(text)
del billboard_songs_list[:6]
del billboard_songs_list[-13:]
for n in billboard_songs_list:
    new = n.replace("\n", "").replace("\t", "")
    if new == "Songwriter(s):" or new == "Songwriter(s):" or new == "Producer(s):" or new == "Imprint/Promotion Label:":
        pass
    elif len(new) > 0:
        billboard_new_list.append(new)
scope = "playlist-modify-private"
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=SPOTIFY_ID_CLIENT,
                                               client_secret=SPOTIFY_CLIENT_SECRET,
                                               redirect_uri="http://example.com",
                                               cache_path=".cache",
                                               scope=scope))
id = sp.current_user()["id"]
billboard_songs_list = []
for item in billboard_new_list:
    try:
        result = sp.search(q='track:' + item + " year:" + year, type='track', limit=1)
        track_id = result['tracks']['items'][0]['id']
        billboard_songs_list.append(track_id)
    except IndexError:
        pass
spotify_list = []
for item in billboard_songs_list:
    new_item = "spotify:track:" + item
    spotify_list.append(new_item)


playlist_data = sp.user_playlist_create(user=id, name=f"{date_time_travel}Billboard 100",
                                       description="New playlist", public=False)
playlist_id = playlist_data["id"]
sp.user_playlist_add_tracks(user=id, playlist_id=playlist_id, tracks=spotify_list)
