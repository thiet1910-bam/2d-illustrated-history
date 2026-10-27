#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SCANNER BƯỚC 1: scan_voice_and_clusters.py
Nhiệm vụ:
1. Đọc Bộ 3 file đầu vào chuẩn trong `1_input/<Ma_Tap>/`:
   - `kich_ban_loi_dan.txt` (100% lời dẫn khớp Audio)
   - `kich_ban_chia_hoi.txt` (chia HỒI / Chương, Phân đoạn X.Y, Skit #N, ghi chú `(Hình ảnh: ...)`)
   - `voice.MP3` (1 file âm thanh nguyên khối)
2. Phân tích cấu trúc Động bằng Regex (không khóa cứng số Hồi hay số Phân đoạn) và áp dụng
   Thuật toán Phân Cụm Thích Ứng Động (`Dynamic Adaptive Clustering 90s - 240s`, <= 22 nhịp/cụm):
   - Hồi ngắn/vừa (<= 22 câu, không có Skit): Gom trọn Hồi thành 1 Cụm (`cum_XX_Hoi_I`), giữ nguyên `segment_id` và `author_visual_note` cho từng nhịp.
   - Hồi có Skit xen giữa: Tách riêng phần Skit thành 1 Cụm (`cum_XX_Skit_N`) để đổi sang nhánh `types/02_khuon_mau_canh_skit_cham_biem.md`.
   - Hồi quá dài (> 22 câu hoặc > 240s): Tự động chia tại ranh giới `Phân đoạn X.Y` sao cho mỗi Cụm nằm trong ngưỡng vàng.
3. Khi truyền tham số `--cluster <cluster_id>`, tự động cắt `voice.MP3` cuốn chiếu cho Cụm đó:
   - Cắt vùng âm thanh của Cụm bằng `ffmpeg` (`44100Hz`, Mono/Stereo PCM).
   - Dùng `faster_whisper` (`word_timestamps=True`) kết hợp dò điểm lặng (`Silence Valley` trên biên độ sóng âm PCM) để định vị chính xác mốc `t0, t1` của từng câu lời dẫn trong Cụm.
   - Xuất các file âm thanh câu lẻ `beats_wav/beat_01..N.wav` (`44100Hz PCM`), đo chính xác thời lượng bằng `nframes / float(framerate)` (`sai số 0.000s`) và xuất `voice_timeline_<cluster_id>.json`.
"""

import argparse
import json
import math
import os
import re
import subprocess
import sys
import wave
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def get_ffmpeg_exe() -> str:
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"


def probe_audio_duration(audio_path: Path) -> float:
    """Đo tổng thời lượng file MP3/WAV bằng ffmpeg hoặc wave."""
    if audio_path.suffix.lower() == ".wav":
        with wave.open(str(audio_path), "rb") as wf:
            return round(wf.getnframes() / float(wf.getframerate()), 6)
    ffmpeg_exe = get_ffmpeg_exe()
    cmd = [ffmpeg_exe, "-i", str(audio_path)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if m:
        h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
        return round(h * 3600 + mi * 60 + s, 3)
    return 1764.02


def normalize_for_match(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^[\-—–•\s]+", "", text)
    text = re.sub(r"\s+", " ", text)
    return text


def parse_structured_script(chia_hoi_path: Path, loi_dan_path: Path, config: dict) -> list:
    """
    Phân tích động `kich_ban_chia_hoi.txt` và đối chiếu 1-1 với `kich_ban_loi_dan.txt`.
    Trả về danh sách các đơn vị (Segment / Skit Block) kèm các câu lời dẫn bên trong.
    """
    raw_lines = chia_hoi_path.read_text(encoding="utf-8").splitlines()
    loi_dan_lines = [
        line.strip() for line in loi_dan_path.read_text(encoding="utf-8").splitlines() if line.strip()
    ]

    act_re = re.compile(r"^\s*(HỒI|ACT|CHƯƠNG|PHẦN)\s+([IVXLCDM0-9]+)\s*[:\-–]?\s*(.*)$", re.IGNORECASE)
    seg_re = re.compile(r"^\s*(Phân đoạn|Đoạn|Mục|Scene)\s+([0-9]+(?:\.[0-9]+)?)\s*[:\]\-–]?\s*(.*)$", re.IGNORECASE)
    skit_re = re.compile(r"\(\s*(?:Chuyển nhịp\s*)?Skit\s*#?([0-9]+)\s*[:\-–]?\s*(.*?)\)", re.IGNORECASE)
    note_re = re.compile(r"\(\s*Hình ảnh\s*:\s*(.*?)\)", re.IGNORECASE)
    stage_note_re = re.compile(r"^\s*\((?:Nhịp nghỉ|Nhạc nền|Chuyển nhịp).*?\)\s*$", re.IGNORECASE)

    current_act_id = "HỒI I"
    current_act_title = ""
    current_seg_id = "1.1"
    current_seg_title = ""
    current_visual_note = ""

    # Chúng ta chia thành các "Sub-block" (mỗi Phân đoạn là 1 Sub-block; nếu trong Phân đoạn có Skit thì tách thành:
    # Pre-Skit HOI, Skit Block SKIT, và Post-Skit HOI nếu dài, hoặc gắn Skit rõ ràng)
    blocks = []
    current_block = None

    def start_new_block(block_type: str, seg_id: str, seg_title: str, visual_note: str, skit_num: str = None):
        nonlocal current_block
        if current_block and current_block["lines"]:
            blocks.append(current_block)
        current_block = {
            "act_id": current_act_id,
            "act_title": current_act_title,
            "segment_id": seg_id,
            "segment_title": seg_title,
            "block_type": block_type,  # "HOI_PHAN_TICH" or "SKIT_CHAM_BIEM"
            "skit_id": f"Skit_{skit_num}" if skit_num else None,
            "author_visual_note": visual_note or "Sân khấu minh họa lịch sử 2D chuẩn Ziro",
            "lines": [],
        }

    in_skit_dialogue = False
    active_skit_num = None

    for raw_line in raw_lines:
        line = raw_line.strip()
        if not line:
            continue

        m_act = act_re.match(line)
        if m_act:
            current_act_id = f"{m_act.group(1).upper()} {m_act.group(2).upper()}"
            current_act_title = m_act.group(3).strip(" )]")
            in_skit_dialogue = False
            continue

        m_seg = seg_re.match(line)
        if m_seg:
            current_seg_id = m_seg.group(2).strip()
            rest = m_seg.group(3)
            m_note = note_re.search(rest)
            if m_note:
                current_visual_note = m_note.group(1).strip()
                current_seg_title = rest[:m_note.start()].strip(" :]-–")
            else:
                current_seg_title = rest.strip(" :]-–")
                current_visual_note = current_seg_title
            in_skit_dialogue = False
            start_new_block("HOI_PHAN_TICH", current_seg_id, current_seg_title, current_visual_note)
            continue

        m_skit = skit_re.search(line)
        if m_skit:
            active_skit_num = m_skit.group(1).strip()
            skit_desc = m_skit.group(2).strip()
            in_skit_dialogue = True
            start_new_block(
                "SKIT_CHAM_BIEM",
                f"{current_seg_id}_Skit_{active_skit_num}",
                f"Skit #{active_skit_num}: {skit_desc}",
                f"{current_visual_note} | Tiểu phẩm Skit #{active_skit_num}: {skit_desc}",
                skit_num=active_skit_num,
            )
            continue

        if stage_note_re.match(line):
            continue

        # Nếu đang ở chế độ Skit (các câu thoại bắt đầu bằng — "...") mà gặp câu văn xuôi không có dấu gạch ngang
        is_dialogue_line = line.startswith("—") or line.startswith("-") or line.startswith('"') or line.startswith("“")
        if in_skit_dialogue and not is_dialogue_line:
            in_skit_dialogue = False
            start_new_block("HOI_PHAN_TICH", current_seg_id, current_seg_title, current_visual_note)

        if current_block is None:
            start_new_block("HOI_PHAN_TICH", current_seg_id, current_seg_title, current_visual_note)

        current_block["lines"].append({
            "text": line,
            "segment_id": current_seg_id,
            "author_visual_note": current_block["author_visual_note"],
        })

    if current_block and current_block["lines"]:
        blocks.append(current_block)

    # Đối chiếu tổng số dòng lời dẫn với `kich_ban_loi_dan.txt`
    extracted_lines = [item["text"] for b in blocks for item in b["lines"]]
    return blocks, extracted_lines, loi_dan_lines


def build_dynamic_adaptive_clusters(blocks: list, total_audio_duration: float, config: dict) -> list:
    """
    Thuật toán Phân Cụm Thích Ứng Động (`Dynamic Adaptive Clustering 90s - 240s`, <= 22 nhịp/cụm):
    - Tự động ước lượng thời lượng từng câu theo số từ (trước khi cắt WAV chính xác) để chia Cụm hợp lý.
    - Quy tắc:
      1. Khối `SKIT_CHAM_BIEM` (và các câu dẫn trực tiếp vào Skit trong cùng Phân đoạn nếu rất ngắn <= 3 câu)
         hoặc tách riêng `SKIT_CHAM_BIEM` thành Cụm Skit độc lập để áp dụng `types/02_khuon_mau_canh_skit_cham_biem.md`.
      2. Các khối `HOI_PHAN_TICH` cùng 1 `act_id` được gom lại nếu tổng số câu <= `max_beats_per_cluster` (22)
         và tổng thời lượng ước tính <= `max_cluster_duration_sec` (240s), VÀ không bị cắt ngang bởi 1 Cụm Skit.
    """
    cluster_cfg = config.get("adaptive_clustering_and_cache", {})
    max_beats = int(cluster_cfg.get("max_beats_per_cluster", 22))
    max_dur = float(cluster_cfg.get("max_cluster_duration_sec", 240.0))

    total_words = sum(len(item["text"].split()) for b in blocks for item in b["lines"])
    sec_per_word = total_audio_duration / max(total_words, 1)

    raw_clusters = []
    current_cluster = None

    for b in blocks:
        b_words = sum(len(item["text"].split()) for item in b["lines"])
        b_est_dur = round(b_words * sec_per_word, 2)
        b_beats = len(b["lines"])

        if b["block_type"] == "SKIT_CHAM_BIEM":
            if current_cluster:
                raw_clusters.append(current_cluster)
                current_cluster = None
            raw_clusters.append({
                "act_id": b["act_id"],
                "act_title": b["act_title"],
                "cluster_type": "SKIT_CHAM_BIEM",
                "skit_id": b["skit_id"],
                "segments": [b["segment_id"]],
                "visual_notes": [b["author_visual_note"]],
                "lines": list(b["lines"]),
                "est_duration": b_est_dur,
            })
            continue

        # Nếu là HOI_PHAN_TICH: kiểm tra xem có gộp vào current_cluster cùng Hồi được không
        if (
            current_cluster is not None
            and current_cluster["cluster_type"] == "HOI_PHAN_TICH"
            and current_cluster["act_id"] == b["act_id"]
            and (len(current_cluster["lines"]) + b_beats) <= max_beats
            and (current_cluster["est_duration"] + b_est_dur) <= max_dur
        ):
            if b["segment_id"] not in current_cluster["segments"]:
                current_cluster["segments"].append(b["segment_id"])
            if b["author_visual_note"] not in current_cluster["visual_notes"]:
                current_cluster["visual_notes"].append(b["author_visual_note"])
            current_cluster["lines"].extend(b["lines"])
            current_cluster["est_duration"] = round(current_cluster["est_duration"] + b_est_dur, 2)
        else:
            if current_cluster:
                raw_clusters.append(current_cluster)
            current_cluster = {
                "act_id": b["act_id"],
                "act_title": b["act_title"],
                "cluster_type": "HOI_PHAN_TICH",
                "skit_id": None,
                "segments": [b["segment_id"]],
                "visual_notes": [b["author_visual_note"]],
                "lines": list(b["lines"]),
                "est_duration": b_est_dur,
            }

    if current_cluster:
        raw_clusters.append(current_cluster)

    # Đặt mã định danh `cluster_id` chuẩn xác và tính mốc thời gian ước lượng ban đầu
    import unicodedata
    def to_ascii_slug(s: str) -> str:
        s_norm = unicodedata.normalize("NFD", s)
        s_ascii = "".join(ch for ch in s_norm if unicodedata.category(ch) != "Mn")
        s_ascii = s_ascii.replace("Đ", "D").replace("đ", "d")
        return re.sub(r"[^A-Za-z0-9]+", "_", s_ascii).strip("_")

    cum_t = 0.0
    final_clusters = []
    for idx, c in enumerate(raw_clusters, start=1):
        act_slug = to_ascii_slug(c["act_id"]).title().replace("Hoi_", "Hoi_")
        # Ví dụ: HỒI I -> Hoi_I, HỒI II -> Hoi_II
        m_roman = re.match(r"(?i)^(Hoi|Act|Chuong|Phan)_([IVXLCDM0-9]+)$", act_slug)
        if m_roman:
            act_slug = f"{m_roman.group(1).capitalize()}_{m_roman.group(2).upper()}"
        if c["cluster_type"] == "SKIT_CHAM_BIEM":
            c_id = f"cum_{idx:02d}_{c['skit_id']}"
        else:
            seg_tag = "_".join(s.replace(".", "_") for s in c["segments"])
            if idx == 1 and act_slug == "Hoi_I":
                c_id = "cum_01_Hoi_I"
            else:
                c_id = f"cum_{idx:02d}_{act_slug}_seg_{seg_tag}"
        t0_est = round(cum_t, 2)
        t1_est = round(min(total_audio_duration, cum_t + c["est_duration"]), 2)
        cum_t = t1_est
        c["cluster_id"] = c_id
        c["order_index"] = idx
        c["est_t0"] = t0_est
        c["est_t1"] = t1_est
        final_clusters.append(c)

    return final_clusters


def split_paragraph_into_beats(lines_list: list, target_min_beats: int = 10, target_max_beats: int = 15) -> list:
    """
    Với các đoạn văn dài trong 1 Cụm (VD Cụm 1 có 11 đoạn văn tương ứng 11 nhịp chuẩn),
    giữ nguyên từng dòng lời dẫn trong `kich_ban_loi_dan.txt` làm 1 nhịp (`beat`) hoặc tách câu nếu đoạn quá dài (> 85 từ).
    Đặc biệt: Ở `Hồi I` của `EP01_Iran`, 11 dòng lời dẫn trong `kich_ban_loi_dan.txt` khớp chính xác 11 nhịp câu!
    """
    beats = []
    for item in lines_list:
        text = item["text"].strip()
        words = text.split()
        # Nếu 1 dòng quá dài (> 95 từ) thì tách làm 2 nhịp tại dấu chấm ở giữa để tránh cảnh đứng lâu
        if len(words) > 95:
            sentences = re.split(r"(?<=[.!?])\s+", text)
            if len(sentences) >= 2:
                mid = len(sentences) // 2
                part1 = " ".join(sentences[:mid]).strip()
                part2 = " ".join(sentences[mid:]).strip()
                if part1:
                    beats.append({
                        "narration_text": part1,
                        "segment_id": item["segment_id"],
                        "author_visual_note": item["author_visual_note"],
                    })
                if part2:
                    beats.append({
                        "narration_text": part2,
                        "segment_id": item["segment_id"],
                        "author_visual_note": item["author_visual_note"],
                    })
                continue
        beats.append({
            "narration_text": text,
            "segment_id": item["segment_id"],
            "author_visual_note": item["author_visual_note"],
        })
    return beats


def find_nearest_silence_valley(wav_path: Path, target_sec: float, search_radius_sec: float = 0.35) -> float:
    """
    Dò điểm lặng (`Silence Valley` — vị trí có năng lượng RMS thấp nhất) quanh mốc `target_sec`
    trên file WAV `44100Hz` để nhát cắt không bao giờ cắt ngang âm tiết đang phát âm.
    """
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        nch = wf.getnchannels()
        sampwidth = wf.getsampwidth()
        total_frames = wf.getnframes()
        total_dur = total_frames / float(sr)

        if target_sec <= 0.05:
            return 0.0
        if target_sec >= total_dur - 0.05:
            return round(total_dur, 6)

        t_start = max(0.0, target_sec - search_radius_sec)
        t_end = min(total_dur, target_sec + search_radius_sec)
        f_start = int(t_start * sr)
        f_end = int(t_end * sr)
        wf.setpos(f_start)
        raw_bytes = wf.readframes(f_end - f_start)

    import struct
    if sampwidth != 2:
        return round(target_sec, 6)

    samples = struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes)
    if nch > 1:
        samples = samples[::nch]

    win_size = int(0.025 * sr)  # Cửa sổ 25ms
    step = int(0.005 * sr)      # Bước trượt 5ms
    if len(samples) < win_size:
        return round(target_sec, 6)

    best_t = target_sec
    min_energy = float("inf")
    for i in range(0, len(samples) - win_size, step):
        chunk = samples[i : i + win_size]
        rms = sum(s * s for s in chunk) / float(win_size)
        t_cur = t_start + (i + win_size / 2.0) / float(sr)
        # Ưu tiên điểm lặng gần target_sec
        dist_penalty = 1.0 + 0.5 * abs(t_cur - target_sec) / max(search_radius_sec, 0.01)
        score = rms * dist_penalty
        if score < min_energy:
            min_energy = score
            best_t = t_cur

    return round(best_t, 6)


def slice_wav_exact_frames(src_wav: Path, dst_wav: Path, t0: float, t1: float) -> tuple:
    """
    Cắt chính xác tới từng mẫu âm thanh (`Sample-Accurate Frame Slicing`) từ `src_wav`
    và trả về `(actual_t0, actual_t1, exact_duration_float64)`.
    """
    with wave.open(str(src_wav), "rb") as rf:
        sr = rf.getframerate()
        nch = rf.getnchannels()
        sampwidth = rf.getsampwidth()
        total_frames = rf.getnframes()

        f0 = max(0, min(total_frames, int(round(t0 * sr))))
        f1 = max(f0 + 1, min(total_frames, int(round(t1 * sr))))
        rf.setpos(f0)
        data = rf.readframes(f1 - f0)

    dst_wav.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(dst_wav), "wb") as wf:
        wf.setnchannels(nch)
        wf.setsampwidth(sampwidth)
        wf.setframerate(sr)
        wf.writeframes(data)

    with wave.open(str(dst_wav), "rb") as vf:
        nframes = vf.getnframes()
        dur = round(nframes / float(vf.getframerate()), 6)

    return round(f0 / float(sr), 6), round(f1 / float(sr), 6), dur


def align_and_slice_cluster_audio(
    mp3_path: Path,
    cluster_dir: Path,
    cluster_info: dict,
    use_whisper: bool = True,
) -> dict:
    """
    Cắt `voice.MP3` cuốn chiếu cho Cụm `cluster_info`:
    1. Trích xuất đoạn WAV `44100Hz, Stereo, 16-bit PCM` từ `voice.MP3` quanh vùng thời gian của Cụm.
    2. Dùng `faster_whisper` (`model="base"`, `word_timestamps=True`) để lấy tọa độ thời gian thực tế của các câu trong Cụm,
       kết hợp tinh chỉnh tại điểm lặng (`Silence Valley`) để cắt ra đúng `beat_01..N.wav` khớp `0.000s`.
    """
    ffmpeg_exe = get_ffmpeg_exe()
    beats_meta = split_paragraph_into_beats(cluster_info["lines"])
    num_beats = len(beats_meta)

    # Bước A: Trích xuất đoạn WAV thô từ `voice.MP3` (lấy dư +25s biên an toàn để Whisper tìm đúng điểm kết thúc Cụm)
    search_t0 = max(0.0, cluster_info["est_t0"] - (5.0 if cluster_info["order_index"] > 1 else 0.0))
    search_dur = (cluster_info["est_t1"] - search_t0) + 35.0
    raw_window_wav = cluster_dir / "_temp_window_44k.wav"
    cluster_dir.mkdir(parents=True, exist_ok=True)

    cmd_extract = [
        ffmpeg_exe,
        "-y",
        "-ss",
        f"{search_t0:.3f}",
        "-t",
        f"{search_dur:.3f}",
        "-i",
        str(mp3_path),
        "-ar",
        "44100",
        "-ac",
        "2",
        "-c:a",
        "pcm_s16le",
        str(raw_window_wav),
    ]
    subprocess.run(cmd_extract, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)

    # Bước B: Dùng faster_whisper (nếu bật) truyền trực tiếp mảng 16kHz float32 để tránh lỗi PyAV `metadata_errors`
    whisper_Boundaries = None
    if use_whisper:
        try:
            import numpy as np
            from faster_whisper import WhisperModel
            raw_16k_wav = cluster_dir / "_temp_window_16k.wav"
            subprocess.run(
                [
                    ffmpeg_exe, "-y", "-i", str(raw_window_wav),
                    "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(raw_16k_wav)
                ],
                stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True
            )
            with wave.open(str(raw_16k_wav), "rb") as wf16:
                audio_16k = np.frombuffer(wf16.readframes(wf16.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            if raw_16k_wav.exists():
                raw_16k_wav.unlink()

            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments_gen, _ = model.transcribe(
                audio_16k,
                language="vi",
                word_timestamps=True,
                vad_filter=False,
            )
            words_timed = []
            for seg in segments_gen:
                if seg.words:
                    for w in seg.words:
                        words_timed.append({
                            "word": w.word.strip().lower(),
                            "start": float(w.start),
                            "end": float(w.end),
                        })
            if len(words_timed) >= 20:
                import difflib
                import unicodedata

                def _clean_ascii(s: str) -> str:
                    s_n = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
                    s_a = "".join(c for c in s_n if unicodedata.category(c) != "Mn")
                    return re.sub(r"[^a-z0-9\s]+", " ", s_a).strip()

                def _tokenize_clean(s: str) -> list:
                    return [t for t in _clean_ascii(s).split() if t]

                w_clean_list = [_clean_ascii(w["word"]) for w in words_timed]
                beat_tokens_list = [_tokenize_clean(b["narration_text"]) for b in beats_meta]

                boundaries = [0.0]
                cur_w_ptr = 0

                for b_idx in range(num_beats):
                    b_toks = beat_tokens_list[b_idx]
                    expected_len = max(1, len(b_toks))
                    approx_k = min(len(words_timed) - 1, cur_w_ptr + expected_len - 1)
                    search_lo = max(cur_w_ptr + 1, approx_k - max(8, int(expected_len * 0.45)))
                    search_hi = min(len(words_timed) - 2, approx_k + max(8, int(expected_len * 0.45)))

                    tail_ref = " ".join(b_toks[-3:]) if len(b_toks) >= 3 else " ".join(b_toks)
                    head_ref = ""
                    if b_idx + 1 < num_beats:
                        nxt_toks = beat_tokens_list[b_idx + 1]
                        head_ref = " ".join(nxt_toks[:3]) if len(nxt_toks) >= 3 else " ".join(nxt_toks)

                    best_k = approx_k
                    best_score = -1e9
                    for k in range(search_lo, search_hi + 1):
                        cand_tail = " ".join(w_clean_list[max(cur_w_ptr, k - 2) : k + 1])
                        sim_tail = difflib.SequenceMatcher(None, tail_ref, cand_tail).ratio()

                        sim_head = 0.0
                        if head_ref and (k + 1) < len(w_clean_list):
                            cand_head = " ".join(w_clean_list[k + 1 : min(len(w_clean_list), k + 4)])
                            sim_head = difflib.SequenceMatcher(None, head_ref, cand_head).ratio()

                        pause_gap = max(0.0, words_timed[k + 1]["start"] - words_timed[k]["end"])
                        pause_bonus = min(0.8, pause_gap) * 0.55
                        dist_pen = abs(k - approx_k) * 0.015

                        score = sim_tail * 1.25 + sim_head * 1.35 + pause_bonus - dist_pen
                        if score > best_score:
                            best_score = score
                            best_k = k

                    raw_cut_t = (words_timed[best_k]["end"] + words_timed[min(len(words_timed) - 1, best_k + 1)]["start"]) / 2.0
                    refined_t = find_nearest_silence_valley(raw_window_wav, raw_cut_t, search_radius_sec=0.18)
                    boundaries.append(refined_t)
                    cur_w_ptr = best_k + 1

                whisper_Boundaries = boundaries
        except Exception as e:
            print(f"[WARN] Whisper fallback sang Silence-Valley Proportional Slicing: {e}")

    if not whisper_Boundaries:
        # Fallback toán học kết hợp Silence Valley
        beat_word_counts = [max(1, len(b["narration_text"].split())) for b in beats_meta]
        total_w = sum(beat_word_counts)
        est_cluster_dur = cluster_info["est_duration"]
        boundaries = [0.0]
        cum_w = 0
        for b_idx in range(num_beats - 1):
            cum_w += beat_word_counts[b_idx]
            target_t = (cum_w / float(total_w)) * est_cluster_dur
            boundaries.append(find_nearest_silence_valley(raw_window_wav, target_t, search_radius_sec=0.45))
        boundaries.append(find_nearest_silence_valley(raw_window_wav, est_cluster_dur, search_radius_sec=0.45))
        whisper_Boundaries = boundaries

    # Đảm bảo tính đơn điệu tăng chặt (`b[i+1] > b[i] + 1.2s`)
    for i in range(1, len(whisper_Boundaries)):
        if whisper_Boundaries[i] <= whisper_Boundaries[i - 1] + 1.0:
            whisper_Boundaries[i] = round(whisper_Boundaries[i - 1] + 2.5, 6)

    # Bước C: Cắt file `voice_<cluster_id>.wav` tổng của Cụm và các file `beats_wav/beat_XX.wav` khớp 100% số frame
    cluster_wav_path = cluster_dir / f"voice_{cluster_info['cluster_id']}.wav"
    _, _, cluster_exact_dur = slice_wav_exact_frames(
        raw_window_wav, cluster_wav_path, whisper_Boundaries[0], whisper_Boundaries[-1]
    )

    beats_wav_dir = cluster_dir / "beats_wav"
    beats_wav_dir.mkdir(parents=True, exist_ok=True)
    # Xóa các file wav cũ nếu có
    for old_wav in beats_wav_dir.glob("*.wav"):
        old_wav.unlink()

    beats_output = []
    cum_t0 = 0.0
    for idx in range(num_beats):
        rel_t0 = whisper_Boundaries[idx] - whisper_Boundaries[0]
        rel_t1 = whisper_Boundaries[idx + 1] - whisper_Boundaries[0]
        beat_id = f"beat_{idx + 1:02d}"
        wav_filename = f"{beat_id}.wav"
        beat_wav_path = beats_wav_dir / wav_filename

        _, _, exact_dur = slice_wav_exact_frames(cluster_wav_path, beat_wav_path, rel_t0, rel_t1)
        beat_t0 = round(cum_t0, 6)
        beat_t1 = round(cum_t0 + exact_dur, 6)
        cum_t0 = beat_t1

        beats_output.append({
            "beat_id": beat_id,
            "segment_id": beats_meta[idx]["segment_id"],
            "author_visual_note": beats_meta[idx]["author_visual_note"],
            "wav_file": f"beats_wav/{wav_filename}",
            "source_mp3_t0": round(search_t0 + whisper_Boundaries[idx], 3),
            "source_mp3_t1": round(search_t0 + whisper_Boundaries[idx + 1], 3),
            "t0": beat_t0,
            "t1": beat_t1,
            "duration": exact_dur,
            "narration_text": beats_meta[idx]["narration_text"],
        })

    if raw_window_wav.exists():
        raw_window_wav.unlink()

    timeline_data = {
        "episode_id": cluster_info.get("episode_id", ""),
        "act_id": cluster_info["act_id"],
        "cluster_id": cluster_info["cluster_id"],
        "cluster_type": cluster_info["cluster_type"],
        "segments": cluster_info["segments"],
        "author_visual_note": " | ".join(cluster_info["visual_notes"]),
        "cluster_wav_file": cluster_wav_path.name,
        "total_duration_sec": round(cum_t0, 6),
        "beats_count": len(beats_output),
        "beats": beats_output,
    }

    timeline_json_path = cluster_dir / f"voice_timeline_{cluster_info['cluster_id']}.json"
    timeline_json_path.write_text(json.dumps(timeline_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return timeline_data


def write_episode_cluster_dossier(
    episode_id: str,
    mp3_dur: float,
    blocks: list,
    clusters: list,
    sliced_results: dict,
    out_md_path: Path,
):
    """Xuất file `01_ho_so_chia_cum.md` theo đúng khuôn mẫu sạch `templates/01_ho_so_chia_cum_va_bible_tap.md`."""
    acts_set = []
    segs_set = []
    skits_set = []
    for b in blocks:
        if b["act_id"] not in acts_set:
            acts_set.append(b["act_id"])
        if b["block_type"] == "SKIT_CHAM_BIEM" and b["skit_id"] not in skits_set:
            skits_set.append(b["skit_id"])
        elif b["segment_id"] not in segs_set:
            segs_set.append(b["segment_id"])

    lines = [
        f"# HỒ SƠ PHÂN CỤM THÍCH ỨNG ĐỘNG & DANH MỤC TƯ LIỆU TẬP PHIM (`{episode_id}`)",
        "",
        f"## 1. Thông Số Tổng Quan Bộ 3 File Đầu Vào (`1_input/{episode_id}/`) & Kho Tư Liệu Tập",
        f"- **Mã tập phim:** `{episode_id}`",
        f"- **File kịch bản lời dẫn (khớp 100% Audio):** `1_input/{episode_id}/kich_ban_loi_dan.txt`",
        f"- **File kịch bản cấu trúc (chia Hồi / Phân đoạn / Skit / Ghi chú hình ảnh):** `1_input/{episode_id}/kich_ban_chia_hoi.txt`",
        f"- **File âm thanh gốc nguyên khối:** `1_input/{episode_id}/voice.MP3`",
        f"- **Tổng thời lượng Audio gốc (`float64`):** `{mp3_dur:.3f}s ({int(mp3_dur // 60)}m {mp3_dur % 60:.2f}s)`",
        f"- **Tổng số Hồi / Phân đoạn / Tiểu phẩm Skit phát hiện tự động:** `{len(acts_set)} Hồi, {len(segs_set)} Phân đoạn ({segs_set[0]} -> {segs_set[-1]}), {len(skits_set)} Skit`",
        f"- **Tổng số Cụm Thích Ứng Động (`Dynamic Adaptive Clusters`, `90s – 240s/cụm`):** `{len(clusters)} Cụm`",
        f"- **Kho tài sản thương hiệu & âm thanh dùng chung toàn kênh:** `2_nguyen_lieu/0_kho_dung_chung/brand_ui_assets/` & `2_nguyen_lieu/0_kho_dung_chung/audio_sfx_bgm/`",
        f"- **Kho tư liệu hình ảnh & bản đồ riêng của Tập (chia theo Cụm + STT + Mốc giây):** `2_nguyen_lieu/{episode_id}/tu_lieu_tap/<cluster_id>/`",
        f"- **Thư mục chứa các gói Cụm & Bộ nhớ đệm từng nhịp (`cache_beats/`):** `2_nguyen_lieu/{episode_id}/cac_cum/`",
        "",
        "---",
        "",
        "## 2. Bảng Theo Dõi Tiến Độ Vòng Lặp Cuốn Chiếu Từng Cụm (`Dynamic Cluster Loop Tracker`)",
        "",
        "| Thứ Tự | Mã Cụm (`cluster_id`) | Thuộc Hồi (`act_id`) | Các Phân Đoạn Gộp Trong Cụm (`segments`) | Loại (`HOI / SKIT`) | Số Nhịp (`beats`) | Mốc Audio (`t0 -> t1`) | Thời Lượng (`s`) | Trạng Thái (`PENDING / SLICED / RENDERED / DONE_PASS`) |",
        "| :---: | :--- | :---: | :--- | :---: | :---: | :---: | :---: | :---: |",
    ]

    ep_dir = out_md_path.parent
    tu_lieu_dir = ep_dir / "tu_lieu_tap"
    tu_lieu_dir.mkdir(parents=True, exist_ok=True)
    cluster_assets_map = {}
    total_asset_count = 0

    running_t0 = 0.0
    for c in clusters:
        cid = c["cluster_id"]
        c_tu_lieu = tu_lieu_dir / cid
        c_tu_lieu.mkdir(parents=True, exist_ok=True)
        c_files = sorted([p.name for p in c_tu_lieu.iterdir() if p.is_file()])
        cluster_assets_map[cid] = c_files
        total_asset_count += len(c_files)
        segs_str = ", ".join(c["segments"])
        existing_tl = ep_dir / "cac_cum" / cid / f"voice_timeline_{cid}.json"
        if not existing_tl.exists():
            existing_tl = ep_dir / "cac_cum" / cid / f"cluster_timeline_{cid}.json"
        if cid in sliced_results:
            sr = sliced_results[cid]
            b_cnt = sr["beats_count"]
            t0_s = sr["beats"][0]["source_mp3_t0"]
            t1_s = sr["beats"][-1]["source_mp3_t1"]
            dur_s = sr["total_duration_sec"]
            running_t0 = t1_s
            status = "SLICED"
        elif existing_tl.exists():
            sr = json.loads(existing_tl.read_text(encoding="utf-8"))
            b_cnt = sr["beats_count"]
            t0_s = sr["beats"][0]["source_mp3_t0"]
            t1_s = sr["beats"][-1]["source_mp3_t1"]
            dur_s = sr["total_duration_sec"]
            running_t0 = t1_s
            status = "SLICED"
        else:
            b_cnt = len(c["lines"])
            t0_s = round(running_t0, 2)
            dur_s = c["est_duration"]
            if c["order_index"] == len(clusters):
                t1_s = round(mp3_dur, 2)
                dur_s = round(t1_s - t0_s, 3)
            else:
                t1_s = round(min(mp3_dur, t0_s + dur_s), 2)
            running_t0 = t1_s
            status = "PENDING"
        lines.append(
            f"| `{c['order_index']:02d}` | `{cid}` | `{c['act_id']}` | `{segs_str}` | `{c['cluster_type']}` | `{b_cnt}` | `{t0_s:.2f} -> {t1_s:.2f}` | `{dur_s:.3f}s` | `{status}` |"
        )

    lines.extend([
        "",
        "---",
        "",
        "## 3. Danh Mục Ghi Chú Hình Ảnh Kịch Bản & File Tư Liệu Theo Cụm (`Episode Visual & Asset Bible`)",
        "",
        f"- **Tổng số file ảnh tư liệu đã phân theo Cụm trong `2_nguyen_lieu/{episode_id}/tu_lieu_tap/<cluster_id>/`:** `{total_asset_count} file` (Chuẩn định danh `{{STT}}_{{beat_id}}_{{t0}}s-{{t1}}s_{{ten_mo_ta}}.jpg`)",
        "",
        "| Mã Phân Đoạn / Skit | Thuộc Cụm (`cluster_id`) | Ghi Chú Hình Ảnh Trích Xuất Tự Động Của Tác Giả (`author_visual_note`) | Các File Tư Liệu Đánh STT + Mốc Giây Trong `tu_lieu_tap/<cluster_id>/` |",
        "| :---: | :--- | :--- | :--- |",
    ])

    seg_to_cluster = {}
    for c in clusters:
        for s_id in c["segments"]:
            seg_to_cluster[s_id] = c["cluster_id"]

    for b in blocks:
        b_label = b["skit_id"] if b["block_type"] == "SKIT_CHAM_BIEM" else b["segment_id"]
        c_mapped = seg_to_cluster.get(b_label, seg_to_cluster.get(b["segment_id"], "N/A"))
        v_note = (b.get("author_visual_note") or "(Dàn dựng hoạt cảnh đối thoại Skit)").replace(" | ", " — ")
        c_files = cluster_assets_map.get(c_mapped, [])
        files_cell = ", ".join(f"`{fn}`" for fn in c_files) if c_files else "`(Chưa có tư liệu)`"
        lines.append(f"| `{b_label}` | `{c_mapped}` | {v_note} | {files_cell} |")

    out_md_path.parent.mkdir(parents=True, exist_ok=True)
    out_md_path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main():
    parser = argparse.ArgumentParser(description="Quét Kịch bản Động & Cắt voice.MP3 Cuốn Chiếu Theo Cụm")
    parser.add_argument("episode_id", help="Mã tập phim trong 1_input/<Ma_Tap> (VD: EP01_Iran)")
    parser.add_argument("--cluster", default=None, help="Mã cụm cần cắt WAV ngay (VD: cum_01_Hoi_I)")
    parser.add_argument("--no-whisper", action="store_true", help="Tắt faster_whisper, chỉ dùng Silence-Valley Slicing")
    args = parser.parse_args()

    script_dir = Path(__file__).resolve().parent
    skill_root = script_dir.parent.parent
    project_root = skill_root.parent.parent.parent
    workspace_dir = project_root / "Du-an-2D-Illustrated-History" / "dung-video-lich-su-hoat-hinh-2d"

    config_path = skill_root / "config" / "ziro_brand_presets.json"
    config = json.loads(config_path.read_text(encoding="utf-8"))

    input_dir = workspace_dir / "1_input" / args.episode_id
    loi_dan_path = input_dir / "kich_ban_loi_dan.txt"
    chia_hoi_path = input_dir / "kich_ban_chia_hoi.txt"
    mp3_path = input_dir / "voice.MP3"
    if not mp3_path.exists():
        mp3_path = input_dir / "voice.mp3"

    for req_file in [loi_dan_path, chia_hoi_path, mp3_path]:
        if not req_file.exists():
            print(f"❌ [FAIL] Thiếu file đầu vào bắt buộc: {req_file}")
            sys.exit(1)

    print("=" * 72)
    print(f"🔍 BƯỚC 1: QUÉT CẤU TRÚC ĐỘNG & PHÂN CỤM THÍCH ỨNG (`{args.episode_id}`)")
    print("=" * 72)

    mp3_dur = probe_audio_duration(mp3_path)
    blocks, extracted_lines, loi_dan_lines = parse_structured_script(chia_hoi_path, loi_dan_path, config)
    clusters = build_dynamic_adaptive_clusters(blocks, mp3_dur, config)

    print(f"• Thời lượng `voice.MP3` gốc          : {mp3_dur:.3f}s ({int(mp3_dur // 60)}m {mp3_dur % 60:.2f}s)")
    print(f"• Số dòng lời dẫn `kich_ban_loi_dan`  : {len(loi_dan_lines)} dòng")
    print(f"• Số dòng bóc từ `kich_ban_chia_hoi`  : {len(extracted_lines)} dòng")
    print(f"• Số Khối Phân đoạn / Skit phát hiện  : {len(blocks)} khối")
    print(f"• Số Cụm Thích Ứng Động (`90s–240s`)   : {len(clusters)} cụm")

    ep_nguyen_lieu_dir = workspace_dir / "2_nguyen_lieu" / args.episode_id
    cac_cum_dir = ep_nguyen_lieu_dir / "cac_cum"
    cac_cum_dir.mkdir(parents=True, exist_ok=True)

    # Xuất gói văn bản `text_<cluster_id>.txt` cho từng Cụm
    for c in clusters:
        c["episode_id"] = args.episode_id
        c_dir = cac_cum_dir / c["cluster_id"]
        c_dir.mkdir(parents=True, exist_ok=True)
        text_lines = [
            f"# CỤM: {c['cluster_id']} | THUỘC: {c['act_id']} ({c['act_title']})",
            f"# LOẠI: {c['cluster_type']} | CÁC PHÂN ĐOẠN: {', '.join(c['segments'])}",
            "",
        ]
        cur_seg = None
        for item in c["lines"]:
            if item["segment_id"] != cur_seg:
                cur_seg = item["segment_id"]
                text_lines.append(f"## [Phân đoạn {cur_seg}] (Hình ảnh: {item['author_visual_note']})")
            text_lines.append(item["text"])
        (c_dir / f"text_{c['cluster_id']}.txt").write_text("\n".join(text_lines) + "\n", encoding="utf-8")

    sliced_results = {}
    target_cluster_id = args.cluster
    if target_cluster_id:
        matched = [c for c in clusters if c["cluster_id"] == target_cluster_id]
        if not matched:
            print(f"❌ [FAIL] Không tìm thấy mã cụm `{target_cluster_id}` trong danh sách: {[c['cluster_id'] for c in clusters]}")
            sys.exit(1)
        c_target = matched[0]
        print("-" * 72)
        print(f"✂️ ĐANG CẮT GÓI ÂM THANH `0.000s` TỪ `voice.MP3` CHO CỤM: `{target_cluster_id}`...")
        c_dir = cac_cum_dir / target_cluster_id
        tl_data = align_and_slice_cluster_audio(
            mp3_path=mp3_path,
            cluster_dir=c_dir,
            cluster_info=c_target,
            use_whisper=(not args.no_whisper),
        )
        sliced_results[target_cluster_id] = tl_data
        print(f"✅ Đã cắt xong `{tl_data['beats_count']}` file `.wav` vào `{c_dir / 'beats_wav'}`!")
        print(f"   • Tổng thời lượng Cụm (`float64`): {tl_data['total_duration_sec']:.6f}s")
        for b in tl_data["beats"]:
            print(
                f"   • [{b['beat_id']} | Seg {b['segment_id']}] {b['t0']:6.3f}s -> {b['t1']:6.3f}s "
                f"(dur={b['duration']:6.3f}s): {b['narration_text'][:65]}..."
            )

    dossier_path = ep_nguyen_lieu_dir / "01_ho_so_chia_cum.md"
    write_episode_cluster_dossier(args.episode_id, mp3_dur, blocks, clusters, sliced_results, dossier_path)
    print("-" * 72)
    print(f"📄 Đã xuất Hồ sơ Phân Cụm: {dossier_path}")
    print("✅ [PASS 100%] Hoàn tất Bước 1 (Quét cấu trúc động & Cắt âm thanh 0.000s)!")
    print("=" * 72)


if __name__ == "__main__":
    main()
