import argparse, download, plugin, pluginmanager

dcmdl_ver = "0.1.0-beta-really-unstable-do-not-use-it-cuz-it-will-break-everything"

def main():  # sourcery skip: extract-duplicate-method, merge-comparisons
    parser = argparse.ArgumentParser(
        prog='dcmd',
        description='the coolest damn media downloader ever.'
    )
    parser.add_argument("-v", '--version', action='version', version=dcmdl_ver)

    # Subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Download command
    download_parser = subparsers.add_parser('download', aliases=['dl'], help='download a media file')
    download_parser.add_argument('-o', '--output', type=str, help='output file name')
    download_parser.add_argument('-F', '--folder', type=str, help='folder to download media')
    download_parser.add_argument('-f', '--format', type=str, help='format of the media to download')
    download_parser.add_argument('-q', '--quality', type=str, help='quality of the media to download')
    download_parser.add_argument('-d', "--downloader", type=str, default="auto", help="downloader to use (auto (default, a bit accurate), ytdlp, dcsdl, tw, ig, gallerydl)")
    download_parser.add_argument('-u', "--username", type=str, help='login username for private content (instagram, pinterest, etc.)')
    download_parser.add_argument('-p', "--password", type=str, help='login password for private content (instagram, pinterest, etc.)')
    download_parser.add_argument('-O', "--oauth", action='store_true', help='enable oauth login for supported sites')
    download_parser.add_argument('-c', "--cookies", type=str, help='path to cookies.txt file for authenticated downloads')
    download_parser.add_argument('-L', "--list-format", action='store_true', help='list available formats for the given URL and exit')
    download_parser.add_argument('-U', "--update", action='store_true', help='download the latest version of the downloader tools (yt-dlp, gallery-dl, etc.)')
    download_parser.add_argument('-D', "--debug", action='store_true', help='enable debug mode (verbose ++)')
    download_parser.add_argument('-m', "--download-missing", action='store_true', help='download only missing files in a playlist/album/user')
    download_parser.add_argument('-N', "--continue", dest='continue_dl', action='store_true', help='resume partially downloaded files')
    download_parser.add_argument("-C", "--cookies-from-browser", type=str, help="attempt to extract cookies from your browser (works with chromium and firefox based browsers)")
    download_parser.add_argument("-t", "--title", type=str, help="title pattern (used by instaloader)")
    download_parser.add_argument("-T", "--tries", type=int, help="# of attempts for download")
    download_parser.add_argument('url', type=str, help='URL of the media to download')

    # the plugin manager command (used for managing plugins listed on github
    pluginm_parser = subparsers.add_parser('plugin-manager', aliases=["pm"], help='manage plugins listed on github')
    pluginm_parser.add_argument('action', type=str, choices=['install', 'remove', 'update', 'list'], help='action to perform on the plugins')
    pluginm_parser.add_argument('-p', '--plain', action='store_true', help='output plain text (for scripting)')
    pluginm_parser.add_argument('plugin', nargs='?', type=str, help='plugin name')

    # Parse arguments
    args, remaining = parser.parse_known_args()

    if args.command in ['download', 'dl']:
        return download.main(args)
    if args.command in ['plugins', 'plgn']:
        return plugin.main(args)
    elif args.command in ['plugin-manager', 'pm']:
        return pluginmanager.main(args)
    else:
        parser.print_help()
        return 1

if __name__ == '__main__':
    raise SystemExit(main())