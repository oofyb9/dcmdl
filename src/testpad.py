# iPad testing
import yt_dlp
from yt_dlp.postprocessor.common import PostProcessor

song_name = "Los Niños De La Calle - Grupo Cumbaya"

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