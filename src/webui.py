from nicegui import ui, html, run
import random
import subprocess
import sys
import asyncio
import main
import download
import io
import contextlib

# async subprocess streamer (for formats, updater, etc.)
async def run_command_and_stream(command: list[str], console):
    process = await asyncio.create_subprocess_exec(
        *command,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    async for line in process.stdout:
        text = line.decode().rstrip()
        console.text += text + '\n'
        console.update()
        ui.run_javascript("var el=document.querySelector('.konsole'); if(el) el.scrollTop=el.scrollHeight;")
        await asyncio.sleep(0)

    await process.wait()
    console.text += f"\n[exit code {process.returncode}]\n"
    console.update()


# capture download.py logs and send them into NiceGUI console
def run_download(downloader, url, output, quality, console):
    buf = io.StringIO()

    class ConsoleRedirect:
        def write(self, data):
            buf.write(data)
            console.text += data
            console.update()
            ui.run_javascript("var el=document.querySelector('.konsole'); if(el) el.scrollTop=el.scrollHeight;")

        def flush(self): pass

    with contextlib.redirect_stdout(ConsoleRedirect()), contextlib.redirect_stderr(ConsoleRedirect()):
        # call into your download.py main function
        class Args:
            pass
        args = Args()
        args.url = url
        args.downloader = downloader
        args.output = output
        args.format = None
        args.quality = quality
        download.main(args)


def checkver():
    ydl_ver = subprocess.run(["yt-dlp","--version"], capture_output=True, text=True, check=True)
    gdl_ver = subprocess.run(["gallery-dl","--version"], capture_output=True, text=True, check=True)
    inl_ver = subprocess.run(["instaloader","--version"], capture_output=True, text=True, check=True)
    ui.notify(f"yt-dlp: {ydl_ver.stdout}, gallery-dl: {gdl_ver.stdout}, instaloader: {inl_ver.stdout}, dcsdl/dcmdl: {main.dcmdl_ver}")


def realupdate(console):
    ui.notify("running `pip install nicegui argparse yt-dlp gallery-dl instaloader ytmusicapi spotipy eyed3`")
    run.io_bound(run_command_and_stream, ["pip", "install", "yt-dlp", "gallery-dl", "instaloader", "ytmusicapi", "spotipy", "eyed3", "nicegui"], console)


def start():
    with open(r'console_quotes.txt', "r") as f:
        l = [line.rstrip() for line in f]
    with open(r'console_quotes.txt', "r") as fi:
        lines = len(fi.readlines())
    num = random.randint(0, lines)

    ui.add_css(""".konsole{
        background-color: #1e1e1e;
        color: #c0c0c0;
        font-family: 'Fira Code', monospace;
        font-size: 12pt;
        padding: 10px;
        border-radius: 5px;
        box-shadow: 0 0 10px rgba(0, 0, 0, 0.5);
        overflow-y: auto;
        height: 400px;
        width: 100%;
        overflow-x: auto;
        white-space: pre-wrap;
    }""")

    ui.markdown("# DCMD WebUI")

    # one shared console
    console = ui.label(l[num] + "\n").classes('konsole')

    # new download section
    with ui.expansion('new download', icon='sym_r_download').classes('w-full'):
        ui.label('new download')
        i = ui.input(placeholder='enter url here...').classes('w-full')
        radio = ui.radio({1: 'yt-dlp', 2: 'gallery-dl', 3: 'instaloader', 4: "dcsdl", 5: "auto"}, value=5).props('inline')
        radio2 = ui.radio({1: 'user + pass', 2: 'oauth', 3: 'cookies', 4: "cookies from browser", 5: "none"}, value=5).props('inline')
        j = ui.input(placeholder='output folder...').classes('w-full')
        radio3 = ui.radio({1: 'trash', 2: 'low', 3: 'medium', 4: "high", 5: "ultra-high"}, value=3).props('inline')
        debug_mode = ui.checkbox('debug mode')

        def start_download():
            downloader_map = {1: "yt-dlp", 2: "gallery-dl", 3: "instaloader", 4: "dcsdl", 5: "auto"}
            downloader = downloader_map.get(radio.value, "auto")
            run.io_bound(run_download, downloader, i.value, j.value, radio3.value, console)

        def see_formats():
            url = i.value
            if not url:
                ui.notify("Enter a URL first")
                return
            run.io_bound(run_command_and_stream, ["yt-dlp", "-F", url], console)

        ui.button('start download').props('color=primary').on('click', start_download)
        ui.button('clear').props('color=primary').on('click', lambda: i.set_value('') or j.set_value(''))
        ui.button('see formats').props('color=primary').on('click', see_formats)

    with ui.expansion('update download', icon='sym_r_download_for_offline').classes('w-full'):
        folder4 = ui.input(placeholder="/path/to/folder/").classes('w-full')

    ui.button('update software').props('color=primary').on('click', lambda: realupdate(console))
    ui.button('check versions').props('color=primary').on('click', lambda: checkver())

    with ui.footer().style('background-color: #3874c8'):
        ui.label('© 2025 oofybruh9. Licensed under the GPLv3.').style('text-align: center; color: white; width: 100%')

    ui.run(port=8343, title="DCMD", reload=True, show=False)


if __name__ in {"__main__", "__mp_main__"}:
    start()
    ui.run(port=8343, title="DCMD", reload=True, show=False)
