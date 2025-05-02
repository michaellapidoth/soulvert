#!/usr/bin/env bash
# download_album.sh
# Called by soulvert. Accepts:
#   --format mp3|flac   (required)
#   --output DIR        (required, absolute path from soulvert)
#   <search query …>    (one or more words / URL)

set -euo pipefail

FORMAT=""          # mp3 or flac
OUTDIR=""          # where the finished album must land
QUERY=()           # collects all search words

# ---------- argument loop ----------
while [[ $# -gt 0 ]]; do
  case "$1" in
    --format|-f)
      FORMAT="$2"; shift 2 ;;
    --output)
      OUTDIR="$2"; shift 2 ;;
    --)                   # end‑of‑options marker
      shift
      QUERY+=("$@")
      break ;;
    *)
      QUERY+=("$1"); shift ;;
  esac
done

# ---------- sanity checks ----------
[[ -z $FORMAT ]] && { echo "need --format mp3|flac" >&2; exit 1; }
[[ -z $OUTDIR  ]] && { echo "need --output <folder>" >&2; exit 1; }
[[ ${#QUERY[@]} -eq 0 ]] && { echo "no search query given" >&2; exit 1; }

SEARCH="${QUERY[*]}"

echo "Format      : $FORMAT"
echo "Output dir  : $OUTDIR"
echo "Search query: $SEARCH"

###############################################################################
# 1. Download to a temp dir (avoids half‑finished folders in $OUTDIR)
###############################################################################
tmp=$(mktemp -d)
soulseek download -d "$tmp" -m "$FORMAT" "$SEARCH"

album_dir=$(find "$tmp" -mindepth 1 -maxdepth 1 -type d | head -n 1)
[[ -z $album_dir ]] && { echo "no album folder produced" >&2; exit 1; }

if [[ -d "$OUTDIR/$(basename "$album_dir")" ]]; then
  echo "Destination exists, renaming..."
  timestamp=$(date +%s)
  mv "$album_dir" "$OUTDIR/$(basename "$album_dir")-$timestamp"
else
  mv "$album_dir" "$OUTDIR/"
fi

rmdir "$tmp"