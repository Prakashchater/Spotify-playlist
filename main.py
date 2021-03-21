from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth
import pprint
from spotify import spoti

s = spoti()

spotify_get_url = "https://accounts.spotify.com/authorize"
OAUTH_TOKEN_URL= 'https://accounts.spotify.com/api/token'

client_id = "951b4b14a7894ab088115ebd9bbf9f4a"
client_secret = "d5ee78d8154b43cbbe9306b0cc0f7039"

date = input("Which year do you want to Travel? YYYY-MM-DD: ")
url = "https://www.billboard.com/charts/hot-100/" + date
response = requests.get(url)
website = response.text

soup = BeautifulSoup(website,"html.parser")
# print(soup.prettify())

all_song_span = soup.find_all("span", class_="chart-element__information__song")
all_song = [songs.getText() for songs in all_song_span]

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id=s.spotifyId(),
        client_secret=s.spotifySecert(),
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
# print(user_id)

song_name = ["The list of song", "titles from your song","web scrape"]
pp = pprint.PrettyPrinter(indent=4)
song_uris = []
year = date.split('-')[0]
for song in song_name:
    results = sp.search(q=f"track:{song} year:{year}", type="track")
    pp.pprint(results)
    try:
        uri = results["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        pp.pprint(f"{song} doesn't exist in Spotify. Skipped")
playlists = sp.user_playlist_create(user=user_id, name=f"{date} Billboards 100", public=False)
pp.pprint(playlists)

sp.playlist_add_items(playlist_id=playlists["id"],items=song_uris)









