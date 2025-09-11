from nicegui import ui
import webview
import threading
import os

os.environ["GDK_BACKEND"] = "x11"
os.environ["PYWEBVIEW_GUI"] = "gtk"   # or "qt"
os.environ["WEBKIT_DISABLE_COMPOSITING_MODE"] = "1"
os.environ["WEBKIT_DISABLE_ACCELERATED_2D_CANVAS"] = "1"
ui.label('Hello NiceGUI!')
def func1():
    ui.run(port=8343, title="DCMD", reload=False, show=False)
def main(arg):
    if arg == "gui":
        t = threading.Thread(target=func1, daemon=True)
        t.start()
        window = webview.create_window('DCMD', 'http://localhost:8343')
        webview.start()
        return
    elif arg == "web":
        ui.run(port=8343, title="DCMD", reload=False, show=True)
        return
    else:
        print("Invalid argument for webui. Use 'gui' or 'web'.")
        return 1
if __name__ == '__main__':
    main()
