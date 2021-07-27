# creates a Charts 100 Playlist in Spotify based on the input date

import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

CHARTS = "https://www.billboard.com/charts/hot-100/"

sp = spotipy.Spotify(auth_manager=SpotifyOAuth(
    scope="playlist-modify-private",
    redirect_uri="http://example.com",
    client_id="YOUR CLIENT ID",
    client_secret="YOUR SECRET",
    show_dialog = True,
    cache_path = "token.txt"
    ))

user_id = sp.current_user()["id"]

# ask for a date
user_input = input("Which date do you want to travel to? Type it in the following format: YYYY-MM-DD: ")

# scrape the top 100 songs from that date from billboard.com
response = requests.get(CHARTS + user_input).text
soup = BeautifulSoup(response, "html.parser")
top100 = soup.find_all(name="span", class_="chart-element__information__song text--truncate color--primary")
top100 = [song.getText() for song in top100]


song_uris = []
year = user_input.split("-")[0]

for song in top100:
    # use song name and year to get the song on spotify
    title = sp.search(q=f"track:{song} year:{year}", type="track")
    #print(title)
    try:
        uri = title["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} not on Spotify.")

#print(song_uris)

# create a playlist with the date
playlist = sp.user_playlist_create(user=user_id, name=f"{user_input} Top 100", public=False)
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)