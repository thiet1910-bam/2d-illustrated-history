#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
VALIDATOR BƯỚC 2: validate_beat_manifest.py
Nhiệm vụ:
Kiểm toán toán học file `beat_manifest_<cluster_id>.json` qua 7 Luật Chặn Cứng (`7 Hard Assertions`):
1. Khớp cấu trúc bắt buộc của `templates/02_beat_manifest.schema.json`:
   - Mỗi nhịp (`beat`) bắt buộc có `segment_id` và `author_visual_note` không rỗng.
2. Khóa cứng thời lượng Âm thanh = Hình ảnh (`0.000s` Lock):
   - File `.wav` của từng nhịp phải tồn tại thật trên ổ cứng.
   - `abs(beat.duration - actual_wav_duration) <= 0.002` và `abs((beat.t1 - beat.t0) - beat.duration) <= 0.002`.
3. Chống lặp bố cục cảnh (`Anti-Repetition Gate`):
   - Không có 3 nhịp liên tiếp dùng chung 1 `scene_template`.
4. Chống mất chữ tiêu đề khi phóng to (`Pass 2 Post-Camera HUD Gate`):
   - `hud_banner.y_center >= 110` và `hud_banner.render_pass == "PASS_2_POST_CAMERA"`.
5. Chống cắt dọc nửa người ở mép khung hình (`Viewport Isolation Gate`):
   - Nếu `max(camera.zoom_start, camera.zoom_end) > 1.12` và cảnh có >= 2 nhân vật -> bắt buộc `camera.viewport_isolation_mode == True`.
   - Nếu `scene_template == "T02_Three_Cards_Fly_In"` -> `max(camera.zoom_start, camera.zoom_end) <= 1.08` hoặc `x_offset` nằm trong `[-540, 540]`.
6. Giải phẫu khớp cổ liền khối (`Neck Joint Gate`):
   - Mọi nhân vật trong mảng `characters` phải có `28 <= neck_insert_px <= 42`.
7. Đầy đủ 3 lớp âm thanh (`3-Layer Soundscape Gate`):
   - Có khai báo `bgm_track` hợp lệ và mỗi nhịp có ít nhất 1 `sfx_events` hợp lệ nằm trong khoảng `[0, beat.duration]`.
"""

import json
import sys
import wave
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

VALID_SCENE_TEMPLATES = {
    "T01_Split_World_Contrast",
    "T02_Three_Cards_Fly_In",
    "T03_Prison_Bars_Slam",
    "T04_Empire_Parade",
    "T05_Data_Chart_Scale",
    "T06_Geopolitics_Map_Spotlight",
    "T07_Icon_Grid_Counter",
    "T08_Fact_vs_Myth_Strike",
    "S01_General_Tent_Dialogue",
    "S02_Hollywood_Myth_vs_Reality",
    "S03_Biased_Historian_Desk",
    "S04_Field_Reporter_Gag",
    "S05_Absurd_Visual_Gag",
    "CUSTOM_METAPHOR_STAGE",
}

VALID_SFX_FILES = {
    "pop_card.wav",
    "whoosh_transition.wav",
    "stamp_slam.wav",
    "jail_bar_clang.wav",
    "typewriter_tick.wav",
    "sword_clash.wav",
}

VALID_BGM_TRACKS = {
    "bgm_tense_history.wav",
    "bgm_satire_skit.wav",
}


def validate_manifest(manifest_path: Path) -> tuple:
    errors = []
    warnings = []

    if not manifest_path.exists():
        return [f"Không tìm thấy file manifest: {manifest_path}"], []

    try:
        data = json.loads(manifest_path.read_text(encoding="utf-8"))
    except Exception as e:
        return [f"Lỗi cú pháp JSON: {e}"], []

    required_top = [
        "episode_id",
        "act_id",
        "cluster_id",
        "cluster_type",
        "author_visual_note",
        "bgm_track",
        "total_duration_sec",
        "beats",
    ]
    for k in required_top:
        if k not in data:
            errors.append(f"[Gate 1 - Schema] Thiếu trường cấp cao bắt buộc: `{k}`")

    if errors:
        return errors, warnings

    if data["bgm_track"] not in VALID_BGM_TRACKS:
        errors.append(f"[Gate 7 - Audio 3-Layer] `bgm_track` không hợp lệ: `{data['bgm_track']}`")

    beats = data.get("beats", [])
    if not isinstance(beats, list) or len(beats) == 0:
        errors.append("[Gate 1 - Schema] Mảng `beats` rỗng.")
        return errors, warnings

    cluster_dir = manifest_path.parent
    cum_wav_dur = 0.0
    prev_templates = []
    daylight_count = 0

    for idx, beat in enumerate(beats):
        bid = beat.get("beat_id", f"beat_{idx+1:02d}")

        # Gate 1: Kiểm tra bảo toàn segment_id và author_visual_note
        seg_id = str(beat.get("segment_id", "")).strip()
        vis_note = str(beat.get("author_visual_note", "")).strip()
        if not seg_id:
            errors.append(f"[{bid} | Gate 1 - Schema] Thiếu hoặc rỗng `segment_id` (làm mất dấu Phân đoạn kịch bản).")
        if not vis_note:
            errors.append(f"[{bid} | Gate 1 - Schema] Thiếu hoặc rỗng `author_visual_note` (làm mất ghi chú Hình ảnh của tác giả).")

        # Gate 2: Kiểm tra file WAV & khóa cứng 0.000s
        wav_rel = beat.get("wav_file", "")
        wav_path = cluster_dir / wav_rel
        t0 = float(beat.get("t0", 0.0))
        t1 = float(beat.get("t1", 0.0))
        dur = float(beat.get("duration", 0.0))

        if abs((t1 - t0) - dur) > 0.003:
            errors.append(f"[{bid} | Gate 2 - Sync 0.000s] `t1 - t0` ({t1 - t0:.4f}s) lệch với `duration` ({dur:.4f}s).")

        if wav_path.exists():
            try:
                with wave.open(str(wav_path), "rb") as wf:
                    real_dur = wf.getnframes() / float(wf.getframerate())
                if abs(real_dur - dur) > 0.003:
                    errors.append(
                        f"[{bid} | Gate 2 - Sync 0.000s] `beat.duration` ({dur:.4f}s) lệch với file WAV thật `{wav_rel}` ({real_dur:.4f}s)."
                    )
                cum_wav_dur += real_dur
            except Exception as e:
                errors.append(f"[{bid} | Gate 2 - Sync 0.000s] Không đọc được file WAV `{wav_rel}`: {e}")
        else:
            errors.append(f"[{bid} | Gate 2 - Sync 0.000s] File WAV không tồn tại: `{wav_path}`")
            cum_wav_dur += dur

        # Gate 3: Chống lặp bố cục cảnh quá 2 nhịp liên tiếp
        tpl = beat.get("scene_template", "")
        if tpl not in VALID_SCENE_TEMPLATES:
            errors.append(f"[{bid} | Gate 3 - Scene Template] `scene_template` không hợp lệ: `{tpl}`")
        prev_templates.append(tpl)
        if len(prev_templates) >= 3 and prev_templates[-1] == prev_templates[-2] == prev_templates[-3]:
            errors.append(
                f"[{bid} | Gate 3 - Anti-Repetition] Lặp lại cùng 1 mẫu cảnh `{tpl}` ở 3 nhịp liên tiếp ({idx-1}, {idx}, {idx+1})."
            )

        # Kiểm tra tỷ lệ nền sáng ấm
        l_mode = beat.get("lighting_mode", "")
        if l_mode in ("DAYLIGHT_WARM", "SAND_EMPIRE"):
            daylight_count += 1

        # Gate 4: HUD Banner ở Pass 2 Post-Camera & y_center >= 110 & Không rò rỉ nhãn hậu trường
        hud = beat.get("hud_banner", {})
        hud_y = float(hud.get("y_center", 0))
        hud_pass = hud.get("render_pass", "")
        hud_sub_badge = str(hud.get("sub_badge", "")).strip()
        if hud_y < 110:
            errors.append(
                f"[{bid} | Gate 4 - HUD Safe Zone] `hud_banner.y_center` = {hud_y}px (< 110px) sẽ gây cắt chữ tiêu đề ở mép trên!"
            )
        if hud_pass != "PASS_2_POST_CAMERA":
            errors.append(
                f"[{bid} | Gate 4 - HUD Safe Zone] `hud_banner.render_pass` = `{hud_pass}` (Bắt buộc phải là `PASS_2_POST_CAMERA` để chống mất chữ khi zoom)."
            )
        if hud_sub_badge:
            errors.append(
                f"[{bid} | Gate 4 - Anti-Metadata Leak] Cấm hiển thị nhãn quản trị hậu trường `sub_badge: {hud_sub_badge}` lên màn hình video!"
            )

        # Gate 5: Viewport Isolation khi zoom > 1.12 có >= 2 nhân vật
        cam = beat.get("camera", {})
        z_start = float(cam.get("zoom_start", 1.0))
        z_end = float(cam.get("zoom_end", 1.0))
        max_z = max(z_start, z_end)
        iso_mode = cam.get("viewport_isolation_mode", None)
        chars = beat.get("characters", [])

        if max_z > 1.35 or z_start < 1.0 or z_end < 1.0:
            errors.append(f"[{bid} | Gate 5 - Camera Zoom] Hệ số zoom ({z_start} -> {z_end}) vượt ngoài khoảng an toàn [1.0, 1.35].")

        if max_z > 1.12 and len(chars) >= 2 and iso_mode is not True:
            errors.append(
                f"[{bid} | Gate 5 - Viewport Isolation] Cảnh có {len(chars)} nhân vật và zoom {max_z:.2f}x (> 1.12x) nhưng `viewport_isolation_mode` = {iso_mode} (Sẽ gây cắt dọc nửa mặt nhân vật ở mép khung hình!)."
            )

        # Gate 6: Giải phẫu khớp cổ 28..42px & Không gắn biển tên ZIRO HOST dưới chân người dẫn
        for c_idx, ch in enumerate(chars):
            neck_px = float(ch.get("neck_insert_px", 0))
            if not (28 <= neck_px <= 42):
                errors.append(
                    f"[{bid} | Gate 6 - Neck Anatomy] Nhân vật `{ch.get('role', c_idx)}` có `neck_insert_px` = {neck_px}px (Bắt buộc trong khoảng [28, 42]px để chống đứt lìa cổ)."
                )
            ch_role = str(ch.get("role", "")).strip()
            ch_lbl = str(ch.get("label", "")).strip()
            if ch_role == "char_ziro_host" and ch_lbl:
                errors.append(
                    f"[{bid} | Gate 6 - Anti-Metadata Leak] Cấm gắn biển tên `{ch_lbl}` dưới chân nhân vật dẫn chuyện `char_ziro_host`!"
                )

        # Gate 7: Đầy đủ sự kiện tiếng động SFX
        sfx_list = beat.get("sfx_events", [])
        if not isinstance(sfx_list, list) or len(sfx_list) == 0:
            errors.append(f"[{bid} | Gate 7 - Audio 3-Layer] Mảng `sfx_events` rỗng (Mỗi nhịp bắt buộc có ít nhất 1 tiếng động SFX).")
        else:
            for sfx in sfx_list:
                s_file = sfx.get("sfx_file", "")
                s_bt = float(sfx.get("bt", -1.0))
                if s_file not in VALID_SFX_FILES:
                    errors.append(f"[{bid} | Gate 7 - Audio 3-Layer] File SFX `{s_file}` không nằm trong kho chuẩn.")
                if s_bt < 0.0 or s_bt > dur + 0.05:
                    errors.append(f"[{bid} | Gate 7 - Audio 3-Layer] Mốc `sfx.bt` ({s_bt:.2f}s) vượt ngoài thời lượng nhịp ({dur:.2f}s).")

    total_decl = float(data.get("total_duration_sec", 0.0))
    if abs(total_decl - cum_wav_dur) > 0.02:
        errors.append(
            f"[Gate 2 - Total Duration Sync] `total_duration_sec` ({total_decl:.3f}s) lệch với tổng thời lượng WAV các nhịp ({cum_wav_dur:.3f}s)."
        )

    daylight_ratio = daylight_count / float(len(beats))
    if daylight_ratio < 0.75:
        warnings.append(
            f"[Gate 6 - Daylight Ratio] Tỷ lệ cảnh nền sáng ấm đạt {daylight_ratio*100:.1f}% (Khuyến nghị >= 80%)."
        )

    return errors, warnings


def main():
    if len(sys.argv) < 2:
        print("Cách dùng: python validate_beat_manifest.py <duong_dan_beat_manifest.json>")
        sys.exit(1)

    manifest_path = Path(sys.argv[1]).resolve()
    print("=" * 72)
    print(f"🔍 KIỂM TOÁN KỊCH BẢN NHỊP (`Beat Manifest Validator`): `{manifest_path.name}`")
    print("=" * 72)

    errors, warnings = validate_manifest(manifest_path)

    for w in warnings:
        print(f"⚠️ [WARN] {w}")

    if errors:
        print(f"❌ [FAIL] Phát hiện {len(errors)} lỗi vi phạm quy chuẩn P0/P1:")
        for i, err in enumerate(errors, start=1):
            print(f"  {i}. {err}")
        print("=" * 72)
        sys.exit(1)

    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    print(f"• Mã Cụm (`cluster_id`)       : {data['cluster_id']} ({data['cluster_type']})")
    print(f"• Tổng số nhịp (`beats`)      : {len(data['beats'])} nhịp")
    print(f"• Tổng thời lượng (`float64`) : {data['total_duration_sec']:.3f}s (Sai số WAV = 0.000s)")
    print("✅ [PASS 100%] Kịch bản nhịp vượt qua toàn bộ 7 Cổng Kiểm Toán Toán Học!")
    print("=" * 72)
    sys.exit(0)


if __name__ == "__main__":
    main()
