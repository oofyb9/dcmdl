from yt_dlp import YoutubeDL  # type: ignore
from gallery_dl import config, job  # type: ignore
import instaloader  # type: ignore
from spotdl import Spotdl  # type: ignore
import gallery_dl_sites
import yt_dlp_sites
import os
from dotenv import load_dotenv
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
import spotifydl
# need to parse this: Namespace(command='download', yt_dlp=True, output=None, format=None, quality=None, gallery_dl=False, spotdl=False, tw=False, ig=False, auto=False, url='jfsdhbslodhfua')


def main(args):  # sourcery skip: use-any, use-named-expression, use-next
    link = args.url
    dl = args.downloader
    opt = args.output
    frmt = args.format
    qual = args.quality
    if dl == "yt-dlp":
        print("Using yt-dlp as downloader")
        def progress_hook(d):
            if d['status'] == 'downloading':
                if not hasattr(progress_hook, "task_id"):
                    progress_hook.task_id = progress.add_task(
                        f"[cyan]{d.get('filename', 'Downloading')}",
                        total=d.get('total_bytes', d.get('total_bytes_estimate', 100))
                    )
                progress.update(
                    progress_hook.task_id,
                    completed=d.get('downloaded_bytes', 0),
                    total=d.get('total_bytes', d.get('total_bytes_estimate', 100))
                )
            elif d['status'] == 'finished':
                progress.update(progress_hook.task_id, completed=progress.tasks[0].total)

        ydl_opts = {
            'progress_hooks': [progress_hook],
        }
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            transient=True,
        ) as progress:
            with YoutubeDL(ydl_opts) as ydl:
                ydl.download(link)
    elif dl == "gallery-dl":
        print("Using gallery-dl as downloader")
    elif dl == "twmd":
        print("Using twmd (twitter media downloader) as downloader")
    elif dl == "instaloader":
        print("Using instaloader as downloader")
    elif dl == "spotdl":
        print("Using dcsdl (custom da cool media dl spotify downloader) as downloader")
        spotifydl.main(link)
    elif dl == "auto":
        print("Using auto-detect downloader")
        found_substring = False
        for substring in yt_dlp_sites.yt_dlp_supported_sites:
            if substring in link:
                found_substring = True
                break  # Exit the loop once a match is found
        if found_substring:
            print(f"Detected '{link}' as a yt-dlp downloadable link. using yt-dlp")
        else:
            print(f"The string '{link}' is not downloadable by yt-dlp, trying gallery-dl")
        found_gdl = False
        for substring in gallery_dl_sites.gallery_dl_supported_sites:
            if substring in link:
                found_gdl = True
                break
        if found_gdl:
            print(f"Detected '{link}' as a gallery-dl downloadable link. Using gallery-dl")
        else:
            print(f"The string '{link}' is not downloadable by gallery-dl, trying twmd (twitter media downloader)")
        twmd_sites = ["x.com", "twitter.com"]
        found_twmd = False
        for substring in twmd_sites:
            if substring in link:
                found_twmd = True
                break
        if found_twmd:
            print(f"Detected '{link}' as a X (formerly Twitter) link, using twmd")
        else:
            print(f"The string '{link}' is not a twitter link. Using instaloader")
        insta_sites = ["instagram.com", "instagr.am"]
        found_insta = False
        for substring in insta_sites:
            if substring in link:
                found_insta = True
                break
        if found_insta:
            print(f"Detected '{link}' as an instagram link, using instaloader")
        else:
            print(f"The string '{link}' is not an instagram link. trtying spotdl (spotify downloader)")
        found_spotdl = False
        spotdl_sites = ["spotify.com", "open.spotify.com"]
        for substring in spotdl_sites:
            if substring in link:
                found_spotdl = True
                break
        if found_spotdl:
            print(f"Detected '{link}' as a spotify link, using spotdl")
        else:
            print(f"Link '{link}' is not downloadable by yt-dlp, gallery-dl, twmd, instaloader, or spotDL. Exiting")
            return 1
    else:
        print("Invalid downloader option. Use 'yt-dlp', 'gallery-dl', 'twmd', 'instaloader', 'spotdl', or 'auto'.")
        return 1
