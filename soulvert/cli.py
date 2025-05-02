import sys, subprocess, pathlib, time, json, shutil
import click
from rich.console import Console
from importlib.resources import files

CFG = pathlib.Path.home() / ".config" / "soulvert" / "config.json"
console = Console()

# ---------- helpers ----------
def load_cfg():
    if CFG.exists():
        return json.loads(CFG.read_text())
    console.print("[red]Run `soulvert init` first.[/]")
    sys.exit(1)

def save_cfg(d):
    CFG.parent.mkdir(parents=True, exist_ok=True)
    CFG.write_text(json.dumps(d, indent=2))

def newest_subdir(root: pathlib.Path):
    return max((p for p in root.iterdir() if p.is_dir()), key=lambda p: p.stat().st_mtime)

def convert_flac_to_alac(folder: pathlib.Path):
    for f in folder.rglob("*.flac"):
        alac = f.with_suffix(".m4a")
        console.print(f"[cyan]ffmpeg:[/] {f.name} → {alac.name}")
        subprocess.run(["ffmpeg", "-loglevel", "error", "-y", "-i", str(f), "-vn", "-c:a", "alac", str(alac)], check=True)
        f.unlink()

def import_to_music(folder: pathlib.Path):
    osa = f'tell application "Music" to add POSIX file "{folder}"'
    subprocess.run(["osascript", "-e", osa], check=True)
    console.print(f"[green]Imported[/] {folder.name}")

# ---------- CLI ----------
@click.group()
def cli():
    """Convert & import freshly‑downloaded albums."""
    ...

@cli.command()
def init():
    dl_root = click.prompt(
        "Folder where new albums appear",
        default=pathlib.Path("~/Music/soulvert").expanduser(),
        type=pathlib.Path,
    )
    save_cfg({"download_root": str(dl_root)})
    console.print(f"[green]Config saved[/] → {CFG}")
    console.print("[yellow]Running initial soulseek login")
    subprocess.run(["soulseek", "login"], check=True)


@cli.command(context_settings=dict(ignore_unknown_options=True))
@click.option(
    "-f", "--format", "fmt",
    type=click.Choice(["mp3", "flac"]),
    default="mp3",
    help="Ask the downloader for MP3 or FLAC.",
)
@click.argument("query", nargs=-1, required=True)
def run(fmt, query):
    cfg = load_cfg()
    dl_root = pathlib.Path(cfg["download_root"]).expanduser()

    script = files("soulvert.scripts").joinpath("download_album.sh")
    if not script.exists():
        console.print("[red]Bundled downloader missing![/]")
        sys.exit(1)

    cmd = [
        str(script),
        "--format", fmt,
        "--output", str(dl_root),
        *query
    ]
    console.print(f"[yellow]-> running:[/] {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

    time.sleep(1)
    album_dir = newest_subdir(dl_root)
    console.print(f"[blue]Latest folder:[/] {album_dir}")

    if fmt == "flac":
        convert_flac_to_alac(album_dir)

    import_to_music(album_dir)

if __name__ == "__main__":
    cli()
