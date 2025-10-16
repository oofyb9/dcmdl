import argparse
import download
dcmdl_ver = "0.1.0-beta-really-unstable-do-not-use-it-cuz-it-will-break-everything"
def main():  # sourcery skip: extract-duplicate-method, merge-comparisons
    dcmdl_ver = "0.1.0-beta-really-unstable-do-not-use-it-cuz-it-will-break-everything"
    parser = argparse.ArgumentParser(
        prog='dcmd',
        description='the coolest damn media downloader ever.'
    )
    parser.add_argument("-v",'--version', action='version', version=dcmdl_ver)

    # subparsers for different commands
    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # download command
    download_parser = subparsers.add_parser('download', aliases=['dl'], help='download a media file')
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
    download_parser.add_argument('-m', "--download-missing", action='store_true', help='download only missing files in a playlist/album/user')
    download_parser.add_argument('-N', "--continue", dest='continue_dl', action='store_true', help='resume partially downloaded files')
    download_parser.add_argument("-C", "--cookies-from-browser", type=str, help="attempt to extract cookies from your browser (only works on some browsers (mostly chromium based ones))")
    download_parser.add_argument('url', type=str, help='URL of the media to download')

    # the plugin command (used for using plugins for better downloading experience (tbd *sigh*))
    plugins_parser = subparsers.add_parser('plugins', aliases=["plgn"], help='use pluging for better downloading experience (tbd *sigh*)')
    plugins_parser.add_argument('plugin', type=str, help='plugin name (tbd *sigh*)')
    plugins_parser.add_argument('args', nargs=argparse.REMAINDER, help='arguments for the plugin (tbd *sigh*)')

    # the plugin manager command (used for managing plugins listed on github (tbd *sigh*))
    pluginm_parser = subparsers.add_parser('plugin-manager', aliases=["pm"], help='manage plugins listed on github (tbd *sigh*)')
    pluginm_parser.add_argument('action', type=str, choices=['install', 'remove', 'update', 'list'], help='action to perform on the plugins (tbd *sigh*)')
    pluginm_parser.add_argument('plugin', nargs='?', type=str, help='plugin name (tbd *sigh*)')

    # configure command (used for configuring dcmdl settings (tbd *sigh*))
    config_parser = subparsers.add_parser('config', aliases=["cfg"], help='configure dcmdl settings (tbd *sigh*)')
    config_parser.add_argument('setting', nargs='?', type=str, help='setting name to configure (tbd *sigh*)')
    config_parser.add_argument('value', nargs='?', type=str, help='value to set for the setting (tbd *sigh*)')

    args = parser.parse_args()

    if args.command == 'download':
        download.main(args)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()