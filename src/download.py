from yt_dlp import YoutubeDL  # type: ignore
from gallery_dl import config, job  # type: ignore
import instaloader  # type: ignore
import gallery_dl_sites
import yt_dlp_sites
import os
from dotenv import load_dotenv
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console
import spotifydl

console = Console()

def yt_dlp_download(link):
    def progress_hook(d):
        if d['status'] == 'downloading':
            if not hasattr(progress_hook, "task_id"):
                progress_hook.task_id = progress.add_task(
                    f"[cyan]{os.path.basename(d.get('filename', 'Downloading'))}",
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
            ydl.download([link])

def gallery_dl_download(link):
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        task_id = progress.add_task(f"[cyan]gallery-dl: {link}", total=1)
        config.load()
        job.Job(link).run()
        progress.update(task_id, advance=1)

def instaloader_download(link):
    post_links = ["post/", "tv/", "reel/", "p/", "stories/", "highlights/", "igtv/"]
    is_post = any(substring in link for substring in post_links)
    L = instaloader.Instaloader()
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        task_id = progress.add_task(f"[cyan]instaloader: {link}", total=1)
        if is_post:
            shortcode = link.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=post.owner_username)
        else:
            username = link.split("/")[-2]
            profile = instaloader.Profile.from_username(L.context, username)
            L.download_profile(profile, profile_pic_only=False)
        progress.update(task_id, advance=1)

def main(args):
    link = args.url
    dl = args.downloader
    opt = args.output
    frmt = args.format
    qual = args.quality

    if dl == "yt-dlp":
        console.print("[bold green]Using yt-dlp as downloader")
        yt_dlp_download(link)
    elif dl == "gallery-dl":
        console.print("[bold green]Using gallery-dl as downloader")
        gallery_dl_download(link)
    elif dl == "instaloader":
        console.print("[bold green]Using instaloader as downloader")
        instaloader_download(link)
    elif dl == "dcsdl":
        console.print("[bold green]Using dcsdl (custom da cool media dl spotify downloader) as downloader")
        spotifydl.main(link)
    elif dl == "auto":
        console.print("[bold green]Using auto-detect downloader")
        found_substring = any(substring in link for substring in yt_dlp_sites.yt_dlp_supported_sites)
        if found_substring:
            console.print(f"[bold yellow]Detected '{link}' as a yt-dlp downloadable link. using yt-dlp")
            yt_dlp_download(link)
        else:
            found_gdl = any(substring in link for substring in gallery_dl_sites.gallery_dl_supported_sites)
            if found_gdl:
                console.print(f"[bold yellow]Detected '{link}' as a gallery-dl downloadable link. Using gallery-dl")
                gallery_dl_download(link)
            else:
                insta_sites = ["instagram.com", "instagr.am"]
                found_insta = any(substring in link for substring in insta_sites)
                if found_insta:
                    console.print(f"[bold yellow]Detected '{link}' as an instagram link, using instaloader")
                    instaloader_download(link)
                else:
                    spotdl_sites = ["spotify.com", "open.spotify.com"]
                    found_spotdl = any(substring in link for substring in spotdl_sites)
                    if found_spotdl:
                        console.print(f"[bold yellow]Detected '{link}' as a spotify link, using dcsdl (custom da cool media dl spotify downloader)")
                        spotifydl.main(link)
                    else:
                        console.print(f"[red]Link '{link}' is not downloadable by yt-dlp, gallery-dl, instaloader, or dcsdl. Exiting")
                        return 1
