---
name: ziro-history-studio-v3
description: >-
  Produces long-form (10–35 minute) 2D cutout history, geopolitical, and economic
  videos for ANY country or topic worldwide matching the authentic Ziro History
  storytelling DNA at 1920x1080 30fps using the Crimson-Hoodie Historian Brand
  Host (30fps audio lip-sync), Two-Actor Sitcom Skits (38% dimmed overhead
  captions + multi-era costumes), kinetic typewriter callouts (zero subtitles/HUD),
  global satellite spotlight maps, and 3-layer 48kHz broadcast audio.
---

# Ziro-History-Studio-v3 — Universal Authentic Ziro Cutout Engine

## 1. Core Ziro DNA Laws (Strictly Enforced)
1. **Channel Brand Host (`shared/ziro_kit/brand_host.js` — ~40% of Episode Runtime):**
   - Use **`drawBrandHost`** (*Giáo Sư / Nhà Sử Học Áo Hoodie Đỏ `#D93829`*) on flat matte `#CCCCCC` stage (`drawZiroGreyStage`).
   - Always pass `{ t, mouth }` provided automatically by `engine/player/main.js` so the Host's mouth articulates at `30fps` in exact sync with `voice.MP3`.
   - Switch `pose` (`'point_right'`, `'point_left'`, `'magnifier'`, `'shrug'`, `'crossed'`, `'drop_pointer'`) and `mood` (`'normal'`, `'skeptical'`, `'shocked'`, `'serious'`, `'happy'`) on keyword beats.
2. **ZERO Subtitles & ZERO Top HUD Banners (Banned 100%):**
   - NEVER call `drawSubtitle` or `drawHudBanner`. Never render karaoke bars at the bottom or news banners at the top.
   - Use **concise 1–4 word Kinetic Callouts** via `drawTypewriter`, `drawOdometerCounter`, `drawIconGrid`, `drawChecklist`, and `drawMasterScroll` from `shared/ziro_kit/kinetic_type.js` right next to visual props.
   - When calling `drawMasterScroll`, ALWAYS pass the current episode's actual `acts` list (`[{ roman: 'I', label: '...' }, ...]`).
3. **1.5s–2.2s Micro-Beat Pacing (`Zero Static Sentences`):**
   - Any sentence longer than `3.5s` MUST be decomposed into sequential micro-actions every `1.5s–2.2s` using `words` timestamps in `timeline_<cluster>.json` (e.g., `[0.0s Host points]` -> `[1.8s Photo pops]` -> `[3.6s Counter spins]` -> `[5.4s State toggles / Stamp slams]`).
4. **Two-Actor Sitcom Skit Mode (`shared/ziro_kit/skit_rig.js` for `SKIT_CHAM_BIEM`):**
   - Full-screen illustrated 2D stage (`2_assets/backgrounds/skitK_*.jpg`), NO Brand Host, NO `#CCCCCC` grey background.
   - **Turn-Taking Lip-Sync Lock:** Pass `mouth` ONLY to the currently speaking actor (`A` or `B`); pass `mouth: 0` to the listener!
   - **Overhead Speech Captions (`38%` Dim Hold):** Render natural dialogue above each speaker's head via `drawOverheadCaptions`. When Actor B replies, Actor A's overhead line stays visible at **`opacity = 0.38` (`38%`)**.
   - **Multi-Era / Multi-Country Costumes:** Use built-in archetypes in `drawSkitActor` (`'president_suit'`, `'diplomat'`, `'general_military'`, `'soldier_helmet'`, `'supreme_leader'`, `'scientist_coat'`, `'king_ancient'`, `'warrior_ancient'`, `'citizen_modern'`) or draw bespoke costumes for specific historical figures and attach `drawActorMouth(ctx, mx, my, mouth, mood)` for 1-line `30fps` lip-sync!
5. **Token-Saving Human Hand-Off (Zero AI Waste on Archiving):**
   - AI ONLY builds and renders individual clusters (`4_output/clusters/cum_XX.mp4`).
   - Do NOT spend AI tokens merging or moving episode folders to external storage. Point the user to double-click **`GOP_VIDEO_VA_DON_RAC.bat`** (and read `HUONG_DAN_VAN_HANH_30_PHUT.md`) to merge `Master.mp4` in ~3s, wipe `.cache/<EP_ID>`, and manually Cut/Paste the episode to their archive drive.

---

## 2. Rolling Per-Cluster Production Pipeline

### Step 0 — Preflight Check
```powershell
python engine/preflight.py
```

### Step 1 — Scan Episode & Slice Active Cluster (`0.000s` Lock + `30fps` Lip-Sync)
Read [`references/02_longform_clustering_and_cache.md`](references/02_longform_clustering_and_cache.md).
- Supports both **3-file input** (`voice.MP3` + `kich_ban_loi_dan.txt` + `kich_ban_chia_hoi.txt`) and **2-file minimal input** (`voice.MP3` + `kich_ban_loi_dan.txt` — if `kich_ban_chia_hoi.txt` is absent, refine or let `scan_clusters.py` bootstrap the Act/Skit structure automatically while keeping 100% verbatim lines).
```powershell
python engine/scan_clusters.py --episode <EP_ID>
python engine/scan_clusters.py --episode <EP_ID> --cluster <CLUSTER_ID>
```
Outputs `2_assets/timelines/timeline_<CLUSTER_ID>.json` containing exact beat boundaries, `words` sub-timestamps, and `mouth_30fps`.

### Step 2 — Auto-Acquire Authentic Visual Assets (Any Topic Worldwide)
- **Historical Photos (Preview Candidates First + Mandatory `cXX_` Cluster Prefix):**
  1. List candidates first so you pick the exact historical event/person:
     ```powershell
     python engine/fetch_wikimedia.py --query "<Historical Subject>" --list
     ```
  2. Download the verified `--pick N` candidate with `--cluster cXX` so 60–80 photos across a 30-minute episode stay chronologically sorted (`c01_...`, `c02_...`, `c17_...`) in `2_assets/photos/` with zero overwrite collisions:
     ```powershell
     python engine/fetch_wikimedia.py --episode <EP_ID> --cluster c01 --query "<Historical Subject>" --pick 1 --out <name>.jpg
     ```
  3. Always inspect downloaded photos with `read_file` to verify subject accuracy.
- **Skit 2D Stage Backgrounds:** Invoke subagent `image-generator` to paint clean, character-free flat 2D Ziro stage backgrounds (`1920x1080`) into `episodes/<EP_ID>/2_assets/backgrounds/skitK_<name>.jpg`.
- **Global Satellite Geopolitics (Works Offline for All 195 Countries):**
  - Load `/shared/maps/world_satellite.jpg` and call `const project = drawWorldRegionStage(ctx, W, H, imgs.worldMap, { centerLat, centerLon, spanLon })` from `shared/ziro_kit/maps.js`!
  - Highlight borders via `drawGeoTerritory(ctx, project, poly)` (using built-in `GEO_BORDERS` or custom `[lat, lon]` coordinates), draw dividing parallels via `drawLatitudeLine` (e.g., 38th Parallel), and place radar pins via `const [x, y] = project(lat, lon); drawRadarPin(ctx, x, y, label, bt)`.
  - Optionally fetch ultra-close regional satellite maps via `fetch_wikimedia.py --episode shared`.

### Step 3 — Code Scene & 3-Layer Stereo Cues
Read [`references/01_ziro_visual_dna_and_6_rules.md`](references/01_ziro_visual_dna_and_6_rules.md) and [`references/03_3layer_audio_and_hybrid_qa.md`](references/03_3layer_audio_and_hybrid_qa.md).
- Author `episodes/<EP_ID>/3_scenes/<CLUSTER_ID>.js` (starting from `templates/scene_cluster_template.js` or `templates/skit_cluster_template.js`).
- Author `episodes/<EP_ID>/3_scenes/cues_<CLUSTER_ID>.json` (using `bgm_tense_history.wav` for analysis clusters or `bgm_satire_skit.wav` for Skit clusters).

### Step 4 — 8-Second Peak-Zoom Visual QA Gate (MANDATORY Before MP4 Render)
```powershell
python engine/build_qa_sheet.py --episode <EP_ID> --cluster <CLUSTER_ID> --capture
```
Inspect `episodes/<EP_ID>/4_output/qa/verify_peak_zoom_<CLUSTER_ID>.png` via `read_file`. Verify zero text collisions, zero subtitles/HUD, expressive Host/Skit poses, and 1.8s micro-beat richness.

### Step 5 — Mix 3-Layer 48kHz Audio & Render Full HD 30fps Cluster
```powershell
python engine/mix_audio.py --episode <EP_ID> --cluster <CLUSTER_ID>
node engine/render.js --episode <EP_ID> --cluster <CLUSTER_ID>
```
Verify A/V sync (`python engine/build_qa_sheet.py --episode <EP_ID> --cluster <CLUSTER_ID>`). Only call `read_file` directly on `.mp4` if its file size is `< 20 MB` (to avoid multimodal payload limits); for larger `90s–240s` clusters (`>= 20 MB`), verify via `verify_peak_zoom_<CLUSTER_ID>.png` + `ffprobe` `0.0ms` drift check.
