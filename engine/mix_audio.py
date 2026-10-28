#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ziro-History-Studio-v3 — 3-Layer Broadcast Audio Mixer (48kHz Stereo PCM WAV)
Combines:
  Layer 1: Voiceover (.cache/<ep>/<cluster>/voice_<cluster>.wav, peak-normalized to -2.5 dBFS)
  Layer 2: Shared BGM (shared/bgm/<track>.wav, crossfade-looped + smooth voice-envelope ducking)
  Layer 3: Frame-Accurate Stereo SFX Cues (episodes/<ep>/3_scenes/cues_<cluster>.json + shared/sfx/*.wav)
Outputs:
  .cache/<ep>/<cluster>/mixed_<cluster>.wav (-1.2 dBFS soft-limited 48kHz Stereo PCM)
"""
import argparse
import json
import subprocess
import sys
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


def get_ffmpeg() -> str:
    return resolve_ffmpeg()


def decode_audio(path: Path) -> np.ndarray:
    if not path.exists():
        raise FileNotFoundError(f"Missing audio file: {path}")
    cmd = [
        get_ffmpeg(), "-hide_banner", "-loglevel", "error",
        "-i", str(path),
        "-f", "f32le", "-ac", "2", "-ar", str(SR), "pipe:1",
    ]
    raw = subprocess.check_output(cmd)
    return np.frombuffer(raw, dtype=np.float32).reshape(-1, 2).copy()


def db_to_lin(db: float) -> float:
    return float(10.0 ** (db / 20.0))


def ensure_voice_wav(episode: str, cluster: str) -> Path:
    cache_dir = STUDIO_ROOT / ".cache" / episode / cluster
    voice_wav = cache_dir / f"voice_{cluster}.wav"
    if voice_wav.exists():
        return voice_wav

    # Auto-regenerate voice_<cluster>.wav from 1_input/voice.MP3 using timeline_<cluster>.json!
    tl_path = STUDIO_ROOT / "episodes" / episode / "2_assets" / "timelines" / f"timeline_{cluster}.json"
    in_dir = STUDIO_ROOT / "episodes" / episode / "1_input"
    mp3_path = in_dir / "voice.MP3" if (in_dir / "voice.MP3").exists() else (in_dir / "voice.mp3")
    if not tl_path.exists() or not mp3_path.exists():
        raise FileNotFoundError(f"Missing {voice_wav} and cannot auto-extract without {tl_path} + {mp3_path}")

    tl = json.loads(tl_path.read_text(encoding="utf-8"))
    t0 = float(tl["beats"][0]["source_mp3_t0"])
    dur = float(tl["total_duration_sec"])
    cache_dir.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            get_ffmpeg(), "-hide_banner", "-loglevel", "error", "-y",
            "-ss", f"{t0:.6f}", "-t", f"{dur:.6f}",
            "-i", str(mp3_path),
            "-ar", str(SR), "-ac", "2", "-c:a", "pcm_s16le", str(voice_wav),
        ],
        check=True,
    )
    return voice_wav


def main():
    parser = argparse.ArgumentParser(description="Ziro-History-Studio-v3 3-Layer Audio Mixer")
    parser.add_argument("--episode", required=True, help="Episode ID (e.g. EP01_Demo)")
    parser.add_argument("--cluster", required=True, help="Cluster ID (e.g. cum_01_Hoi_I)")
    args = parser.parse_args()

    voice_wav = ensure_voice_wav(args.episode, args.cluster)
    voice = decode_audio(voice_wav)
    total_samples = voice.shape[0]
    dur_sec = total_samples / float(SR)

    # Layer 1: Peak-normalize narration cleanly to -2.5 dBFS
    v_peak = float(np.max(np.abs(voice))) + 1e-9
    voice = voice * (db_to_lin(-2.5) / v_peak)

    # Smooth speech envelope for dynamic BGM ducking
    mono_env = np.mean(np.abs(voice), axis=1)
    win1 = int(SR * 0.18)
    smooth_env = np.convolve(mono_env, np.ones(win1, dtype=np.float32) / win1, mode="same")
    speaking = np.clip(smooth_env / 0.035, 0.0, 1.0)
    win2 = int(SR * 0.35)
    speaking = np.convolve(speaking, np.ones(win2, dtype=np.float32) / win2, mode="same")

    cues_path = STUDIO_ROOT / "episodes" / args.episode / "3_scenes" / f"cues_{args.cluster}.json"
    cues_cfg = json.loads(cues_path.read_text(encoding="utf-8")) if cues_path.exists() else {}

    # Layer 2: BGM with crossfade looping & voice ducking
    bgm_name = cues_cfg.get("bgm", "bgm_tense_history.wav")
    bgm_speak_db = float(cues_cfg.get("bgm_duck_db", -20.5))
    bgm_pause_db = float(cues_cfg.get("bgm_pause_db", -13.5))
    bgm_path = STUDIO_ROOT / "shared" / "bgm" / bgm_name

    mix = voice.copy()
    if bgm_path.exists():
        bgm_raw = decode_audio(bgm_path)
        bgm_raw = bgm_raw / (float(np.max(np.abs(bgm_raw))) + 1e-9)

        bgm = np.zeros_like(voice)
        pos = 0
        xfade = int(SR * 1.5)
        chunk_len = bgm_raw.shape[0]
        while pos < total_samples:
            take = min(chunk_len, total_samples - pos)
            seg = bgm_raw[:take].copy()
            if pos > 0 and take > xfade:
                fade_in = np.linspace(0.0, 1.0, xfade, dtype=np.float32)[:, None]
                bgm[pos : pos + xfade] = bgm[pos : pos + xfade] * (1.0 - fade_in) + seg[:xfade] * fade_in
                bgm[pos + xfade : pos + take] = seg[xfade:]
            else:
                bgm[pos : pos + take] = seg
            pos += max(1, chunk_len - xfade)

        duck_gain = db_to_lin(bgm_pause_db) * (1.0 - speaking) + db_to_lin(bgm_speak_db) * speaking
        fi = min(int(SR * 0.8), total_samples)
        fo = min(int(SR * 1.5), total_samples)
        duck_gain[:fi] *= np.linspace(0.2, 1.0, fi)
        duck_gain[-fo:] *= np.linspace(1.0, 0.0, fo)
        mix = mix + bgm * duck_gain[:, None]

    # Layer 3: Frame-Accurate Stereo SFX Cues from shared/sfx/
    sfx_dir = STUDIO_ROOT / "shared" / "sfx"
    sfx_cache = {}

    def get_sfx(sfx_file: str) -> np.ndarray:
        fname = sfx_file if sfx_file.lower().endswith(".wav") else f"{sfx_file}.wav"
        if fname not in sfx_cache:
            p = sfx_dir / fname
            if not p.exists():
                p = sfx_dir / "card_pop.wav"
            arr = decode_audio(p)
            sfx_cache[fname] = arr / (float(np.max(np.abs(arr))) + 1e-9)
        return sfx_cache[fname]

    raw_cues = cues_cfg.get("cues", [])
    placed_count = 0
    for item in raw_cues:
        if isinstance(item, dict):
            t_sec = float(item["t"])
            sfx_name = item["sfx"]
            gain_db = float(item.get("gain_db", -10.0))
            max_dur = float(item.get("max_dur", 2.5))
            pan = float(item.get("pan", 0.0))
        else:
            t_sec, sfx_name, gain_db, max_dur, pan = float(item[0]), str(item[1]), float(item[2]), float(item[3]), float(item[4])

        arr = get_sfx(sfx_name)
        max_len = int(SR * max_dur)
        if arr.shape[0] > max_len:
            arr = arr[:max_len].copy()
            fo_len = min(int(SR * 0.15), arr.shape[0] // 3)
            if fo_len > 0:
                arr[-fo_len:] *= np.linspace(1.0, 0.0, fo_len, dtype=np.float32)[:, None]

        idx = int(t_sec * SR)
        if idx < 0 or idx >= total_samples:
            continue
        end = min(total_samples, idx + arr.shape[0])
        seg = arr[: end - idx] * db_to_lin(gain_db)
        pan_clamped = max(-1.0, min(1.0, pan))
        l_gain = np.sqrt(0.5 * (1.0 - pan_clamped)) * np.sqrt(2.0)
        r_gain = np.sqrt(0.5 * (1.0 + pan_clamped)) * np.sqrt(2.0)
        mix[idx:end, 0] += seg[:, 0] * l_gain
        mix[idx:end, 1] += seg[:, 1] * r_gain
        placed_count += 1

    # Soft Limiter at -1.2 dBFS
    limit = db_to_lin(-1.2)
    peak = float(np.max(np.abs(mix)))
    if peak > limit:
        mix = np.tanh(mix / limit) * limit

    # Slight 60ms tail pad so AAC encoder never clips the final syllable
    pad = np.zeros((int(0.06 * SR), 2), dtype=np.float32)
    mix = np.vstack([mix, pad])

    out_wav = STUDIO_ROOT / ".cache" / args.episode / args.cluster / f"mixed_{args.cluster}.wav"
    out_wav.parent.mkdir(parents=True, exist_ok=True)
    pcm16 = np.clip(mix * 32767.0, -32768, 32767).astype(np.int16)
    with wave.open(str(out_wav), "wb") as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(SR)
        wf.writeframes(pcm16.tobytes())

    rms_db = 20.0 * np.log10(float(np.sqrt(np.mean(mix ** 2))) + 1e-9)
    pk_db = 20.0 * np.log10(float(np.max(np.abs(mix))) + 1e-9)
    print(
        f"[AUDIO MIX PASS] {out_wav} | dur={dur_sec:.2f}s | SFX={placed_count} cues | "
        f"RMS={rms_db:.1f} dBFS | Peak={pk_db:.2f} dBFS"
    )


if __name__ == "__main__":
    main()
