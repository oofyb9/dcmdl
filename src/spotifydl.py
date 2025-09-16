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
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console

def main(spotify_track_link):
    console = Console()
    load_dotenv(dotenv_path="spotify.env")
    SPOTIPY_CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
    SPOTIPY_SECRET_ID = os.getenv('SPOTIPY_SECRET_ID')
    client_credentials_manager = SpotifyClientCredentials(client_id=SPOTIPY_CLIENT_ID, client_secret=SPOTIPY_SECRET_ID)
    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

    # Step 1: Get song name
    with console.status("[bold green]Getting song name from Spotify link..."):
        def get_song_name_from_link(spotify_link):
            try:
                track_id = spotify_link.split('/')[-1].split('?')[0]
                track_info = sp.track(track_id)
                song_name = track_info['name']
                song_artist = track_info['artists'][0]['name']
                song_sdsdfsd = f"{song_name} - {song_artist}"
                return song_sdsdfsd
            except Exception as e:
                console.print(f"[red]Error: {e}")
                return None

        song_name = get_song_name_from_link(spotify_track_link)
        real_song_name = song_name.split(" -", 1)[0] if song_name else None

    if song_name:
        console.print(f"[bold green]The song name is: {song_name}")
    else:
        console.print("[red]Could not retrieve song name.")
        return

    # Step 2: Search song with ytmusicapi
    with console.status("[bold green]Searching song on YouTube Music..."):
        yt = ytmusicapi.YTMusic()
        search_results = yt.search(song_name, filter='songs')
        if search_results:
            first_result = search_results[0]
            video_id = first_result['videoId']
            console.print(f"[bold green]First search result video ID: {video_id}")
        else:
            console.print("[red]No search results found.")
            return

    # Step 3: Download video with yt-dlp and Rich progress bar
    console.print("[bold green]Downloading audio and thumbnail with yt-dlp...")
    class RichSilentLogger:
        def debug(self, msg): pass
        def warning(self, msg): pass
        def error(self, msg): pass
        def info(self, msg): pass

    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        DownloadColumn(),
        TransferSpeedColumn(),
        TimeRemainingColumn(),
        transient=True,
    ) as progress:
        task_ids = {}

        def ytdlp_progress_hook(d):
            # Only show progress for downloading files (not thumbnails, metadata, etc.)
            if d['status'] == 'downloading' and 'filename' in d:
                filename = d['filename']
                total = d.get('total_bytes') or d.get('total_bytes_estimate', 100)
                completed = d.get('downloaded_bytes', 0)
                if filename not in task_ids:
                    task_ids[filename] = progress.add_task(
                        f"[cyan]{os.path.basename(filename)}", total=total
                    )
                progress.update(
                    task_ids[filename],
                    completed=completed,
                    total=total
                )
            elif d['status'] == 'finished' and 'filename' in d:
                filename = d['filename']
                if filename in task_ids:
                    progress.update(task_ids[filename], completed=progress.tasks[task_ids[filename]].total)

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
            ],
            'progress_hooks': [ytdlp_progress_hook],
            'logger': RichSilentLogger(),
        }

        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([video_id])

    # Step 4: Crop album image
    with console.status("[bold green]Cropping album image..."):
        def crop_to_square_same_height(image_path, output_path):
            try:
                img = Image.open(image_path)
            except FileNotFoundError:
                console.print(f"[red]Error: Image not found at {image_path}")
                return
            width, height = img.size
            left = (width - height) / 2
            top = 0
            right = (width + height) / 2
            bottom = height
            crop_box = (int(left), int(top), int(right), int(bottom))
            cropped_img = img.crop(crop_box)
            cropped_img.save(output_path)
            console.print(f"[bold green]Image cropped and saved to {output_path}")

        crop_to_square_same_height(f'{real_song_name}.jpg', f'{real_song_name}.jpg')

    # Step 5: Embed album image
    with console.status("[bold green]Embedding album image into MP3..."):
        audiofile = eyed3.load(f'{real_song_name}.mp3')
        if (audiofile.tag == None):
            audiofile.initTag()
        audiofile.tag.images.set(ImageFrame.FRONT_COVER, open(f'{real_song_name}.jpg','rb').read(), 'image/jpeg')
        audiofile.tag.save()
        os.remove(f'{real_song_name}.jpg')
        console.print(f"[bold green]Album image embedded and temp image removed.")