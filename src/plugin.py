from pathlib import Path
import os, sys, importlib.util

from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.traceback import install

install()  # nicer tracebacks in terminal
console = Console()

def get_plugins_dir() -> Path:
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        base = Path(appdata) if appdata else (Path.home() / "AppData" / "Roaming")
        return base / "dcmdl" / "plugins"
    return Path.home() / ".config" / "dcmdl" / "plugins"

def load_plugin_module(path: Path):
    spec = importlib.util.spec_from_file_location(f"plugins.{path.stem}", str(path))
    if spec is None or spec.loader is None:
        raise ImportError(f"Cannot create import spec for {path}")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module

def use_plgn(name: str, args) -> int:
    local_path = Path("plugins") / f"{name}.py"
    config_path = get_plugins_dir() / f"{name}.py"

    if local_path.exists():
        source = local_path
        origin = "local ./plugins"
    elif config_path.exists():
        source = config_path
        origin = str(config_path)
    else:
        console.print(f"[red]Plugin '{name}' not found.[/red]\nSearched:\n• {local_path}\n• {config_path}")
        return 1
    try:
        module = load_plugin_module(source)
    except Exception as e:
        console.print(f"[red]Failed to load plugin:[/red] {e}", title="Load error")
        return 2

    if not hasattr(module, "main"):
        console.print("[red]Plugin missing required function: main(args)[/red]", title="Invalid plugin")
        return 3

    try:
        # If plugin expects parsed args, pass as-is; otherwise pass list
        module.main(args)
        console.print(f"[green]Plugin '{name}' executed successfully.[/green]")
    except Exception as e:
        console.print(f"[red]Error executing plugin:[/red] {e}", title="Execution error")
        return 4

if __name__ == "__main__":
    console.print("[red]This module is not meant to be run directly. Please use 'dcmdl dl --downloader <plugin name here> <other options here> <url here>' command instead.[/red]")