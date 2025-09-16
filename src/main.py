import argparse
import download
import webui

def main():  # sourcery skip: extract-duplicate-method, merge-comparisons
    parser = argparse.ArgumentParser(
        prog='dcmd',
        description='the coolest damn media downloader ever.'
    )

    # subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # GUI command
    gui_parser = subparsers.add_parser('web', help='launch the webUI', aliases="w")

    # download command
    download_parser = subparsers.add_parser('download', aliases="d", help='download a media file')
    download_parser.add_argument('-o', '--output', type=str, help='output file name')
    download_parser.add_argument('-f', '--format', type=str, help='format of the media to download')
    download_parser.add_argument('-q', '--quality', type=str, help='quality of the media to download')
    download_parser.add_argument('-d', "--downloader", type=str, default="auto", help="downloader to use (auto (default, a bit accurate), ytdlp, dcsdl, tw, ig, gallerydl)")
    download_parser.add_argument('-u', "--username", type=str, help='login username for private content (instagram, twitter, etc.)')
    download_parser.add_argument('-p', "--password", type=str, help='login password for private content (instagram, twitter, etc.)')
    download_parser.add_argument('-O', "--oauth", action='store_true', help='enable oauth login for supported sites')
    download_parser.add_argument('-c', "--cookies", type=str, help='path to cookies.txt file for authenticated downloads')
    download_parser.add_argument('-L', "--list-format", action='store_true', help='list available formats for the given URL and exit')
    download_parser.add_argument('-U', "--update", action='store_true', help='download the latest version of the downloader tools (yt-dlp, gallery-dl, etc.)')
    download_parser.add_argument('-D', "--debug", action='store_true', help='enable debug mode (more verbose output)')
    download_parser.add_argument('-v', "--version", action='store_true', help='show version information and exit')
    download_parser.add_argument('-m', "--download-missing", action='store_true', help='download only missing files in a playlist/album/user')
    download_parser.add_argument('-N', "--continue", dest='continue_dl', action='store_true', help='resume partially downloaded files')
    download_parser.add_argument("-C", "--cookies-from-browser", type=str, help="attempt to extract cookies from your browser (only works on some browsers (mostly chromium based ones))")
    download_parser.add_argument('url', type=str, help='URL of the media to download')

    args = parser.parse_args()

    if args.command == 'download':
        download.main(args)
    elif args.command == 'web':
        webui.main()
    else:
        parser.print_help()

if __name__ == '__main__':
    main()