#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ziro-History-Studio-v3 — Portable Cross-Machine FFmpeg / FFprobe Resolver
Ensures zero hardcoded personal machine paths are required when handing the Studio
to a new user or another computer.
"""
import json
import os
import shutil
from pathlib import Path

STUDIO_ROOT = Path(__file__).resolve().parent.parent


def _search_common_windows_dirs(exe_name: str) -> str:
    candidates = [
        STUDIO_ROOT / "engine" / "bin" / exe_name,
        Path("C:/ffmpeg/bin") / exe_name,
        Path("C:/Program Files/ffmpeg/bin") / exe_name,
    ]
    local_app = os.environ.get("LOCALAPPDATA", "")
    user_prof = os.environ.get("USERPROFILE", "")

    if local_app:
        winget_dir = Path(local_app) / "Microsoft" / "WinGet" / "Packages"
        if winget_dir.exists():
            candidates.extend(winget_dir.rglob(exe_name))
    if user_prof:
        scoop_shim = Path(user_prof) / "scoop" / "shims" / exe_name
        candidates.append(scoop_shim)
        dl_dir = Path(user_prof) / "Downloads"
        if dl_dir.exists():
            for sub in dl_dir.iterdir():
                if sub.is_dir():
                    direct = sub / exe_name
                    nested = sub / "donetool" / exe_name
                    nested_bin = sub / "bin" / exe_name
                    for p in (direct, nested, nested_bin):
                        if p.exists():
                            return str(p.resolve()).replace("\\", "/")

    for c in candidates:
        if c.exists():
            return str(c.resolve()).replace("\\", "/")

    if exe_name.lower().startswith("ffmpeg"):
        try:
            import imageio_ffmpeg
            return str(Path(imageio_ffmpeg.get_ffmpeg_exe()).resolve()).replace("\\", "/")
        except Exception:
            pass
    return ""


def resolve_bin(kind: str = "ffmpeg", persist: bool = False) -> str:
    """
    Resolves 'ffmpeg' or 'ffprobe' portably across any Windows/macOS/Linux machine:
      1. Environment variable MVD_FFMPEG / MVD_FFPROBE
      2. .mvd/config.json (ONLY if that path actually exists on THIS machine)
      3. System PATH (shutil.which)
      4. Common local/Windows folders (engine/bin, C:/ffmpeg, WinGet, Scoop, Downloads)
    """
    env_key = f"MVD_{kind.upper()}"
    if os.environ.get(env_key) and Path(os.environ[env_key]).exists():
        return os.environ[env_key]

    cfg_path = STUDIO_ROOT / ".mvd" / "config.json"
    cfg = {}
    if cfg_path.exists():
        try:
            cfg = json.loads(cfg_path.read_text(encoding="utf-8"))
        except Exception:
            cfg = {}

    configured = cfg.get(kind, "")
    if configured and Path(configured).exists():
        return configured

    on_path = shutil.which(kind)
    if on_path:
        resolved = str(Path(on_path).resolve()).replace("\\", "/")
    else:
        exe_name = f"{kind}.exe" if os.name == "nt" else kind
        resolved = _search_common_windows_dirs(exe_name) or kind

    if persist and resolved and Path(resolved).exists():
        cfg[kind] = resolved
        cfg_path.parent.mkdir(parents=True, exist_ok=True)
        cfg_path.write_text(json.dumps(cfg, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    return resolved


def resolve_ffmpeg() -> str:
    return resolve_bin("ffmpeg", persist=False)


def resolve_ffprobe() -> str:
    return resolve_bin("ffprobe", persist=False)


if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else "ffmpeg"
    print(resolve_bin(target, persist=False))

