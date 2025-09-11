import yt_dlp
import gallery_dl # type: ignore
import instaloader # type: ignore
from spotdl import Spotdl # type: ignore
# need to parse this: Namespace(command='download', yt_dlp=True, output=None, format=None, quality=None, gallery_dl=False, spotdl=False, tw=False, ig=False, auto=False, url='jfsdhbslodhfua')

def main (args):
    link = args.url
    dl = args.downloader
    opt = args.output
    frmt = args.format
    qual = args.quality

    print(args)
    print(link)
    print(dl)
    print(opt)
    print(frmt)
    print(qual)
    substring_array = ["sample", "example", "test"]

    found_substring = False
    for substring in substring_array:
       if substring in link:
           found_substring = True
           break  # Exit the loop once a match is found

    if found_substring:
        print(f"The string '{link}' contains at least one substring from the array.")
    else:
        print(f"The string '{link}' does not contain any substring from the array."