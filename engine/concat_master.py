#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ziro-History-Studio-v3 — Lossless Zero-Reencode Master Episode Concatenator
Stitches all rendered cluster MP4s (episodes/<ep>/4_output/clusters/cum_*.mp4)
into episodes/<ep>/4_output/master/<ep>_Master.mp4 via ffmpeg -f concat -c copy.
"""
import argparse
import json
import subprocess
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STUDIO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bins import resolve_ffmpeg, resolve_ffprobe


def get_bins() -> tuple:
    return resolve_ffmpeg(), resolve_ffprobe()


def main():
    parser = argparse.ArgumentParser(description="Concatenate cluster MP4s into a seamless Master Episode MP4")
    parser.add_argument("--episode", required=True, help="Episode ID (e.g. EP01_Demo)")
    args = parser.parse_args()

    ffmpeg, ffprobe = get_bins()
    clusters_dir = STUDIO_ROOT / "episodes" / args.episode / "4_output" / "clusters"
    mp4_files = sorted(clusters_dir.glob("cum_*.mp4"))
    if not mp4_files:
        print(f"[FAIL] No cluster MP4 files found in {clusters_dir}")
        sys.exit(1)

    cache_dir = STUDIO_ROOT / ".cache" / args.episode
    cache_dir.mkdir(parents=True, exist_ok=True)
    concat_txt = cache_dir / "concat_list.txt"

    lines = []
    for p in mp4_files:
        safe_p = str(p.resolve()).replace("\\", "/").replace("'", "'\\''")
        lines.append(f"file '{safe_p}'")
    concat_txt.write_text("\n".join(lines) + "\n", encoding="utf-8")

    master_dir = STUDIO_ROOT / "episodes" / args.episode / "4_output" / "master"
    master_dir.mkdir(parents=True, exist_ok=True)
    out_master = master_dir / f"{args.episode}_Master.mp4"

    subprocess.run(
        [
            ffmpeg, "-hide_banner", "-loglevel", "error", "-y",
            "-f", "concat", "-safe", "0",
            "-i", str(concat_txt),
            "-c", "copy", "-movflags", "+faststart",
            str(out_master),
        ],
        check=True,
    )

    probe = subprocess.check_output(
        [ffprobe, "-v", "error", "-show_entries", "format=duration,size", "-of", "json", str(out_master)],
        text=True,
    )
    fmt = json.loads(probe).get("format", {})
    dur = float(fmt.get("duration", 0))
    mb = int(fmt.get("size", 0)) / (1024 * 1024)
    print(f"[MASTER CONCAT PASS] Stitched {len(mp4_files)} clusters -> {out_master} ({dur:.2f}s | {mb:.2f} MB)")


if __name__ == "__main__":
    main()
