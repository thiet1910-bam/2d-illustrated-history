#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 4.1 & 4.4: Ziro Stage Components & 2x SSAA Character Sprite Engine
-----------------------------------------------------------------------
100% Data-Driven Pass 1 World Stage Renderer:
  - Resolves episode-specific historical photos & satellite maps strictly from
    `2_nguyen_lieu/<episode_id>/tu_lieu_tap/` (zero hardcoded episode filenames).
  - Renders 2x SSAA Ziro characters with Deep Neck-Lock (`neck_insert_px` 28-42px)
    and zero metadata nameplate clutter.
  - Supports Continuous Multi-Beat Stage Progression (`Left 1970 vs Right 1980`),
    Curved Arrows, Cause-to-Prison Flows, Split-Screen Youth vs Clerics, Satellite
    Map Spotlights, and Persian Carpet Metaphor Stages.
"""

import os
import math
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance

W, H = 1920, 1080
INK = (35, 30, 28)
SKIN = (244, 210, 182)

_FONT_CACHE = {}
_SPRITE_CACHE = {}
_IMG_CACHE = {}


def get_font(size: int, bold: bool = True, organic: bool = False) -> ImageFont.FreeTypeFont:
    """
    Returns 100% Vietnamese-Unicode-safe font (`Segoe UI Semibold` / `Segoe UI Bold` / `Calibri Bold`).
    Never uses `comic.ttf` because Windows `comic.ttf` lacks Vietnamese compound diacritics!
    """
    key = (int(size), bool(bold), bool(organic))
    if key not in _FONT_CACHE:
        if organic:
            candidates = [
                r"C:\Windows\Fonts\seguisb.ttf",
                r"C:\Windows\Fonts\calibrib.ttf",
                r"C:\Windows\Fonts\segoeuib.ttf",
            ]
        else:
            candidates = [
                r"C:\Windows\Fonts\segoeuib.ttf" if bold else r"C:\Windows\Fonts\seguisb.ttf",
                r"C:\Windows\Fonts\calibrib.ttf" if bold else r"C:\Windows\Fonts\calibri.ttf",
                r"C:\Windows\Fonts\arialbd.ttf" if bold else r"C:\Windows\Fonts\arial.ttf",
            ]
        for p in candidates:
            if os.path.exists(p):
                _FONT_CACHE[key] = ImageFont.truetype(p, max(10, int(size)))
                break
        if key not in _FONT_CACHE:
            _FONT_CACHE[key] = ImageFont.load_default()
    return _FONT_CACHE[key]


def clamp01(t: float) -> float:
    return max(0.0, min(1.0, float(t)))


def ease_out_cubic(t: float) -> float:
    t = clamp01(t)
    return 1.0 - (1.0 - t) ** 3


def ease_out_back(t: float, s: float = 1.35) -> float:
    t = clamp01(t)
    t -= 1.0
    return t * t * ((s + 1.0) * t + s) + 1.0


def ease_in_out_cubic(t: float) -> float:
    t = clamp01(t)
    return 4 * t * t * t if t < 0.5 else 1.0 - (-2.0 * t + 2.0) ** 3 / 2.0


def resolve_episode_asset(filename: str, episode_id: str = "EP01_Iran", workspace_root: Path = None) -> str:
    """
    Resolves an image asset strictly from the episode's own cluster-partitioned asset folder:
    `2_nguyen_lieu/<episode_id>/tu_lieu_tap/<cluster_id>/<filename>` (or direct relative path).
    """
    if not filename:
        return ""
    search_dirs = []
    if workspace_root:
        ws = Path(workspace_root)
        search_dirs.append(ws / "2_nguyen_lieu" / episode_id / "tu_lieu_tap")
    base_proj = Path(r"e:\02_CHANNEL\thu-nghiem\edit-video\2D-Illustrated-History\Du-an-2D-Illustrated-History")
    search_dirs.append(
        base_proj / "dung-video-lich-su-hoat-hinh-2d" / "2_nguyen_lieu" / episode_id / "tu_lieu_tap"
    )
    base_name = Path(filename).name
    for d in search_dirs:
        if not d.exists():
            continue
        p = d / filename
        if p.exists() and p.is_file():
            return str(p)
        # Also search inside `<cluster_id>/` subdirectories
        for sub in d.iterdir():
            if sub.is_dir():
                p_sub = sub / base_name
                if p_sub.exists() and p_sub.is_file():
                    return str(p_sub)
    return ""


def get_cached_image(filename: str, size=None, episode_id: str = "EP01_Iran", workspace_root: Path = None) -> Image.Image:
    key = (episode_id, filename, size)
    if key in _IMG_CACHE:
        return _IMG_CACHE[key]
    p = resolve_episode_asset(filename, episode_id, workspace_root)
    if p and os.path.exists(p):
        im = Image.open(p).convert("RGB")
        if size:
            im = ImageOps.fit(im, size, method=Image.LANCZOS)
        _IMG_CACHE[key] = im
        return im
    fallback = Image.new("RGB", size or (400, 300), (165, 162, 155))
    return fallback


def draw_thick_line_ss(draw: ImageDraw.ImageDraw, p1, p2, color=INK, width=4.0, ss=2):
    w = max(1, int(round(width * ss)))
    draw.line([p1, p2], fill=color, width=w)
    r = w // 2
    for px, py in (p1, p2):
        draw.ellipse([px - r, py - r, px + r, py + r], fill=color)


# ==============================================================================
# 1. 2X SSAA CHARACTER SPRITE ENGINE WITH DEEP NECK-LOCK (28-42px)
# ==============================================================================
def get_character_sprite(
    role: str = "char_ziro_host",
    emotion: str = "explaining",
    mouth: str = "closed",
    left_arm: str = "down",
    right_arm: str = "point_right",
    prop_right: str = None,
    scale: float = 1.0,
    neck_insert_px: int = 35,
) -> Image.Image:
    key = (role, emotion, mouth, left_arm, right_arm, prop_right, round(scale, 2), int(neck_insert_px))
    if key in _SPRITE_CACHE:
        return _SPRITE_CACHE[key]

    ss = 2
    cw, ch = int(340 * scale), int(390 * scale)
    img = Image.new("RGBA", (cw * ss, ch * ss), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    def s(v):
        return int(round(v * scale * ss))

    cx = (cw * ss) // 2
    by = int(ch * ss - s(16 / max(0.2, scale)))

    leg_h = 64
    torso_h = 110
    head_rx, head_ry = 35, 39
    if role == "hollywood_xerxes":
        leg_h = 84
        torso_h = 134
        head_rx, head_ry = 38, 42

    hip_y = by - s(leg_h)
    sh_y = hip_y - s(torso_h)

    neck_depth = max(28, min(42, int(neck_insert_px)))
    head_cy = sh_y - s(head_ry) + s(15)

    w_top = s(52)
    w_bot = s(58)
    skin = SKIN

    if role in ("char_ziro_host", "mascot_time_traveler"):
        shirt_col = (217, 56, 41)
        inner_col = (245, 245, 242)
        accent_col = (242, 198, 65)
        hair_col = (42, 34, 30)
    elif role in ("char_iran_cleric", "cleric"):
        shirt_col = (54, 49, 46)
        inner_col = (124, 118, 112)
        accent_col = (38, 35, 32)
        hair_col = (235, 235, 235)
        w_bot = s(64)
    elif role in ("char_persian_king", "emperor_xerxes"):
        shirt_col = (118, 48, 144)
        inner_col = (238, 192, 62)
        accent_col = (215, 45, 45)
        hair_col = (35, 28, 26)
        w_bot = s(64)
    elif role == "student_boy":
        shirt_col = (68, 138, 204)
        inner_col = (245, 245, 245)
        accent_col = (235, 190, 55)
        hair_col = (42, 34, 30)
    elif role == "student_girl":
        shirt_col = (214, 88, 134)
        inner_col = (245, 245, 245)
        accent_col = (235, 190, 55)
        hair_col = (40, 30, 28)
    elif role == "spartan":
        shirt_col = skin
        inner_col = (212, 38, 38)
        accent_col = (208, 162, 84)
        hair_col = (45, 35, 30)
    else:
        shirt_col = (85, 105, 135)
        inner_col = (240, 240, 240)
        accent_col = (215, 65, 55)
        hair_col = (40, 35, 30)

    if role in ("char_ziro_host", "mascot_time_traveler"):
        draw.ellipse(
            [cx - s(42), sh_y - s(16), cx + s(42), sh_y + s(18)],
            fill=(182, 42, 30),
            outline=INK,
            width=s(3.0),
        )

    leg_dx = s(19)
    for lx in (cx - leg_dx, cx + leg_dx):
        draw_thick_line_ss(draw, (lx, hip_y - s(4)), (lx, by - s(6)), INK, 4.8 * scale, ss)
        sr_x, sr_y = s(14), s(6.5)
        draw.ellipse([lx - sr_x, by - sr_y * 2, lx + sr_x, by], fill=INK)

    def draw_arm(side: str, mode: str):
        sign = -1 if side == "left" else 1
        ax0 = cx + sign * (w_top - s(10))
        ay0 = sh_y + s(16)
        sleeve_col = skin if role == "spartan" else shirt_col

        if mode == "down":
            ax1, ay1 = ax0 + sign * s(20), hip_y - s(6)
        elif mode == "point_left":
            ax1, ay1 = ax0 - s(64), ay0 - s(4)
        elif mode == "point_right":
            ax1, ay1 = ax0 + s(64), ay0 - s(4)
        elif mode == "up":
            ax1, ay1 = ax0 + sign * s(36), ay0 - s(46)
        elif mode == "hold_front":
            ax1, ay1 = ax0 + sign * s(40), ay0 + s(14)
        else:
            ax1, ay1 = ax0 + sign * s(20), hip_y - s(8)

        draw_thick_line_ss(draw, (ax0, ay0), (ax1, ay1), INK, 24 * scale, ss)
        draw_thick_line_ss(draw, (ax0, ay0), (ax1, ay1), sleeve_col, 17.5 * scale, ss)

        hr = s(11.5)
        draw.ellipse([ax1 - hr, ay1 - hr, ax1 + hr, ay1 + hr], fill=skin, outline=INK, width=s(3))
        draw.arc([ax1 - s(5), ay1 - s(5), ax1 + s(5), ay1 + s(5)], 35, 225, fill=INK, width=s(2.2))
        return (ax1, ay1)

    draw_arm("left", left_arm)
    r_hand = draw_arm("right", right_arm)

    draw.rounded_rectangle([cx - w_top, sh_y, cx + w_top, hip_y], radius=s(22), fill=shirt_col, outline=INK, width=s(3.4))

    neck_w = s(16)
    neck_top_y = head_cy + s(10)
    neck_bot_y = sh_y + s(neck_depth * 0.65)
    draw.rounded_rectangle(
        [cx - neck_w, neck_top_y, cx + neck_w, neck_bot_y],
        radius=s(8),
        fill=skin,
        outline=INK,
        width=s(2.8),
    )

    if role in ("char_ziro_host", "mascot_time_traveler"):
        draw.polygon(
            [(cx - s(18), sh_y + s(2)), (cx + s(18), sh_y + s(2)), (cx, sh_y + s(28))],
            fill=inner_col,
            outline=INK,
            width=s(2.6),
        )
        draw_thick_line_ss(draw, (cx - s(11), sh_y + s(12)), (cx - s(11), sh_y + s(46)), (248, 248, 248), 3.0 * scale, ss)
        draw_thick_line_ss(draw, (cx + s(11), sh_y + s(12)), (cx + s(11), sh_y + s(46)), (248, 248, 248), 3.0 * scale, ss)
        draw.polygon(
            [
                (cx - s(32), hip_y - s(34)),
                (cx + s(32), hip_y - s(34)),
                (cx + s(38), hip_y - s(6)),
                (cx - s(38), hip_y - s(6)),
            ],
            fill=(192, 46, 34),
            outline=INK,
            width=s(2.4),
        )
    elif role in ("student_boy", "student_girl"):
        draw.polygon(
            [(cx - s(16), sh_y + s(4)), (cx + s(16), sh_y + s(4)), (cx + s(14), hip_y), (cx - s(14), hip_y)],
            fill=inner_col,
            outline=INK,
            width=s(2.6),
        )
    elif role in ("char_iran_cleric", "cleric"):
        draw.polygon(
            [(cx - s(18), sh_y + s(4)), (cx + s(18), sh_y + s(4)), (cx + s(16), hip_y), (cx - s(16), hip_y)],
            fill=inner_col,
            outline=INK,
            width=s(2.6),
        )
        draw.rectangle([cx - s(18), hip_y - s(36), cx + s(18), hip_y - s(22)], fill=accent_col, outline=INK, width=s(2.2))

    hr_x, hr_y = s(head_rx), s(head_ry)
    if role == "student_girl":
        draw.ellipse(
            [cx - hr_x - s(7), head_cy - hr_y - s(5), cx + hr_x + s(7), head_cy + hr_y + s(12)],
            fill=(45, 95, 148),
            outline=INK,
            width=s(3),
        )

    for sgn in (-1, 1):
        ex = cx + sgn * hr_x
        draw.ellipse([ex - s(6.5), head_cy - s(7), ex + s(6.5), head_cy + s(9)], fill=skin, outline=INK, width=s(2.8))

    draw.ellipse([cx - hr_x, head_cy - hr_y, cx + hr_x, head_cy + hr_y], fill=skin, outline=INK, width=s(3.4))

    if role in ("char_iran_cleric", "cleric"):
        beard_pts = [
            (cx - hr_x + s(2), head_cy + s(2)),
            (cx - s(20), head_cy + s(12)),
            (cx, head_cy + s(8)),
            (cx + s(20), head_cy + s(12)),
            (cx + hr_x - s(2), head_cy + s(2)),
            (cx + s(26), head_cy + hr_y + s(16)),
            (cx, head_cy + hr_y + s(24)),
            (cx - s(26), head_cy + hr_y + s(16)),
        ]
        draw.polygon(beard_pts, fill=(235, 235, 235), outline=INK, width=s(3))

    eye_y = head_cy - s(4)
    eye_dx = s(12.5)
    er_x, er_y = s(3.8), s(4.8)
    for ex in (cx - eye_dx, cx + eye_dx):
        draw.ellipse([ex - er_x, eye_y - er_y, ex + er_x, eye_y + er_y], fill=INK)

    if role in ("char_ziro_host", "mascot_time_traveler"):
        gr = s(9.5)
        for ex in (cx - eye_dx, cx + eye_dx):
            draw.ellipse([ex - gr, eye_y - gr, ex + gr, eye_y + gr], outline=INK, width=s(2.5))
        draw_thick_line_ss(draw, (cx - eye_dx + gr, eye_y), (cx + eye_dx - gr, eye_y), INK, 2.2 * scale, ss)

    eb_y = eye_y - s(10.5)
    if emotion in ("angry", "stern"):
        draw_thick_line_ss(draw, (cx - eye_dx - s(7), eb_y - s(3.5)), (cx - eye_dx + s(7), eb_y + s(3.5)), INK, 2.8 * scale, ss)
        draw_thick_line_ss(draw, (cx + eye_dx - s(7), eb_y + s(3.5)), (cx + eye_dx + s(7), eb_y - s(3.5)), INK, 2.8 * scale, ss)
    elif emotion in ("shocked", "scared", "worried"):
        draw_thick_line_ss(draw, (cx - eye_dx - s(7), eb_y + s(3.5)), (cx - eye_dx + s(7), eb_y - s(3.5)), INK, 2.8 * scale, ss)
        draw_thick_line_ss(draw, (cx + eye_dx - s(7), eb_y - s(3.5)), (cx + eye_dx + s(7), eb_y + s(3.5)), INK, 2.8 * scale, ss)
        sd_x, sd_y = cx - hr_x + s(10), head_cy - s(10)
        draw.ellipse([sd_x - s(4), sd_y, sd_x + s(4), sd_y + s(10)], fill=(110, 205, 255), outline=INK, width=s(1.8))
    else:
        draw_thick_line_ss(draw, (cx - eye_dx - s(6.5), eb_y), (cx - eye_dx + s(6.5), eb_y), INK, 2.6 * scale, ss)
        draw_thick_line_ss(draw, (cx + eye_dx - s(6.5), eb_y), (cx + eye_dx + s(6.5), eb_y), INK, 2.6 * scale, ss)

    my = head_cy + s(18)
    if mouth == "open" or emotion in ("shocked", "scared"):
        draw.ellipse([cx - s(7), my - s(5), cx + s(7), my + s(6)], fill=(185, 55, 55), outline=INK, width=s(2.4))
    elif mouth == "half":
        draw.ellipse([cx - s(5.5), my - s(3), cx + s(5.5), my + s(3.5)], fill=(185, 55, 55), outline=INK, width=s(2.2))
    elif mouth == "smile" or emotion == "smug":
        draw.arc([cx - s(10), my - s(7), cx + s(10), my + s(5)], 10, 170, fill=INK, width=s(2.8))
    elif emotion in ("stern", "angry"):
        draw.arc([cx - s(10), my - s(2), cx + s(10), my + s(9)], 195, 345, fill=INK, width=s(2.8))
    else:
        draw_thick_line_ss(draw, (cx - s(8), my), (cx + s(8), my), INK, 2.6 * scale, ss)

    if role in ("char_ziro_host", "mascot_time_traveler"):
        draw.chord(
            [cx - hr_x - s(2), head_cy - hr_y - s(8), cx + hr_x + s(4), head_cy - s(10)],
            175,
            365,
            fill=hair_col,
            outline=INK,
            width=s(3),
        )
    elif role in ("student_boy", "student_girl"):
        draw.chord([cx - hr_x, head_cy - hr_y - s(2), cx + hr_x, head_cy - s(8)], 180, 360, fill=hair_col, outline=INK, width=s(3))
        cap_y = head_cy - hr_y - s(2)
        draw.polygon(
            [(cx, cap_y - s(16)), (cx + s(48), cap_y - s(2)), (cx, cap_y + s(10)), (cx - s(48), cap_y - s(2))],
            fill=(40, 42, 48),
            outline=INK,
            width=s(2.8),
        )
        draw_thick_line_ss(draw, (cx + s(34), cap_y), (cx + s(40), cap_y + s(20)), (235, 190, 55), 2.4 * scale, ss)
    elif role in ("char_iran_cleric", "cleric"):
        tb_box = [cx - hr_x - s(6), head_cy - hr_y - s(16), cx + hr_x + s(6), head_cy - s(14)]
        draw.ellipse(tb_box, fill=(32, 32, 35), outline=INK, width=s(3.2))

    px, py = r_hand
    if prop_right == "laser_pointer":
        tip_x, tip_y = px + s(38), py - s(38)
        draw_thick_line_ss(draw, (px, py), (tip_x, tip_y), (75, 82, 92), 4 * scale, ss)
        draw.ellipse([tip_x - s(7), tip_y - s(7), tip_x + s(7), tip_y + s(7)], fill=(255, 65, 65), outline=INK, width=s(2.2))
    elif prop_right == "phone":
        draw.rounded_rectangle([px - s(10), py - s(24), px + s(14), py + s(8)], radius=s(4), fill=(45, 52, 62), outline=INK, width=s(2.5))

    out = img.resize((cw, ch), Image.LANCZOS)
    _SPRITE_CACHE[key] = out
    return out


# ==============================================================================
# 2. ORGANIC ZIRO STAGE PRIMITIVES (Typewriter Text, Photo Cards, Curved Arrows, Stamps)
# ==============================================================================
def draw_kinetic_text(
    img: Image.Image,
    pos,
    text: str,
    size: int = 32,
    color=INK,
    stroke_col=None,
    stroke_w: int = 0,
    align: str = "center",
    bold: bool = True,
    organic: bool = True,
    prog: float = 1.0,
    safe_box=None,
):
    """
    Draws smooth typewriter-revealed stage text (Frameless Kinetic Typography)
    exactly like Ziro History's organic stage captions.
    """
    if prog <= 0.01 or not text:
        return
    n_chars = max(1, int(round(len(text) * clamp01(prog))))
    sub = text[:n_chars]
    draw = ImageDraw.Draw(img)
    font = get_font(size, bold=bold, organic=organic)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    cx, cy = int(pos[0]), int(pos[1])
    if safe_box:
        sx0, sy0, sx1, sy1 = safe_box
        if align == "center":
            cx = max(sx0 + tw // 2 + 12, min(sx1 - tw // 2 - 12, cx))
        elif align == "left":
            cx = max(sx0 + 12, min(sx1 - tw - 12, cx))
        cy = max(sy0 + th // 2 + 8, min(sy1 - th // 2 - 8, cy))
    tx = cx - tw // 2 if align == "center" else (cx if align == "left" else cx - tw)
    ty = cy - th // 2
    if stroke_col and stroke_w > 0:
        draw.text((tx, ty), sub, font=font, fill=color, stroke_width=int(stroke_w), stroke_fill=stroke_col)
    else:
        draw.text((tx, ty), sub, font=font, fill=color)


def draw_stamp(
    img: Image.Image,
    center,
    text: str,
    bg_col=(198, 42, 42),
    txt_col=(255, 255, 255),
    size: int = 28,
    pop_t: float = 1.0,
    safe_box=None,
):
    if pop_t <= 0.01 or not text:
        return
    sc = ease_out_back(pop_t, 1.45) if pop_t < 1.0 else 1.0
    draw = ImageDraw.Draw(img)
    font = get_font(max(12, int(size * sc)), bold=True, organic=False)
    bbox = draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    pad_x, pad_y = int(22 * sc), int(12 * sc)
    half_w = tw // 2 + pad_x
    half_h = th // 2 + pad_y
    cx, cy = int(center[0]), int(center[1])
    if safe_box:
        sx0, sy0, sx1, sy1 = safe_box
        cx = max(sx0 + half_w + 10, min(sx1 - half_w - 10, cx))
        cy = max(sy0 + half_h + 10, min(sy1 - half_h - 10, cy))
    box = [cx - half_w, cy - half_h, cx + half_w, cy + half_h]
    draw.rounded_rectangle([box[0] + 4, box[1] + 5, box[2] + 4, box[3] + 5], radius=int(10 * sc), fill=(72, 72, 76))
    draw.rounded_rectangle(box, radius=int(10 * sc), fill=bg_col, outline=INK, width=3)
    draw.text((cx - tw // 2, cy - th // 2 - int(2 * sc)), text, font=font, fill=txt_col)


def draw_curved_arrow(img: Image.Image, p1, p2, arch: float = -28.0, prog: float = 1.0):
    """Draws Ziro-style white curved arrow with ink border and crimson arrowhead."""
    if prog <= 0.02:
        return
    prog = clamp01(prog)
    draw = ImageDraw.Draw(img)
    x1, y1 = p1
    x2, y2 = p2
    dx_chord = x2 - x1
    dy_chord = y2 - y1
    L_chord = max(1.0, math.hypot(dx_chord, dy_chord))
    px_n, py_n = -dy_chord / L_chord, dx_chord / L_chord
    mx = (x1 + x2) / 2.0 + px_n * arch
    my = (y1 + y2) / 2.0 + py_n * arch
    steps = max(4, int(26 * prog))
    upper, lower = [], []
    for i in range(steps + 1):
        t = (i / 26.0) * 0.86
        bx = (1 - t) ** 2 * x1 + 2 * (1 - t) * t * mx + t**2 * x2
        by = (1 - t) ** 2 * y1 + 2 * (1 - t) * t * my + t**2 * y2
        tx = 2 * (1 - t) * (mx - x1) + 2 * t * (x2 - mx)
        ty = 2 * (1 - t) * (my - y1) + 2 * t * (y2 - my)
        tL = max(1.0, math.hypot(tx, ty))
        nx, ny = -ty / tL, tx / tL
        w_half = 3.0 + 4.0 * (i / 26.0)
        upper.append((bx + nx * w_half, by + ny * w_half))
        lower.append((bx - nx * w_half, by - ny * w_half))
    if len(upper) >= 2:
        draw.polygon(upper + lower[::-1], fill=(252, 252, 252), outline=INK, width=2)
    if prog > 0.75:
        dx, dy = x2 - mx, y2 - my
        L = max(1.0, math.hypot(dx, dy))
        ux, uy = dx / L, dy / L
        px, py = -uy, ux
        b1 = (x2 - ux * 26 + px * 13, y2 - uy * 26 + py * 13)
        b2 = (x2 - ux * 26 - px * 13, y2 - uy * 26 - py * 13)
        draw.polygon([(x2, y2), b1, b2], fill=(212, 42, 42), outline=INK, width=2)


def draw_archival_photo_card(
    img: Image.Image,
    photo_file: str,
    center,
    size_wh,
    badge_text: str,
    caption_text: str = "",
    badge_col=(52, 112, 172),
    pop_t: float = 1.0,
    safe_box=None,
    episode_id: str = "EP01_Iran",
    workspace_root: Path = None,
):
    """
    Draws Ziro-authentic archival photo frame with top-left ribbon badge (`Tehran, 1970`)
    and organic handwritten caption underneath (`"Paris of the Middle East?"`).
    """
    if pop_t <= 0.01:
        return
    sc = ease_out_back(pop_t, 1.32) if pop_t < 1.0 else 1.0
    cw, ch = max(60, int(size_wh[0] * sc)), max(60, int(size_wh[1] * sc))
    cx, cy = int(center[0]), int(center[1])
    if safe_box:
        sx0, sy0, sx1, sy1 = safe_box
        cx = max(sx0 + cw // 2 + 14, min(sx1 - cw // 2 - 14, cx))
        cy = max(sy0 + ch // 2 + 46, min(sy1 - ch // 2 - 42, cy))

    draw = ImageDraw.Draw(img)
    x0, y0, x1, y1 = cx - cw // 2, cy - ch // 2, cx + cw // 2, cy + ch // 2
    draw.rounded_rectangle([x0 + 6, y0 + 8, x1 + 6, y1 + 8], radius=12, fill=(162, 160, 156))
    draw.rounded_rectangle([x0, y0, x1, y1], radius=12, fill=(248, 248, 246), outline=INK, width=3)

    if photo_file:
        ph = get_cached_image(photo_file, (max(20, cw - 18), max(20, ch - 18)), episode_id, workspace_root)
        img.paste(ph, (x0 + 9, y0 + 9))
        draw.rectangle([x0 + 9, y0 + 9, x1 - 9, y1 - 9], outline=INK, width=2)

    if badge_text and pop_t > 0.35:
        font_b = get_font(19, bold=True, organic=False)
        bb = draw.textbbox((0, 0), badge_text, font=font_b)
        bw = (bb[2] - bb[0]) + 26
        # Ziro-authentic Flat Corner Tab (no heavy black border)
        draw.rounded_rectangle([x0, y0 - 34, x0 + bw, y0 - 3], radius=5, fill=badge_col)
        draw.text((x0 + 13, y0 - 31), badge_text, font=font_b, fill=(255, 255, 255))

    if caption_text and pop_t > 0.45:
        draw_kinetic_text(
            img,
            (cx, y1 + 30),
            caption_text,
            size=24,
            color=INK,
            bold=True,
            organic=True,
            prog=min(1.0, (pop_t - 0.4) * 1.8),
            safe_box=safe_box,
        )


def paste_char_safe(
    canvas: Image.Image,
    x: int,
    y: int,
    role: str = "char_ziro_host",
    emotion: str = "explaining",
    mouth: str = "closed",
    left_arm: str = "down",
    right_arm: str = "down",
    prop_right: str = None,
    scale: float = 1.0,
    neck_insert_px: int = 35,
    pop_t: float = 1.0,
    label: str = "",
    safe_box=None,
):
    if pop_t <= 0.01:
        return
    sc_eff = scale * (ease_out_back(pop_t, 1.25) if pop_t < 1.0 else 1.0)
    sc_eff = max(0.2, sc_eff)
    spr = get_character_sprite(role, emotion, mouth, left_arm, right_arm, prop_right, sc_eff, neck_insert_px)
    sw, sh = spr.size

    cx, foot_y = int(x), int(y + 135 * sc_eff)
    if safe_box:
        sx0, sy0, sx1, sy1 = safe_box
        half_vis_w = int(sw * 0.42)
        cx = max(sx0 + half_vis_w, min(sx1 - half_vis_w, cx))
        foot_y = max(sy0 + sh, min(sy1 + 30, foot_y))

    px = int(cx - sw // 2)
    py = int(foot_y - sh)
    canvas.paste(spr, (px, py), spr)

    if label and role != "char_ziro_host":
        draw_kinetic_text(
            canvas,
            (cx, foot_y + 18),
            label,
            size=20,
            color=INK,
            bold=True,
            organic=True,
            prog=min(1.0, pop_t * 1.2),
            safe_box=safe_box,
        )


# ==============================================================================
# 3. 100% DATA-DRIVEN PASS 1 WORLD STAGE RENDERER
# ==============================================================================
def render_stage_pass1(
    beat_data: dict,
    bt: float,
    m_code: int = 0,
    safe_box=(80, 165, 1840, 1020),
    episode_id: str = "EP01_Iran",
    workspace_root: Path = None,
) -> Image.Image:
    """
    Renders Pass 1 World Stage driven 100% by `beat_data["sub_triggers_bt"]` and `beat_data["characters"]`.
    - Studio Gray `#CCCCCC` (`DAYLIGHT_WARM`) is 100% seamless from y=0 to y=1080 (NO horizontal floor line at y=855!).
    - 90% of stage typography is Frameless Color-Pop & Typewriter Text matching Ziro History.
    """
    lighting = beat_data.get("lighting_mode", "DAYLIGHT_WARM")
    triggers = beat_data.get("sub_triggers_bt", [])
    chars = beat_data.get("characters", [])
    m_state = "open" if m_code == 2 else ("half" if m_code == 1 else "closed")

    floor_y = 855
    if lighting == "PRISON_NIGHT":
        img = Image.new("RGB", (W, H), (34, 38, 48))
        draw = ImageDraw.Draw(img)
    elif lighting == "SAND_EMPIRE":
        img = Image.new("RGB", (W, H), (224, 214, 194))
        draw = ImageDraw.Draw(img)
    else:
        # Ziro signature #CCCCCC studio gray: 100% uniform seamless canvas, zero horizontal floor line!
        img = Image.new("RGB", (W, H), (204, 204, 204))
        draw = ImageDraw.Draw(img)

    sx0, sy0, sx1, sy1 = safe_box
    stage_cx = (sx0 + sx1) // 2
    stage_w = sx1 - sx0
    skip_default_chars = False

    # Process every sub-trigger in chronological order
    for idx, trig in enumerate(triggers):
        t0 = float(trig.get("bt", 0.0))
        if bt < t0:
            continue
        dt = bt - t0
        pop_t = dt / 0.36
        act = trig.get("action_type", "")
        lbl = trig.get("label", "")
        sub_lbl = trig.get("sub_label", "")
        p_file = trig.get("photo_file", "")

        # ------------------------------------------------------------------
        # A. Continuous Split Photo Comparison (1970 Left vs 1980 Right)
        # ------------------------------------------------------------------
        if act == "MYSTERY_FRAMES_2":
            for fx, delay in [(stage_cx - 280, 0.0), (stage_cx + 340, 0.35)]:
                if dt >= delay:
                    sc = ease_out_back((dt - delay) / 0.35)
                    cw, ch = int(460 * sc), int(350 * sc)
                    draw.rounded_rectangle([fx - cw // 2, 500 - ch // 2, fx + cw // 2, 500 + ch // 2], radius=14, fill=(236, 236, 232), outline=INK, width=3)
                    draw_kinetic_text(img, (fx, 500), "?", size=105, color=(145, 145, 150), organic=True)

        elif act == "PHOTO_CARD_LEFT":
            draw_archival_photo_card(
                img, p_file, (stage_cx - 285, 485), (465, 355),
                lbl, sub_lbl, (52, 112, 172), pop_t, safe_box, episode_id, workspace_root
            )

        elif act == "PHOTO_CARD_TOP_RIGHT":
            draw_archival_photo_card(
                img, p_file, (stage_cx + 340, 385), (430, 285),
                lbl, sub_lbl, (68, 138, 188), pop_t, safe_box, episode_id, workspace_root
            )

        elif act == "CINEMA_CAFE_PILLS":
            # Frameless minimalist icon + organic text (no heavy outer box)
            rx = stage_cx + 195
            draw.rounded_rectangle([rx - 135, 600, rx - 98, 634], radius=4, fill=(48, 52, 60), outline=INK, width=2)
            draw.line([(rx - 135, 610), (rx - 98, 610)], fill=(245, 245, 242), width=2)
            draw_kinetic_text(img, (rx + 12, 617), lbl or "Rạp chiếu phim", size=26, color=INK, organic=True, prog=dt / 0.45, safe_box=safe_box)
            if dt > 0.65 and sub_lbl:
                rx2 = stage_cx + 495
                draw.rounded_rectangle([rx2 - 135, 602, rx2 - 101, 634], radius=6, fill=(168, 102, 58), outline=INK, width=2)
                draw_kinetic_text(img, (rx2 + 12, 617), sub_lbl, size=26, color=INK, organic=True, prog=(dt - 0.65) / 0.45, safe_box=safe_box)

        elif act == "PARIS_LA_STAMPS":
            # Frameless Color-Pop Text with vector checkmark (zero missing glyph boxes)
            clean_lbl = lbl.replace("✓", "").strip()
            cx1, cy1 = stage_cx + 195, 715
            draw.line([(cx1 - 118, cy1 - 2), (cx1 - 108, cy1 + 9), (cx1 - 92, cy1 - 11)], fill=(28, 138, 68), width=4)
            draw_kinetic_text(img, (cx1 + 10, cy1), clean_lbl, size=31, color=(28, 128, 68), bold=True, organic=True, prog=dt / 0.5, safe_box=safe_box)
            if dt > 0.60 and sub_lbl:
                clean_sub = sub_lbl.replace("✓", "").strip()
                cx2, cy2 = stage_cx + 505, 715
                draw.line([(cx2 - 148, cy2 - 2), (cx2 - 138, cy2 + 9), (cx2 - 122, cy2 - 11)], fill=(32, 92, 168), width=4)
                draw_kinetic_text(img, (cx2 + 10, cy2), clean_sub, size=31, color=(32, 92, 168), bold=True, organic=True, prog=(dt - 0.60) / 0.5, safe_box=safe_box)

        elif act == "PHOTO_CARD_RIGHT":
            # Draw Ziro-style transition arrow ("10 năm") cleanly in the 120px gap between 1970 Left Card and 1980 Right Card
            draw_curved_arrow(img, (stage_cx - 42, 495), (stage_cx + 52, 495), arch=-18, prog=min(1.0, dt / 0.45))
            draw_kinetic_text(img, (stage_cx + 5, 445), "10 năm", size=22, color=(198, 34, 34), bold=True, organic=True, prog=dt / 0.45, safe_box=safe_box)
            draw_archival_photo_card(
                img, p_file, (stage_cx + 298, 485), (465, 355),
                lbl, sub_lbl, (185, 38, 38), pop_t, safe_box, episode_id, workspace_root
            )

        elif act == "CHADOR_ROW_5":
            for i in range(5):
                if dt > i * 0.18:
                    ix = stage_cx + 130 + i * 90
                    iy = 805
                    draw.polygon([(ix, iy - 55), (ix - 26, iy + 20), (ix + 26, iy + 20)], fill=(32, 32, 36), outline=INK, width=2)
                    draw.ellipse([ix - 11, iy - 62, ix + 11, iy - 38], fill=(225, 195, 170), outline=INK, width=2)

        elif act == "BUILDING_5_FLOORS":
            bx0 = min(sx1 - 145, stage_cx + 595)
            bx1 = bx0 + 125
            draw.rounded_rectangle([bx0, 295, bx1, 665], radius=8, fill=(75, 78, 84), outline=INK, width=3)
            for fl in range(5):
                fy = 605 - fl * 70
                draw.rectangle([bx0 + 18, fy, bx0 + 52, fy + 34], fill=(235, 205, 85), outline=INK, width=2)
                draw.rectangle([bx0 + 72, fy, bx0 + 106, fy + 34], fill=(235, 205, 85), outline=INK, width=2)
            draw_kinetic_text(img, ((bx0 + bx1) // 2, 260), lbl or "CAO 5 TẦNG!", size=22, color=(198, 34, 34), bold=True, organic=True, safe_box=safe_box)

        elif act == "STAMP_SLAM_RIGHT":
            # Frameless bold crimson callout above the 1980 photo so the historical photo is 100% unobstructed
            draw_kinetic_text(
                img, (stage_cx + 310, 232), lbl,
                size=34, color=(198, 28, 28), stroke_col=(248, 248, 246), stroke_w=3,
                bold=True, organic=True, prog=dt / 0.45, safe_box=safe_box
            )

        # ------------------------------------------------------------------
        # B. Fact vs Myth (2 Planets Crossed Out -> Satellite Map of Tehran)
        # ------------------------------------------------------------------
        elif act == "TWO_PLANETS_MYTH":
            switch_t = 3.8
            for tr2 in triggers:
                if tr2.get("action_type") == "SATELLITE_TEHRAN_REVEAL":
                    switch_t = float(tr2.get("bt", 3.8))
            if bt < switch_t:
                draw.ellipse([stage_cx - 340, 360, stage_cx - 110, 590], fill=(68, 148, 215), outline=INK, width=4)
                draw.ellipse([stage_cx + 150, 360, stage_cx + 380, 590], fill=(215, 92, 58), outline=INK, width=4)
                if dt > 0.8:
                    draw_thick_line_ss(draw, (stage_cx - 370, 330), (stage_cx + 410, 620), (215, 32, 32), 8, ss=1)
                    draw_thick_line_ss(draw, (stage_cx + 410, 330), (stage_cx - 370, 620), (215, 32, 32), 8, ss=1)
                if dt > 1.3:
                    # True Rubber Stamp Verdict (<10% usage)
                    draw_stamp(img, (stage_cx + 20, 475), lbl, bg_col=(205, 35, 35), size=34, pop_t=(dt - 1.3) / 0.30, safe_box=safe_box)

        elif act == "SATELLITE_TEHRAN_REVEAL":
            skip_default_chars = True
            sat = get_cached_image(p_file or "07_beat04_0028s-0034s_satellite_iran_middle_east.jpg", (W, H), episode_id, workspace_root).copy()
            dark = ImageEnhance.Brightness(sat).enhance(0.45)
            mask = Image.new("L", (W, H), 0)
            mdraw = ImageDraw.Draw(mask)
            iran_poly = [
                (955, 395), (1030, 390), (1065, 520), (1180, 520),
                (1325, 470), (1405, 575), (1435, 725), (1265, 755),
                (1145, 665), (1035, 585), (975, 485)
            ]
            mdraw.polygon(iran_poly, fill=255)
            dark.paste(sat, (0, 0), mask)
            img.paste(dark, (0, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon(iran_poly, outline=(255, 215, 65), width=5)

            tx, ty = 1135, 538
            pr = int(16 + 20 * ((bt * 2.0) % 1.0))
            draw.ellipse([tx - pr, ty - pr, tx + pr, ty + pr], outline=(255, 75, 75), width=3)
            draw.ellipse([tx - 10, ty - 10, tx + 10, ty + 10], fill=(255, 55, 55), outline=(255, 255, 255), width=3)
            draw_kinetic_text(img, (tx, ty - 48), "THỦ ĐÔ TEHRAN", size=28, color=(255, 235, 95), stroke_col=INK, stroke_w=3, organic=False, prog=dt / 0.6)
            if dt > 1.4:
                draw_kinetic_text(img, (stage_cx, 225), lbl, size=34, color=(255, 225, 85), stroke_col=INK, stroke_w=4, bold=True, organic=True, prog=(dt - 1.4) / 0.5, safe_box=safe_box)
            if dt > 2.8 and sub_lbl:
                draw_kinetic_text(img, (1215, 615), sub_lbl, size=68, color=(255, 255, 255), stroke_col=INK, stroke_w=5, organic=False, prog=(dt - 2.8) / 0.5)

        # ------------------------------------------------------------------
        # C. Split-Screen 50/50: Modern Youth (<35, Instagram) vs 7th-Century Clerics
        #    Matches Ziro Reference (`70% of population` / bold red `under 35 years old`)
        # ------------------------------------------------------------------
        elif act == "SPLIT_YOUTH_LEFT":
            skip_default_chars = True
            draw.rectangle([0, 0, stage_cx, floor_y], fill=(205, 232, 248))
            draw.rectangle([0, floor_y, stage_cx, H], fill=(138, 192, 112))
            draw.line([(0, floor_y), (stage_cx, floor_y)], fill=INK, width=4)
            draw.rectangle([stage_cx, 0, W, floor_y], fill=(212, 202, 186))
            draw.rectangle([stage_cx, floor_y, W, H], fill=(154, 132, 106))
            draw.line([(stage_cx, floor_y), (W, floor_y)], fill=INK, width=4)
            draw.line([(stage_cx, 0), (stage_cx, H)], fill=INK, width=5)

            lcx = (sx0 + stage_cx) // 2
            paste_char_safe(img, lcx - 190, 715, role="student_girl", mouth="smile", right_arm="hold_front", prop_right="phone", scale=0.96, pop_t=pop_t, safe_box=safe_box)
            paste_char_safe(img, lcx, 725, role="student_boy", mouth=m_state if bt < 6.0 else "smile", left_arm="up", right_arm="hold_front", prop_right="phone", scale=1.02, pop_t=pop_t, safe_box=safe_box)
            paste_char_safe(img, lcx + 190, 715, role="student_girl", mouth="smile", right_arm="hold_front", prop_right="phone", scale=0.96, pop_t=pop_t, safe_box=safe_box)

            # Ziro Frameless Hierarchy: dark setup line + bold red keyword pop (ZERO boxes!)
            draw_kinetic_text(img, (lcx, 222), "70% dân số Iran", size=28, color=(38, 48, 62), bold=False, organic=True, prog=dt / 0.7, safe_box=safe_box)
            if dt > 1.0:
                draw_kinetic_text(img, (lcx, 278), lbl or "dưới 35 tuổi", size=44, color=(208, 32, 32), bold=True, organic=True, prog=(dt - 1.0) / 0.55, safe_box=safe_box)
            if dt > 2.3:
                draw.line([(lcx - 112, 346), (lcx - 102, 356), (lcx - 88, 338)], fill=(24, 98, 158), width=4)
                draw_kinetic_text(img, (lcx + 12, 348), "Học thức cao", size=29, color=(24, 98, 158), bold=True, organic=True, prog=(dt - 2.3) / 0.5, safe_box=safe_box)
            if dt > 3.4 and sub_lbl:
                clean_sub = sub_lbl.replace("✓", "").strip()
                draw.line([(lcx - 228, 403), (lcx - 218, 413), (lcx - 204, 395)], fill=(188, 38, 92), width=4)
                draw_kinetic_text(img, (lcx + 14, 405), clean_sub, size=27, color=(188, 38, 92), bold=True, organic=True, prog=(dt - 3.4) / 0.55, safe_box=safe_box)
                for hx in (lcx - 125, lcx + 68, lcx + 255):
                    hy = int(605 - ((dt - 3.4) * 35) % 55)
                    draw_kinetic_text(img, (hx, hy), "♥", size=28, color=(228, 42, 78), bold=True, organic=False)

        elif act == "SPLIT_CLERICS_RIGHT":
            skip_default_chars = True
            rcx = (stage_cx + sx1) // 2
            paste_char_safe(img, rcx - 190, 715, role="cleric", emotion="angry", left_arm="point_left", scale=0.96, pop_t=pop_t, safe_box=safe_box)
            paste_char_safe(img, rcx, 725, role="cleric", emotion="angry", mouth=m_state, left_arm="point_left", scale=1.02, pop_t=pop_t, safe_box=safe_box)
            paste_char_safe(img, rcx + 190, 715, role="cleric", emotion="angry", left_arm="point_left", scale=0.96, pop_t=pop_t, safe_box=safe_box)

            draw_kinetic_text(img, (rcx, 222), "Nhưng lại bị cai trị bởi", size=28, color=(55, 44, 38), bold=False, organic=True, prog=dt / 0.7, safe_box=safe_box)
            if dt > 1.0:
                draw_kinetic_text(img, (rcx, 278), lbl or "Hội đồng giáo sĩ già", size=38, color=(48, 32, 26), bold=True, organic=True, prog=(dt - 1.0) / 0.55, safe_box=safe_box)
            if dt > 2.6 and sub_lbl:
                draw_kinetic_text(img, (rcx, 348), sub_lbl, size=34, color=(192, 28, 28), bold=True, organic=True, prog=(dt - 2.6) / 0.55, safe_box=safe_box)

        # ------------------------------------------------------------------
        # D. 3 Everyday Causes -> Curved Arrows -> Iron Prison Bars (Beat 07)
        # ------------------------------------------------------------------
        elif act == "PRISON_CAGE_RIGHT":
            px0, py0, px1, py1 = stage_cx + 390, 340, min(sx1 - 30, stage_cx + 710), 690
            for bx in range(px0 + 30, px1, 45):
                draw.line([(bx, py0), (bx, py1)], fill=(80, 80, 85), width=6)
            draw.line([(px0, py0 + 95), (px1, py0 + 95)], fill=(80, 80, 85), width=6)
            draw.line([(px0, py1), (px1, py1)], fill=(105, 105, 110), width=10)
            mid_px = (px0 + px1) // 2
            draw.arc([mid_px - 26, 460, mid_px + 26, 520], 180, 360, fill=(80, 80, 85), width=8)
            draw.rounded_rectangle([mid_px - 38, 498, mid_px + 38, 570], radius=8, fill=(238, 198, 62), outline=INK, width=3)
            draw.ellipse([mid_px - 5, 528, mid_px + 5, 538], fill=INK)
            draw_kinetic_text(img, (mid_px, 745), lbl or "BẮT BỎ TÙ!", size=38, color=(198, 38, 38), organic=True, safe_box=safe_box)

        elif act in ("CAUSE_ARROW_1", "CAUSE_ARROW_2", "CAUSE_ARROW_3"):
            row_idx = 0 if act.endswith("1") else (1 if act.endswith("2") else 2)
            cy_row = 285 + row_idx * 235
            box_x0, box_x1 = stage_cx - 500, stage_cx - 310
            draw.rounded_rectangle([box_x0, cy_row - 60, box_x1, cy_row + 60], radius=14, fill=(238, 238, 235), outline=INK, width=3)
            icx = (box_x0 + box_x1) // 2
            if row_idx == 0:
                draw.ellipse([icx - 12, cy_row - 36, icx + 12, cy_row - 12], fill=SKIN, outline=INK, width=3)
                draw.polygon([(icx - 18, cy_row - 10), (icx + 18, cy_row - 10), (icx + 26, cy_row + 36), (icx - 26, cy_row + 36)], fill=(215, 58, 102), outline=INK, width=3)
            elif row_idx == 1:
                draw.rounded_rectangle([icx - 32, cy_row - 8, icx + 24, cy_row + 22], radius=8, fill=(205, 152, 95), outline=INK, width=3)
                draw.ellipse([icx + 12, cy_row - 24, icx + 42, cy_row + 6], fill=(205, 152, 95), outline=INK, width=3)
            else:
                for wy in (-14, 0, 14):
                    draw.line([(icx - 50, cy_row + wy), (icx + 5, cy_row + wy)], fill=(85, 162, 218), width=4)
                draw.polygon([(icx + 15, cy_row - 18), (icx + 58, cy_row - 5), (icx + 42, cy_row + 24), (icx + 8, cy_row + 10)], fill=(58, 112, 188), outline=INK, width=3)

            draw_kinetic_text(img, (box_x1 + 28, cy_row), lbl, size=29, color=INK, align="left", organic=True, prog=dt / 0.65, safe_box=safe_box)
            target_y = 430 if row_idx == 0 else (520 if row_idx == 1 else 610)
            arch_v = -25 if row_idx <= 1 else 25
            draw_curved_arrow(img, (stage_cx + 120, cy_row), (stage_cx + 360, target_y), arch=arch_v, prog=(dt - 0.35) / 0.45)

        # ------------------------------------------------------------------
        # E. Bright Civilization Skyline -> Lights Off & Prison Bars Slam (Beat 08)
        # ------------------------------------------------------------------
        elif act == "CIVILIZATION_SKYLINE":
            slam_t = 4.6
            for tr2 in triggers:
                if tr2.get("action_type") == "SLAM_PRISON_BARS":
                    slam_t = float(tr2.get("bt", 4.6))
            lights_on = bt < slam_t
            sky_col = (42, 62, 102) if lights_on else (14, 16, 22)
            draw.rectangle([0, 0, W, floor_y], fill=sky_col)
            draw.rectangle([0, floor_y, W, H], fill=(28, 30, 36))
            draw.line([(0, floor_y), (W, floor_y)], fill=INK, width=4)
            buildings = [
                (260, 460, 450, floor_y),
                (470, 380, 700, floor_y),
                (720, 320, 1200, floor_y),
                (1220, 390, 1450, floor_y),
                (1470, 470, 1660, floor_y),
            ]
            dome_col = (52, 158, 168) if lights_on else (24, 48, 54)
            draw.chord([810, 185, 1110, 460], 180, 360, fill=dome_col, outline=INK, width=4)
            win_col = (255, 222, 75) if lights_on else (22, 24, 28)
            for bx0, by0, bx1, by1 in buildings:
                draw.rectangle([bx0, by0, bx1, by1], fill=(38, 42, 52) if lights_on else (20, 22, 26), outline=INK, width=3)
                for wy in range(by0 + 35, by1 - 40, 62):
                    for wx in range(bx0 + 28, bx1 - 35, 52):
                        draw.rectangle([wx, wy, wx + 28, wy + 38], fill=win_col, outline=INK, width=2)

        elif act == "SLAM_PRISON_BARS":
            bar_h = int(H * ease_out_cubic(min(1.0, dt / 0.35)))
            for bx in range(sx0 + 40, sx1 - 20, 125):
                draw.line([(bx, 0), (bx, bar_h)], fill=(95, 100, 108), width=10)
            draw_kinetic_text(img, (stage_cx, 515), lbl, size=44, color=(255, 75, 75), stroke_col=INK, stroke_w=4, bold=True, organic=True, prog=dt / 0.4, safe_box=safe_box)

        # ------------------------------------------------------------------
        # F. Geopolitics Satellite Map & Persian Carpet Metaphor (Beats 09, 10, 11, 12)
        # ------------------------------------------------------------------
        elif act == "UNROLL_PERSIAN_CARPET":
            draw.polygon([(stage_cx - 160, 180), (stage_cx + 160, 180), (stage_cx + 260, floor_y), (stage_cx - 260, floor_y)], fill=(192, 178, 152), outline=INK, width=2)
            draw.rectangle([sx0, 410, sx1, 560], fill=(192, 178, 152), outline=INK, width=2)
            cw_c = int(620 * ease_out_cubic(min(1.0, dt / 0.55)))
            c_x0, c_y0, c_x1, c_y1 = stage_cx - cw_c // 2, 360, stage_cx + cw_c // 2, 595
            if cw_c > 60:
                draw.rounded_rectangle([c_x0, c_y0, c_x1, c_y1], radius=14, fill=(168, 36, 42), outline=(242, 198, 65), width=5)
                draw.rounded_rectangle([c_x0 + 20, c_y0 + 20, c_x1 - 20, c_y1 - 20], radius=8, fill=(132, 28, 34), outline=(242, 198, 65), width=3)
            draw_kinetic_text(img, (stage_cx, 285), lbl, size=30, color=(138, 28, 32), organic=True, prog=dt / 0.8, safe_box=safe_box)

        elif act == "BOOTS_STOMP_CARPET":
            for bx, by in [(stage_cx - 140, 455), (stage_cx + 40, 495), (stage_cx + 165, 435)]:
                draw.rounded_rectangle([bx - 36, by - 18, bx + 36, by + 18], radius=8, fill=(48, 42, 38), outline=INK, width=3)
            draw_kinetic_text(img, (stage_cx, 655), lbl, size=34, color=(198, 32, 32), bold=True, organic=True, prog=dt / 0.5, safe_box=safe_box)

        elif act == "MAP_ARROWS_4_EMPIRES":
            skip_default_chars = True
            sat = get_cached_image(p_file or "07_beat04_0028s-0034s_satellite_iran_middle_east.jpg", (W, H), episode_id, workspace_root).copy()
            dark = ImageEnhance.Brightness(sat).enhance(0.62)
            mask = Image.new("L", (W, H), 0)
            mdraw = ImageDraw.Draw(mask)
            iran_poly = [
                (955, 395), (1030, 390), (1065, 520), (1180, 520),
                (1325, 470), (1405, 575), (1435, 725), (1265, 755),
                (1145, 665), (1035, 585), (975, 485)
            ]
            mdraw.polygon(iran_poly, fill=255)
            dark.paste(sat, (0, 0), mask)
            img.paste(dark, (0, 0))
            draw = ImageDraw.Draw(img)
            draw.polygon(iran_poly, outline=(255, 215, 65), width=5)
            draw_kinetic_text(img, (1205, 575), "I R A N", size=42, color=(255, 245, 215), stroke_col=INK, stroke_w=4, bold=True, organic=False, prog=dt / 0.45, safe_box=safe_box)

            # Tách biệt hoàn toàn tọa độ đặt chữ (txt_pos) và tọa độ gốc mũi tên (arr_start) để 0 mũi tên nào đè lên chữ!
            empires = [
                # (txt_pos, arr_start, arr_end, arch, label_text)
                ((1085, 205), (1085, 242), (1065, 382), -14, "PHÍA BẮC: ĐẾ CHẾ NGA"),
                ((1635, 575), (1495, 575), (1412, 575), 14, "PHÍA ĐÔNG: ẤN ĐỘ"),
                ((690, 745), (835, 720), (1040, 635), 16, "THẾ GIỚI Ả RẬP"),
                ((535, 360), (710, 375), (945, 435), -16, "ĐẾ CHẾ PHƯƠNG TÂY"),
            ]
            for txt_pos, arr_start, arr_end, arch_v, name in empires:
                draw_kinetic_text(img, txt_pos, name, size=25, color=(255, 235, 95), stroke_col=INK, stroke_w=4, bold=True, organic=False, prog=dt / 0.5, safe_box=safe_box)
                draw_curved_arrow(img, arr_start, arr_end, arch=arch_v, prog=dt / 0.65)

        elif act == "OIL_SEA_ERUPT":
            skip_default_chars = True
            draw.ellipse([1045, 625, 1315, 735], fill=(22, 24, 28), outline=(242, 198, 65), width=4)
            draw_kinetic_text(img, (1180, 680), "MỎ DẦU VỊNH BA TƯ", size=22, color=(255, 215, 65), stroke_col=INK, stroke_w=3, bold=True, organic=False, prog=dt / 0.4, safe_box=safe_box)
            draw_kinetic_text(img, (1180, 810), lbl, size=32, color=(255, 228, 75), stroke_col=INK, stroke_w=4, bold=True, organic=True, prog=dt / 0.5, safe_box=safe_box)

        elif act == "WEAVER_CARPET_STAGE":
            c_x0, c_y0, c_x1, c_y1 = stage_cx - 310, 380, stage_cx + 310, 575
            draw.rounded_rectangle([c_x0, c_y0, c_x1, c_y1], radius=14, fill=(168, 36, 42), outline=(242, 198, 65), width=5)
            draw.rounded_rectangle([c_x0 + 20, c_y0 + 20, c_x1 - 20, c_y1 - 20], radius=8, fill=(132, 28, 34), outline=(242, 198, 65), width=3)
            draw_kinetic_text(img, (stage_cx, 225), lbl, size=28, color=(65, 45, 38), organic=True, prog=dt / 0.75, safe_box=safe_box)

        elif act == "POISON_SPIKES_SPROUT":
            for sp_x in range(stage_cx - 235, stage_cx + 255, 58):
                draw.polygon([(sp_x - 14, 520), (sp_x, 405), (sp_x + 14, 520)], fill=(148, 42, 188), outline=INK, width=3)
            # Frameless bold purple keyword pop above carpet (ZERO box!)
            draw_kinetic_text(img, (stage_cx, 295), lbl, size=35, color=(122, 24, 162), bold=True, organic=True, prog=dt / 0.55, safe_box=safe_box)

        elif act == "CHALLENGE_WORLD_STAMP":
            # Frameless bold crimson punchline below carpet so spikes & carpet are 100% visible!
            draw_kinetic_text(img, (stage_cx, 645), lbl, size=36, color=(198, 28, 28), bold=True, organic=True, prog=dt / 0.55, safe_box=safe_box)

        elif act in ("FLY_CARD_1", "FLY_CARD_2", "FLY_CARD_3"):
            c_idx = 0 if act.endswith("1") else (1 if act.endswith("2") else 2)
            col_centers = [stage_cx - int(stage_w * 0.30), stage_cx + 30, stage_cx + int(stage_w * 0.33)]
            cols = [(52, 112, 172), (198, 48, 42), (48, 142, 88)]
            draw_archival_photo_card(
                img, p_file, (col_centers[c_idx], 455), (370, 280),
                lbl, sub_lbl, cols[c_idx], pop_t, safe_box, episode_id, workspace_root
            )

        elif act == "PARADOX_QUESTION_BURST":
            draw_kinetic_text(img, (stage_cx, 255), lbl, size=44, color=(198, 32, 32), bold=True, organic=True, prog=dt / 0.5, safe_box=safe_box)
            for qx, qy in [(stage_cx - 260, 460), (stage_cx + 260, 460), (stage_cx - 200, 345), (stage_cx + 200, 345)]:
                draw_kinetic_text(img, (qx, qy), "?", size=64, color=(198, 42, 42), organic=True)

    # Render Characters (unless custom split-screen already placed them)
    if not skip_default_chars:
        for ch_idx, ch_spec in enumerate(chars):
            role = ch_spec.get("role", "char_ziro_host")
            lbl = ch_spec.get("label", "")
            cx = int(ch_spec.get("x", 220))
            cy = int(ch_spec.get("y", 720))
            sc = float(ch_spec.get("scale", 1.0))
            emo = ch_spec.get("emotion", "explaining")
            neck_px = int(ch_spec.get("neck_insert_px", 35))

            ch_mouth = m_state if ch_idx == 0 else "closed"
            r_arm = "point_right" if cx <= 960 else "down"
            l_arm = "point_left" if cx > 960 else "down"
            prop = "laser_pointer" if role == "char_ziro_host" else None

            paste_char_safe(
                img,
                cx,
                cy,
                role=role,
                emotion=emo,
                mouth=ch_mouth,
                left_arm=l_arm,
                right_arm=r_arm,
                prop_right=prop,
                scale=sc,
                neck_insert_px=neck_px,
                pop_t=min(1.0, (bt + 0.15) / 0.35),
                label=lbl,
                safe_box=safe_box,
            )

    return img


# ==============================================================================
# 4. PHYSICAL BRAND UI ASSET VAULT GENERATOR (`0_kho_dung_chung/brand_ui_assets/`)
# ==============================================================================
def ensure_brand_ui_assets(workspace_root: Path = None) -> dict:
    """
    Materializes channel-wide reusable Brand UI Assets physically on disk inside:
    `2_nguyen_lieu/0_kho_dung_chung/brand_ui_assets/`:
      1. `char_ziro_host/` (6 PNG sprite states + `host_rig_manifest.json`)
      2. `backgrounds_and_scrolls/` (`ziro_studio_gray_1080p.png`, `ziro_master_scroll_1080p.png`)
      3. `arrows_and_markers/` (`arrow_curved_right.png`, `icon_check_green.png`, `icon_cross_red.png`)
      4. `stamps/` (`stamp_red_frame.png`, `stamp_green_frame.png`)
    """
    if workspace_root is None:
        base_proj = Path(r"e:\02_CHANNEL\thu-nghiem\edit-video\2D-Illustrated-History\Du-an-2D-Illustrated-History")
        workspace_root = base_proj / "dung-video-lich-su-hoat-hinh-2d"
    else:
        workspace_root = Path(workspace_root)

    brand_dir = workspace_root / "2_nguyen_lieu" / "0_kho_dung_chung" / "brand_ui_assets"
    host_dir = brand_dir / "char_ziro_host"
    bg_dir = brand_dir / "backgrounds_and_scrolls"
    arr_dir = brand_dir / "arrows_and_markers"
    st_dir = brand_dir / "stamps"
    for d in (host_dir, bg_dir, arr_dir, st_dir):
        d.mkdir(parents=True, exist_ok=True)

    # 1. Ziro Host Character Sprites (6 canonical states)
    host_states = [
        ("host_idle_closed.png", "explaining", "closed", "down", "down", None),
        ("host_talk_half.png", "explaining", "half", "down", "point_right", "laser_pointer"),
        ("host_talk_open.png", "explaining", "open", "down", "point_right", "laser_pointer"),
        ("host_point_right.png", "explaining", "closed", "down", "point_right", "laser_pointer"),
        ("host_shocked_hands_up.png", "shocked", "open", "up", "up", None),
        ("host_stern.png", "angry", "closed", "down", "point_right", "laser_pointer"),
    ]
    for fn, emo, mouth, l_arm, r_arm, prop in host_states:
        out_p = host_dir / fn
        if not out_p.exists():
            spr = get_character_sprite("char_ziro_host", emo, mouth, l_arm, r_arm, prop, 1.0, 35)
            spr.save(out_p, "PNG")

    import json as _json
    rig_manifest = {
        "character_id": "char_ziro_host",
        "brand_palette": {"hoodie_red": "#D93829", "ink_outline": "#222222", "skin_warm": "#F3D9C2"},
        "neck_insert_px": 35,
        "sprites": [s[0] for s in host_states],
    }
    (host_dir / "host_rig_manifest.json").write_text(_json.dumps(rig_manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    # 2. Backgrounds & Master Scroll
    gray_p = bg_dir / "ziro_studio_gray_1080p.png"
    if not gray_p.exists():
        Image.new("RGB", (W, H), (204, 204, 204)).save(gray_p, "PNG")

    scroll_p = bg_dir / "ziro_master_scroll_1080p.png"
    if not scroll_p.exists():
        sc_im = Image.new("RGB", (W, H), (204, 204, 204))
        sd = ImageDraw.Draw(sc_im)
        sd.rounded_rectangle([140, 220, W - 140, H - 220], radius=24, fill=(236, 218, 178), outline=INK, width=5)
        sd.rounded_rectangle([110, 195, 165, H - 195], radius=16, fill=(184, 142, 88), outline=INK, width=4)
        sd.rounded_rectangle([W - 165, 195, W - 110, H - 195], radius=16, fill=(184, 142, 88), outline=INK, width=4)
        sc_im.save(scroll_p, "PNG")

    # 3. Arrows & Markers
    arr_p = arr_dir / "arrow_curved_right.png"
    if not arr_p.exists():
        a_im = Image.new("RGBA", (320, 140), (0, 0, 0, 0))
        draw_curved_arrow(a_im, (20, 90), (295, 60), arch=-24.0, prog=1.0)
        a_im.save(arr_p, "PNG")

    chk_p = arr_dir / "icon_check_green.png"
    if not chk_p.exists():
        c_im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        cd = ImageDraw.Draw(c_im)
        cd.rounded_rectangle([4, 4, 60, 60], radius=10, fill=(42, 152, 78), outline=INK, width=3)
        cd.line([(16, 33), (28, 46), (48, 18)], fill=(255, 255, 255), width=6)
        c_im.save(chk_p, "PNG")

    crs_p = arr_dir / "icon_cross_red.png"
    if not crs_p.exists():
        x_im = Image.new("RGBA", (64, 64), (0, 0, 0, 0))
        xd = ImageDraw.Draw(x_im)
        xd.rounded_rectangle([4, 4, 60, 60], radius=10, fill=(205, 38, 38), outline=INK, width=3)
        xd.line([(18, 18), (46, 46)], fill=(255, 255, 255), width=6)
        xd.line([(46, 18), (18, 46)], fill=(255, 255, 255), width=6)
        x_im.save(crs_p, "PNG")

    # 4. Rubber Stamp Frames
    st_red = st_dir / "stamp_red_frame.png"
    if not st_red.exists():
        sr_im = Image.new("RGBA", (360, 96), (0, 0, 0, 0))
        srd = ImageDraw.Draw(sr_im)
        srd.rounded_rectangle([8, 8, 352, 88], radius=10, fill=(198, 36, 36), outline=INK, width=4)
        sr_im.save(st_red, "PNG")

    st_grn = st_dir / "stamp_green_frame.png"
    if not st_grn.exists():
        sg_im = Image.new("RGBA", (360, 96), (0, 0, 0, 0))
        sgd = ImageDraw.Draw(sg_im)
        sgd.rounded_rectangle([8, 8, 352, 88], radius=10, fill=(42, 148, 78), outline=INK, width=4)
        sg_im.save(st_grn, "PNG")

    return {
        "brand_dir": str(brand_dir),
        "files_count": sum(1 for _ in brand_dir.rglob("*") if _.is_file()),
    }


if __name__ == "__main__":
    res = ensure_brand_ui_assets()
    print(f"[BRAND UI ASSETS READY] {res['brand_dir']} ({res['files_count']} files)")
