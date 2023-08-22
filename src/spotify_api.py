import spotipy
from spotipy.oauth2 import SpotifyOAuth
from dotenv import load_dotenv
import os


sp = spotipy.Spotify(auth_manager=SpotifyOAuth(client_id=os.getenv('CLIENT_ID'),
                                               client_secret=os.getenv('CLIENT_SECRET'),
                                               redirect_uri=os.getenv('REDIRECT_URI'),
                                               scope="user-library-read"))

response = sp.current_user_saved_tracks()['items']
liked_tracks=[]
for track in response:
    liked_tracks.append(track['track']['external_urls']['spotify'])


