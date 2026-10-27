#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 4.2 & 4.4: 2-Pass Camera & Post-Camera Kinetic Stage Typography (`camera_2pass_renderer.py`)
------------------------------------------------------------------------------------------------
Enforces strict separation between:
  - PASS 1 (World Stage + Viewport Safe-Box + Camera Crop/Zoom/Pan)
  - PASS 2 (Post-Camera Frameless Kinetic Stage Title at y_center >= 115px)
Eliminates all metadata clutter (no `PHÂN ĐOẠN X.Y` badges, no `ZIRO HOST` footplates,
no bottom Karaoke subtitle boxes) and matches Ziro History's organic stage typography.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from PIL import Image, ImageDraw

ENGINE_DIR = Path(__file__).resolve().parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

from ziro_stage_components import (
    W,
    H,
    INK,
    clamp01,
    ease_in_out_cubic,
    draw_kinetic_text,
    draw_stamp,
    render_stage_pass1,
)


def compute_camera_window(beat_data: dict, bt: float):
    """
    Computes instantaneous (zoom, pan_x, crop_box, world_safe_box) at local time `bt`.
    `world_safe_box` is the exact world-space rectangle that maps to screen-space
    `[85..1835] x [165..1030]` AFTER camera crop and zoom!
    """
    dur = max(0.1, float(beat_data.get("duration", 5.0)))
    cam = beat_data.get("camera", {})
    z0 = float(cam.get("zoom_start", 1.0))
    z1 = float(cam.get("zoom_end", 1.08))
    px0 = float(cam.get("pan_x_start", 0.0))
    px1 = float(cam.get("pan_x_end", 0.0))

    prog = ease_in_out_cubic(clamp01(bt / dur))
    zoom = max(1.0, z0 + (z1 - z0) * prog)
    pan_x = px0 + (px1 - px0) * prog
    pan_y = 0.0

    zw = max(320, int(round(W / zoom)))
    zh = max(180, int(round(H / zoom)))
    cx = int(round(W / 2.0 + pan_x))
    cy = int(round(H / 2.0 + pan_y))

    x0 = max(0, min(W - zw, cx - zw // 2))
    y0 = max(0, min(H - zh, cy - zh // 2))
    crop_box = (x0, y0, x0 + zw, y0 + zh)

    sx0 = x0 + int(round(85.0 / zoom))
    sx1 = x0 + zw - int(round(85.0 / zoom))
    sy0 = y0 + int(round(165.0 / zoom))
    sy1 = y0 + zh - int(round(45.0 / zoom))
    world_safe_box = (sx0, sy0, sx1, sy1)

    return zoom, pan_x, crop_box, world_safe_box


def render_hud_pass2(img: Image.Image, beat_data: dict, bt: float) -> Image.Image:
    """
    PASS 2: Post-Camera Kinetic Stage Typography.
    Drawn strictly in screen coordinates (1920x1080) AFTER Pass 1 camera zoom/pan.
    Uses Ziro-style Frameless Typewriter Reveal (`FRAMELESS_TYPEWRITER`) or `STAMP_HEADER`
    at `y_center >= 115px` with zero metadata badges and zero subtitle boxes.
    """
    hud = beat_data.get("hud_banner", {})
    title_text = (hud.get("text") or hud.get("main_title") or "").strip()
    style = hud.get("style", "FRAMELESS_TYPEWRITER")
    if not title_text or style == "NONE":
        return img

    y_center = max(115, int(hud.get("y_center", 118)))
    lighting = beat_data.get("lighting_mode", "DAYLIGHT_WARM")
    tpl = beat_data.get("scene_template", "")

    if style == "STAMP_HEADER":
        draw_stamp(
            img,
            (960, y_center),
            title_text,
            bg_col=(198, 38, 38),
            size=30,
            pop_t=min(1.0, (bt + 0.1) / 0.35),
            safe_box=(96, 70, W - 96, H - 70),
        )
        return img

    # Default: Frameless Typewriter Stage Title (Organic Ziro Style)
    if lighting == "PRISON_NIGHT" or tpl == "T06_Geopolitics_Map_Spotlight":
        txt_col = (255, 236, 115)
        stroke_col = INK
        stroke_w = 4
    elif "BÊN TRÁI" in title_text.upper() or "1970" in title_text:
        txt_col = (32, 78, 138)
        stroke_col = (245, 245, 242)
        stroke_w = 2
    elif "BÊN PHẢI" in title_text.upper() or "1980" in title_text:
        txt_col = (178, 34, 34)
        stroke_col = (245, 245, 242)
        stroke_w = 2
    else:
        txt_col = INK
        stroke_col = (242, 240, 235)
        stroke_w = 2

    reveal_prog = clamp01((bt + 0.15) / 1.15)
    draw_kinetic_text(
        img,
        (960, y_center),
        title_text,
        size=38,
        color=txt_col,
        stroke_col=stroke_col,
        stroke_w=stroke_w,
        align="center",
        bold=True,
        organic=True,
        prog=reveal_prog,
        safe_box=(96, 65, W - 96, H - 65),
    )
    return img


def render_frame_2pass(
    beat_data: dict,
    bt: float,
    m_code: int = 0,
    high_quality: bool = False,
    episode_id: str = "EP01_Iran",
    workspace_root: Path = None,
) -> Image.Image:
    """
    Executes the full 2-Pass Rendering Pipeline for a single frame:
      Pass 1: Render World Stage inside inverse-projected `world_safe_box`, then apply Camera Crop/Scale.
      Pass 2: Render Post-Camera Frameless Kinetic Stage Title (`y_center >= 115px`).
    """
    zoom, pan_x, crop_box, world_safe_box = compute_camera_window(beat_data, bt)

    world_img = render_stage_pass1(
        beat_data=beat_data,
        bt=bt,
        m_code=m_code,
        safe_box=world_safe_box,
        episode_id=episode_id,
        workspace_root=workspace_root,
    )
    if abs(zoom - 1.0) > 0.002 or abs(pan_x) > 0.5:
        cropped = world_img.crop(crop_box)
        resample = Image.LANCZOS if high_quality else Image.BILINEAR
        stage_post_cam = cropped.resize((W, H), resample)
    else:
        stage_post_cam = world_img

    final_img = render_hud_pass2(stage_post_cam, beat_data, bt)
    return final_img


def get_peak_zoom_timestamp(beat_data: dict) -> float:
    dur = float(beat_data.get("duration", 5.0))
    triggers = beat_data.get("sub_triggers_bt", [])
    last_trig = max([float(t.get("bt", 0.0)) for t in triggers], default=0.0)
    return min(dur - 0.08, max(dur * 0.90, last_trig + 0.65))


def main():
    parser = argparse.ArgumentParser(description="Render Peak-Zoom 2-Pass PNG snapshots for Gate 4 QA.")
    parser.add_argument("--manifest", required=True, help="Path to beat_manifest_<cluster_id>.json")
    parser.add_argument("--out-dir", required=True, help="Directory to output Peak-Zoom PNG snapshots")
    parser.add_argument(
        "--beats",
        nargs="*",
        default=["beat_02", "beat_03", "beat_06", "beat_07", "beat_11"],
        help="Beat IDs to render at Peak-Zoom",
    )
    args = parser.parse_args()

    manifest_path = Path(args.manifest).resolve()
    out_dir = Path(args.out_dir).resolve()
    out_dir.mkdir(parents=True, exist_ok=True)

    workspace_root = manifest_path.parents[4] if len(manifest_path.parents) >= 5 else manifest_path.parent

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    episode_id = manifest.get("episode_id", "EP01_Iran")
    beats_by_id = {b["beat_id"]: b for b in manifest.get("beats", [])}
    report = []

    for bid in args.beats:
        if bid not in beats_by_id:
            continue
        bdata = beats_by_id[bid]
        t_peak = get_peak_zoom_timestamp(bdata)
        zoom, pan_x, crop_box, world_safe_box = compute_camera_window(bdata, t_peak)
        img = render_frame_2pass(
            bdata,
            bt=t_peak,
            m_code=2,
            high_quality=True,
            episode_id=episode_id,
            workspace_root=workspace_root,
        )
        out_png = out_dir / f"peak_zoom_{bid}.png"
        img.save(out_png, "PNG")
        info = {
            "beat_id": bid,
            "scene_template": bdata.get("scene_template"),
            "t_peak_zoom_sec": round(t_peak, 3),
            "duration_sec": round(float(bdata.get("duration", 0.0)), 3),
            "peak_zoom": round(zoom, 4),
            "peak_pan_x": round(pan_x, 2),
            "crop_box": crop_box,
            "world_safe_box": world_safe_box,
            "hud_render_pass": bdata.get("hud_banner", {}).get("render_pass"),
            "hud_style": bdata.get("hud_banner", {}).get("style", "FRAMELESS_TYPEWRITER"),
            "hud_y_center": bdata.get("hud_banner", {}).get("y_center"),
            "png_path": str(out_png),
        }
        report.append(info)
        print(
            f"[PASS 2-PASS PEAK-ZOOM] {bid} ({bdata.get('scene_template')}) "
            f"@ bt={t_peak:.2f}s | zoom={zoom:.3f}x | pan_x={pan_x:.1f}px -> {out_png.name}"
        )

    report_path = out_dir / "peak_zoom_audit_report.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump({"cluster_id": manifest.get("cluster_id"), "snapshots": report}, f, ensure_ascii=False, indent=2)
    print(f"[DONE] Saved {len(report)} Peak-Zoom PNG snapshots and report -> {report_path}")


if __name__ == "__main__":
    main()
