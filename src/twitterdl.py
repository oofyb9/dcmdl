import requests
import re
import sys
import json
from pathlib import Path
from rich.console import Console
from rich.progress import Progress, BarColumn, TextColumn, DownloadColumn, TransferSpeedColumn, TimeRemainingColumn
from browser_cookie3 import load

console = Console()

def parse_cookie_file(cookiefile):
    cookies = {}
    with open(cookiefile, 'r') as fp:
        for line in fp:
            if not re.match(r'^\#', line):
                line_fields = line.strip().split('\t')
                cookies[line_fields[5]] = line_fields[6]
    return cookies


def get_tweet(link, file_format, output, quality, folder, cookies, browser_cookies):
    url = link
    cookies = parse_cookie_file(cookies) if cookies else {}
    if browser_cookies:
        browser_cookies_dict = {}
        cj = load(browser=browser_cookies)
        for cookie in cj:
            browser_cookies_dict[cookie.name] = cookie.value
        cookies.update(browser_cookies_dict)

    console.print(f"[cyan]Fetching tweet from {url}...[/cyan]")
    response = requests.get(url, cookies=cookies)
    if response.status_code != 200:
        console.print("[red]Failed to retrieve tweet. Please check the link and your authentication tokens.[/red]")
        sys.exit(1)

    html = response.text

    # Extract image URLs
    image_urls = re.findall(r'https://pbs\.twimg\.com/media/[^\s"]+\?format=\w+', html)

    # Extract video URLs
    video_urls = re.findall(r'https://video\.twimg\.com/[^\s"]+\.mp4', html)

    if not image_urls and not video_urls:
        console.print("[red]No media found in the tweet.[/red]")
        sys.exit(1)

    # Download images
    for idx, image_url in enumerate(image_urls, start=1):
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        filename = folder_path / (output or f"tweet_image_{idx}.{file_format}")
        console.print(f"[cyan]Downloading image to {filename}...[/cyan]")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            transient=True,
        ) as progress:
            task_id = progress.add_task("[cyan]Downloading...[/cyan]", total=None)
            with requests.get(image_url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                progress.update(task_id, total=total)
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(task_id, advance=len(chunk))
        console.print(f"[green]Downloaded image to {filename}[/green]")

    # Download videos
    for idx, video_url in enumerate(video_urls, start=1):
        folder_path = Path(folder)
        folder_path.mkdir(parents=True, exist_ok=True)
        filename = folder_path / (output or f"tweet_video_{idx}.{file_format}")
        console.print(f"[cyan]Downloading video to {filename}...[/cyan]")

        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            DownloadColumn(),
            TransferSpeedColumn(),
            TimeRemainingColumn(),
            transient=True,
        ) as progress:
            task_id = progress.add_task("[cyan]Downloading...[/cyan]", total=None)
            with requests.get(video_url, stream=True) as r:
                r.raise_for_status()
                total = int(r.headers.get('content-length', 0))
                progress.update(task_id, total=total)
                with open(filename, 'wb') as f:
                    for chunk in r.iter_content(chunk_size=8192):
                        f.write(chunk)
                        progress.update(task_id, advance=len(chunk))
        console.print(f"[green]Downloaded video to {filename}[/green]")


def main(args):
    """
    Namespace(command='download', output=None, folder=None, format=None, quality=None, downloader='dcxdl', username=None, password=None, oauth=False, cookies=None, list_format=False, update=False, debug=False, download_missing=False, continue_dl=False, cookies_from_browser=None, url='https://x.com/oofybruh9/status/1967786001763615076')
    """
    term = Console()
    if args.username is not None and args.password is not None:
        term.print("[red]Error: twitterdl does not support login authentication due to Twitter's restrictions. Please remove the username and password arguments and use either --cookies-from-browser or --cookies. Logins will save automatically.[/red]")
        sys.exit(1)
    else:
        get_tweet(args.url, args.format, args.output, args.quality, args.folder, args.cookies, args.cookies_from_browser)