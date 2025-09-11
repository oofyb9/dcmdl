import requests
import re

YT_DLP_URL = "https://raw.githubusercontent.com/yt-dlp/yt-dlp/master/supportedsites.md"
GALLERY_DL_URL = "https://raw.githubusercontent.com/mikf/gallery-dl/master/docs/supportedsites.md"

def fetch_sites(url):
    resp = requests.get(url)
    resp.raise_for_status()
    text = resp.text
    # Each site is usually a list item starting with "- **SiteName**" or "- SiteName"
    # Let's capture both patterns:
    pattern = re.compile(r"^\s*-\s*(?:\*\*)?([^*\n:]+)(?:\*\*)?(?::|\s|$)", re.MULTILINE)
    sites = pattern.findall(text)
    # Clean up whitespace
    sites = [site.strip() for site in sites]
    # Remove duplicates, preserve order
    seen = set()
    out = []
    for s in sites:
        if s not in seen:
            seen.add(s)
            out.append(s)
    return out

if __name__ == "__main__":
    yt_sites = fetch_sites(YT_DLP_URL)
    gal_sites = fetch_sites(GALLERY_DL_URL)

    # Print or save as Python arrays
    print("yt_dlp_supported_sites = [")
    for s in yt_sites:
        print(f"    {s!r},")
    print("]\n")

    print("gallery_dl_supported_sites = [")
    for s in gal_sites:
        print(f"    {s!r},")
    print("]")
    
    # Optionally, write to files
    with open("yt_dlp_sites.py", "w", encoding="utf-8") as f:
        f.write("yt_dlp_supported_sites = [\n")
        for s in yt_sites:
            f.write(f"    {s!r},\n")
        f.write("]\n")

    with open("gallery_dl_sites.py", "w", encoding="utf-8") as f:
        f.write("gallery_dl_supported_sites = [\n")
        for s in gal_sites:
            f.write(f"    {s!r},\n")
        f.write("]\n")
