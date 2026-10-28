# Ziro-History-Studio-v3 — Workspace Operating Law

When working inside `Ziro-History-Studio-v3`, ALWAYS read and follow [`.agent/skills/ziro-history-studio-v3/SKILL.md`](.agent/skills/ziro-history-studio-v3/SKILL.md).

## Non-Negotiable Production Rules
1. **Self-Contained Fortress:** Zero imports or path references outside `Ziro-History-Studio-v3/`.
2. **Authentic Ziro Visual DNA:**
   - **Brand Host:** Crimson-Hoodie Historian (`shared/ziro_kit/brand_host.js`, `#D93829`) on `#CCCCCC` matte stage with automatic `30fps` audio lip-sync (`mouth`).
   - **Zero Subtitles / Zero Top HUD:** Bottom karaoke subtitle bars and top news banners are strictly BANNED. Use `1–4 word` `drawTypewriter` callouts, `drawOdometerCounter`, `drawIconGrid`, and `drawChecklist` (`shared/ziro_kit/kinetic_type.js`).
   - **Two-Actor Sitcom Skits:** Full-screen 2D illustrated stage + Turn-Taking Lip-Sync (only active speaker moves mouth) + Overhead Speech Captions dimmed to `38%` (`opacity = 0.38`) when the other character replies (`shared/ziro_kit/skit_rig.js`).
   - **Micro-Beat Pacing:** Every `1.5s–2.2s` must introduce a visual pop, counter roll, pointer shift, state toggle, or stamp slam.
3. **Strict `.cache/` Isolation:** Sliced `.wav` files, `mixed_*.wav`, and raw `peak_*.png` frames belong exclusively in `.cache/<EP_ID>/<CLUSTER_ID>/`.
4. **Zero-Token Human Archiving:** AI produces per-cluster MP4s (`4_output/clusters/`). Human runs `GOP_VIDEO_VA_DON_RAC.bat` to concat `Master.mp4`, wipe `.cache`, and move finished episodes to external storage.
