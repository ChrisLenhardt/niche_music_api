import os

from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

load_dotenv()

spotify = spotipy.Spotify(
    auth_manager=SpotifyClientCredentials(client_id=os.getenv("SPOTIPY_CLIENT_ID"),
                                          client_secret=os.getenv("SPOTIPY_CLIENT_SECRET"))
                                          )

def get_artist_image():
    name = 'Radiohead'

    results = spotify.search(q='artist:' + name, type='artist')
    items = results['artists']['items']
    if len(items) > 0:
        artist = items[0]
        r_val = artist['name'], artist['images'][0]['url']
        print(artist['name'], artist['images'][0]['url'])
    return r_val
