#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ziro-History-Studio-v3 — Wikimedia Commons Multi-Candidate Archival Photo Fetcher
Upgrades:
  1. --list: Lists top 8 historical photo candidates with exact title, resolution & snippet
             so AI never downloads the wrong photo blindly.
  2. --pick N: Picks exact candidate #N (1-based) from the search results.
  3. --cluster c01: Automatically prefixes filenames (e.g. c01_incheon_1950.jpg) so 60-80 photos
                    in a 30-minute episode stay chronologically ordered with zero collisions!

Usage:
  python engine/fetch_wikimedia.py --query "Korean War Incheon 1950" --list
  python engine/fetch_wikimedia.py --episode EP02_Korea --cluster c01 --query "Korean War Incheon 1950" --pick 1 --out incheon_1950.jpg
"""
import argparse
import json
import re
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

STUDIO_ROOT = Path(__file__).resolve().parent.parent
UA = "ZiroHistoryStudioV3/2.0 (https://commons.wikimedia.org; Educational Historical Documentary Tool)"


def _open_with_retry(url: str, timeout: int = 25, retries: int = 3) -> bytes:
    last_err = None
    for attempt in range(retries):
        try:
            req = urllib.request.Request(url, headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=timeout) as resp:
                return resp.read()
        except urllib.error.HTTPError as e:
            last_err = e
            if e.code in (429, 500, 502, 503, 504) and attempt + 1 < retries:
                time.sleep(1.5 * (attempt + 1))
                continue
            raise
        except Exception as e:
            last_err = e
            if attempt + 1 < retries:
                time.sleep(1.2 * (attempt + 1))
                continue
            raise
    raise last_err


def fetch_json(url: str) -> dict:
    return json.loads(_open_with_retry(url, timeout=20).decode("utf-8"))


def download_file(url: str, dest: Path):
    dest.parent.mkdir(parents=True, exist_ok=True)
    dest.write_bytes(_open_with_retry(url, timeout=35))


def clean_html(raw: str) -> str:
    text = re.sub(r"<[^>]+>", " ", raw or "")
    return re.sub(r"\s+", " ", text).strip()


def search_candidates(query: str, width: int, limit: int = 8) -> list:
    params = urllib.parse.urlencode({
        "action": "query",
        "format": "json",
        "generator": "search",
        "gsrnamespace": "6",
        "gsrsearch": f"{query} filetype:bitmap",
        "gsrlimit": str(limit),
        "prop": "imageinfo",
        "iiprop": "url|size|mime|extmetadata",
        "iiurlwidth": str(width),
    })
    api_url = f"https://commons.wikimedia.org/w/api.php?{params}"
    data = fetch_json(api_url)
    pages = sorted(
        data.get("query", {}).get("pages", {}).values(),
        key=lambda p: p.get("index", 999),
    )
    results = []
    for p in pages:
        info = (p.get("imageinfo") or [{}])[0]
        mime = info.get("mime", "")
        if "jpeg" not in mime and "png" not in mime:
            continue
        url = info.get("thumburl") or info.get("url")
        if not url:
            continue
        meta = info.get("extmetadata") or {}
        desc = clean_html((meta.get("ImageDescription") or {}).get("value", ""))[:140]
        date_str = clean_html((meta.get("DateTimeOriginal") or {}).get("value", ""))[:40]
        results.append({
            "title": p.get("title", ""),
            "url": url,
            "w": info.get("width", 0),
            "h": info.get("height", 0),
            "date": date_str,
            "desc": desc,
        })
    return results


def normalize_cluster_prefix(cluster_arg: str, out_name: str) -> str:
    if not cluster_arg or "/" in out_name or "\\" in out_name:
        return out_name
    m = re.search(r"(\d+)", cluster_arg)
    prefix = f"c{int(m.group(1)):02d}_" if m else f"{cluster_arg.strip('_')}_"
    if out_name.lower().startswith(prefix.lower()):
        return out_name
    return prefix + out_name


def main():
    parser = argparse.ArgumentParser(description="Search & download authentic historical photos from Wikimedia Commons")
    parser.add_argument("--episode", default="", help="Episode ID (or 'shared' to save into shared/maps/)")
    parser.add_argument("--cluster", default="", help="Optional cluster ID/code (e.g. c01 or cum_01) to auto-prefix photo name")
    parser.add_argument("--query", required=True, help="Search query on Wikimedia Commons")
    parser.add_argument("--out", default="", help="Output filename (e.g. incheon_1950.jpg)")
    parser.add_argument("--pick", type=int, default=1, help="1-based candidate index from --list results (default: 1)")
    parser.add_argument("--list", action="store_true", help="List top 8 candidates with metadata without downloading")
    parser.add_argument("--width", type=int, default=1400, help="Preferred thumbnail width")
    args = parser.parse_args()

    candidates = search_candidates(args.query, args.width, limit=8)
    if not candidates:
        print(f"[WARN] No Wikimedia bitmap results for query: {args.query}")
        sys.exit(1)

    if args.list:
        print(f"=== WIKIMEDIA CANDIDATES FOR: '{args.query}' ===")
        for idx, c in enumerate(candidates, 1):
            dt = f" | Date: {c['date']}" if c["date"] else ""
            ds = f" | {c['desc']}" if c["desc"] else ""
            print(f"  [{idx}] {c['title']} ({c['w']}x{c['h']}{dt}){ds}")
        return

    if not args.episode or not args.out:
        print("[FAIL] --episode and --out are required when downloading (or pass --list to preview candidates).")
        sys.exit(1)

    pick_idx = max(1, min(len(candidates), args.pick)) - 1
    chosen = candidates[pick_idx]

    if args.episode == "shared":
        dest = STUDIO_ROOT / "shared" / "maps" / args.out
    else:
        final_name = normalize_cluster_prefix(args.cluster, args.out)
        dest = STUDIO_ROOT / "episodes" / args.episode / "2_assets" / "photos" / final_name

    download_file(chosen["url"], dest)
    kb = dest.stat().st_size / 1024.0
    print(f"[WIKIMEDIA PASS] #{pick_idx + 1} '{chosen['title']}' -> {dest} ({kb:.1f} KB)")


if __name__ == "__main__":
    main()
