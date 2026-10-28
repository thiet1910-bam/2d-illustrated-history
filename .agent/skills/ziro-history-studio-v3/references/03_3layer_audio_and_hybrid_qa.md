# 3-Layer Broadcast Audio Mixing & Hybrid Visual/Multimodal QA

## 1. The 3-Layer Broadcast Audio Architecture (`engine/mix_audio.py`)
Every cluster mixes 3 distinct `48000 Hz` Stereo layers before rendering:
1. **Layer 1 — Voiceover (`-2.5 dBFS` peak-normalized):** Crisp, centered narration from `.cache/<EP_ID>/<CLUSTER_ID>/voice_<CLUSTER_ID>.wav`.
2. **Layer 2 — Auto-Ducked BGM (`shared/bgm/`):**
   - `bgm_tense_history.wav`: Geopolitical tension, mystery, ancient empires (`HOI_PHAN_TICH`).
   - `bgm_satire_skit.wav`: Light ironic rhythm for comedic dialogues (`SKIT_CHAM_BIEM`).
   - Automatically crossfade-looped (`1.5s` overlap) and sidechain-ducked via smooth speech envelope (`-20.5 dB` while narrator speaks, rising gently to `-13.5 dB` during dramatic pauses).
3. **Layer 3 — Frame-Accurate Stereo SFX (`shared/sfx/`):**
   - Target density: **3–5 purposeful SFX cues per 10 seconds** (`~35–50 cues` per 100s cluster), panned subtly left/right (`pan` from `-0.45` to `+0.45`) to match where visual objects appear on the `1920x1080` canvas!
   - Protected by a `-1.2 dBFS` soft hyperbolic-tangent limiter (`np.tanh`) so heavy slams never clip or drown out Vietnamese narration.

### Verified Shared SFX Catalog (`shared/sfx/` — 100% Genuine 48kHz PCM WAV)
| Filename | Category / Sound Character | Recommended `gain_db` | Typical Visual Trigger |
| :--- | :--- | :---: | :--- |
| `whoosh_smooth.wav` | Butter-smooth air transition | `-10.5` to `-9.5` | Warm scene wipe, Polaroid swoop, carpet unfurl |
| `whoosh_low.wav` | Deep cinematic sub-whoosh | `-9.5` to `-8.5` | Dark era transition, giant map reveal, heavy slab descent |
| `whoosh_fast.wav` | Crisp fast whip-pan | `-10.5` to `-9.5` | Fast cut, kinetic card slide |
| `whoosh_transition.wav` | Classic documentary transition | `-10.0` | Act/segment header transition |
| `camera_shutter.wav` | Mechanical SLR photo snap | `-9.5` | Archival Polaroid #1 slamming onto detective board |
| `shutter_clean.wav` | Clean modern shutter click | `-10.0` | Secondary archival Polaroid pop |
| `card_pop.wav` | Tactile paper card pop | `-11.5` to `-9.5` | Triptych panels (1, 2, 3), UI cards |
| `pop_clean.wav` | Crisp single UI bubble pop | `-12.0` to `-11.0` | Stat badge, speech bubble, shop/cafe pop-up |
| `pop_multi.wav` | Cascade of playful pops | `-11.0` to `-9.5` | Multiple floating icons, orbiting `?` badges |
| `click_cinematic.wav` | Precision lock click | `-12.5` to `-10.5` | Radar pin lock on capital city, VS badge lock |
| `typewriter_tick.wav` | Crisp mechanical counter tick | `-11.5` | Year counter flipping (`1970 -> 1980`), date roll |
| `data_tick.wav` | Digital telemetry tick | `-12.0` | Percentage counter (`0% -> 70%`), HUD readout |
| `gear_mech.wav` | Heavy clockwork/loom gear | `-13.5` to `-12.0` | Marching cadence, weaver's loom, industrial machinery |
| `riser_smooth.wav` | Suspenseful tonal build-up | `-12.5` to `-11.0` | Rising 5-story wall, pre-climax tension before spikes/bars |
| `stamp_slam.wav` | Heavy ink stamp / boot thud | `-9.5` to `-7.5` | Rubber stamp (`drawRubberStamp`), bandit boot stomps |
| `jail_clang.wav` | Iron prison door / bars slam | `-8.0` to `-7.0` | Iron bars slamming down, Persepolis iron doors locking |
| `sword_clash.wav` | Metallic blade / thorn slash | `-10.5` to `-9.0` | Red X strike, converging empire war arrows, poison spikes |
| `coin_drop.wav` | Metallic gold/wealth chime | `-11.5` | Oil wealth reveal, treasury, economic trade |

---

## 2. Two-Stage Hybrid QA Protocol
### Stage A — Pre-Render `Peak-Zoom QA Contact Sheet` (8 Seconds)
Run `python engine/build_qa_sheet.py --episode <EP_ID> --cluster <CLUSTER_ID> --capture`.
- Inspect `episodes/<EP_ID>/4_output/qa/verify_peak_zoom_<CLUSTER_ID>.png` via `read_file`.
- **Fail Criteria (Must fix before MP4 render):**
  1. Any Vietnamese word touching or overflowing a card/pill border.
  2. Two consecutive beats sharing the exact same background color and layout.
  3. Dark foreground silhouettes placed against an equally dark background without rim contrast.
  4. Any bottom karaoke subtitle bar or top persistent HUD banner appearing anywhere on canvas (100% BANNED — use concise 1–4 word `drawTypewriter` callouts or Skit `38%` dimmed overhead dialogue).

### Stage B — Post-Render Stream & Multimodal Audit
1. Run `python engine/build_qa_sheet.py --episode <EP_ID> --cluster <CLUSTER_ID>` (without `--capture`) to verify `ffprobe` stream duration drift (`<= 80ms`, target `0.0ms` between `libx264` and `aac`).
2. Only call `read_file` directly on the rendered `.mp4` when file size is `< 20 MB` (e.g., Skit clusters). For longer `90s–240s` clusters (`>= 20 MB`), rely on the `Peak-Zoom QA` contact sheet + `ffprobe` sync audit (or render a short `480p` `.cache/` snippet if motion check is needed) to prevent multimodal payload overflows.
