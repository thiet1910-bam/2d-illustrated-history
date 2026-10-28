#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ziro-History-Studio-v3 — Peak-Zoom Visual QA Sheet Builder & A/V Stream Sync Verifier
Usage:
  python engine/build_qa_sheet.py --episode EP01_Demo --cluster cum_01_Hoi_I --capture
"""
import argparse
import json
import math
import subprocess
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STUDIO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bins import resolve_ffprobe


def get_ffprobe() -> str:
    return resolve_ffprobe()


def load_font(size: int):
    for candidate in (
        "C:/Windows/Fonts/segoeuib.ttf",
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/segoeui.ttf",
    ):
        if Path(candidate).exists():
            return ImageFont.truetype(candidate, size)
    return ImageFont.load_default()


def main():
    parser = argparse.ArgumentParser(description="Build 3-Column Peak-Zoom QA Contact Sheet & Verify A/V Sync")
    parser.add_argument("--episode", required=True, help="Episode ID (e.g. EP01_Demo)")
    parser.add_argument("--cluster", required=True, help="Cluster ID (e.g. cum_01_Hoi_I)")
    parser.add_argument("--capture", action="store_true", help="Invoke render.js --peaks to capture fresh PNGs first")
    args = parser.parse_args()

    tl_path = STUDIO_ROOT / "episodes" / args.episode / "2_assets" / "timelines" / f"timeline_{args.cluster}.json"
    if not tl_path.exists():
        print(f"[FAIL] Missing timeline JSON: {tl_path}")
        sys.exit(1)

    tl = json.loads(tl_path.read_text(encoding="utf-8"))
    beats = tl.get("beats", [])

    cues_path = STUDIO_ROOT / "episodes" / args.episode / "3_scenes" / f"cues_{args.cluster}.json"
    cues_cfg = json.loads(cues_path.read_text(encoding="utf-8")) if cues_path.exists() else {}

    custom_peaks = cues_cfg.get("qa_peaks")
    if custom_peaks and len(custom_peaks) == len(beats):
        peak_times = [round(float(x), 2) for x in custom_peaks]
    else:
        # Default to 82% into each beat (where climax stamps, zoom, and full cards have settled)
        peak_times = [round(float(b["t0"]) + float(b["duration"]) * 0.82, 2) for b in beats]

    peaks_dir = STUDIO_ROOT / ".cache" / args.episode / args.cluster / "peaks"
    if args.capture or not (peaks_dir / "peak_01.png").exists():
        if peaks_dir.exists():
            for old_png in peaks_dir.glob("peak_*.png"):
                old_png.unlink()
        peaks_arg = ",".join(f"{t:.2f}" for t in peak_times)
        subprocess.run(
            [
                "node", str(STUDIO_ROOT / "engine" / "render.js"),
                "--episode", args.episode,
                "--cluster", args.cluster,
                "--peaks", peaks_arg,
            ],
            cwd=str(STUDIO_ROOT),
            check=True,
        )

    png_files = sorted(peaks_dir.glob("peak_*.png"))
    if not png_files:
        print(f"[FAIL] No peak PNG frames found in {peaks_dir}")
        sys.exit(1)

    cols = 3
    rows = math.ceil(len(png_files) / cols)
    thumb_w, thumb_h = 640, 360
    pad = 16
    header_h = 34
    title_h = 58

    sheet_w = cols * thumb_w + (cols + 1) * pad
    sheet_h = title_h + rows * (thumb_h + header_h) + (rows + 1) * pad

    sheet = Image.new("RGB", (sheet_w, sheet_h), (18, 21, 28))
    draw = ImageDraw.Draw(sheet)
    title_font = load_font(24)
    label_font = load_font(17)

    draw.text(
        (pad, 16),
        f"ZIRO-HISTORY-STUDIO-V3 • PEAK-ZOOM QA SHEET • {args.episode} / {args.cluster} ({len(png_files)} BEATS)",
        fill=(250, 204, 21),
        font=title_font,
    )

    for idx, png_path in enumerate(png_files):
        r, c = divmod(idx, cols)
        x = pad + c * (thumb_w + pad)
        y = title_h + pad + r * (thumb_h + header_h + pad)

        t_val = peak_times[idx] if idx < len(peak_times) else 0.0
        seg_id = beats[idx]["segment_id"] if idx < len(beats) else "?"
        draw.rectangle([x, y, x + thumb_w, y + header_h], fill=(30, 41, 59))
        draw.text(
            (x + 10, y + 7),
            f"BEAT {idx + 1:02d} (Seg {seg_id})  |  Peak @ {t_val:06.2f}s",
            fill=(248, 250, 252),
            font=label_font,
        )

        with Image.open(png_path) as im:
            thumb = im.convert("RGB").resize((thumb_w, thumb_h), Image.Resampling.LANCZOS)
            sheet.paste(thumb, (x, y + header_h))
        draw.rectangle([x, y, x + thumb_w, y + header_h + thumb_h], outline=(71, 85, 105), width=2)

    out_qa = STUDIO_ROOT / "episodes" / args.episode / "4_output" / "qa" / f"verify_peak_zoom_{args.cluster}.png"
    out_qa.parent.mkdir(parents=True, exist_ok=True)
    sheet.save(out_qa, format="PNG", optimize=True)
    print(f"[QA SHEET PASS] {len(png_files)} panels stitched -> {out_qa}")

    # Optional: Verify rendered MP4 A/V sync if cluster MP4 already exists
    mp4_path = STUDIO_ROOT / "episodes" / args.episode / "4_output" / "clusters" / f"{args.cluster}.mp4"
    if mp4_path.exists():
        probe_out = subprocess.check_output(
            [
                get_ffprobe(), "-v", "error",
                "-show_entries", "stream=codec_type,codec_name,width,height,duration",
                "-of", "json", str(mp4_path),
            ],
            text=True,
        )
        streams = json.loads(probe_out).get("streams", [])
        v_s = next((s for s in streams if s.get("codec_type") == "video"), None)
        a_s = next((s for s in streams if s.get("codec_type") == "audio"), None)
        if v_s and a_s:
            v_dur = float(v_s.get("duration", 0))
            a_dur = float(a_s.get("duration", 0))
            drift = abs(v_dur - a_dur)
            status = "PASS" if drift <= 0.08 else "WARN"
            print(
                f"[MP4 STREAM {status}] {mp4_path.name}: {v_s.get('width')}x{v_s.get('height')} "
                f"video={v_dur:.3f}s | audio={a_dur:.3f}s | drift={drift*1000:.1f}ms"
            )


if __name__ == "__main__":
    main()
