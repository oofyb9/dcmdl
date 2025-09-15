import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import yt_dlp
import ffmpeg
import  ytmusicapi
from PIL import Image
import eyed3
from eyed3.id3.frames import ImageFrame

def main(spotify_track_link):
    load_dotenv(dotenv_path="spotify.env")
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_SECRET_ID = os.getenv('SPOTIPY_SECRET_ID')
    print(f"Using SPOTIPY_CLIENT_ID: {SPOTIPY_CLIENT_ID}")
    print(f"Using SPOTIPY_SECRET_ID: {SPOTIPY_SECRET_ID}")
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_SECRET_ID)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    def get_song_name_from_link(spotify_link):
        try:
            track_id = spotify_link.split('/')[-1].split('?')[0]
            track_info = sp.track(track_id)
            song_name = track_info['name']
            song_artist = track_info['artists'][0]['name']
            song_sdsdfsd = f"{song_name} - {song_artist}"
            return song_sdsdfsd
        except Exception as e:
            print(f"Error: {e}")
            return None

    song_name = get_song_name_from_link(spotify_track_link)
    real_song_name = song_name.split(" -", 1)[0]

    if song_name:
        print(f"The song name is: {song_name}")
    else:
        print("Could not retrieve song name.")

    yt = ytmusicapi.YTMusic()
    search_results = yt.search(song_name, filter='songs')
    if search_results:
        first_result = search_results[0]
        video_id = first_result['videoId']
        print(f"First search result video ID: {video_id}")
        video_info = yt.get_song(video_id)
        print(f"Video Info: {video_info}")
    else:
        print("No search results found.")

    ydl_opts = {
        'cookiesfrombrowser': ('opera',),
        'format': 'bestaudio/best',
        'outtmpl': '%(title)s.%(ext)s',
        'default_search': 'https://music.youtube.com/search?q=',
        'writethumbnail': True,
        'addmetadata': True,

        'postprocessors': [
            {
                'key': 'FFmpegExtractAudio',
                'preferredcodec': 'mp3',
                'preferredquality': '192',
            },
            {
                'key': 'FFmpegThumbnailsConvertor',
                'format': 'jpg',
            },
            {
                'key': 'FFmpegMetadata',
            },
        ]
    }

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download(f"{video_id}")

    def crop_to_square_same_height(image_path, output_path):
        try:
            img = Image.open(image_path)
        except FileNotFoundError:
            print(f"Error: Image not found at {image_path}")
            return
        width, height = img.size
        left = (width - height) / 2
        top = 0
        right = (width + height) / 2
        bottom = height
        crop_box = (int(left), int(top), int(right), int(bottom))
        cropped_img = img.crop(crop_box)
        cropped_img.save(output_path)
        print(f"Image cropped and saved to {output_path}")
    crop_to_square_same_height(f'{real_song_name}.jpg', f'{real_song_name}.jpg')
    audiofile = eyed3.load(f'{real_song_name}.mp3')
    if (audiofile.tag == None):
        audiofile.initTag()
    audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(f'{real_song_name}.jpg','rb').read(), 'image/jpeg')
    audiofile.tag.save()
    os.remove(f'{real_song_name}.jpg')