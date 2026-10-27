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
    base_proj = Path(__file__).resolve().parents[4] / "Du-an-2D-Illustrated-History"
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
    blink: bool = False,
    leg_phase: int = 0,
) -> Image.Image:
    key = (role, emotion, mouth, left_arm, right_arm, prop_right, round(scale, 2), int(neck_insert_px), bool(blink), int(leg_phase))
    if key in _SPRITE_CACHE:
        return _SPRITE_CACHE[key]

    ss = 2
    cw, ch = int(340 * scale), int(410 * scale)
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
    skin = (224, 178, 128) if role == "hollywood_xerxes" else SKIN

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
    elif role in ("char_persian_king", "emperor_xerxes", "king"):
        shirt_col = (118, 44, 142)
        inner_col = (238, 192, 62)
        accent_col = (215, 45, 45)
        hair_col = (35, 28, 26)
        w_bot = s(64)
    elif role in ("general", "messenger"):
        shirt_col = (76, 98, 62)
        inner_col = (158, 134, 88)
        accent_col = (198, 162, 64)
        hair_col = (38, 32, 28)
    elif role == "scholar":
        shirt_col = (242, 238, 228)
        inner_col = (54, 108, 168)
        accent_col = (218, 178, 68)
        hair_col = (225, 225, 225)
    elif role == "hollywood_xerxes":
        shirt_col = (218, 168, 96)
        inner_col = (238, 192, 62)
        accent_col = (245, 205, 68)
        hair_col = (35, 28, 26)
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

    # Back Cape for Spartan or Persian King
    if role == "spartan":
        draw.polygon(
            [(cx - s(46), sh_y + s(6)), (cx + s(46), sh_y + s(6)), (cx + s(64), by - s(18)), (cx - s(64), by - s(18))],
            fill=(192, 28, 28),
            outline=INK,
            width=s(3.0),
        )
    elif role in ("char_persian_king", "emperor_xerxes", "king"):
        draw.polygon(
            [(cx - s(48), sh_y + s(8)), (cx + s(48), sh_y + s(8)), (cx + s(60), by - s(20)), (cx - s(60), by - s(20))],
            fill=(92, 28, 114),
            outline=INK,
            width=s(3.0),
        )
    elif role in ("char_ziro_host", "mascot_time_traveler"):
        draw.ellipse(
            [cx - s(42), sh_y - s(16), cx + s(42), sh_y + s(18)],
            fill=(182, 42, 30),
            outline=INK,
            width=s(3.0),
        )

    leg_dx = s(19)
    for idx_l, lx in enumerate((cx - leg_dx, cx + leg_dx)):
        swing_x = s(10 * leg_phase * (1 if idx_l == 0 else -1))
        swing_y = -s(5 * abs(leg_phase)) if ((idx_l == 0 and leg_phase > 0) or (idx_l == 1 and leg_phase < 0)) else 0
        foot_x = lx + swing_x
        foot_y = by + swing_y
        draw_thick_line_ss(draw, (lx, hip_y - s(4)), (foot_x, foot_y - s(6)), INK, 4.8 * scale, ss)
        sr_x, sr_y = s(14), s(6.5)
        draw.ellipse([foot_x - sr_x, foot_y - sr_y * 2, foot_x + sr_x, foot_y], fill=INK)

    def draw_arm(side: str, mode: str):
        sign = -1 if side == "left" else 1
        ax0 = cx + sign * (w_top - s(10))
        ay0 = sh_y + s(16)
        sleeve_col = skin if role in ("spartan", "hollywood_xerxes") else shirt_col

        if mode == "down":
            ax1, ay1 = ax0 + sign * s(20), hip_y - s(6)
        elif mode == "point_left":
            ax1, ay1 = ax0 - s(64), ay0 - s(4)
        elif mode == "point_right":
            ax1, ay1 = ax0 + s(64), ay0 - s(4)
        elif mode == "up":
            ax1, ay1 = ax0 + sign * s(38), ay0 - s(52)
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

    l_hand = draw_arm("left", left_arm)
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
    elif role in ("general", "messenger"):
        # Segmented military armor plates like Ziro's Sui General & Messenger at 05:00
        for row_y in range(sh_y + s(24), hip_y - s(12), s(20)):
            draw.line([(cx - w_top + s(4), row_y), (cx + w_top - s(4), row_y)], fill=INK, width=s(2.4))
        draw.rectangle([cx - w_top, hip_y - s(24), cx + w_top, hip_y - s(10)], fill=(128, 92, 54), outline=INK, width=s(2.4))
        draw.rectangle([cx - s(10), hip_y - s(26), cx + s(10), hip_y - s(8)], fill=accent_col, outline=INK, width=s(2.2))
    elif role in ("char_persian_king", "emperor_xerxes", "king"):
        draw.polygon(
            [(cx - s(22), sh_y + s(2)), (cx + s(22), sh_y + s(2)), (cx + s(16), hip_y), (cx - s(16), hip_y)],
            fill=inner_col,
            outline=INK,
            width=s(2.6),
        )
        draw.rectangle([cx - w_top, hip_y - s(26), cx + w_top, hip_y - s(12)], fill=accent_col, outline=INK, width=s(2.4))
    elif role == "spartan":
        # Red Spartan trunks + 6-pack oiled abs
        draw.rounded_rectangle([cx - w_top, hip_y - s(36), cx + w_top, hip_y + s(4)], radius=s(8), fill=(208, 32, 32), outline=INK, width=s(3.0))
        draw.line([(cx - w_top, hip_y - s(36)), (cx + w_top, hip_y - s(36))], fill=accent_col, width=s(4.0))
        # Pectorals & 6-pack abs
        draw.arc([cx - s(34), sh_y + s(12), cx - s(2), sh_y + s(42)], 10, 170, fill=INK, width=s(2.4))
        draw.arc([cx + s(2), sh_y + s(12), cx + s(34), sh_y + s(42)], 10, 170, fill=INK, width=s(2.4))
        for ab_i in range(3):
            aby = sh_y + s(46 + ab_i * 15)
            draw.rounded_rectangle([cx - s(20), aby, cx - s(2), aby + s(12)], radius=s(4), fill=(252, 224, 192), outline=INK, width=s(2.0))
            draw.rounded_rectangle([cx + s(2), aby, cx + s(20), aby + s(12)], radius=s(4), fill=(252, 224, 192), outline=INK, width=s(2.0))
    elif role == "hollywood_xerxes":
        # Golden crossed chains & collar + golden loincloth
        draw.rounded_rectangle([cx - w_top, hip_y - s(38), cx + w_top, hip_y + s(4)], radius=s(8), fill=accent_col, outline=INK, width=s(3.0))
        draw.ellipse([cx - s(38), sh_y - s(4), cx + s(38), sh_y + s(28)], fill=accent_col, outline=INK, width=s(2.8))
        draw_thick_line_ss(draw, (cx - s(38), sh_y + s(18)), (cx + s(38), hip_y - s(38)), accent_col, 5.0 * scale, ss)
        draw_thick_line_ss(draw, (cx + s(38), sh_y + s(18)), (cx - s(38), hip_y - s(38)), accent_col, 5.0 * scale, ss)
    elif role == "scholar":
        # Greek blue sash drape across white chiton
        draw.polygon(
            [(cx - w_top + s(4), sh_y + s(6)), (cx - s(10), sh_y + s(4)), (cx + w_top - s(4), hip_y - s(8)), (cx + s(6), hip_y - s(4))],
            fill=inner_col,
            outline=INK,
            width=s(2.6),
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
        if role == "hollywood_xerxes":
            # Gold hoop earrings
            draw.ellipse([ex - s(8), head_cy + s(4), ex + s(8), head_cy + s(20)], outline=(250, 205, 55), width=s(3.0))

    draw.ellipse([cx - hr_x, head_cy - hr_y, cx + hr_x, head_cy + hr_y], fill=skin, outline=INK, width=s(3.4))

    if role in ("char_iran_cleric", "cleric", "scholar"):
        b_col = (235, 235, 235)
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
        draw.polygon(beard_pts, fill=b_col, outline=INK, width=s(3))
    elif role in ("char_persian_king", "emperor_xerxes", "king", "general"):
        b_col = (36, 30, 28)
        beard_pts = [
            (cx - hr_x + s(4), head_cy + s(4)),
            (cx - s(18), head_cy + s(12)),
            (cx, head_cy + s(9)),
            (cx + s(18), head_cy + s(12)),
            (cx + hr_x - s(4), head_cy + s(4)),
            (cx + s(22), head_cy + hr_y + s(14)),
            (cx, head_cy + hr_y + s(20)),
            (cx - s(22), head_cy + hr_y + s(14)),
        ]
        draw.polygon(beard_pts, fill=b_col, outline=INK, width=s(2.8))

    eye_y = head_cy - s(4)
    eye_dx = s(12.5)
    er_x, er_y = s(3.8), s(4.8)
    for ex in (cx - eye_dx, cx + eye_dx):
        if blink:
            draw_thick_line_ss(draw, (ex - s(5.5), eye_y), (ex + s(5.5), eye_y), INK, 2.8 * scale, ss)
        else:
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
    if mouth == "open":
        draw.ellipse([cx - s(7.5), my - s(5.5), cx + s(7.5), my + s(6.5)], fill=(195, 52, 52), outline=INK, width=s(2.4))
    elif mouth == "half":
        draw.ellipse([cx - s(5.5), my - s(3), cx + s(5.5), my + s(3.5)], fill=(195, 52, 52), outline=INK, width=s(2.2))
    elif mouth == "smile" or emotion in ("smug", "proud"):
        draw.arc([cx - s(10), my - s(7), cx + s(10), my + s(5)], 10, 170, fill=INK, width=s(2.8))
    elif emotion in ("stern", "angry"):
        draw.arc([cx - s(10), my - s(2), cx + s(10), my + s(9)], 195, 345, fill=INK, width=s(2.8))
    else:
        draw_thick_line_ss(draw, (cx - s(8), my), (cx + s(8), my), INK, 2.6 * scale, ss)

    if role == "hollywood_xerxes":
        # Facial piercings all over nose, eyebrows, cheeks & chin
        for px_p, py_p in [
            (cx, head_cy + s(6)), (cx - s(18), eb_y - s(3)), (cx + s(18), eb_y - s(3)),
            (cx - s(22), head_cy + s(10)), (cx + s(22), head_cy + s(10)), (cx, my + s(10))
        ]:
            draw.ellipse([px_p - s(3.5), py_p - s(3.5), px_p + s(3.5), py_p + s(3.5)], fill=(255, 215, 55), outline=INK, width=s(1.6))

    # Headgear / Hair
    if role in ("char_ziro_host", "mascot_time_traveler"):
        draw.chord(
            [cx - hr_x - s(2), head_cy - hr_y - s(8), cx + hr_x + s(4), head_cy - s(10)],
            175,
            365,
            fill=hair_col,
            outline=INK,
            width=s(3),
        )
    elif role in ("char_persian_king", "emperor_xerxes", "king"):
        # Golden fluted Persian Imperial Crown (Kidaris)
        cr_y = head_cy - hr_y + s(6)
        crown_pts = [
            (cx - hr_x, cr_y),
            (cx - hr_x - s(6), cr_y - s(28)),
            (cx - s(18), cr_y - s(18)),
            (cx - s(9), cr_y - s(32)),
            (cx, cr_y - s(20)),
            (cx + s(9), cr_y - s(32)),
            (cx + s(18), cr_y - s(18)),
            (cx + hr_x + s(6), cr_y - s(28)),
            (cx + hr_x, cr_y),
        ]
        draw.polygon(crown_pts, fill=(245, 198, 52), outline=INK, width=s(3.0))
        draw.rectangle([cx - hr_x, cr_y - s(8), cx + hr_x, cr_y + s(2)], fill=(208, 42, 42), outline=INK, width=s(2.4))
    elif role in ("general", "messenger"):
        # Conical bronze military helmet with top knob (matching 05:00 Sui General/Messenger)
        hm_y = head_cy - hr_y + s(8)
        draw.chord([cx - hr_x - s(4), head_cy - hr_y - s(16), cx + hr_x + s(4), hm_y + s(10)], 180, 360, fill=(118, 126, 134), outline=INK, width=s(3.0))
        draw.ellipse([cx - s(6), head_cy - hr_y - s(24), cx + s(6), head_cy - hr_y - s(12)], fill=(198, 42, 42), outline=INK, width=s(2.4))
    elif role == "spartan":
        # Corinthian helmet crest on top of head
        draw.chord([cx - s(18), head_cy - hr_y - s(28), cx + s(18), head_cy - hr_y + s(6)], 180, 360, fill=(212, 34, 34), outline=INK, width=s(2.8))
        draw.rectangle([cx - hr_x, head_cy - hr_y - s(2), cx + hr_x, head_cy - hr_y + s(8)], fill=(212, 168, 78), outline=INK, width=s(2.6))
    elif role == "scholar":
        # Greek olive laurel wreath
        for sgn in (-1, 1):
            draw.arc([cx - hr_x - s(4), head_cy - hr_y - s(4), cx + hr_x + s(4), head_cy], 190 if sgn < 0 else 280, 260 if sgn < 0 else 350, fill=(58, 142, 68), width=s(4.0))
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
    elif prop_right == "scroll":
        # Dispatch letter / envelope with red wax seal (matching 05:00 Messenger!)
        ex0, ey0, ex1, ey1 = px - s(24), py - s(16), px + s(24), py + s(16)
        draw.rectangle([ex0, ey0, ex1, ey1], fill=(250, 248, 242), outline=INK, width=s(2.6))
        draw.line([(ex0, ey0), (px, py + s(2)), (ex1, ey0)], fill=INK, width=s(2.2))
        draw.ellipse([px - s(5), py - s(3), px + s(5), py + s(7)], fill=(208, 36, 36), outline=INK, width=s(1.8))
    elif prop_right == "scepter":
        draw_thick_line_ss(draw, (px, py + s(28)), (px, py - s(52)), (238, 192, 52), 4.5 * scale, ss)
        draw.ellipse([px - s(10), py - s(64), px + s(10), py - s(44)], fill=(248, 205, 58), outline=INK, width=s(2.6))
    elif prop_right == "quill":
        draw_thick_line_ss(draw, (px - s(4), py + s(8)), (px + s(28), py - s(34)), (248, 248, 245), 4.0 * scale, ss)
        draw.polygon([(px + s(8), py - s(12)), (px + s(34), py - s(42)), (px + s(18), py - s(6))], fill=(252, 252, 250), outline=INK, width=s(2.2))
    elif prop_right == "shield":
        draw.ellipse([px - s(28), py - s(32), px + s(28), py + s(32)], fill=(212, 162, 68), outline=INK, width=s(3.0))

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
    bt: float = 0.0,
    walk_vx: float = 0.0,
    walk_start_bt: float = 0.0,
    hide_label: bool = False,
):
    if pop_t <= 0.01:
        return
    sc_eff = scale * (ease_out_back(pop_t, 1.18) if pop_t < 1.0 else 1.0)
    sc_eff = max(0.2, sc_eff)

    # Periodic Auto Eye-Blink (every 3.1s, phase-offset by character X coordinate)
    blink_cycle = (bt + (x * 0.0023)) % 3.1
    is_blinking = (1.85 <= blink_cycle <= 1.99)

    # Walk-cycle leg stride & horizontal motion if walk_vx != 0
    leg_phase = 0
    dx_walk = 0
    if abs(walk_vx) > 0.5 and bt > walk_start_bt:
        w_dt = bt - walk_start_bt
        dx_walk = int(round(walk_vx * w_dt))
        leg_phase = 1 if math.sin(w_dt * 14.0) >= 0 else -1

    # Subtle speech bobbing (2.5px vertical bounce when speaking)
    bob_dy = int(round(2.5 * math.sin(bt * 16.0))) if mouth in ("open", "half") else 0

    spr = get_character_sprite(
        role, emotion, mouth, left_arm, right_arm, prop_right, sc_eff, neck_insert_px,
        blink=is_blinking, leg_phase=leg_phase
    )
    sw, sh = spr.size

    cx, foot_y = int(x + dx_walk), int(y + 135 * sc_eff + bob_dy)
    if safe_box:
        sx0, sy0, sx1, sy1 = safe_box
        half_vis_w = int(sw * 0.42)
        cx = max(sx0 + half_vis_w, min(sx1 - half_vis_w, cx))
        foot_y = max(sy0 + sh, min(sy1 + 30, foot_y))

    px = int(cx - sw // 2)
    py = int(foot_y - sh)
    canvas.paste(spr, (px, py), spr)

    if label and not hide_label and role != "char_ziro_host":
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


def draw_skit_overhead_speech(
    img: Image.Image,
    pos,
    text: str,
    size: int = 28,
    color=(252, 252, 248),
    stroke_col=INK,
    stroke_w: int = 3,
    opacity: float = 1.0,
    prog: float = 1.0,
    show_tick: bool = True,
    tick_dir: int = 0,
    safe_box=None,
):
    """
    Renders Ziro History's signature Overhead Skit Dialogue Typography (matching 02:10, 05:00, 13:56):
      - Natural sentence-case multiline text directly above the speaker's head.
      - Supports Turn-Taking Dimming (`opacity = 0.38` for the previous speaker's held line, `1.0` for current speaker).
      - Draws a crisp 14px pointer tick pointing down toward the speaker's head.
    """
    if prog <= 0.01 or opacity <= 0.02 or not text:
        return
    n_chars = max(1, int(round(len(text) * clamp01(prog))))
    sub_text = text[:n_chars]
    lines_full = [ln.strip() for ln in text.split("\n") if ln.strip()]
    lines_sub = sub_text.split("\n")

    font = get_font(size, bold=True, organic=True)
    dummy = ImageDraw.Draw(img)
    line_h = int(size * 1.32)
    max_w = 0
    for ln in lines_full:
        bb = dummy.textbbox((0, 0), ln, font=font)
        max_w = max(max_w, bb[2] - bb[0])
    total_h = len(lines_full) * line_h

    cx, cy = int(pos[0]), int(pos[1])
    if safe_box:
        sx0, sy0, sx1, sy1 = safe_box
        cx = max(sx0 + max_w // 2 + 20, min(sx1 - max_w // 2 - 20, cx))
        cy = max(sy0 + total_h // 2 + 10, min(sy1 - total_h // 2 - 24, cy))

    overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    odraw = ImageDraw.Draw(overlay)
    alpha = max(0, min(255, int(round(255 * clamp01(opacity)))))
    fill_rgba = (color[0], color[1], color[2], alpha)
    stroke_rgba = (stroke_col[0], stroke_col[1], stroke_col[2], alpha)

    start_y = cy - total_h // 2
    for idx_l, ln_sub in enumerate(lines_sub):
        if idx_l >= len(lines_full):
            break
        ln_full = lines_full[idx_l]
        bb = odraw.textbbox((0, 0), ln_full, font=font)
        lw = bb[2] - bb[0]
        lx = cx - lw // 2
        ly = start_y + idx_l * line_h
        odraw.text((lx, ly), ln_sub, font=font, fill=fill_rgba, stroke_width=int(stroke_w), stroke_fill=stroke_rgba)

    if show_tick and prog > 0.15:
        ty0 = start_y + total_h + 6
        ty1 = ty0 + 15
        tx0 = cx + int(tick_dir * 8)
        tx1 = cx + int(tick_dir * 3)
        odraw.line([(tx0, ty0), (tx1, ty1)], fill=stroke_rgba, width=6)
        odraw.line([(tx0, ty0), (tx1, ty1)], fill=fill_rgba, width=3)

    img_rgba = img.convert("RGBA")
    composited = Image.alpha_composite(img_rgba, overlay)
    img.paste(composited.convert("RGB"), (0, 0))


def draw_skit_stage_bg(
    img: Image.Image,
    stage_type: str,
    bt: float,
    episode_id: str = "EP01_Iran",
    workspace_root: Path = None,
):
    """
    Renders Full-Screen 2D Illustrated Skit Environments (1920x1080) modeled directly on
    Ziro History's 02:10 (Cave), 05:00 (Sui Command Tent & Study), and 13:56 (Map Table & Night Office).
    """
    draw = ImageDraw.Draw(img)

    if stage_type == "PERSIAN_COMMAND_TENT":
        # Modeled directly on 05:00 Sui General Command Tent (+5s..+13s, +22s..+23s)
        floor_y = 665
        draw.rectangle([0, 0, W, floor_y], fill=(216, 198, 162))
        draw.rectangle([0, floor_y, W, H], fill=(142, 98, 64))
        # Tent vertical fabric panel seams
        for sx in (310, 680, 1240, 1610):
            draw.line([(sx, 0), (sx, floor_y)], fill=(156, 138, 108), width=2)
        # Diagonal wooden tent roof beams (top left & right, exactly like 05:00)
        draw.polygon([(0, 62), (480, 0), (590, 0), (0, 86)], fill=(116, 76, 46), outline=INK, width=3)
        draw.polygon([(W, 62), (W - 480, 0), (W - 590, 0), (W, 86)], fill=(116, 76, 46), outline=INK, width=3)
        draw.line([(0, floor_y), (W, floor_y)], fill=INK, width=4)
        # Center Wooden War Table with rolled tactical map on top
        tx0, ty0, tx1, ty1 = 590, 560, 1180, floor_y
        draw.rectangle([tx0 + 25, ty0 + 28, tx0 + 48, ty1], fill=(104, 66, 38), outline=INK, width=3)
        draw.rectangle([tx1 - 48, ty0 + 28, tx1 - 25, ty1], fill=(104, 66, 38), outline=INK, width=3)
        draw.rectangle([tx0, ty0, tx1, ty0 + 30], fill=(128, 84, 50), outline=INK, width=3)
        # Unrolled white/sand scroll map lying flat on the table
        draw.rectangle([tx0 + 115, ty0 - 14, tx1 - 115, ty0], fill=(246, 242, 232), outline=INK, width=2)
        draw.ellipse([tx0 + 108, ty0 - 16, tx0 + 124, ty0 + 2], fill=(235, 228, 212), outline=INK, width=2)
        draw.ellipse([tx1 - 124, ty0 - 16, tx1 - 108, ty0 + 2], fill=(235, 228, 212), outline=INK, width=2)
        # Right Military Pennant Flag on Pole (like the green flag at x=1360 in 05:00)
        fx = 1390
        draw.rectangle([fx - 5, 235, fx + 5, floor_y], fill=(112, 74, 44), outline=INK, width=2)
        wave_dy = int(round(6.0 * math.sin(bt * 4.5)))
        draw.polygon([(fx + 5, 245), (fx + 145, 285 + wave_dy), (fx + 5, 345)], fill=(76, 138, 68), outline=INK, width=3)

    elif stage_type == "THERMOPYLAE_MAP_DESK":
        # Modeled directly on 13:56 (+0s..+5s) Tactical Map lying on a Wooden Desk
        draw.rectangle([0, 0, W, H], fill=(134, 84, 48))
        for py in range(95, H, 105):
            draw.line([(0, py), (W, py)], fill=(96, 58, 32), width=2)
        # Gold-bordered Tactical Map sheet in center of table
        mx0, my0, mx1, my1 = 440, 65, 1480, 1015
        draw.rectangle([mx0 + 8, my0 + 10, mx1 + 8, my1 + 10], fill=(78, 48, 26))
        draw.rectangle([mx0, my0, mx1, my1], fill=(242, 202, 82), outline=INK, width=4)
        sat = get_cached_image("01_beat01_0219s-0226s_satellite_thermopylae_pass.jpg", (mx1 - mx0 - 36, my1 - my0 - 36), episode_id, workspace_root)
        img.paste(sat, (mx0 + 18, my0 + 18))
        draw.rectangle([mx0 + 18, my0 + 18, mx1 - 18, my1 - 18], outline=INK, width=3)

    elif stage_type == "SPARTAN_STAGE_SPOTLIGHT":
        # Full-screen Persian Tent interior + theatrical inspection spotlight in center
        draw_skit_stage_bg(img, "PERSIAN_COMMAND_TENT", bt, episode_id, workspace_root)
        draw = ImageDraw.Draw(img)
        # Warm spotlight cone on center stage for inspecting the 300 Spartans
        poly_spot = [(720, 0), (1200, 0), (1380, 880), (540, 880)]
        overlay = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        odraw = ImageDraw.Draw(overlay)
        odraw.polygon(poly_spot, fill=(255, 242, 185, 65))
        img_rgba = img.convert("RGBA")
        img.paste(Image.alpha_composite(img_rgba, overlay).convert("RGB"), (0, 0))

    elif stage_type == "GREEK_HISTORIAN_STUDY":
        # Modeled on 05:00 (+2s..+4s) & 13:56 (+6s..+12s): Indoor Study Room with Desk & Night Window
        floor_y = 675
        draw.rectangle([0, 0, W, floor_y], fill=(118, 124, 134))
        draw.rectangle([0, floor_y, W, H], fill=(108, 76, 52))
        draw.line([(0, floor_y), (W, floor_y)], fill=INK, width=4)
        # Night window on top-right (just like 13:56 +6s..+12s!)
        wx0, wy0, wx1, wy1 = 1380, 140, 1650, 430
        draw.rectangle([wx0, wy0, wx1, wy1], fill=(24, 34, 58), outline=(245, 245, 242), width=6)
        draw.ellipse([wx1 - 75, wy0 + 30, wx1 - 30, wy0 + 75], fill=(252, 244, 188))
        draw.rectangle([wx0 + 35, wy0 + 130, wx0 + 85, wy1], fill=(16, 20, 32))
        draw.rectangle([wx0 + 145, wy0 + 95, wx0 + 205, wy1], fill=(16, 20, 32))
        draw.line([(wx0, (wy0 + wy1) // 2), (wx1, (wy0 + wy1) // 2)], fill=(245, 245, 242), width=5)
        draw.line([((wx0 + wx1) // 2, wy0), ((wx0 + wx1) // 2, wy1)], fill=(245, 245, 242), width=5)
        # Historian's Wooden Desk in left-center
        dx0, dy0, dx1, dy1 = 310, 585, 830, 835
        draw.rectangle([dx0, dy0, dx1, dy1], fill=(132, 88, 54), outline=INK, width=4)
        draw.rectangle([dx0 - 15, dy0 - 18, dx1 + 15, dy0 + 6], fill=(152, 104, 64), outline=INK, width=3)

    elif stage_type == "HOLLYWOOD_VS_REALITY_STAGE":
        # Split 50/50 Full-Screen Stage: Left = Civilized 480 BC Tent | Right = Dark Neon Hollywood 300 Set
        floor_y = 685
        # Left half: Warm Persian Royal Court
        draw.rectangle([0, 0, 960, floor_y], fill=(222, 206, 172))
        draw.rectangle([0, floor_y, 960, H], fill=(148, 104, 68))
        # Right half: Dark Red/Black Hollywood Fantasy Set
        draw.rectangle([960, 0, W, floor_y], fill=(38, 24, 32))
        draw.rectangle([960, floor_y, W, H], fill=(58, 32, 38))
        draw.line([(0, floor_y), (W, floor_y)], fill=INK, width=4)
        draw.line([(960, 0), (960, H)], fill=(245, 245, 242), width=6)

    elif stage_type == "PERSIAN_TENT_TO_MODERN_CINEMA":
        # At bt < 2.05s: Inside Persian Command Tent (Xerxes says "Chẳng ai lại đi tin mấy thứ vớ vẩn đó đâu")
        # At bt >= 2.05s: Hard cut to Modern Movie Theater where audience in 3D glasses believes every word!
        if bt < 2.05:
            draw_skit_stage_bg(img, "PERSIAN_COMMAND_TENT", bt, episode_id, workspace_root)
        else:
            draw.rectangle([0, 0, W, H], fill=(24, 26, 36))
            # Giant Glowing Movie Screen in Theater
            sx0, sy0, sx1, sy1 = 340, 75, 1580, 585
            draw.rounded_rectangle([sx0 - 8, sy0 - 8, sx1 + 8, sy1 + 8], radius=12, fill=(245, 205, 65), outline=INK, width=4)
            ph = get_cached_image("03_beat04_0235s-0244s_spartan_red_trunks_baby_oil.jpg", (sx1 - sx0, sy1 - sy0), episode_id, workspace_root)
            img.paste(ph, (sx0, sy0))
            draw.rectangle([sx0, sy0, sx1, sy0 + 62], fill=(198, 28, 28))
            draw_kinetic_text(img, (960, sy0 + 31), "HOLLYWOOD: \"300\" — DOANH THU $456,000,000!", size=28, color=(255, 255, 255), bold=True, organic=False)
            # Row of crimson cinema seats & audience silhouettes at bottom
            for seat_x in range(260, 1700, 230):
                draw.rounded_rectangle([seat_x - 75, 760, seat_x + 75, 980], radius=18, fill=(148, 28, 38), outline=INK, width=3)


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
            dark = ImageEnhance.Brightness(sat).enhance(float(trig.get("darken_factor", 0.62)))
            mask = Image.new("L", (W, H), 0)
            mdraw = ImageDraw.Draw(mask)
            raw_poly = trig.get("polygon_pts") or beat_data.get("map_polygon_pts")
            if raw_poly and len(raw_poly) >= 3:
                iran_poly = [(int(pt[0]), int(pt[1])) for pt in raw_poly]
            else:
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
            map_title = trig.get("map_title", "I R A N")
            map_title_xy = trig.get("map_title_xy", [1205, 575])
            draw_kinetic_text(img, (int(map_title_xy[0]), int(map_title_xy[1])), map_title, size=42, color=(255, 245, 215), stroke_col=INK, stroke_w=4, bold=True, organic=False, prog=dt / 0.45, safe_box=safe_box)

            # Tách biệt hoàn toàn tọa độ đặt chữ (txt_pos) và tọa độ gốc mũi tên (arr_start) để 0 mũi tên nào đè lên chữ!
            custom_arrows = trig.get("arrows_list") or beat_data.get("map_arrows_list")
            if custom_arrows:
                empires = [
                    (
                        (int(a["txt_pos"][0]), int(a["txt_pos"][1])),
                        (int(a["arr_start"][0]), int(a["arr_start"][1])),
                        (int(a["arr_end"][0]), int(a["arr_end"][1])),
                        float(a.get("arch", -14)),
                        str(a.get("label", "")),
                    )
                    for a in custom_arrows
                ]
            else:
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

        # ------------------------------------------------------------------
        # G. UNIVERSAL ATOMIC SCENE-GRAPH PRIMITIVES (For Episode 2, 3, N — Zero Code Edits)
        # ------------------------------------------------------------------
        elif act == "ATOMIC_BG_IMAGE":
            if trig.get("hide_default_chars", False):
                skip_default_chars = True
            sat = get_cached_image(p_file, (W, H), episode_id, workspace_root).copy()
            darken = float(trig.get("darken_factor", 1.0))
            if darken < 0.99:
                dark = ImageEnhance.Brightness(sat).enhance(darken)
                poly_pts = trig.get("polygon_pts")
                if poly_pts and len(poly_pts) >= 3:
                    mask = Image.new("L", (W, H), 0)
                    ImageDraw.Draw(mask).polygon([(int(p[0]), int(p[1])) for p in poly_pts], fill=255)
                    dark.paste(sat, (0, 0), mask)
                    img.paste(dark, (0, 0))
                    draw = ImageDraw.Draw(img)
                    draw.polygon([(int(p[0]), int(p[1])) for p in poly_pts], outline=(255, 215, 65), width=5)
                else:
                    img.paste(dark, (0, 0))
                    draw = ImageDraw.Draw(img)
            else:
                img.paste(sat, (0, 0))
                draw = ImageDraw.Draw(img)

        elif act in ("ATOMIC_PROP_CARD", "ATOMIC_CUTOUT_PROP"):
            px = int(trig.get("x", stage_cx))
            py = int(trig.get("y", 480))
            pw = int(trig.get("w", 460))
            ph_h = int(trig.get("h", 340))
            anim_style = trig.get("anim_style", "pop")
            if anim_style == "slide_left":
                px = int(px - (1.0 - ease_out_cubic(min(1.0, dt / 0.45))) * 520)
            elif anim_style == "slide_right":
                px = int(px + (1.0 - ease_out_cubic(min(1.0, dt / 0.45))) * 520)
            elif anim_style == "slam_drop":
                py = int(py - (1.0 - ease_out_bounce(min(1.0, dt / 0.45))) * 480)
            b_col = tuple(trig.get("badge_col", [52, 112, 172]))
            draw_archival_photo_card(
                img, p_file, (px, py), (pw, ph_h),
                lbl, sub_lbl, b_col, pop_t, safe_box, episode_id, workspace_root
            )

        elif act == "ATOMIC_ACTOR":
            paste_char_safe(
                img,
                int(trig.get("x", stage_cx)),
                int(trig.get("y", 720)),
                role=trig.get("role", "char_historic"),
                emotion=trig.get("emotion", "explaining"),
                mouth=m_state if trig.get("lip_sync", False) else "closed",
                left_arm=trig.get("left_arm", "down"),
                right_arm=trig.get("right_arm", "point_right"),
                prop_right=trig.get("prop_right", None),
                scale=float(trig.get("scale", 0.95)),
                neck_insert_px=int(trig.get("neck_insert_px", 35)),
                pop_t=pop_t,
                label=lbl,
                safe_box=safe_box,
            )

        elif act == "ATOMIC_VECTOR_ARROW":
            st_xy = trig.get("arr_start", [stage_cx - 220, 420])
            en_xy = trig.get("arr_end", [stage_cx + 120, 420])
            arch_v = float(trig.get("arch", -22.0))
            draw_curved_arrow(img, (int(st_xy[0]), int(st_xy[1])), (int(en_xy[0]), int(en_xy[1])), arch=arch_v, prog=dt / 0.55)
            if lbl:
                t_xy = trig.get("txt_pos", [int(st_xy[0]), int(st_xy[1]) - 36])
                t_col = tuple(trig.get("color", [22, 22, 22]))
                draw_kinetic_text(img, (int(t_xy[0]), int(t_xy[1])), lbl, size=int(trig.get("size", 26)), color=t_col, bold=True, organic=False, prog=dt / 0.45, safe_box=safe_box)

        elif act == "ATOMIC_VECTOR_SHAPE":
            shape_kind = trig.get("shape", "jail_bars")
            if shape_kind == "jail_bars":
                bar_h = int(H * ease_out_cubic(min(1.0, dt / 0.35)))
                bx0 = int(trig.get("x0", sx0 + 40))
                bx1 = int(trig.get("x1", sx1 - 20))
                for bx in range(bx0, bx1, 125):
                    draw.line([(bx, 0), (bx, bar_h)], fill=(95, 100, 108), width=10)
            elif shape_kind == "red_cross":
                cx_s, cy_s = int(trig.get("x", stage_cx)), int(trig.get("y", 480))
                rad = int(trig.get("radius", 140) * min(1.0, dt / 0.3))
                draw.line([(cx_s - rad, cy_s - rad), (cx_s + rad, cy_s + rad)], fill=(205, 32, 32), width=14)
                draw.line([(cx_s + rad, cy_s - rad), (cx_s - rad, cy_s + rad)], fill=(205, 32, 32), width=14)
            elif shape_kind == "split_line":
                lx1, ly1 = trig.get("p1", [stage_cx, 160])
                lx2, ly2 = trig.get("p2", [stage_cx, floor_y])
                p_line = ease_out_cubic(min(1.0, dt / 0.4))
                cur_x2 = int(lx1 + (lx2 - lx1) * p_line)
                cur_y2 = int(ly1 + (ly2 - ly1) * p_line)
                draw.line([(int(lx1), int(ly1)), (cur_x2, cur_y2)], fill=tuple(trig.get("color", [205, 32, 32])), width=int(trig.get("width", 6)))
            elif shape_kind == "radar_pin":
                rx, ry = int(trig.get("x", stage_cx)), int(trig.get("y", 520))
                pulse_r = int(20 + 28 * ((bt * 2.2) % 1.0))
                draw.ellipse([rx - pulse_r, ry - pulse_r, rx + pulse_r, ry + pulse_r], outline=(235, 45, 45), width=4)
                draw.ellipse([rx - 10, ry - 10, rx + 10, ry + 10], fill=(235, 45, 45), outline=INK, width=2)
            if lbl:
                draw_kinetic_text(img, (int(trig.get("x", stage_cx)), int(trig.get("y", 520)) - 48), lbl, size=int(trig.get("size", 32)), color=tuple(trig.get("color", [205, 32, 32])), bold=True, organic=True, prog=dt / 0.45, safe_box=safe_box)

        elif act == "ATOMIC_KINETIC_TEXT":
            tx, ty = int(trig.get("x", stage_cx)), int(trig.get("y", 280))
            t_col = tuple(trig.get("color", [22, 22, 22]))
            t_size = int(trig.get("size", 36))
            if trig.get("is_stamp", False):
                draw_stamp(img, (tx, ty), lbl, bg_col=t_col, txt_col=(255, 255, 255), size=t_size, pop_t=pop_t, safe_box=safe_box)
            else:
                draw_kinetic_text(
                    img, (tx, ty), lbl, size=t_size, color=t_col,
                    stroke_col=INK if trig.get("stroke", False) else None,
                    stroke_w=int(trig.get("stroke_w", 3)),
                    bold=bool(trig.get("bold", True)),
                    organic=bool(trig.get("organic", True)),
                    prog=dt / max(0.15, float(trig.get("type_dur", 0.5))),
                    safe_box=safe_box,
                )

    # Optional declarative `custom_scene_graph` block inside `beat_data`
    csg = beat_data.get("custom_scene_graph")
    if isinstance(csg, dict):
        if csg.get("hide_default_chars", False):
            skip_default_chars = True

        # 1. Full-Screen 2D Skit Stage Background (`02:10 / 05:00 / 13:56` style)
        skit_bg = csg.get("skit_stage_bg", "")
        if skit_bg:
            draw_skit_stage_bg(img, skit_bg, bt, episode_id, workspace_root)
            draw = ImageDraw.Draw(img)

        # 2. Props & Images (with optional active_window `[t_min, t_max]`)
        for prop_node in csg.get("props_and_images", []):
            nt = float(prop_node.get("trigger_bt", 0.0))
            end_bt = float(prop_node.get("end_bt", 999.0))
            if nt <= bt <= end_bt:
                n_pop = min(1.0, (bt - nt) / 0.38)
                draw_archival_photo_card(
                    img,
                    prop_node.get("photo_file", ""),
                    (int(prop_node.get("x", stage_cx)), int(prop_node.get("y", 480))),
                    (int(prop_node.get("w", 440)), int(prop_node.get("h", 320))),
                    prop_node.get("badge_text", ""),
                    prop_node.get("caption_text", ""),
                    tuple(prop_node.get("badge_col", [52, 112, 172])),
                    n_pop,
                    safe_box,
                    episode_id,
                    workspace_root,
                )

        # 3. Animated Vector Lines & Stage Overlays (5 Ziro Live-Drawing Primitives)
        for vec_node in csg.get("vector_overlays", []):
            nt = float(vec_node.get("trigger_bt", 0.0))
            end_bt = float(vec_node.get("end_bt", 999.0))
            if nt <= bt <= end_bt:
                ndt = bt - nt
                v_kind = vec_node.get("kind", "curved_arrow")
                if v_kind == "curved_arrow":
                    s_xy = vec_node.get("arr_start", [stage_cx - 180, 440])
                    e_xy = vec_node.get("arr_end", [stage_cx + 180, 440])
                    draw_curved_arrow(img, (int(s_xy[0]), int(s_xy[1])), (int(e_xy[0]), int(e_xy[1])), arch=float(vec_node.get("arch", -20.0)), prog=ndt / 0.55)
                    if vec_node.get("label"):
                        l_xy = vec_node.get("txt_pos", [stage_cx, 380])
                        draw_kinetic_text(img, (int(l_xy[0]), int(l_xy[1])), vec_node["label"], size=int(vec_node.get("size", 26)), color=tuple(vec_node.get("color", [22, 22, 22])), bold=True, organic=False, prog=ndt / 0.45, safe_box=safe_box)

                elif v_kind == "live_pencil_line":
                    # Modeled on 13:56 (+0s..+5s): Animated pencil drawing a red line/polyline on the map
                    pts = vec_node.get("pts", [[720, 520], [1180, 520]])
                    draw_dur = max(0.25, float(vec_node.get("draw_dur", 1.35)))
                    p_prog = clamp01(ndt / draw_dur)
                    col = tuple(vec_node.get("color", [218, 32, 32]))
                    dashed = bool(vec_node.get("dashed", False))
                    if len(pts) >= 2 and p_prog > 0.01:
                        # Interpolate along polyline segments
                        seg_lens = [math.hypot(pts[i+1][0] - pts[i][0], pts[i+1][1] - pts[i][1]) for i in range(len(pts) - 1)]
                        tot_len = max(1.0, sum(seg_lens))
                        target_len = tot_len * p_prog
                        acc = 0.0
                        tip_x, tip_y = pts[0][0], pts[0][1]
                        for i, slen in enumerate(seg_lens):
                            x0_l, y0_l = pts[i]
                            x1_l, y1_l = pts[i+1]
                            if acc + slen <= target_len:
                                if dashed:
                                    steps_d = max(2, int(slen // 18))
                                    for d_i in range(0, steps_d, 2):
                                        f0, f1 = d_i / float(steps_d), min(1.0, (d_i + 1) / float(steps_d))
                                        draw.line([(x0_l + (x1_l - x0_l)*f0, y0_l + (y1_l - y0_l)*f0), (x0_l + (x1_l - x0_l)*f1, y0_l + (y1_l - y0_l)*f1)], fill=col, width=6)
                                else:
                                    draw.line([(x0_l, y0_l), (x1_l, y1_l)], fill=col, width=6)
                                tip_x, tip_y = x1_l, y1_l
                                acc += slen
                            else:
                                rem = (target_len - acc) / max(1.0, slen)
                                tip_x = x0_l + (x1_l - x0_l) * rem
                                tip_y = y0_l + (y1_l - y0_l) * rem
                                if dashed:
                                    steps_d = max(2, int((slen * rem) // 18))
                                    for d_i in range(0, steps_d, 2):
                                        f0, f1 = (d_i / float(max(1, int(slen // 18)))), min(rem, (d_i + 1) / float(max(1, int(slen // 18))))
                                        draw.line([(x0_l + (x1_l - x0_l)*f0, y0_l + (y1_l - y0_l)*f0), (x0_l + (x1_l - x0_l)*f1, y0_l + (y1_l - y0_l)*f1)], fill=col, width=6)
                                else:
                                    draw.line([(x0_l, y0_l), (tip_x, tip_y)], fill=col, width=6)
                                break
                        # Draw 2D Yellow Wooden Pencil at (tip_x, tip_y) while drawing (13:56 style!)
                        if p_prog < 0.98 or vec_node.get("keep_pencil", True):
                            px, py = int(tip_x), int(tip_y)
                            # Pencil angled at -55 deg (up-left from tip)
                            ux, uy = -0.57, -0.82
                            nx, ny = 0.82, -0.57
                            # Wood cone tip
                            cone_b1 = (px + ux * 22 + nx * 7, py + uy * 22 + ny * 7)
                            cone_b2 = (px + ux * 22 - nx * 7, py + uy * 22 - ny * 7)
                            draw.polygon([(px, py), cone_b1, cone_b2], fill=(232, 196, 145), outline=INK, width=2)
                            draw.ellipse([px - 3, py - 3, px + 3, py + 3], fill=col)
                            # Yellow pencil body
                            body_e1 = (px + ux * 125 + nx * 7, py + uy * 125 + ny * 7)
                            body_e2 = (px + ux * 125 - nx * 7, py + uy * 125 - ny * 7)
                            draw.polygon([cone_b1, body_e1, body_e2, cone_b2], fill=(245, 202, 48), outline=INK, width=2)
                            # Pink eraser cap
                            er_e1 = (px + ux * 142 + nx * 7, py + uy * 142 + ny * 7)
                            er_e2 = (px + ux * 142 - nx * 7, py + uy * 142 - ny * 7)
                            draw.polygon([body_e1, er_e1, er_e2, body_e2], fill=(235, 128, 148), outline=INK, width=2)
                    if vec_node.get("label") and ndt > 0.35:
                        l_xy = vec_node.get("txt_pos", [960, 500])
                        draw_skit_overhead_speech(
                            img, (int(l_xy[0]), int(l_xy[1])), vec_node["label"],
                            size=int(vec_node.get("size", 26)), color=tuple(vec_node.get("text_color", [255, 240, 120])),
                            prog=(ndt - 0.35) / 0.5, show_tick=False, safe_box=safe_box
                        )
                        draw = ImageDraw.Draw(img)

                elif v_kind == "wavy_steam_lines":
                    # Modeled on 02:10 (+12s..+15s): 3 sinusoidal wavy smoke/steam lines rising upward
                    cx_s, cy_s = int(vec_node.get("x", 960)), int(vec_node.get("y", 420))
                    s_col = tuple(vec_node.get("color", [148, 212, 92]))
                    h_len = int(vec_node.get("height", 75))
                    for s_i in (-1, 0, 1):
                        base_x = cx_s + s_i * 28
                        wave_pts = []
                        for wy in range(0, h_len, 5):
                            wx = base_x + int(round(7.5 * math.sin((wy * 0.11) - (bt * 7.5) + s_i * 1.1)))
                            wave_pts.append((wx, cy_s - wy))
                        if len(wave_pts) >= 2:
                            draw.line(wave_pts, fill=INK, width=6)
                            draw.line(wave_pts, fill=s_col, width=3)

                elif v_kind == "sparkle_bursts":
                    # Modeled on 00:46: Animated 4-point star sparkles & shine strokes (for oiled 6-pack abs / golden Xerxes)
                    sp_list = vec_node.get("points", [[960, 520], [880, 480], [1040, 490]])
                    sp_col = tuple(vec_node.get("color", [255, 235, 85]))
                    for idx_sp, (spx, spy) in enumerate(sp_list):
                        pulse = 0.55 + 0.45 * math.sin(bt * 8.5 + idx_sp * 1.7)
                        r_long = int(round(20 * pulse))
                        r_short = max(3, int(round(5 * pulse)))
                        star_pts = [
                            (spx, spy - r_long), (spx + r_short, spy - r_short),
                            (spx + r_long, spy), (spx + r_short, spy + r_short),
                            (spx, spy + r_long), (spx - r_short, spy + r_short),
                            (spx - r_long, spy), (spx - r_short, spy - r_short),
                        ]
                        draw.polygon(star_pts, fill=sp_col, outline=INK, width=2)

                elif v_kind == "checklist_board":
                    # Modeled on Ziro History's signature Checklist Card + Animated Oil Bottle Pour
                    bx, by = int(vec_node.get("x", 960)), int(vec_node.get("y", 410))
                    bw, bh = int(vec_node.get("w", 460)), int(vec_node.get("h", 250))
                    draw.rounded_rectangle([bx - bw//2 + 6, by - bh//2 + 8, bx + bw//2 + 6, by + bh//2 + 8], radius=14, fill=(108, 74, 46))
                    draw.rounded_rectangle([bx - bw//2, by - bh//2, bx + bw//2, by + bh//2], radius=14, fill=(248, 244, 232), outline=INK, width=3)
                    items = vec_node.get("items", ["1 quần đùi đỏ", "Áo choàng đỏ", "Dầu bóng 6 múi"])
                    for it_i, it_txt in enumerate(items):
                        it_delay = it_i * 0.65
                        if ndt >= it_delay:
                            iy = by - bh//2 + 52 + it_i * 68
                            ix = bx - bw//2 + 38
                            draw.rounded_rectangle([ix, iy - 18, ix + 36, iy + 18], radius=6, fill=(42, 158, 78), outline=INK, width=2)
                            draw.line([(ix + 8, iy), (ix + 16, iy + 9), (ix + 28, iy - 9)], fill=(255, 255, 255), width=4)
                            draw_kinetic_text(img, (ix + 54, iy), it_txt, size=26, color=INK, align="left", bold=True, organic=True, prog=(ndt - it_delay) / 0.45, safe_box=safe_box)
                            draw = ImageDraw.Draw(img)

                elif v_kind == "live_quill_scroll":
                    # Modeled on 05:00 (+14s..+21s): Giant unrolled parchment scroll where a feather quill writes lines live!
                    sx, sy = int(vec_node.get("x", 1180)), int(vec_node.get("y", 495))
                    sw_s, sh_s = int(vec_node.get("w", 860)), int(vec_node.get("h", 540))
                    unroll = ease_out_cubic(min(1.0, ndt / 0.4))
                    cur_w = max(80, int(sw_s * unroll))
                    x0_s, y0_s, x1_s, y1_s = sx - cur_w // 2, sy - sh_s // 2, sx + cur_w // 2, sy + sh_s // 2
                    draw.rectangle([x0_s, y0_s, x1_s, y1_s], fill=(246, 238, 214), outline=INK, width=4)
                    # Wooden scroll rollers on left & right edges (exactly like 05:00 +14s!)
                    draw.rectangle([x0_s - 18, y0_s - 18, x0_s + 6, y1_s + 18], fill=(124, 82, 48), outline=INK, width=3)
                    draw.rectangle([x1_s - 6, y0_s - 18, x1_s + 18, y1_s + 18], fill=(124, 82, 48), outline=INK, width=3)
                    lines_q = vec_node.get("lines", [])
                    font_q = get_font(28, bold=True, organic=True)
                    quill_xy = None
                    for l_i, l_str in enumerate(lines_q):
                        l_start = 0.35 + l_i * 0.95
                        if ndt >= l_start:
                            l_prog = clamp01((ndt - l_start) / 0.80)
                            n_ch = max(1, int(round(len(l_str) * l_prog)))
                            sub_s = l_str[:n_ch]
                            ly = y0_s + 78 + l_i * 78
                            bb_full = draw.textbbox((0, 0), l_str, font=font_q)
                            lw_full = bb_full[2] - bb_full[0]
                            lx = sx - lw_full // 2
                            draw.text((lx, ly), sub_s, font=font_q, fill=INK)
                            if l_prog < 0.99:
                                bb_sub = draw.textbbox((0, 0), sub_s, font=font_q)
                                quill_xy = (lx + (bb_sub[2] - bb_sub[0]), ly + 10)
                    if quill_xy:
                        qx, qy = quill_xy
                        draw.polygon([(qx, qy), (qx + 28, qy - 52), (qx + 52, qy - 64), (qx + 34, qy - 22)], fill=(252, 252, 248), outline=INK, width=2)
                        draw.line([(qx, qy), (qx + 42, qy - 54)], fill=INK, width=3)

                elif v_kind == "live_ruler_measure":
                    # Animated vertical height measurement line (0.0m -> 3.0m) next to 3m Hollywood Xerxes
                    rx, ry0, ry1 = int(vec_node.get("x", 1220)), int(vec_node.get("y_bottom", 840)), int(vec_node.get("y_top", 310))
                    r_prog = ease_out_cubic(min(1.0, ndt / 0.85))
                    cur_top = int(ry0 - (ry0 - ry1) * r_prog)
                    r_col = (255, 225, 75)
                    draw.line([(rx, ry0), (rx, cur_top)], fill=r_col, width=5)
                    draw.line([(rx - 18, ry0), (rx + 18, ry0)], fill=r_col, width=4)
                    draw.line([(rx - 18, cur_top), (rx + 18, cur_top)], fill=r_col, width=4)
                    for tk_y in range(ry0, cur_top, -45):
                        draw.line([(rx - 9, tk_y), (rx + 9, tk_y)], fill=r_col, width=3)
                    cur_m = 3.0 * r_prog
                    draw_skit_overhead_speech(
                        img, (rx - 85, (ry0 + cur_top) // 2), f"{cur_m:.1f} mét!",
                        size=30, color=(255, 225, 75), prog=1.0, show_tick=False, safe_box=safe_box
                    )
                    draw = ImageDraw.Draw(img)

        # 4. Actors with Auto Eye-Blink, Speech Bobbing, Walk-Cycle & Mid-Beat Pose Swaps
        for act_node in csg.get("actors", []):
            nt = float(act_node.get("trigger_bt", 0.0))
            end_bt = float(act_node.get("end_bt", 999.0))
            if nt <= bt <= end_bt:
                l_arm = act_node.get("left_arm", "down")
                r_arm = act_node.get("right_arm", "point_right")
                emo = act_node.get("emotion", "explaining")
                swap_bt = act_node.get("pose_swap_bt", None)
                if swap_bt is not None and bt >= float(swap_bt):
                    l_arm = act_node.get("swap_left_arm", l_arm)
                    r_arm = act_node.get("swap_right_arm", r_arm)
                    emo = act_node.get("swap_emotion", emo)

                speak_win = act_node.get("speak_window", None)
                if speak_win and len(speak_win) == 2:
                    is_speaking = (float(speak_win[0]) <= bt <= float(speak_win[1])) and bool(act_node.get("lip_sync", False))
                else:
                    is_speaking = bool(act_node.get("lip_sync", False))

                paste_char_safe(
                    img,
                    int(act_node.get("x", stage_cx)),
                    int(act_node.get("y", 720)),
                    role=act_node.get("role", "char_historic"),
                    emotion=emo,
                    mouth=m_state if is_speaking else "closed",
                    left_arm=l_arm,
                    right_arm=r_arm,
                    prop_right=act_node.get("prop_right", None),
                    scale=float(act_node.get("scale", 0.95)),
                    neck_insert_px=int(act_node.get("neck_insert_px", 35)),
                    pop_t=min(1.0, (bt - nt + 0.1) / 0.35) if not act_node.get("no_pop", False) else 1.0,
                    label=act_node.get("label", ""),
                    safe_box=safe_box,
                    bt=bt,
                    walk_vx=float(act_node.get("walk_vx", 0.0)),
                    walk_start_bt=float(act_node.get("walk_start_bt", 0.0)),
                    hide_label=bool(act_node.get("hide_label", bool(skit_bg))),
                )

        # 5. Overhead Turn-Taking Skit Speech Captions (matching 02:10, 05:00, 13:56)
        for sp_node in csg.get("skit_speech_captions", []):
            nt = float(sp_node.get("trigger_bt", 0.0))
            end_bt = float(sp_node.get("end_bt", 999.0))
            if nt <= bt <= end_bt:
                ndt = bt - nt
                base_op = float(sp_node.get("opacity", 1.0))
                dim_bt = sp_node.get("dim_after_bt", None)
                if dim_bt is not None and bt >= float(dim_bt):
                    base_op = float(sp_node.get("dim_opacity", 0.38))
                type_dur = float(sp_node.get("type_dur", 0.85))
                prog_s = 1.0 if type_dur <= 0.01 else (ndt / type_dur)
                draw_skit_overhead_speech(
                    img,
                    (int(sp_node.get("x", stage_cx)), int(sp_node.get("y", 320))),
                    sp_node.get("text", ""),
                    size=int(sp_node.get("size", 28)),
                    color=tuple(sp_node.get("color", [252, 252, 248])),
                    stroke_col=tuple(sp_node.get("stroke_col", list(INK))),
                    stroke_w=int(sp_node.get("stroke_w", 3)),
                    opacity=base_op,
                    prog=prog_s,
                    show_tick=bool(sp_node.get("show_tick", True)),
                    tick_dir=int(sp_node.get("tick_dir", 0)),
                    safe_box=safe_box,
                )

        # 6. Standard Kinetic Texts (if any)
        for txt_node in csg.get("kinetic_texts", []):
            nt = float(txt_node.get("trigger_bt", 0.0))
            end_bt = float(txt_node.get("end_bt", 999.0))
            if nt <= bt <= end_bt:
                ndt = bt - nt
                tx, ty = int(txt_node.get("x", stage_cx)), int(txt_node.get("y", 260))
                t_col = tuple(txt_node.get("color", [22, 22, 22]))
                t_sz = int(txt_node.get("size", 36))
                if txt_node.get("is_stamp", False):
                    draw_stamp(img, (tx, ty), txt_node.get("text", ""), bg_col=t_col, txt_col=(255, 255, 255), size=t_sz, pop_t=min(1.0, ndt / 0.35), safe_box=safe_box)
                else:
                    draw_kinetic_text(img, (tx, ty), txt_node.get("text", ""), size=t_sz, color=t_col, bold=bool(txt_node.get("bold", True)), organic=bool(txt_node.get("organic", True)), prog=ndt / 0.5, safe_box=safe_box)

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
            r_arm = ch_spec.get("right_arm") or ("point_right" if cx <= 960 else "down")
            l_arm = ch_spec.get("left_arm") or ("point_left" if cx > 960 else "down")
            prop = ch_spec.get("prop_right") if "prop_right" in ch_spec else ("laser_pointer" if role == "char_ziro_host" else None)

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
                bt=bt,
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
        base_proj = Path(__file__).resolve().parents[4] / "Du-an-2D-Illustrated-History"
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
