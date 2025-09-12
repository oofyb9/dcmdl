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
    gui_parser = subparsers.add_parser('gui', help='launch the GUI')
    gui_parser.add_argument('-t', '--type', type=str, default="gui", help=' (launch as gui or web app, default: gui)')

    # download command
    download_parser = subparsers.add_parser('download', help='download a media file')
    download_parser.add_argument('-o', '--output', type=str, help='output file name')
    download_parser.add_argument('-f', '--format', type=str, help='format of the media to download')
    download_parser.add_argument('-q', '--quality', type=str, help='quality of the media to download')
    download_parser.add_argument('-d', "--downloader", type=str, default="auto", help="downloader to use (auto (default, a bit accurate), ytdlp, spotdl, tw, ig, gallerydl)")
    download_parser.add_argument('url', type=str, help='URL of the media to download')

    # shorter download command (dl)
    dl_parser = subparsers.add_parser('dl', help='same as above')
    dl_parser.add_argument('-o', '--output', type=str, help='output file name')
    dl_parser.add_argument('-f', '--format', type=str, help='format of the media to download')
    dl_parser.add_argument('-q', '--quality', type=str, help='quality of the media to download')
    dl_parser.add_argument('-d', "--downloader", type=str, default="auto", help="downloader to use (auto (default, a bit accurate), ytdlp, spotdl, tw, ig, gallerydl)")
    dl_parser.add_argument('url', type=str, help='URL of the media to download')

    args = parser.parse_args()

    if args.command == 'dl' or args.command == 'download':
        download.main(args)
    elif args.command == 'gui':
        webui.main(args.type)
    else:
        parser.print_help()

if __name__ == '__main__':
    main()