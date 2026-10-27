#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Task 5.1: Cluster & Master Video Orchestrator with 1.5s Beat Cache (`build_cluster_and_master.py`)
--------------------------------------------------------------------------------------------------
Features:
  1. Ensures 3-layer mixed audio (`mixed_audio_<cluster_id>.wav` & per-beat `beat_XX_mixed.wav`) is ready.
  2. Computes an 8-char MD5 hash (`beat_hash`) for each beat in `beat_manifest_<cluster_id>.json`.
  3. Checks `cache_beats/beat_XX_<hash>.mp4`:
     - If present -> `[CACHE HIT — 0.00s]` (instant skip).
     - If modified/missing -> `[CACHE MISS]` renders 30fps 2-Pass frames with real-time Audio RMS Lip-Sync
       and encodes `beat_XX_<hash>.mp4`.
  4. Concatenates all cached beat MP4s via `ffmpeg -f concat -c:v copy` and locks the master 3-layer audio
     into `3_output/<episode_id>/1_video_cac_cum/<cluster_id>.mp4`.
  5. Supports `--concat <episode_id>` to stitch all completed clusters into the full episode master MP4.
"""

import os
import sys
import json
import time
import wave
import shutil
import hashlib
import argparse
import subprocess
from pathlib import Path
import numpy as np

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
if hasattr(sys.stderr, "reconfigure"):
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

ENGINE_DIR = Path(__file__).resolve().parent
if str(ENGINE_DIR) not in sys.path:
    sys.path.insert(0, str(ENGINE_DIR))

import re
from ziro_stage_components import W, H, ensure_brand_ui_assets
from camera_2pass_renderer import render_frame_2pass
from audio_3layer_mixer import mix_cluster_audio, read_wav_stereo_float, SR

try:
    import imageio_ffmpeg
    FFMPEG_EXE = imageio_ffmpeg.get_ffmpeg_exe()
except ImportError:
    FFMPEG_EXE = "ffmpeg"

FPS = 30
ENGINE_CACHE_SALT = "ziro_2pass_v5_skit_authentic"


def compute_beat_hash(beat_data: dict) -> str:
    """Computes deterministic 8-char MD5 hash for a single beat configuration."""
    canonical = json.dumps(beat_data, sort_keys=True, ensure_ascii=False) + "|" + ENGINE_CACHE_SALT
    return hashlib.md5(canonical.encode("utf-8")).hexdigest()[:8]


def extract_rms_mouth_states_30fps(wav_path: Path, n_frames: int) -> list:
    """
    Computes 30fps lip-sync mouth state codes (`0=closed`, `1=half`, `2=open`)
    directly from the beat's voice WAV waveform.
    """
    if not wav_path.exists():
        return [0] * n_frames
    stereo = read_wav_stereo_float(wav_path)
    mono = np.mean(stereo, axis=1)
    samples_per_frame = max(1, int(round(SR / float(FPS))))

    rms_vals = []
    for i in range(n_frames):
        s0 = i * samples_per_frame
        s1 = min(len(mono), s0 + samples_per_frame)
        if s0 >= len(mono) or s1 <= s0:
            rms_vals.append(0.0)
        else:
            chunk = mono[s0:s1]
            rms_vals.append(float(np.sqrt(np.mean(chunk * chunk))))

    peak_rms = max(rms_vals) if rms_vals else 0.0
    if peak_rms < 1e-4:
        return [0] * n_frames

    codes = []
    for idx, r in enumerate(rms_vals):
        norm_r = r / peak_rms
        if norm_r < 0.16:
            codes.append(0)
        elif norm_r < 0.46:
            codes.append(1)
        else:
            # Alternate between half (1) and open (2) on sustained vowels for natural articulation
            codes.append(2 if (idx % 3 != 0) else 1)
    return codes


def render_single_beat_mp4(
    beat_data: dict,
    voice_wav_path: Path,
    mixed_beat_wav_path: Path,
    out_mp4_path: Path,
    episode_id: str,
    workspace_root: Path,
) -> float:
    """Renders a single beat at 1920x1080 @ 30fps into `out_mp4_path` and returns elapsed seconds."""
    t_start = time.perf_counter()
    dur = max(0.1, float(beat_data.get("duration", 5.0)))
    n_frames = max(1, int(round(dur * FPS)))
    mouth_codes = extract_rms_mouth_states_30fps(voice_wav_path, n_frames)

    out_mp4_path.parent.mkdir(parents=True, exist_ok=True)
    tmp_mp4 = out_mp4_path.with_suffix(".tmp.mp4")

    audio_input = mixed_beat_wav_path if mixed_beat_wav_path.exists() else voice_wav_path
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-f",
        "rawvideo",
        "-vcodec",
        "rawvideo",
        "-s",
        f"{W}x{H}",
        "-pix_fmt",
        "rgb24",
        "-r",
        str(FPS),
        "-i",
        "-",
    ]
    if audio_input and audio_input.exists():
        cmd.extend(["-i", str(audio_input), "-c:a", "aac", "-b:a", "192k"])
    cmd.extend([
        "-c:v",
        "libx264",
        "-preset",
        "ultrafast",
        "-crf",
        "20",
        "-pix_fmt",
        "yuv420p",
        "-shortest",
        str(tmp_mp4),
    ])

    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    try:
        for f_idx in range(n_frames):
            bt = f_idx / float(FPS)
            m_code = mouth_codes[f_idx]
            frame_im = render_frame_2pass(
                beat_data,
                bt,
                m_code=m_code,
                episode_id=episode_id,
                workspace_root=workspace_root,
            )
            proc.stdin.write(frame_im.tobytes())
        proc.stdin.close()
        stderr_bytes = proc.stderr.read()
        proc.wait()
        if proc.returncode != 0:
            raise RuntimeError(f"FFmpeg beat encode failed: {stderr_bytes.decode('utf-8', errors='ignore')}")
    finally:
        if proc.stdin and not proc.stdin.closed:
            proc.stdin.close()

    if tmp_mp4.exists():
        tmp_mp4.replace(out_mp4_path)
    return time.perf_counter() - t_start


def probe_media_duration(path: Path) -> float:
    cmd = [FFMPEG_EXE, "-i", str(path)]
    res = subprocess.run(cmd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+(?:\.\d+)?)", res.stderr)
    if m:
        return int(m.group(1)) * 3600 + int(m.group(2)) * 60 + float(m.group(3))
    return 0.0


def build_cluster_video(manifest_path: Path, workspace_root: Path = None, force_rebuild: bool = False) -> dict:
    manifest_path = manifest_path.resolve()
    if not manifest_path.exists():
        # Fallback: check inside cac_cum/<cluster_id>/beat_manifest_<cluster_id>.json
        m_cid = re.sub(r"^beat_manifest_|\.json$", "", manifest_path.name)
        alt_path = manifest_path.parent / m_cid / manifest_path.name
        if alt_path.exists():
            manifest_path = alt_path.resolve()
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    episode_id = manifest.get("episode_id", "EP01_Iran")
    cluster_id = manifest.get("cluster_id", "cum_01_Hoi_I")
    beats = manifest.get("beats", [])

    cluster_dir = manifest_path.parent
    if workspace_root is None:
        workspace_root = cluster_dir
        for p in manifest_path.parents:
            if (p / "2_nguyen_lieu").exists() and (p / "3_output").exists():
                workspace_root = p
                break
    else:
        workspace_root = Path(workspace_root).resolve()

    # 1. Ensure physical Brand UI Assets exist in 0_kho_dung_chung/brand_ui_assets/
    ensure_brand_ui_assets(workspace_root)

    # 2. Ensure 3-Layer Audio Mix is up to date
    master_mixed_wav = cluster_dir / f"mixed_audio_{cluster_id}.wav"
    audio_report = mix_cluster_audio(manifest_path, master_mixed_wav)

    # 3. Render or Reuse Beat Cache (`cache_beats/beat_XX_<hash>.mp4`)
    cache_dir = cluster_dir / "cache_beats"
    cache_dir.mkdir(parents=True, exist_ok=True)

    print("=" * 76)
    print(f"🎬 BƯỚC 3: RENDER MÁY QUAY 2 LỚP & BỘ NHỚ ĐỆM NHỊP (`{cluster_id}`)")
    print("=" * 76)

    cached_mp4_paths = []
    cache_hits = 0
    cache_misses = 0
    t_cluster_start = time.perf_counter()

    for b in beats:
        bid = b["beat_id"]
        b_hash = compute_beat_hash(b)
        target_cache_mp4 = cache_dir / f"{bid}_{b_hash}.mp4"

        # Clean obsolete hashes for this beat_id
        for old_f in cache_dir.glob(f"{bid}_*.mp4"):
            if old_f.name != target_cache_mp4.name:
                try:
                    old_f.unlink()
                except OSError:
                    pass

        if not force_rebuild and target_cache_mp4.exists() and target_cache_mp4.stat().st_size > 1024:
            cache_hits += 1
            cached_mp4_paths.append(target_cache_mp4)
            print(f"  ⚡ [CACHE HIT  — 0.00s] {bid} ({b['duration']:.2f}s) | hash={b_hash} -> {target_cache_mp4.name}")
        else:
            cache_misses += 1
            voice_wav = cluster_dir / b.get("wav_file", f"beats_wav/{bid}.wav")
            mixed_b_wav = cluster_dir / "beats_wav" / f"{bid}_mixed.wav"
            elapsed = render_single_beat_mp4(
                b, voice_wav, mixed_b_wav, target_cache_mp4, episode_id, workspace_root
            )
            cached_mp4_paths.append(target_cache_mp4)
            print(f"  🔨 [CACHE MISS — {elapsed:4.2f}s] {bid} ({b['duration']:.2f}s) | hash={b_hash} -> {target_cache_mp4.name}")

    # 4. Concatenate Beat MP4s and lock Master 3-Layer Audio
    concat_txt = cache_dir / "concat_beats.txt"
    concat_lines = [f"file '{p.resolve().as_posix()}'" for p in cached_mp4_paths]
    concat_txt.write_text("\n".join(concat_lines) + "\n", encoding="utf-8")

    out_cluster_dir = workspace_root / "3_output" / episode_id / "1_video_cac_cum"
    out_cluster_dir.mkdir(parents=True, exist_ok=True)
    final_cluster_mp4 = out_cluster_dir / f"{cluster_id}.mp4"

    cmd_concat = [
        FFMPEG_EXE,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(concat_txt),
        "-i",
        str(master_mixed_wav),
        "-map",
        "0:v:0",
        "-map",
        "1:a:0",
        "-c:v",
        "copy",
        "-c:a",
        "aac",
        "-b:a",
        "192k",
        "-shortest",
        str(final_cluster_mp4),
    ]
    res = subprocess.run(cmd_concat, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"FFmpeg cluster concat failed: {res.stderr}")

    total_elapsed = time.perf_counter() - t_cluster_start

    mp4_dur = probe_media_duration(final_cluster_mp4)
    wav_dur = float(audio_report["mixed_duration_sec"])
    av_drift = abs(mp4_dur - wav_dur)

    try:
        rel_out_mp4 = final_cluster_mp4.relative_to(workspace_root).as_posix()
    except ValueError:
        rel_out_mp4 = f"3_output/{episode_id}/1_video_cac_cum/{cluster_id}.mp4"

    build_report = {
        "episode_id": episode_id,
        "cluster_id": cluster_id,
        "beats_total": len(beats),
        "cache_hits": cache_hits,
        "cache_misses": cache_misses,
        "total_elapsed_sec": round(total_elapsed, 3),
        "voice_wav_duration_sec": round(wav_dur, 4),
        "video_mp4_duration_sec": round(mp4_dur, 4),
        "av_sync_drift_sec": round(av_drift, 4),
        "output_mp4": rel_out_mp4,
    }
    (cluster_dir / f"build_report_{cluster_id}.json").write_text(
        json.dumps(build_report, ensure_ascii=False, indent=2), encoding="utf-8"
    )

    print("-" * 76)
    print(f"• Tổng số nhịp (`beats`)      : {len(beats)} nhịp (Hits: {cache_hits}, Misses: {cache_misses})")
    print(f"• Tổng thời gian xử lý        : {total_elapsed:.2f}s")
    print(f"• Thời lượng Audio / Video    : {wav_dur:.3f}s / {mp4_dur:.3f}s (Độ lệch = {av_drift:.4f}s)")
    print(f"• Video Cụm xuất bản          : {final_cluster_mp4}")
    print("✅ [PASS 100%] Hoàn tất xuất bản Video Cụm (2-Pass Camera + 3-Layer Audio + Beat Cache)!")
    print("=" * 76)
    return build_report


def concat_episode_master(episode_id: str, workspace_root: Path):
    """Concatenates all completed cluster MP4s in `3_output/<episode_id>/1_video_cac_cum/` into a Master MP4."""
    cluster_vid_dir = workspace_root / "3_output" / episode_id / "1_video_cac_cum"
    master_out_dir = workspace_root / "3_output" / episode_id / "3_video_hoan_chinh_30p"
    master_out_dir.mkdir(parents=True, exist_ok=True)

    mp4_files = sorted(cluster_vid_dir.glob("cum_*.mp4"))
    if not mp4_files:
        raise FileNotFoundError(f"Không tìm thấy video cụm nào trong {cluster_vid_dir}")

    list_file = master_out_dir / "concat_clusters.txt"
    list_file.write_text(
        "\n".join(f"file '{p.resolve().as_posix()}'" for p in mp4_files) + "\n",
        encoding="utf-8",
    )
    out_master = master_out_dir / f"{episode_id}_full_master.mp4"
    cmd = [
        FFMPEG_EXE,
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        str(list_file),
        "-c",
        "copy",
        str(out_master),
    ]
    subprocess.run(cmd, check=True)
    print(f"✅ [MASTER READY] Đã nối {len(mp4_files)} cụm thành: {out_master}")


def main():
    parser = argparse.ArgumentParser(description="Build Cluster Video with 1.5s Beat Cache or Concat Episode Master")
    parser.add_argument("manifest_or_episode", help="Path to beat_manifest_<cluster_id>.json OR episode_id when --concat is used")
    parser.add_argument("--workspace", default=None, help="Path to dung-video-lich-su-hoat-hinh-2d workspace")
    parser.add_argument("--force", action="store_true", help="Force re-render all beats ignoring cache")
    parser.add_argument("--concat", action="store_true", help="Concatenate all rendered cluster MP4s into Episode Master")
    args = parser.parse_args()

    if args.concat:
        default_ws = Path(__file__).resolve().parents[4] / "Du-an-2D-Illustrated-History" / "dung-video-lich-su-hoat-hinh-2d"
        ws = Path(args.workspace) if args.workspace else default_ws
        concat_episode_master(args.manifest_or_episode, ws)
    else:
        build_cluster_video(Path(args.manifest_or_episode), args.workspace, force_rebuild=args.force)


if __name__ == "__main__":
    main()
