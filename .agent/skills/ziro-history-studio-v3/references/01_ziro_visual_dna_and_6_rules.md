# Authentic Ziro History Visual DNA & 6 Script-to-Visual Laws

Every scene in `Ziro-History-Studio-v3` MUST replicate the exact visual pacing, humor, and cutout puppet mechanics of the Ziro History format across **any country, historical era, geopolitical conflict, or economic topic**:

---

## 1. Episode Shot Mix (35-Minute Structural Ratio)
- **~40% — `#CCCCCC` Matte Stage + Crimson-Hoodie Brand Host (`drawBrandHost`):**
  - Host stands left (`x = 270..330`, `y = 680`) or right (`x = 1600`, `flip = -1`), lip-syncing at `30fps` (`mouth = 0..3`), pointing with a telescopic stick at archival Polaroids, `[✓]` checklists, odometer counters, or cause-effect `[Left -> Arrow -> Right]` diagrams.
  - On shocking twists, trigger `pose: 'drop_pointer'` (dropping the pointer stick to the floor!) or `sweat: true` / `question: true` / `idea: true`.
- **~25% — Real Global Satellite Relief Map + Spotlight Vignette + Clip-Mask (`drawWorldRegionStage` & `drawGeoTerritory`):**
  - Never draw flat colored polygons on blank dark backgrounds alone. Load `/shared/maps/world_satellite.jpg` (or a regional satellite tile), zoom to any `(centerLat, centerLon, spanLon)` on Earth, darken surrounding areas via radial spotlight, sweep territory color fills via `ctx.clip()`, draw dividing lines (`drawLatitudeLine`), and fire bold outlined `drawEmpireArrow` vectors.
- **~25% — Detailed 2D Environments & Two-Actor Sitcom Skits (`drawSkitActor` & `drawOverheadCaptions`):**
  - Full-bleed illustrated 2D stages (`1920x1080` from `image-generator` or multi-layer vector sets).
  - **Turn-Taking Lip-Sync:** ONLY the active speaker receives `mouth` (`0..3`); the listener MUST receive `mouth: 0`!
  - **Overhead Speech Captions (`38%` Dim Law):** Active line types above speaker's head at `opacity = 1.0`; when the partner replies, the previous line dims to `opacity = 0.38`.
  - **Multi-Era Costumes:** Choose from built-in archetypes (`president_suit`, `diplomat`, `general_military`, `soldier_helmet`, `supreme_leader`, `scientist_coat`, `king_ancient`, `warrior_ancient`, `citizen_modern`) or craft custom character outfits paired with `drawActorMouth()`.
- **~10% — Master Multi-Act Parchment Scroll (`drawMasterScroll`) & 50/50 Split-Screen Light-Off Transitions.**

---

## 2. Strict Typography & Micro-Beat Laws
1. **BANNED 100%:** Bottom karaoke subtitle bars (`drawSubtitle`) and top broadcast news banners (`drawHudBanner`).
2. **REQUIRED 100%:** Short `1–4 word` director callouts (`drawTypewriter`) placed directly beside the prop or above the actor, timed to exact `words` timestamps in `timeline_<cluster>.json`.
3. **1.5s–2.2s Micro-Beat Decomposition:**
   - Never leave a 10-second sentence on a static composition. Break every sentence into sequential reveals:
     - `bt = 0.0s`: Host enters / shifts pose + background sets.
     - `bt = 1.8s`: Archival photo (`cXX_*.jpg`) or prop #1 pops in + `Typewriter` callout.
     - `bt = 3.6s`: Odometer counter spins (`drawOdometerCounter`) or `drawIconGrid` fires 20–100 icons.
     - `bt = 5.5s`: In-place **State Toggle** (lights snap off, eyes blink/shut, chains lock, prison bars slam) or `drawRubberStamp` slams with camera shake!
