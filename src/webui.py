from nicegui import ui, html
import random
def start():
    with open(r'console_quotes.txt', "r") as f:
        l = [line.rstrip() for line in f]
        print(l)
    with open(r'console_quotes.txt', "r") as fi:
        lines = len(fi.readlines())
        print(lines)
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
    height: 10%;
}
            """)
    ui.markdown("""
    # DCMD WebUI
    """)
    with ui.expansion('new download', icon='sym_r_download').classes('w-full'):
        ui.label('new download')
        i = ui.input(placeholder='enter url here...').classes('w-full')
        ui.label('select downloader')
        radio = ui.radio({1: 'yt-dlp', 2: 'gallery-dl', 3: 'instaloader', 4: "dcsdl", 5: "auto"}, value=5).props('inline')
        ui.label('select auth method')
        radio2 = ui.radio({1: 'user + pass', 2: 'oauth', 3: 'cookies', 4: "cookies from browser", 5: "none"}, value=5).props('inline')
        j = ui.input(placeholder='output folder and styling...').classes('w-full')
        ui.label('select quality')
        radio3 = ui.radio({1: 'trash', 2: 'low', 3: 'medium', 4: "high", 5: "ultra-high"}, value=3).props('inline')
        debug_mode = ui.checkbox('debug mode')
        ui.button('start download').props('color=primary').on('click', lambda: print(i.value, radio.value, radio2.value, j.value, radio3.value, debug_mode.value))
        ui.button('clear').props('color=primary').on('click', lambda: i.set_value('') or j.set_value(''))
        ui.button('see formats').props('color=primary')
    with ui.expansion('continue', icon='sym_r_downloading').classes('w-full'):
        ui.label('continue download')
    with ui.expansion('update download', icon='sym_r_download_for_offline').classes('w-full'):
        ui.label('update download')
    ui.button('update software').props('color=primary').on('click', lambda: ui.notify('updating... (not really, this is just a demo)'))
    ui.button('check versions').props('color=primary').on('click', lambda: ui.notify('yt-dlp: 2024.06.06, gallery-dl: 1.28.3, instaloader: 4.9.6, dcsdl: 0.3.5, dcmd: 0.1.0-beta-really-unstable-do-not-use-it-cuz-it-will-break-everything'))
    html.div(l[num]).classes('konsole')
    with ui.footer().style('background-color: #3874c8'):
            ui.label('© 2025 oofybruh9. Licensed under the GPLv3.').style('text-align: center; color: white; width: 100%')
    ui.run(port=8343, title="DCMD", reload=True, show=False)

if __name__ in {"__main__", "__mp_main__"}:  # ✅ works with multiprocessing too
    start()
    ui.run(port=8343, title="DCMD", reload=True, show=False)