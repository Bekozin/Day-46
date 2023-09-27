from bs4 import BeautifulSoup
import requests
import spotipy
from spotipy.oauth2 import SpotifyOAuth

date = (input("Which year dou you want to travel to? Type the data in this format YYYY-MM-DD  "))

URL = ("https://www.billboard.com/charts/hot-100/" + date)

response = requests.get(URL)
website_html = response.text

soup = BeautifulSoup(website_html, "html.parser")
all_music = soup.select("li ul li h3")
musics = [song.getText().strip() for song in all_music]

with open("music.txt", mode="w") as file:
    for music in musics:
        file.write(f"{music}\n")


client_id = YOUR CLIENT ID
client_secret = YOUR CLIENT SECRET
scope = "playlist-modify-private"

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri="http://example.com",
        scope=scope,
        show_dialog=True,
        cache_path="token.txt",
        username=Your Username, ))
# show_dialog, cche_path, username ve user_id kodunu dosyadan bakarken bulamadım yada örneklerden ?

user_id = sp.current_user()["id"]

print(user_id)

song_uris = []
year = date.split("-")[0]
for song in musics:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_uris.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

# Creating a new private playlist in Spotify
playlist = sp.user_playlist_create(user=user_id, name=f"{date} Billboard 100", public=False)
print(playlist)

# Adding songs found into the new playlist
sp.playlist_add_items(playlist_id=playlist["id"], items=song_uris)
