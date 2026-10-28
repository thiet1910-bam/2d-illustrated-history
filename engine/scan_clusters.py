#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ziro-History-Studio-v3 — Dynamic Adaptive Cluster Scanner, 0ms Slicer & 30fps Lip-Sync Extractor
Usage:
  1. Scan episode & generate cluster_plan.json:
     python engine/scan_clusters.py --episode EP01_Demo
  2. Slice sample-accurate 48kHz WAVs + extract 30fps mouth_30fps & word timestamps:
     python engine/scan_clusters.py --episode EP01_Demo --cluster cum_01_Hoi_I
  3. Refresh mouth_30fps on an already-sliced timeline JSON:
     python engine/scan_clusters.py --episode EP01_Demo --cluster cum_01_Hoi_I --lipsync-only
"""
import argparse
import difflib
import json
import math
import re
import struct
import subprocess
import sys
import unicodedata
import wave
from pathlib import Path
import numpy as np

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STUDIO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bins import resolve_ffmpeg

SR = 48000
FPS = 30


def get_ffmpeg() -> str:
    return resolve_ffmpeg()


def probe_audio_duration(audio_path: Path) -> float:
    if audio_path.suffix.lower() == ".wav":
        with wave.open(str(audio_path), "rb") as wf:
            return round(wf.getnframes() / float(wf.getframerate()), 6)
    cmd = [get_ffmpeg(), "-hide_banner", "-i", str(audio_path)]
    proc = subprocess.run(cmd, stderr=subprocess.PIPE, stdout=subprocess.PIPE, text=True, encoding="utf-8", errors="ignore")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", proc.stderr)
    if m:
        h, mi, s = int(m.group(1)), int(m.group(2)), float(m.group(3))
        return round(h * 3600 + mi * 60 + s, 3)
    raise RuntimeError(f"Could not determine duration of {audio_path}")


def compute_mouth_states_30fps(wav_path: Path, fps: int = FPS) -> list:
    """
    Computes discrete Ziro cutout lip-sync states at 30fps from a WAV file:
      0 = closed (silence / pause)
      1 = slightly open
      2 = medium D-mouth
      3 = wide open vowel peak
    """
    with wave.open(str(wav_path), "rb") as wf:
        sr = wf.getframerate()
        nch = wf.getnchannels()
        raw = wf.readframes(wf.getnframes())

    arr = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if nch > 1:
        arr = arr.reshape(-1, nch).mean(axis=1)

    total_dur = len(arr) / float(sr)
    num_frames = max(1, int(math.ceil(total_dur * fps)))
    hop = sr / float(fps)

    rms_vals = np.zeros(num_frames, dtype=np.float32)
    for i in range(num_frames):
        s0 = int(i * hop)
        s1 = min(len(arr), int((i + 1) * hop))
        if s1 > s0:
            rms_vals[i] = float(np.sqrt(np.mean(arr[s0:s1] ** 2)))

    nonzero = rms_vals[rms_vals > 0.008]
    ref = float(np.percentile(nonzero, 88)) if len(nonzero) > 5 else 0.12
    ref = max(ref, 0.025)

    states = []
    for i, r in enumerate(rms_vals):
        norm = r / ref
        if norm < 0.14:
            st = 0
        elif norm < 0.42:
            st = 1
        elif norm < 0.78:
            st = 2
        else:
            st = 3
        # Add natural syllable flutter so sustained loud vowels still articulate like Ziro cutout puppets
        if st >= 2 and i >= 2 and states[-1] == st and states[-2] == st:
            st = 1 if st == 2 else 2
        states.append(st)
    return states


def parse_structured_script(chia_hoi_path: Path, loi_dan_path: Path):
    raw_lines = chia_hoi_path.read_text(encoding="utf-8").splitlines()
    loi_dan_lines = [ln.strip() for ln in loi_dan_path.read_text(encoding="utf-8").splitlines() if ln.strip()]

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
            "block_type": block_type,
            "skit_id": f"Skit_{skit_num}" if skit_num else None,
            "author_visual_note": visual_note or "2D Ziro Historical Stage",
            "lines": [],
        }

    in_skit_dialogue = False

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
            skit_num = m_skit.group(1).strip()
            skit_desc = m_skit.group(2).strip()
            in_skit_dialogue = True
            start_new_block(
                "SKIT_CHAM_BIEM",
                f"{current_seg_id}_Skit_{skit_num}",
                f"Skit #{skit_num}: {skit_desc}",
                f"{current_visual_note} | Skit #{skit_num}: {skit_desc}",
                skit_num=skit_num,
            )
            continue

        if stage_note_re.match(line):
            continue

        is_dialogue_line = line.startswith(("—", "-", '"', "“"))
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

    extracted_lines = [item["text"] for b in blocks for item in b["lines"]]
    return blocks, extracted_lines, loi_dan_lines


def to_ascii_slug(s: str) -> str:
    s_norm = unicodedata.normalize("NFD", s)
    s_ascii = "".join(ch for ch in s_norm if unicodedata.category(ch) != "Mn")
    s_ascii = s_ascii.replace("Đ", "D").replace("đ", "d")
    return re.sub(r"[^A-Za-z0-9]+", "_", s_ascii).strip("_")


def build_dynamic_clusters(blocks: list, total_audio_duration: float, max_beats: int = 22, max_dur: float = 240.0) -> list:
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

    cum_t = 0.0
    final_clusters = []
    for idx, c in enumerate(raw_clusters, start=1):
        act_slug = to_ascii_slug(c["act_id"]).title()
        m_roman = re.match(r"(?i)^(Hoi|Act|Chuong|Phan)_([IVXLCDM0-9]+)$", act_slug)
        if m_roman:
            act_slug = f"{m_roman.group(1).capitalize()}_{m_roman.group(2).upper()}"
        if c["cluster_type"] == "SKIT_CHAM_BIEM":
            c_id = f"cum_{idx:02d}_{c['skit_id']}"
        else:
            seg_tag = "_".join(s.replace(".", "_") for s in c["segments"])
            c_id = "cum_01_Hoi_I" if (idx == 1 and act_slug == "Hoi_I") else f"cum_{idx:02d}_{act_slug}_seg_{seg_tag}"

        t0_est = round(cum_t, 2)
        t1_est = round(min(total_audio_duration, cum_t + c["est_duration"]), 2)
        cum_t = t1_est
        c["cluster_id"] = c_id
        c["order_index"] = idx
        c["est_t0"] = t0_est
        c["est_t1"] = t1_est
        final_clusters.append(c)

    return final_clusters


def split_paragraph_into_beats(lines_list: list) -> list:
    beats = []
    for item in lines_list:
        text = item["text"].strip()
        if len(text.split()) > 95:
            sentences = re.split(r"(?<=[.!?])\s+", text)
            if len(sentences) >= 2:
                mid = len(sentences) // 2
                for part in (" ".join(sentences[:mid]).strip(), " ".join(sentences[mid:]).strip()):
                    if part:
                        beats.append({
                            "narration_text": part,
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

    if sampwidth != 2:
        return round(target_sec, 6)

    samples = struct.unpack(f"<{len(raw_bytes)//2}h", raw_bytes)
    if nch > 1:
        samples = samples[::nch]

    win_size = int(0.025 * sr)
    step = int(0.005 * sr)
    if len(samples) < win_size:
        return round(target_sec, 6)

    best_t = target_sec
    min_energy = float("inf")
    for i in range(0, len(samples) - win_size, step):
        chunk = samples[i : i + win_size]
        rms = sum(s * s for s in chunk) / float(win_size)
        t_cur = t_start + (i + win_size / 2.0) / float(sr)
        dist_penalty = 1.0 + 0.5 * abs(t_cur - target_sec) / max(search_radius_sec, 0.01)
        score = rms * dist_penalty
        if score < min_energy:
            min_energy = score
            best_t = t_cur

    return round(best_t, 6)


def slice_wav_exact_frames(src_wav: Path, dst_wav: Path, t0: float, t1: float) -> tuple:
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
        dur = round(vf.getnframes() / float(vf.getframerate()), 6)

    return round(f0 / float(sr), 6), round(f1 / float(sr), 6), dur


def align_and_slice_cluster_audio(
    mp3_path: Path,
    cache_cluster_dir: Path,
    timelines_dir: Path,
    cluster_info: dict,
    use_whisper: bool = True,
) -> dict:
    ffmpeg_exe = get_ffmpeg()
    beats_meta = split_paragraph_into_beats(cluster_info["lines"])
    num_beats = len(beats_meta)
    is_skit = cluster_info["cluster_type"] == "SKIT_CHAM_BIEM"
    min_beat_gap = 0.45 if is_skit else 1.0

    if cluster_info.get("exact_prev_t1") is not None:
        search_t0 = float(cluster_info["exact_prev_t1"])
    else:
        search_t0 = max(0.0, cluster_info["est_t0"] - (5.0 if cluster_info["order_index"] > 1 else 0.0))
    search_dur = max(cluster_info["est_duration"] + 35.0, (cluster_info["est_t1"] - search_t0) + 35.0)

    cache_cluster_dir.mkdir(parents=True, exist_ok=True)
    raw_window_wav = cache_cluster_dir / "_temp_window_48k.wav"

    subprocess.run(
        [
            ffmpeg_exe, "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{search_t0:.3f}", "-t", f"{search_dur:.3f}",
            "-i", str(mp3_path),
            "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(raw_window_wav),
        ],
        check=True,
    )

    whisper_boundaries = None
    words_timed = []
    if use_whisper:
        try:
            from faster_whisper import WhisperModel

            raw_16k_wav = cache_cluster_dir / "_temp_window_16k.wav"
            subprocess.run(
                [
                    ffmpeg_exe, "-hide_banner", "-loglevel", "error", "-y",
                    "-i", str(raw_window_wav),
                    "-ar", "16000", "-ac", "1", "-c:a", "pcm_s16le", str(raw_16k_wav),
                ],
                check=True,
            )
            with wave.open(str(raw_16k_wav), "rb") as wf16:
                audio_16k = np.frombuffer(wf16.readframes(wf16.getnframes()), dtype=np.int16).astype(np.float32) / 32768.0
            if raw_16k_wav.exists():
                raw_16k_wav.unlink()

            model = WhisperModel("base", device="cpu", compute_type="int8")
            segments_gen, _ = model.transcribe(audio_16k, language="vi", word_timestamps=True, vad_filter=False)
            words_timed = [
                {"word": w.word.strip(), "start": float(w.start), "end": float(w.end)}
                for seg in segments_gen if seg.words for w in seg.words
            ]
            if len(words_timed) >= 10:
                def _clean_ascii(s: str) -> str:
                    s_n = unicodedata.normalize("NFD", s.lower().replace("đ", "d"))
                    s_a = "".join(c for c in s_n if unicodedata.category(c) != "Mn")
                    return re.sub(r"[^a-z0-9\s]+", " ", s_a).strip()

                w_clean_list = [_clean_ascii(w["word"]) for w in words_timed]
                beat_tokens_list = [[t for t in _clean_ascii(b["narration_text"]).split() if t] for b in beats_meta]

                boundaries = [0.0]
                cur_w_ptr = 0
                for b_idx in range(num_beats):
                    b_toks = beat_tokens_list[b_idx]
                    expected_len = max(1, len(b_toks))
                    approx_k = min(len(words_timed) - 1, cur_w_ptr + expected_len - 1)
                    search_lo = max(cur_w_ptr, approx_k - max(6, int(expected_len * 0.5)))
                    search_hi = min(len(words_timed) - 2, approx_k + max(6, int(expected_len * 0.5)))

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
                    boundaries.append(find_nearest_silence_valley(raw_window_wav, raw_cut_t, search_radius_sec=0.18))
                    cur_w_ptr = best_k + 1

                whisper_boundaries = boundaries
        except Exception as e:
            print(f"[WARN] faster_whisper unavailable/failed ({e}) -> using Silence-Valley Proportional Slicing")

    if not whisper_boundaries:
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
        whisper_boundaries = boundaries

    for i in range(1, len(whisper_boundaries)):
        if whisper_boundaries[i] <= whisper_boundaries[i - 1] + min_beat_gap:
            whisper_boundaries[i] = round(whisper_boundaries[i - 1] + max(1.1, min_beat_gap + 0.5), 6)

    cluster_wav_path = cache_cluster_dir / f"voice_{cluster_info['cluster_id']}.wav"
    slice_wav_exact_frames(raw_window_wav, cluster_wav_path, whisper_boundaries[0], whisper_boundaries[-1])

    # Extract 30fps lip-sync states for the entire cluster!
    mouth_30fps = compute_mouth_states_30fps(cluster_wav_path, FPS)

    beats_wav_dir = cache_cluster_dir / "beats_wav"
    beats_wav_dir.mkdir(parents=True, exist_ok=True)
    for old_wav in beats_wav_dir.glob("*.wav"):
        old_wav.unlink()

    beats_output = []
    cum_t0 = 0.0
    base_offset = whisper_boundaries[0]
    for idx in range(num_beats):
        rel_t0 = whisper_boundaries[idx] - base_offset
        rel_t1 = whisper_boundaries[idx + 1] - base_offset
        beat_id = f"beat_{idx + 1:02d}"
        wav_filename = f"{beat_id}.wav"
        _, _, exact_dur = slice_wav_exact_frames(cluster_wav_path, beats_wav_dir / wav_filename, rel_t0, rel_t1)
        beat_t0 = round(cum_t0, 6)
        beat_t1 = round(cum_t0 + exact_dur, 6)
        cum_t0 = beat_t1

        # Attach relative word timestamps inside this beat for micro-beat triggers
        beat_words = [
            {"w": w["word"], "bt": round(max(0.0, (w["start"] - base_offset) - beat_t0), 3)}
            for w in words_timed
            if (w["start"] - base_offset) >= (beat_t0 - 0.15) and (w["start"] - base_offset) < (beat_t1 + 0.1)
        ]

        beats_output.append({
            "beat_id": beat_id,
            "segment_id": beats_meta[idx]["segment_id"],
            "author_visual_note": beats_meta[idx]["author_visual_note"],
            "wav_file": f"beats_wav/{wav_filename}",
            "source_mp3_t0": round(search_t0 + whisper_boundaries[idx], 3),
            "source_mp3_t1": round(search_t0 + whisper_boundaries[idx + 1], 3),
            "t0": beat_t0,
            "t1": beat_t1,
            "duration": exact_dur,
            "narration_text": beats_meta[idx]["narration_text"],
            "words": beat_words,
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
        "fps": FPS,
        "beats_count": len(beats_output),
        "beats": beats_output,
        "mouth_30fps": mouth_30fps,
    }

    timelines_dir.mkdir(parents=True, exist_ok=True)
    tl_path = timelines_dir / f"timeline_{cluster_info['cluster_id']}.json"
    tl_path.write_text(json.dumps(timeline_data, ensure_ascii=False, indent=2), encoding="utf-8")
    return timeline_data


def refresh_lipsync_only(episode: str, cluster: str):
    timelines_dir = STUDIO_ROOT / "episodes" / episode / "2_assets" / "timelines"
    tl_path = timelines_dir / f"timeline_{cluster}.json"
    cache_wav = STUDIO_ROOT / ".cache" / episode / cluster / f"voice_{cluster}.wav"
    if not tl_path.exists() or not cache_wav.exists():
        raise FileNotFoundError(f"Need both {tl_path} and {cache_wav} for --lipsync-only")
    tl = json.loads(tl_path.read_text(encoding="utf-8"))
    tl["fps"] = FPS
    tl["mouth_30fps"] = compute_mouth_states_30fps(cache_wav, FPS)
    tl_path.write_text(json.dumps(tl, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"[LIPSYNC PASS] Injected {len(tl['mouth_30fps'])} frames of 30fps lip-sync states -> {tl_path}")


def auto_bootstrap_chia_hoi(loi_dan_path: Path, chia_hoi_path: Path):
    """
    When a user provides ONLY voice.MP3 + kich_ban_loi_dan.txt (2-file minimal input),
    automatically constructs a clean kich_ban_chia_hoi.txt grouping dialogue lines (— "...")
    into Skit #K blocks and narrative lines into ~14-beat segments across Acts.
    """
    raw_lines = [ln.strip() for ln in loi_dan_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    romans = ["I", "II", "III", "IV", "V", "VI", "VII", "VIII", "IX", "X"]
    out = ["HỒI I: MỞ ĐẦU", "Phân đoạn 1.1:"]
    act_idx = 1
    seg_idx = 1
    skit_idx = 0
    in_skit = False
    narr_in_seg = 0

    for ln in raw_lines:
        is_dialogue = bool(re.match(r"^[—–\-]\s*[\"“]", ln))
        if is_dialogue:
            if not in_skit:
                skit_idx += 1
                out.append(f"(Chuyển nhịp Skit #{skit_idx}: Tiểu phẩm đối đáp châm biếm)")
                in_skit = True
            out.append(ln)
        else:
            if in_skit:
                in_skit = False
                seg_idx += 1
                narr_in_seg = 0
                out.append(f"Phân đoạn {act_idx}.{seg_idx}:")
            elif narr_in_seg >= 14:
                if seg_idx >= 3 and act_idx < len(romans):
                    act_idx += 1
                    seg_idx = 1
                    out.append(f"HỒI {romans[act_idx - 1]}: DIỄN BIẾN TIẾP THEO")
                else:
                    seg_idx += 1
                narr_in_seg = 0
                out.append(f"Phân đoạn {act_idx}.{seg_idx}:")
            out.append(ln)
            narr_in_seg += 1

    chia_hoi_path.write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"[AUTO-STRUCTURE] Generated {chia_hoi_path.name} from plain script ({act_idx} Acts, {skit_idx} Skits)")


def main():
    parser = argparse.ArgumentParser(description="Ziro-History-Studio-v3 Dynamic Cluster Scanner & 30fps Lip-Sync Slicer")
    parser.add_argument("--episode", required=True, help="Episode ID inside episodes/<EP_ID> (e.g. EP02_Korea)")
    parser.add_argument("--cluster", default=None, help="Cluster ID to slice WAVs into .cache/ (e.g. cum_01_Hoi_I)")
    parser.add_argument("--no-whisper", action="store_true", help="Disable faster_whisper and use Silence-Valley slicing")
    parser.add_argument("--lipsync-only", action="store_true", help="Compute 30fps mouth states on existing sliced WAV")
    args = parser.parse_args()

    if args.lipsync_only and args.cluster:
        refresh_lipsync_only(args.episode, args.cluster)
        return

    ep_dir = STUDIO_ROOT / "episodes" / args.episode
    in_dir = ep_dir / "1_input"
    loi_dan_path = in_dir / "kich_ban_loi_dan.txt"
    chia_hoi_path = in_dir / "kich_ban_chia_hoi.txt"
    mp3_path = in_dir / "voice.MP3" if (in_dir / "voice.MP3").exists() else (in_dir / "voice.mp3")

    for req_file in (loi_dan_path, mp3_path):
        if not req_file.exists():
            print(f"[FAIL] Missing required input file: {req_file}")
            sys.exit(1)

    if not chia_hoi_path.exists():
        auto_bootstrap_chia_hoi(loi_dan_path, chia_hoi_path)

    mp3_dur = probe_audio_duration(mp3_path)
    blocks, extracted_lines, loi_dan_lines = parse_structured_script(chia_hoi_path, loi_dan_path)
    clusters = build_dynamic_clusters(blocks, mp3_dur)

    timelines_dir = ep_dir / "2_assets" / "timelines"
    timelines_dir.mkdir(parents=True, exist_ok=True)

    if args.cluster:
        matched = [c for c in clusters if c["cluster_id"] == args.cluster]
        if not matched:
            print(f"[FAIL] Cluster '{args.cluster}' not found in {[c['cluster_id'] for c in clusters]}")
            sys.exit(1)
        c_target = matched[0]
        c_target["episode_id"] = args.episode
        if c_target["order_index"] > 1:
            prev_c = clusters[c_target["order_index"] - 2]
            prev_tl = timelines_dir / f"timeline_{prev_c['cluster_id']}.json"
            if prev_tl.exists():
                prev_data = json.loads(prev_tl.read_text(encoding="utf-8"))
                if prev_data.get("beats"):
                    c_target["exact_prev_t1"] = prev_data["beats"][-1]["source_mp3_t1"]

        cache_cluster_dir = STUDIO_ROOT / ".cache" / args.episode / args.cluster
        tl_data = align_and_slice_cluster_audio(
            mp3_path=mp3_path,
            cache_cluster_dir=cache_cluster_dir,
            timelines_dir=timelines_dir,
            cluster_info=c_target,
            use_whisper=(not args.no_whisper),
        )
        print(f"[SLICE + LIPSYNC PASS] {args.cluster}: {tl_data['beats_count']} beats ({tl_data['total_duration_sec']:.3f}s) | {len(tl_data['mouth_30fps'])} mouth frames")

    plan_summary = []
    for c in clusters:
        c["episode_id"] = args.episode
        tl_file = timelines_dir / f"timeline_{c['cluster_id']}.json"
        mp4_file = ep_dir / "4_output" / "clusters" / f"{c['cluster_id']}.mp4"
        status = "RENDERED" if mp4_file.exists() else ("SLICED" if tl_file.exists() else "PENDING")
        plan_summary.append({
            "order_index": c["order_index"],
            "cluster_id": c["cluster_id"],
            "act_id": c["act_id"],
            "cluster_type": c["cluster_type"],
            "segments": c["segments"],
            "beats_est": len(c["lines"]),
            "est_t0": c["est_t0"],
            "est_t1": c["est_t1"],
            "est_duration": c["est_duration"],
            "status": status,
        })

    plan_path = timelines_dir / "cluster_plan.json"
    plan_path.write_text(
        json.dumps({"episode_id": args.episode, "audio_duration_sec": mp3_dur, "clusters": plan_summary}, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(f"[SCAN PASS] Episode={args.episode} | Audio={mp3_dur:.2f}s | Clusters={len(clusters)} -> {plan_path}")


if __name__ == "__main__":
    main()
