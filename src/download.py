import yt_dlp
import gallery_dl # type: ignore
import instaloader # type: ignore
from spotdl import Spotdl # type: ignore
import gallery_dl_sites
import yt_dlp_sites
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
            found_twmd =  True
            break
    if found_twmd:
        print(f"Detected '{link}' as a X (formerly Twitter) link, using twmd")
    else:
        print(f"The string '{link}' is not a twitter link. Using instaloader")
    insta_sites = ["instagram.com"]
    found_insta = False
    for substring in insta_sites:
        if substring in link:
            found_insta =  True
            break
    if found_insta:
        print(f"Detected '{link}' as an instagram link, using instaloader")
    else:
        print(f"Link '{link}' is not downloadable by yt-dlp, gallery-dl, twmd, or instaloader. Exiting")