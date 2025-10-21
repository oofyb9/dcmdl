import requests, os,sys, platform
from pathlib import Path
from typing import Optional, Dict, List
from rich.prompt import Confirm
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
from rich.markdown import Markdown
console = Console()
def fetch_plugin_metadata(name: str) -> Optional[Dict]:
    url = f"https://raw.githubusercontent.com/oofybruh9/dcmdl-plugins/refs/heads/main/plugins/{name}.json"
    with console.status(f"[cyan]Fetching metadata for [bold]{name}[/bold]...", spinner="dots"):
        try:
            resp = requests.get(url, timeout=10)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 404:
                console.print(f"[red]Plugin '{name}' not found (404).")
                return None
            console.print(f"[red]Failed to fetch metadata: HTTP {resp.status_code}")
            return None
        except requests.RequestException as e:
            console.print(f"[red]Request error: {e}")
            return None
def show_metadata(data: Dict) -> None:
    table = Table.grid(expand=True)
    table.add_column(ratio=1)
    table.add_column(ratio=3)
    table.add_row("[bold]Title[/bold]", f"{data.get('title', '[unknown]')}")
    table.add_row("[bold]Author[/bold]", f"{data.get('author', '[unknown]')}")
    table.add_row("[bold]Version[/bold]", f"{data.get('version', '[unknown]')}")
    table.add_row("[bold]Download[/bold]", f"{data.get('download', '[none]')}")
    desc = data.get("description", "")
    panel = Panel.fit(Markdown(desc), title="Description", border_style="bright_blue")
    console.print(table)
    console.print(panel)
def download_with_progress(urls: List[str], out_path: Path) -> bool:
    out_path.parent.mkdir(parents=True, exist_ok=True)
    for url in urls:
        if not url:
            continue
        try:
            with requests.get(url, stream=True, timeout=15) as r:
                r.raise_for_status()
                total = int(r.headers.get("content-length", 0)) or None
                desc = f"Downloading from {url}"
                with Progress(SpinnerColumn(), TextColumn("[progress.description]{task.description}"), BarColumn()) as progress:
                    task = progress.add_task(desc, total=total)
                    with open(out_path, "wb") as f:
                        for chunk in r.iter_content(chunk_size=8192):
                            if not chunk:
                                continue
                            f.write(chunk)
                            progress.update(task, advance=len(chunk))
                console.print(f"[green]Saved to[/green] {out_path}")
                return True
        except requests.RequestException as e:
            console.print(f"[yellow]Download failed from:[/yellow] {url} — {e}")
            continue
    return False
def install_plugin(name: str, metadata: Dict, update: bool) -> int:
    download_candidates = [
        metadata.get("download"),
        metadata.get("download-mirror2"),
        metadata.get("download-mirror3"),
    ]
    safe_name = Path(name).stem

    if update:
        msg = "Update"
        msgs = "Updating"
        msgin = "Updated"
        msged = "Update"
    else:
        msg = "Install"
        msgs = "Installing"
        msgin = "Installed"
        msged = "Installation"

    # OS-specific config directory
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        base_dir = Path(appdata) if appdata else (Path.home() / "AppData" / "Roaming")
        config_dir = base_dir / "dcmdl" / "plugins"
    else:
        config_dir = Path.home() / ".config" / "dcmdl" / "plugins"

    out_path = config_dir / f"{safe_name}.py"

    confirm = Confirm.ask(f"{msg} plugin [bold]{metadata.get('title', safe_name)}[/bold]?")
    if not confirm:
        console.print(f"[red]{msged} cancelled.[/red]")
        return 1

    console.print("[cyan]Attempting download...[/cyan]")
    success = download_with_progress(download_candidates, out_path)
    if success:
        console.print(f"[green]Plugin '{safe_name}' {msgin} successfully at[/green] {out_path}")
        return 0

    console.print(f"[red]All download attempts failed for '{safe_name}'.[/red]")
    return 2

def install_plgn(name: str) -> int:
    if not name:
        console.print("[red]Invalid plugin name.[/red]")
        return 1
    metadata = fetch_plugin_metadata(name)
    if metadata is None:
        return 1
    show_metadata(metadata)
    return install_plugin(name, metadata, False)

def rm_plgn(name: str) -> int:
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        base_dir = Path(appdata) if appdata else (Path.home() / "AppData" / "Roaming")
        config_dir = base_dir / "dcmdl" / "plugins"
    else:
        config_dir = Path.home() / ".config" / "dcmdl" / "plugins"

    plugin_path = config_dir / f"{name}.py"
    if not plugin_path.exists():
        console.print(f"[red]Plugin '{name}' not found at {plugin_path}.[/red]")
        return 1

    confirm = Confirm.ask(f"Are you sure you want to remove plugin '{name}'?")
    if not confirm:
        console.print("[red]Removal cancelled.[/red]")
        return 1

    try:
        plugin_path.unlink()
        console.print(f"[green]Plugin '{name}' removed successfully.[/green]")
        return 0
    except Exception as e:
        console.print(f"[red]Failed to remove plugin '{name}': {e}[/red]")
        return 1

def list_plgn() -> int:
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        base_dir = Path(appdata) if appdata else (Path.home() / "AppData" / "Roaming")
        config_dir = base_dir / "dcmdl" / "plugins"
    else:
        config_dir = Path.home() / ".config" / "dcmdl" / "plugins"

    if not config_dir.exists():
        console.print("[yellow]No plugins directory found.[/yellow]")
        return 0

    plugins = [p.stem for p in config_dir.glob("*.py")]
    if not plugins:
        console.print("[yellow]No plugins installed.[/yellow]")
        return 0

    table = Table(title="Installed Plugins")
    table.add_column("Plugin Name", style="cyan", no_wrap=True)

    for plugin in plugins:
        table.add_row(plugin)

    console.print(table)
    return 0

def update_plgn(name: str) -> int:
    if not name:
        console.print("[red]Invalid plugin name.[/red]")
        return 1
    metadata = fetch_plugin_metadata(name)
    if metadata is None:
        return 1
    show_metadata(metadata)
    return install_plugin(name, metadata, True)

def main(argv: List[str]) -> int:
    print(argv)
    if argv.action == "install":
        return install_plgn(argv.plugin)
    elif argv.action == "remove":
        return rm_plgn(argv.plugin)
    elif argv.action == "list":
        return list_plgn()
    elif argv.action == "update":
        return update_plgn(argv.plugin)
    else:
        console.print("[red]Unknown action.[/red]")
        return 1
if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
