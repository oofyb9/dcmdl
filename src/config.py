from __future__ import annotations
import os
import json
import tempfile
from pathlib import Path
from typing import Any, Dict, Optional

try:
    import yaml  # type: ignore
except Exception:
    yaml = None  # YAML support optional

DEFAULT_CONFIG: Dict[str, Any] = {
    "color_scheme": {
        "primary": "cyan",
        "accent": "yellow",
        "background": "black",
        "text": "white",
    },
    "formats": {
        "video": "mp4",
        "audio": "mp3",
        "image": "jpg",
    },
    "debug": False,
    "default_output_name": "%(title)s.%(ext)s",
    "default_quality": "best",
    "release_channel": "stable",  # "stable" or "beta"
}

CONFIG_FILENAMES = ("config.yaml", "config.yml", "config.json")


def get_config_dir() -> Path:
    if os.name == "nt":
        appdata = os.getenv("APPDATA")
        base = Path(appdata) if appdata else Path.home() / "AppData" / "Roaming"
        return base / "dcmdl"
    return Path.home() / ".config" / "dcmdl"


def _detect_existing_file(config_dir: Path) -> Optional[Path]:
    for name in CONFIG_FILENAMES:
        p = config_dir / name
        if p.exists():
            return p
    return None


def _read_json(path: Path) -> Dict[str, Any]:
    with path.open("r", encoding="utf-8") as fh:
        return json.load(fh)


def _write_json(path: Path, data: Dict[str, Any]) -> None:
    tmp = Path(tempfile.mkstemp(prefix=path.name, dir=str(path.parent))[1])
    with tmp.open("w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=2, ensure_ascii=False)
    tmp.replace(path)


def _read_yaml(path: Path) -> Dict[str, Any]:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed")
    with path.open("r", encoding="utf-8") as fh:
        return yaml.safe_load(fh) or {}


def _write_yaml(path: Path, data: Dict[str, Any]) -> None:
    if yaml is None:
        raise RuntimeError("PyYAML is not installed")
    tmp = Path(tempfile.mkstemp(prefix=path.name, dir=str(path.parent))[1])
    with tmp.open("w", encoding="utf-8") as fh:
        yaml.safe_dump(data, fh, sort_keys=False)
    tmp.replace(path)


def load_config() -> Dict[str, Any]:
    """
    Load config. If none exists, write defaults to config.yaml (if PyYAML available)
    or config.json and return defaults.
    """
    cfg_dir = get_config_dir()
    cfg_dir.mkdir(parents=True, exist_ok=True)

    existing = _detect_existing_file(cfg_dir)
    if existing:
        if existing.suffix in (".yml", ".yaml"):
            try:
                return _read_yaml(existing)
            except Exception:
                return DEFAULT_CONFIG.copy()
        else:
            try:
                return _read_json(existing)
            except Exception:
                return DEFAULT_CONFIG.copy()

    # no existing file: create default
    target = cfg_dir / ("config.yaml" if yaml is not None else "config.json")
    save_config(DEFAULT_CONFIG.copy(), path=target)
    return DEFAULT_CONFIG.copy()


def save_config(config: Dict[str, Any], path: Optional[Path] = None, fmt: Optional[str] = None) -> Path:
    """
    Save config dict. If path provided it will be used. Otherwise write to detected path
    or default (config.yaml if PyYAML available else config.json).
    fmt can be 'json' or 'yaml' to force format when path not provided.
    Returns the path written to.
    """
    cfg_dir = get_config_dir()
    cfg_dir.mkdir(parents=True, exist_ok=True)

    if path is None:
        if fmt is None:
            fmt = "yaml" if yaml is not None else "json"
        filename = "config.yaml" if fmt == "yaml" else "config.json"
        path = cfg_dir / filename

    path.parent.mkdir(parents=True, exist_ok=True)

    if path.suffix in (".yml", ".yaml") or (fmt == "yaml" and path.suffix == ""):
        _write_yaml(path, config)
    else:
        _write_json(path, config)

    return path


def update_config(updates: Dict[str, Any]) -> Path:
    """
    Shallow-merge updates into existing config and save.
    """
    current = load_config()
    current.update(updates)
    return save_config(current)


# simple CLI for inspection / editing
def cli_main(argv: Optional[list[str]] = None) -> int:
    import argparse

    parser = argparse.ArgumentParser(prog="dcmdl-config")
    parser.add_argument("--show", action="store_true", help="Print current config")
    parser.add_argument("--export-json", metavar="PATH", help="Write config as JSON to PATH")
    parser.add_argument("--export-yaml", metavar="PATH", help="Write config as YAML to PATH (requires PyYAML)")
    parser.add_argument("--set", nargs=2, action="append", metavar=("KEY", "VALUE"), help="Set top-level key")
    args = parser.parse_args(argv)

    cfg = load_config()

    if args.set:
        for k, v in args.set:
            # naive type handling for booleans and numbers
            if v.lower() in ("true", "false"):
                parsed: Any = v.lower() == "true"
            else:
                try:
                    parsed = int(v)
                except Exception:
                    try:
                        parsed = float(v)
                    except Exception:
                        parsed = v
            cfg[k] = parsed
        save_config(cfg)
        print("Saved config.")
        return 0

    if args.export_json:
        p = Path(args.export_json)
        _write_json(p, cfg)
        print(f"Exported to {p}")
        return 0

    if args.export_yaml:
        if yaml is None:
            print("PyYAML not installed")
            return 2
        p = Path(args.export_yaml)
        _write_yaml(p, cfg)
        print(f"Exported to {p}")
        return 0

    if args.show:
        print(json.dumps(cfg, indent=2, ensure_ascii=False))
        return 0

    parser.print_help()
    return 1


if __name__ == "__main__":
    raise SystemExit(cli_main())