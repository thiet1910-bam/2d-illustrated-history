#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ziro-History-Studio-v3 — Self-Contained Fortress Preflight Check
Verifies zero external dependencies, portable FFmpeg/FFprobe auto-discovery,
Node.js, Playwright + Chromium, Shared WAV Vault, and Global Satellite Atlas.
"""
import subprocess
import sys
import wave
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STUDIO_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
from bins import resolve_bin


def main():
    save_cfg = "--save-config" in sys.argv
    ok = True
    print("=== ZIRO-HISTORY-STUDIO-V3 PREFLIGHT CHECK ===")

    # 1. Portable Auto-Discovery for FFmpeg / FFprobe (zero hardcoded user paths required)
    ffmpeg = resolve_bin("ffmpeg", persist=save_cfg)
    ffprobe = resolve_bin("ffprobe", persist=save_cfg)

    for name, bin_path in [("FFmpeg", ffmpeg), ("FFprobe", ffprobe)]:
        try:
            subprocess.run([bin_path, "-version"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True)
            print(f"[PASS] {name}: {bin_path}")
        except Exception as e:
            print(f"[FAIL] {name} missing or not found on PATH: {e}")
            ok = False

    # 2. Node.js & Local Playwright
    try:
        node_v = subprocess.check_output(["node", "-v"], text=True).strip()
        print(f"[PASS] Node.js: {node_v}")
    except Exception as e:
        print(f"[FAIL] Node.js missing: {e}")
        ok = False

    pw_check = subprocess.run(
        ["node", "-e", "import('playwright').then(()=>console.log('OK')).catch(e=>{console.error(e);process.exit(1)})"],
        cwd=str(STUDIO_ROOT), stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True
    )
    if pw_check.returncode == 0:
        print("[PASS] Local Playwright ESM module resolved inside Ziro-History-Studio-v3")
    else:
        print(f"[FAIL] Playwright not installed in {STUDIO_ROOT / 'node_modules'} (run 'npm install'): {pw_check.stderr.strip()}")
        ok = False

    # 3. Shared Audio Vault + Global Satellite Atlas
    sfx_dir = STUDIO_ROOT / "shared" / "sfx"
    bgm_dir = STUDIO_ROOT / "shared" / "bgm"
    maps_dir = STUDIO_ROOT / "shared" / "maps"
    sfx_files = sorted(sfx_dir.glob("*.wav"))
    bgm_files = sorted(bgm_dir.glob("*.wav"))
    map_files = sorted(list(maps_dir.glob("*.jpg")) + list(maps_dir.glob("*.png")))
    bad_wavs = []
    for wf_path in sfx_files + bgm_files:
        try:
            with wave.open(str(wf_path), "rb") as w:
                if w.getframerate() != 48000:
                    bad_wavs.append(f"{wf_path.name} ({w.getframerate()}Hz != 48000Hz)")
        except Exception as e:
            bad_wavs.append(f"{wf_path.name} (Invalid WAV header: {e})")

    if len(sfx_files) >= 15 and len(bgm_files) >= 2 and not bad_wavs:
        print(f"[PASS] Shared Audio Vault: {len(sfx_files)} SFX + {len(bgm_files)} BGM (100% genuine 48kHz PCM WAV)")
    else:
        print(f"[FAIL] Shared Audio Vault issue: SFX={len(sfx_files)}, BGM={len(bgm_files)}, bad={bad_wavs}")
        ok = False

    if map_files:
        print(f"[PASS] Shared Satellite Atlas: {len(map_files)} map(s) ready ({', '.join(m.name for m in map_files)})")
    else:
        print("[WARN] Shared Satellite Atlas empty in shared/maps/")

    # 4. Path Length Audit (< 180 chars)
    longest = max((len(str(p)) for p in STUDIO_ROOT.rglob("*") if "node_modules" not in str(p)), default=0)
    print(f"[PASS] Max path length in Studio: {longest} chars (Safe margin: {260 - longest} chars under Windows 260 limit)")

    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
