from pathlib import Path
import os
import sys
import importlib.util

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

def main(argv) -> int:
    """
    Accept either:
      - a list like sys.argv[1:] (preferred for CLI), or
      - an object with attributes .plugin and .args (legacy callers/tests).
    """
    # normalize input
    if isinstance(argv, list):
        if not argv:
            console.print(Panel("[red]Usage:[/red] plugin <plugin-name> [args...]", title="Usage"))
            return 1
        plugin_name = argv[0]
        plugin_args = argv[1:]
    else:
        # support namespace-like objects (argparse Namespace)
        plugin_name = getattr(argv, "plugin", None)
        plugin_args = getattr(argv, "args", [])
        if not plugin_name:
            console.print(Panel("[red]Usage:[/red] plugin <plugin-name> [args...]", title="Usage"))
            return 1

    local_path = Path("plugins") / f"{plugin_name}.py"
    config_path = get_plugins_dir() / f"{plugin_name}.py"

    if local_path.exists():
        source = local_path
        origin = "local ./plugins"
    elif config_path.exists():
        source = config_path
        origin = str(config_path)
    else:
        console.print(
            Panel(
                f"[red]Plugin '{plugin_name}' not found.[/red]\nSearched:\n• {local_path}\n• {config_path}",
                title="Plugin not found",
                border_style="red",
            )
        )
        return 1

    header = Table.grid()
    header.add_column()
    header.add_row(f"[bold green]Loading plugin[/bold green] [yellow]{plugin_name}[/yellow]")
    header.add_row(f"[dim]Source: {origin}[/dim]")
    console.print(Panel(header, border_style="blue"))

    try:
        module = load_plugin_module(source)
    except Exception as e:
        console.print(Panel(f"[red]Failed to load plugin:[/red] {e}", title="Load error", border_style="red"))
        return 2

    if not hasattr(module, "main"):
        console.print(Panel("[red]Plugin missing required function: main(args)[/red]", title="Invalid plugin", border_style="red"))
        return 3

    try:
        # If plugin expects parsed args, pass as-is; otherwise pass list
        module.main(plugin_args)
        console.print(Panel(f"[green]Plugin '{plugin_name}' executed successfully.[/green]", border_style="green"))
    except Exception as e:
        console.print(Panel(f"[red]Error executing plugin:[/red] {e}", title="Execution error", border_style="red"))
        return 4

if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))