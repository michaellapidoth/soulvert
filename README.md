# soulvert

**Convert freshly downloaded albums and import them into Music.app.**

`soulvert` is a command-line tool for macOS that automates the steps of music acquisition: converting lossless files to ALAC, and importing the result into the native Music.app — ready to sync across your devices.

You supply an artist or album name; it uses `soulseek-cli` to download the album, optionally converts FLAC to ALAC, and then adds the album to your Music library.

---

## Features

- Download albums from Soulseek via the excellent [`soulseek-cli`](https://github.com/aeyoll/soulseek-cli)
- Convert FLAC to ALAC (`.m4a`) using `ffmpeg`
- Automatically imports the result into macOS Music.app
- Remembers your preferred downloads folder

---

## Requirements

Make sure the following are installed:

- **Python ≥ 3.9**
- **`soulseek-cli`**  
  → Install from [https://github.com/aeyoll/soulseek-cli](https://github.com/aeyoll/soulseek-cli)

- **`ffmpeg`** (for audio conversion)  
  ```bash
  brew install ffmpeg
  ```

---

## Installation

```bash
git clone https://github.com/michaellapidoth/soulvert.git
cd soulvert

python3 -m venv .venv
source .venv/bin/activate

pip install -e .
```

To install system-wide use pipx
```bash
brew install pipx
```
then restart your terminal and and while in the soulvert root run
```bash
pipx install --editable .
```
This will build and install soulvert as a global command.

---

## Usage

- `soulvert init` will prompt you to set your download folder, will log you into soulvert and will save your config under ~/.config/soulvert/config.json .
- `soulvert run -f [option] "[query]" will download and import the album to mac music. the options are mp3 or flac, with flac being converted to alac using ffmpeg.

e.g.
```bash
soulvert run -f flac "Brian Eno Apollo"
soulvert run -f mp3 "Lucki Flawless Like Me"
```

---

## Disclaimer

This tool is intended only for converting and organizing music you legally own. Please respect artists’ rights and applicable copyright laws in your country.

---

## License

Released under the MIT License.
