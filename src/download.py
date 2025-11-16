from yt_dlp import YoutubeDL  # type: ignore
from gallery_dl import config, job  # type: ignore
import instaloader, gallery_dl_sites, yt_dlp_sites, os, spotifydl, pluginmanager, plugin  # type: ignore
from dotenv import load_dotenv
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from rich.console import Console
import requests
console = Console()

def yt_dlp_download(args):
    format = args.format if args.format else "best"
    quality = args.quality if args.quality else "best"
    cookies = args.cookies if args.cookies else None
    cookies_from_browser = args.cookies_from_browser if args.cookies_from_browser else None
    continue_dl = args.continue_dl if args.continue_dl else True
    output = args.output if args.output else "%(title)s.%(ext)s"
    folder = args.folder if args.folder else "~/Downloads"
    username = args.username if args.username else None
    password = args.password if args.password else None
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
        'format': f"{format}[height<={quality}]",
        'outtmpl': os.path.join(os.path.expanduser(folder), output),
        'continuedl': continue_dl,
        'download_archive': os.path.join(os.path.expanduser(folder), 'downloaded.txt'),
        'username': username,
        'password': password,
        'cookies': cookies,
        'cookies_from_browser': cookies_from_browser,
        'quality': quality,
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
            ydl.download([args.url])

def gallery_dl_download(args):
    console.print("[yellow]Unfortunately, we can not pass args to gallery-dl, you will have to set a separate gallery-dl.conf file in your home folder ($HOME for *nix users, %HOMEPATH% for Windows users)")
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        task_id = progress.add_task(f"[cyan]gallery-dl: {args.url}", total=1)
        config.load()
        job.Job(args.url).run()
        progress.update(task_id, advance=1)

def instaloader_download(args):
    post_links = ["post/", "tv/", "reel/", "p/", "stories/", "highlights/", "igtv/"]
    is_post = any(substring in args.url for substring in post_links)
    L = instaloader.Instaloader(False, False, None, args.folder, args.filename, True, True, True, save_metadata=True, title_pattern=args.title, max_connection_attempts=args.tries)
    with Progress(
        TextColumn("[progress.description]{task.description}"),
        BarColumn(),
        transient=True,
    ) as progress:
        task_id = progress.add_task(f"[cyan]instaloader: {args.url}", total=1)
        if is_post:
            shortcode = args.url.split("/")[-2]
            post = instaloader.Post.from_shortcode(L.context, shortcode)
            L.download_post(post, target=post.owner_username)
        else:
            username = args.url.split("/")[-2]
            profile = instaloader.Profile.from_username(L.context, username)
            L.download_profile(profile, profile_pic_only=False)
        progress.update(task_id, advance=1)

def main(args):
    dl = args.downloader
    if dl == "yt-dlp":
        console.print("[bold green]Using yt-dlp as downloader")
        yt_dlp_download(args)
    elif dl == "gallery-dl":
        console.print("[bold green]Using gallery-dl as downloader")
        gallery_dl_download(args)
    elif dl == "instaloader":
        console.print("[bold green]Using instaloader as downloader")
        instaloader_download(args)
    elif dl == "dcsdl":
        console.print("[bold green]Using dcsdl (custom da cool media dl spotify downloader) as downloader")
        spotifydl.main(args)
    elif dl == "auto":
        console.print("[bold green]Using auto-detect downloader")
        found_substring = any(substring in args.url for substring in yt_dlp_sites.yt_dlp_supported_sites)
        if found_substring:
            console.print(f"[bold yellow]Detected '{args.url}' as a yt-dlp downloadable link. using yt-dlp")
            yt_dlp_download(args)
        else:
            found_gdl = any(substring in args.url for substring in gallery_dl_sites.gallery_dl_supported_sites)
            if found_gdl:
                console.print(f"[bold yellow]Detected '{args.url}' as a gallery-dl downloadable link. Using gallery-dl")
                gallery_dl_download(args)
            else:
                insta_sites = ["instagram.com", "instagr.am"]
                found_insta = any(substring in args.url for substring in insta_sites)
                if found_insta:
                    console.print(f"[bold yellow]Detected '{args.url}' as an instagram link, using instaloader")
                    instaloader_download(args)
                else:
                    spotdl_sites = ["spotify.com", "open.spotify.com"]
                    found_spotdl = any(substring in args.url for substring in spotdl_sites)
                    if found_spotdl:
                        console.print(f"[bold yellow]Detected '{args.url}' as a spotify link, using dcsdl (custom da cool media dl spotify downloader)")
                        spotifydl.main(args)
                    else:
                        plugins = pluginmanager.list_plgn_plain(True, False)
                        plugin_array = plugins.splitlines()
                        for item in plugin_array:
                            url = f"https://raw.githubusercontent.com/oofybruh9/dcmdl-plugins/refs/heads/main/plugins/{item}.json"
                            with console.status(f"[cyan]Checking if plugin [bold]{item}[/bold] supports [bold]{args.url}[/bold]...", spinner="dots"):
                                try:
                                    # Fetch plugin metadata
                                    resp = requests.get(url, timeout=10)
                                    if resp.status_code == 200:
                                        jsonmn = resp.json()
                                    elif resp.status_code == 404:
                                        console.print(f"[red]Plugin '{item}' not found (404).")
                                        continue
                                    else:
                                        console.print(f"[red]Failed to fetch metadata for plugin '{item}': HTTP {resp.status_code}")
                                        continue
                                except requests.RequestException as e:
                                    console.print(f"[red]Request error while fetching plugin '{item}': {e}")
                                    continue

                                # Check if the URL is supported by the plugin
                                if jsonmn and 'supported_sites' in jsonmn:
                                    found_plugin = any(substring in args.url for substring in jsonmn['supported_sites'])
                                    if found_plugin:
                                        console.print(f"[bold yellow]Detected '{args.url}' as a {item} link. Using {item} plugin.")
                                        try:
                                            return plugin.use_plgn(item, args)
                                        except Exception as e:
                                            console.print(f"[red]Error while running plugin '{item}': {e}")
                                            return 1
                                else:
                                    console.print(f"[red]Plugin '{item}' does not have valid metadata or does not support the URL.")
    else:
        plugins = pluginmanager.list_plgn_plain(True, False)
        if dl in plugins:
            console.print(f"[bold green]Using plugin '{dl}' as downloader")
            return plugin.use_plgn(dl, args)
        else:
            plugin_names = pluginmanager.list_plgn_plain(True, True)
            console.print(f"[red]no downloader found out of list of downloaders: yt-dlp, dcsdl, gallery-dl, instaloader, or any plugin ({plugin_names}). Exiting")
            return 1
