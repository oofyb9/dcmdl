import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import yt_dlp
import ffmpeg
load_dotenv(dotenv_path="spotify.env")

# Replace with your actual Client ID and Client Secret
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_SECRET_ID')

# Authenticate with Spotify API
client_credentials_manager = SpotifyClientCredentials(client_id=CLIENT_ID, client_secret=CLIENT_SECRET)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

def get_song_name_from_link(spotify_link):
    try:
    # Extract the track ID from the Spotify link
        # Spotify track links typically look like: https://open.spotify.com/track/{track_id}
        track_id = spotify_link.split('/')[-1].split('?')[0]
        # Get track information using the track ID
        track_info = sp.track(track_id)
        # Extract the song name
        song_name = track_info['name']
        song_artist = track_info['artists'][0]['name']
        song_sdsdfsd = f"{song_name} - {song_artist}"
        return song_sdsdfsd
    except Exception as e:
        print(f"Error: {e}")
        return None

# Example usage:
spotify_track_link = "https://open.spotify.com/track/3mEVkbQZ1p7y4YDHYNSTTv?si=c7af4998416a4d1e" # Replace with a valid Spotify track link
song_name = get_song_name_from_link(spotify_track_link)

if song_name:
    print(f"The song name is: {song_name}")
    
else:
    print("Could not retrieve song name.")
from yt_dlp.postprocessor.common import PostProcessor

# ipad only song_name = "Los Niños De La Calle - Grupo Cumbaya"

ydl_opts = {
    'cookiesfrombrowser': ('opera',),
    'format': 'bestaudio/best',
    'outtmpl': '%(title)s.%(ext)s',
    'writethumbnail': True,
    'addmetadata': True,

    'postprocessors': [
        {   # Extract audio
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        },
        {   # Convert thumbnails to jpg
            'key': 'FFmpegThumbnailsConvertor',
            'format': 'jpg',
        },
        {   # Embed metadata
            'key': 'FFmpegMetadata',
        },
    ]
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([f'ytsearch:{song_name}'])