// Template: Narrative / Analysis Cluster (HOI_PHAN_TICH) — Authentic Ziro Style
// ZERO bottom subtitles! ZERO top HUD banners! Works for ANY country/topic worldwide.
import {
  lerp, prog, loadImg, withCamera, drawPolaroid, drawRubberStamp
} from '../../../shared/ziro_kit/helpers.js';
import { drawBrandHost } from '../../../shared/ziro_kit/brand_host.js';
import {
  drawZiroGreyStage, drawTypewriter, drawOdometerCounter
} from '../../../shared/ziro_kit/kinetic_type.js';
import {
  GEO_BORDERS, drawWorldRegionStage, drawGeoTerritory, drawLatitudeLine, drawRadarPin
} from '../../../shared/ziro_kit/maps.js';

let imgs = {};

export async function init() {
  const [worldMap] = await Promise.all([
    loadImg('/shared/maps/world_satellite.jpg'),
  ]);
  imgs = { worldMap };
}

export function draw(ctx, t, { W, H, mouth }) {
  if (t < 8.500) drawBeat01(ctx, t, t, W, H, mouth);
  else drawBeat02(ctx, t - 8.500, t, W, H);
}

function drawBeat01(ctx, bt, t, W, H, mouth) {
  drawZiroGreyStage(ctx, W, H, '#CCCCCC');
  withCamera(ctx, W, H, { zoom: lerp(1.0, 1.05, bt / 8.5), t }, () => {
    // Crimson-Hoodie Brand Host lip-syncing automatically at 30fps
    drawBrandHost(ctx, 310, 680, 1.35, {
      t, mouth,
      pose: bt > 1.6 ? 'point_right' : 'idle',
      mood: bt > 5.0 ? 'skeptical' : 'normal',
    });

    // Micro-Beat 1 (bt=1.6s): Archival Polaroid pops in
    drawPolaroid(ctx, {
      cx: 1180, cy: 480, w: 480, h: 310,
      rot: -0.03, tag: 'TƯ LIỆU', caption: '',
      pop: prog(bt, 1.6, 0.45), mystery: true,
    });

    // Micro-Beat 2 (bt=3.2s): Short Typewriter keyword next to prop
    drawTypewriter(ctx, 'BƯỚC NGOẶT LỊCH SỬ!', 1180, 745, bt, 3.2, {
      size: 46, align: 'center', color: '#18181C', outline: '#FFFFFF',
    });

    // Micro-Beat 3 (bt=5.4s): Rubber stamp punchline
    if (bt > 5.4) {
      drawRubberStamp(ctx, 1180, 480, 'SỰ THẬT 100%', '#DC2626', -0.08, prog(bt, 5.4, 0.35));
    }
  });
}

function drawBeat02(ctx, bt, t, W, H) {
  withCamera(ctx, W, H, { zoom: lerp(1.0, 1.12, bt / 10.0), t }, () => {
    // Universal Earth Satellite Zoom (Example: Korean Peninsula @ 38.5N, 127.0E)
    const project = drawWorldRegionStage(ctx, W, H, imgs.worldMap, {
      centerLat: 38.5, centerLon: 127.0, spanLon: 26.0,
    });
    drawGeoTerritory(ctx, project, GEO_BORDERS.north_korea, {
      fill: 'rgba(220, 38, 38, 0.48)',
      stroke: '#FEF08A',
      progress: prog(bt, 0.3, 1.2),
    });
    drawLatitudeLine(ctx, project, 38.0, 124.2, 130.2, 'VĨ TUYẾN 38', prog(bt, 1.6, 0.8));

    const [capX, capY] = project(39.03, 125.75);
    drawRadarPin(ctx, capX, capY, 'THỦ ĐÔ', bt);

    drawOdometerCounter(ctx, {
      from: 1945, to: 1953, commas: false,
      x: 340, y: 520, p: prog(bt, 2.2, 1.4), size: 76, color: '#FACC15', outline: '#0F172A',
    });
  });
}
