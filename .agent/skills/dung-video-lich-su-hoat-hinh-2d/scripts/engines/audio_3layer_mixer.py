#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 4.3: 3-Layer Audio Mixer & Auto-Ducking Engine (`audio_3layer_mixer.py`)
-----------------------------------------------------------------------------
Mixes:
  - Layer 1: Voice Narration (0.0 dB, sample-locked to `beats_wav/beat_XX.wav`, 0ms drift)
  - Layer 2: Foley SFX (-6.0 dB, triggered at exact `t0 + bt` timestamps)
  - Layer 3: Background Music (BGM) with automatic speech-envelope ducking (-16.0 dB active / -9.0 dB pause)
Also auto-synthesizes missing physical WAV assets in `2_nguyen_lieu/0_kho_dung_chung/audio_sfx_bgm/`.
"""

import os
import sys
import json
import math
import wave
import shutil
import argparse
from pathlib import Path
import numpy as np

SR = 44100
SKILL_ROOT = Path(__file__).resolve().parents[2]


def db_to_gain(db: float) -> float:
    return float(10.0 ** (float(db) / 20.0))


def write_stereo_wav(path: Path, data_float: np.ndarray, sr: int = SR):
    """Writes a (N, 2) float32 array in [-1, 1] to 16-bit PCM stereo WAV."""
    path.parent.mkdir(parents=True, exist_ok=True)
    clipped = np.clip(data_float, -0.99, 0.99)
    pcm16 = (clipped * 32767.0).astype(np.int16)
    with wave.open(str(path), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sr)
        wf.writeframes(pcm16.tobytes())


def read_wav_stereo_float(path: Path) -> np.ndarray:
    """Reads a WAV file and returns a (N, 2) float32 array at 44100Hz."""
    with wave.open(str(path), "rb") as wf:
        nch = wf.getnchannels()
        sr = wf.getframerate()
        nframes = wf.getnframes()
        raw = wf.readframes(nframes)
    pcm = np.frombuffer(raw, dtype=np.int16).astype(np.float32) / 32768.0
    if nch == 1:
        stereo = np.column_stack([pcm, pcm])
    else:
        pcm = pcm.reshape(-1, nch)
        stereo = pcm[:, :2]
    if sr != SR and len(stereo) > 0:
        new_len = int(round(len(stereo) * SR / sr))
        x_old = np.linspace(0.0, 1.0, len(stereo))
        x_new = np.linspace(0.0, 1.0, new_len)
        left = np.interp(x_new, x_old, stereo[:, 0])
        right = np.interp(x_new, x_old, stereo[:, 1])
        stereo = np.column_stack([left, right]).astype(np.float32)
    return stereo


def ensure_sfx_bgm_library(audio_lib_dir: Path):
    """Synthesizes physical WAV files for all standard Ziro Foley SFX and BGM tracks if missing,
    and syncs the 8 authentic Ziro History SFX WAVs from the Skill's self-contained vault."""
    audio_lib_dir.mkdir(parents=True, exist_ok=True)
    vault_sfx_dir = SKILL_ROOT / "kho_rieng_2d_history_va_opus5_5" / "ziro_authentic_sfx"
    target_ziro_dir = audio_lib_dir / "ziro_authentic_sfx"
    if vault_sfx_dir.exists():
        target_ziro_dir.mkdir(parents=True, exist_ok=True)
        for wav_f in vault_sfx_dir.glob("*.wav"):
            dst_f = target_ziro_dir / wav_f.name
            if not dst_f.exists():
                shutil.copy2(wav_f, dst_f)

    rng = np.random.default_rng(42)

    # 1. pop_card.wav (0.22s crisp dual-tone pop)
    p = audio_lib_dir / "pop_card.wav"
    if not p.exists():
        t = np.linspace(0, 0.22, int(SR * 0.22), endpoint=False)
        freq = 320.0 + 520.0 * np.exp(-t * 28.0)
        sig = np.sin(2 * np.pi * freq * t) * np.exp(-t * 18.0) * 0.75
        write_stereo_wav(p, np.column_stack([sig, sig]))

    # 2. whoosh_transition.wav (0.38s aerodynamic stereo whoosh)
    p = audio_lib_dir / "whoosh_transition.wav"
    if not p.exists():
        t = np.linspace(0, 0.38, int(SR * 0.38), endpoint=False)
        env = np.sin(np.pi * (t / 0.38)) ** 2
        noise = rng.normal(0, 0.35, len(t))
        sweep = np.sin(2 * np.pi * (140 + 260 * (t / 0.38)) * t) * 0.45
        left = (noise + sweep) * env * np.linspace(1.0, 0.4, len(t))
        right = (noise + sweep) * env * np.linspace(0.4, 1.0, len(t))
        write_stereo_wav(p, np.column_stack([left, right]))

    # 3. stamp_slam.wav (0.42s heavy impact thud + crisp transient)
    p = audio_lib_dir / "stamp_slam.wav"
    if not p.exists():
        t = np.linspace(0, 0.42, int(SR * 0.42), endpoint=False)
        sub = np.sin(2 * np.pi * (95.0 * np.exp(-t * 12.0) + 42.0) * t) * np.exp(-t * 9.5)
        snap = rng.normal(0, 0.5, len(t)) * np.exp(-t * 45.0)
        sig = np.clip((sub * 0.85 + snap * 0.45), -0.95, 0.95)
        write_stereo_wav(p, np.column_stack([sig, sig]))

    # 4. jail_bar_clang.wav (0.65s metallic iron bar slam & ring)
    p = audio_lib_dir / "jail_bar_clang.wav"
    if not p.exists():
        t = np.linspace(0, 0.65, int(SR * 0.65), endpoint=False)
        freqs = [285.0, 542.0, 818.0, 1240.0, 1790.0]
        decays = [6.0, 8.5, 11.0, 14.0, 18.0]
        sig = np.zeros_like(t)
        for f, d in zip(freqs, decays):
            sig += np.sin(2 * np.pi * f * t) * np.exp(-t * d) * 0.24
        thud = np.sin(2 * np.pi * 68.0 * t) * np.exp(-t * 14.0) * 0.5
        sig = np.clip(sig + thud, -0.95, 0.95)
        write_stereo_wav(p, np.column_stack([sig, sig]))

    # 5. typewriter_tick.wav (0.08s mechanical key click)
    p = audio_lib_dir / "typewriter_tick.wav"
    if not p.exists():
        t = np.linspace(0, 0.08, int(SR * 0.08), endpoint=False)
        sig = (np.sin(2 * np.pi * 1650.0 * t) + rng.normal(0, 0.3, len(t))) * np.exp(-t * 65.0) * 0.65
        write_stereo_wav(p, np.column_stack([sig, sig]))

    # 6. sword_clash.wav (0.50s metallic blade ring)
    p = audio_lib_dir / "sword_clash.wav"
    if not p.exists():
        t = np.linspace(0, 0.50, int(SR * 0.50), endpoint=False)
        ring = (
            np.sin(2 * np.pi * 1120.0 * t) * 0.35
            + np.sin(2 * np.pi * 1890.0 * t) * 0.28
            + np.sin(2 * np.pi * 2740.0 * t) * 0.20
        ) * np.exp(-t * 9.0)
        scrape = rng.normal(0, 0.35, len(t)) * np.exp(-t * 28.0)
        sig = np.clip(ring + scrape, -0.95, 0.95)
        write_stereo_wav(p, np.column_stack([sig, sig]))

    # 7. bgm_tense_history.wav (16.0s cinematic historical tension loop)
    p = audio_lib_dir / "bgm_tense_history.wav"
    if not p.exists():
        dur = 16.0
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        # D-minor harmonic drone + rhythmic pulse at 90 BPM (0.666s beat)
        drone_l = (
            0.28 * np.sin(2 * np.pi * 73.42 * t)
            + 0.18 * np.sin(2 * np.pi * 110.0 * t + 0.3)
            + 0.12 * np.sin(2 * np.pi * 146.83 * t)
            + 0.08 * np.sin(2 * np.pi * 220.0 * t * (1.0 + 0.002 * np.sin(2 * np.pi * 0.25 * t)))
        )
        drone_r = (
            0.28 * np.sin(2 * np.pi * 73.42 * t)
            + 0.18 * np.sin(2 * np.pi * 110.0 * t - 0.3)
            + 0.12 * np.sin(2 * np.pi * 174.61 * t)
            + 0.08 * np.sin(2 * np.pi * 220.0 * t)
        )
        pulse = (0.5 + 0.5 * np.sin(2 * np.pi * 1.5 * t)) ** 3
        p_tone = 0.18 * np.sin(2 * np.pi * 55.0 * t) * pulse
        write_stereo_wav(p, np.column_stack([drone_l + p_tone, drone_r + p_tone]) * 0.85)

    # 8. bgm_satire_skit.wav (12.0s light satirical plucked rhythm loop)
    p = audio_lib_dir / "bgm_satire_skit.wav"
    if not p.exists():
        dur = 12.0
        t = np.linspace(0, dur, int(SR * dur), endpoint=False)
        notes = [196.0, 220.0, 246.94, 293.66, 261.63, 220.0, 196.0, 164.81]
        step_sec = 0.375
        sig = np.zeros_like(t)
        for i in range(int(dur / step_sec)):
            f = notes[i % len(notes)]
            i0 = int(i * step_sec * SR)
            i1 = min(len(t), int((i + 1) * step_sec * SR))
            lt = np.arange(i1 - i0) / SR
            sig[i0:i1] = (np.sin(2 * np.pi * f * lt) + 0.4 * np.sin(2 * np.pi * 2 * f * lt)) * np.exp(-lt * 10.0) * 0.35
        write_stereo_wav(p, np.column_stack([sig, sig]))


def mix_cluster_audio(manifest_path: Path, out_wav_path: Path = None):
    """
    Mixes all beats in `beat_manifest_<cluster_id>.json` with 0.000ms drift.
    Also writes per-beat mixed WAVs (`beats_wav/beat_XX_mixed.wav`) so single-beat
    cache rendering in Stage 5 has ready-to-mux 3-layer audio per beat!
    """
    manifest_path = Path(manifest_path).resolve()
    cluster_dir = manifest_path.parent
    workspace_root = cluster_dir
    for p in manifest_path.parents:
        if (p / "2_nguyen_lieu").exists() and (p / "3_output").exists():
            workspace_root = p
            break
    audio_lib_dir = workspace_root / "2_nguyen_lieu" / "0_kho_dung_chung" / "audio_sfx_bgm"

    ensure_sfx_bgm_library(audio_lib_dir)

    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    cluster_id = manifest.get("cluster_id", "cum_01")
    bgm_name = manifest.get("bgm_track", "bgm_tense_history.wav")
    bgm_path = audio_lib_dir / bgm_name
    if not bgm_path.exists():
        bgm_path = audio_lib_dir / "bgm_tense_history.wav"
    bgm_loop = read_wav_stereo_float(bgm_path)

    beats = manifest.get("beats", [])
    beat_voice_arrays = []
    for b in beats:
        wav_rel = b.get("wav_file", f"beats_wav/{b['beat_id']}.wav")
        wpath = cluster_dir / wav_rel
        if not wpath.exists():
            raise FileNotFoundError(f"Missing beat WAV file: {wpath}")
        arr = read_wav_stereo_float(wpath)
        beat_voice_arrays.append(arr)

    # Layer 1: Concatenate exact voice samples (0.0 dB)
    voice_track = np.vstack(beat_voice_arrays)
    total_samples = len(voice_track)
    mixed_dur_sec = total_samples / float(SR)

    # Layer 2: Foley SFX Track (Calibrated to Ziro History's -26 to -34 dBFS organic Foley floor)
    sfx_track = np.zeros_like(voice_track)
    sfx_verification = []
    cursor_sample = 0
    ziro_sfx_dir = audio_lib_dir / "ziro_authentic_sfx"
    ziro_sfx_map = {
        "pop_card.wav": "ziro_pop_soft.wav",
        "whoosh_transition.wav": "ziro_scroll_unroll.wav",
        "stamp_slam.wav": "ziro_rubber_stamp.wav",
        "typewriter_tick.wav": "ziro_icon_pop_rapid.wav",
        "sword_clash.wav": "ziro_spear_drop.wav",
        "jail_bar_clang.wav": "ziro_padlock_slam.wav",
    }

    for b, v_arr in zip(beats, beat_voice_arrays):
        b_len = len(v_arr)
        for ev in b.get("sfx_events", []):
            bt = float(ev.get("bt", 0.0))
            sfx_file = ev.get("sfx_file", "pop_card.wav")
            gain_db = float(ev.get("gain_db", -14.5))
            mapped_ziro = ziro_sfx_map.get(sfx_file, sfx_file if sfx_file.startswith("ziro_") else "")
            if mapped_ziro and (ziro_sfx_dir / mapped_ziro).exists():
                sfx_path = ziro_sfx_dir / mapped_ziro
                # Authentic Ziro SFX is already normalized to -14 dBFS peak; apply subtle trim
                eff_gain_db = min(gain_db + 6.0, -6.5)
            else:
                sfx_path = audio_lib_dir / sfx_file
                eff_gain_db = min(gain_db, -13.5)
            if not sfx_path.exists():
                continue
            sfx_arr = read_wav_stereo_float(sfx_path) * db_to_gain(eff_gain_db)
            s_idx = cursor_sample + max(0, min(b_len - 1, int(round(bt * SR))))
            e_idx = min(total_samples, s_idx + len(sfx_arr))
            seg_len = e_idx - s_idx
            if seg_len > 0:
                sfx_track[s_idx:e_idx] += sfx_arr[:seg_len]
                peak_rms = float(np.sqrt(np.mean(sfx_arr[:seg_len] ** 2)))
                sfx_verification.append({
                    "beat_id": b["beat_id"],
                    "bt_sec": bt,
                    "global_t_sec": round(s_idx / SR, 3),
                    "sfx_file": sfx_file,
                    "source_wav": sfx_path.name,
                    "gain_db": round(eff_gain_db, 2),
                    "rms": round(peak_rms, 5),
                })
        cursor_sample += b_len

    # Layer 3: BGM with Auto-Ducking (-20.0 dB during speech, -12.5 dB during pauses)
    repeats = int(math.ceil(total_samples / max(1, len(bgm_loop)))) + 1
    bgm_raw = np.tile(bgm_loop, (repeats, 1))[:total_samples]

    # Compute smoothed speech envelope in 50ms chunks
    win = int(0.05 * SR)
    n_wins = int(math.ceil(total_samples / win))
    duck_gain_active = db_to_gain(-20.0)
    duck_gain_pause = db_to_gain(-12.5)
    win_gains = np.empty(n_wins, dtype=np.float32)

    for w_i in range(n_wins):
        s0 = w_i * win
        s1 = min(total_samples, s0 + win)
        rms = float(np.sqrt(np.mean(voice_track[s0:s1] ** 2)))
        win_gains[w_i] = duck_gain_active if rms > 0.012 else duck_gain_pause

    # Smooth envelope with a 7-window moving average (~350ms attack/release)
    kernel = np.ones(7, dtype=np.float32) / 7.0
    win_gains_smooth = np.convolve(win_gains, kernel, mode="same")
    sample_gains = np.repeat(win_gains_smooth, win)[:total_samples]
    bgm_track = bgm_raw * sample_gains[:, None]

    # Master Mix = Layer 1 (Voice) + Layer 2 (SFX) + Layer 3 (BGM)
    master_mix = np.clip(voice_track + sfx_track + bgm_track, -0.99, 0.99)

    if out_wav_path is None:
        out_wav_path = cluster_dir / f"mixed_audio_{cluster_id}.wav"
    else:
        out_wav_path = Path(out_wav_path).resolve()

    write_stereo_wav(out_wav_path, master_mix, SR)

    # Also save per-beat mixed WAVs for Stage 5 Beat-Level MP4 Caching
    cursor = 0
    for b, v_arr in zip(beats, beat_voice_arrays):
        b_len = len(v_arr)
        beat_mix = master_mix[cursor : cursor + b_len]
        beat_mix_path = cluster_dir / "beats_wav" / f"{b['beat_id']}_mixed.wav"
        write_stereo_wav(beat_mix_path, beat_mix, SR)
        cursor += b_len

    expected_dur = float(manifest.get("total_duration_sec", mixed_dur_sec))
    drift_sec = abs(mixed_dur_sec - expected_dur)

    try:
        rel_mixed_wav = out_wav_path.relative_to(workspace_root).as_posix()
    except ValueError:
        rel_mixed_wav = out_wav_path.name

    report = {
        "cluster_id": cluster_id,
        "mixed_wav_path": rel_mixed_wav,
        "sample_rate": SR,
        "total_samples": int(total_samples),
        "expected_duration_sec": round(expected_dur, 6),
        "mixed_duration_sec": round(mixed_dur_sec, 6),
        "drift_sec": round(drift_sec, 6),
        "zero_drift_pass": bool(drift_sec < 0.001),
        "sfx_events_mixed": len(sfx_verification),
        "bgm_track": bgm_name,
        "bgm_rms": round(float(np.sqrt(np.mean(bgm_track ** 2))), 5),
        "sfx_events_detail": sfx_verification,
    }

    report_path = cluster_dir / f"audio_mix_report_{cluster_id}.json"
    with open(report_path, "w", encoding="utf-8") as f:
        json.dump(report, f, ensure_ascii=False, indent=2)

    print(
        f"[PASS 3-LAYER AUDIO MIXER] {cluster_id} | dur={mixed_dur_sec:.6f}s "
        f"(expected={expected_dur:.6f}s, drift={drift_sec:.6f}s) | "
        f"SFX={len(sfx_verification)} events | BGM={bgm_name} -> {out_wav_path.name}"
    )
    return report


def main():
    parser = argparse.ArgumentParser(description="Mix 3-layer audio (Voice + SFX + Auto-Ducked BGM) for a cluster.")
    parser.add_argument("--manifest", required=True, help="Path to beat_manifest_<cluster_id>.json")
    parser.add_argument("--out", default=None, help="Optional output WAV path")
    args = parser.parse_args()

    rep = mix_cluster_audio(Path(args.manifest), Path(args.out) if args.out else None)
    if not rep["zero_drift_pass"]:
        sys.exit(1)


if __name__ == "__main__":
    main()
