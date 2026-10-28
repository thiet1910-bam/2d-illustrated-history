// Ziro-History-Studio-v3 — Universal Global Satellite Atlas & Geopolitical Cartography Kit
// Supports ANY country/region on Earth offline via /shared/maps/world_satellite.jpg (Equirectangular -180..+180, +90..-90)
// as well as custom high-res regional satellite tiles!
import { FONT, roundRect, lerp, clamp, easeOutBack, easeOutCubic, prog, drawImageCover } from './helpers.js';

// Built-in simplified geopolitical [lat, lon] contours for rapid universal highlighting
export const GEO_BORDERS = {
  north_korea: [
    [38.0, 124.9], [39.0, 125.2], [39.8, 124.3], [40.5, 125.1], [41.4, 126.9],
    [41.8, 128.2], [42.9, 130.0], [42.3, 130.7], [40.6, 129.2], [39.2, 127.5], [38.3, 128.4], [37.9, 126.2]
  ],
  south_korea: [
    [37.9, 126.2], [38.3, 128.4], [37.0, 129.4], [35.1, 129.1], [34.4, 126.5],
    [35.8, 126.5], [36.9, 126.2], [37.5, 126.6]
  ],
  usa: [
    [48.8, -124.6], [49.0, -95.1], [46.8, -84.5], [45.0, -71.5], [44.8, -67.0],
    [40.5, -74.0], [35.2, -75.5], [25.2, -80.4], [29.0, -83.0], [29.5, -94.8],
    [26.0, -97.2], [31.8, -106.5], [31.3, -111.0], [32.5, -117.1], [37.8, -122.5], [43.0, -124.5]
  ],
  china: [
    [49.2, 119.5], [48.0, 134.5], [43.0, 131.2], [40.0, 124.2], [38.8, 118.0],
    [31.2, 121.8], [24.5, 118.1], [21.5, 108.5], [22.8, 103.0], [27.8, 92.0],
    [28.5, 84.0], [35.5, 76.5], [40.0, 74.0], [45.0, 80.0], [49.0, 87.8], [43.5, 111.5]
  ],
  russia: [
    [60.0, 30.0], [68.9, 33.1], [69.5, 60.0], [73.0, 80.0], [72.0, 130.0],
    [66.0, 170.0], [52.0, 158.0], [43.1, 131.9], [49.5, 118.0], [50.0, 88.0],
    [54.5, 73.0], [51.0, 55.0], [45.0, 39.0], [52.0, 34.0]
  ],
  vietnam: [
    [21.5, 108.0], [23.3, 105.3], [22.4, 102.2], [19.5, 104.0], [16.5, 106.6],
    [14.5, 107.6], [11.5, 106.0], [10.4, 104.5], [8.6, 104.8], [10.8, 108.2],
    [13.8, 109.3], [16.1, 108.2], [18.8, 105.8], [20.8, 106.8]
  ],
  ukraine: [
    [51.5, 24.0], [52.2, 33.5], [49.8, 38.2], [47.2, 39.5], [45.3, 36.5],
    [44.4, 33.8], [46.2, 30.5], [45.4, 28.8], [48.2, 22.2]
  ],
  iran: [
    [39.4, 44.2], [38.8, 48.8], [37.4, 49.2], [36.8, 53.9], [37.9, 55.5],
    [37.5, 59.5], [35.6, 61.2], [31.2, 61.8], [27.2, 62.8], [25.2, 61.4],
    [25.8, 57.3], [27.1, 56.2], [26.6, 54.0], [29.0, 50.8], [30.4, 48.1],
    [33.8, 45.8], [35.8, 46.1]
  ],
  taiwan: [
    [25.3, 121.5], [24.8, 121.9], [23.1, 121.4], [21.9, 120.8], [23.1, 120.1], [24.7, 120.9]
  ],
};

/**
 * Renders any region on Earth from /shared/maps/world_satellite.jpg (2:1 Equirectangular)
 * with Ziro's signature Spotlight Vignette, returning a `project(lat, lon) => [x, y]` mapper!
 */
export function drawWorldRegionStage(ctx, W, H, worldImg, {
  centerLat = 38.5,
  centerLon = 127.0,
  spanLon = 32.0,     // Horizontal degrees of longitude visible across W (smaller = closer zoom!)
  spotX = W / 2,
  spotY = H / 2,
  spotR = 470,
  dimAlpha = 0.66,
} = {}) {
  ctx.fillStyle = '#09111E';
  ctx.fillRect(0, 0, W, H);

  const spanLat = spanLon * (H / W);
  const west = clamp(centerLon - spanLon / 2, -180, 180 - spanLon);
  const north = clamp(centerLat + spanLat / 2, -90 + spanLat, 90);

  if (worldImg && worldImg.width > 0) {
    const iw = worldImg.naturalWidth || worldImg.width;
    const ih = worldImg.naturalHeight || worldImg.height;
    const sx = ((west + 180) / 360) * iw;
    const sy = ((90 - north) / 180) * ih;
    const sw = (spanLon / 360) * iw;
    const sh = (spanLat / 180) * ih;

    ctx.save();
    ctx.filter = 'saturate(0.88) contrast(1.10)';
    ctx.drawImage(worldImg, sx, sy, sw, sh, 0, 0, W, H);
    ctx.filter = 'none';
    ctx.restore();
  }

  // Ziro Spotlight Vignette
  const sg = ctx.createRadialGradient(spotX, spotY, spotR * 0.32, spotX, spotY, spotR * 1.45);
  sg.addColorStop(0, 'rgba(8, 12, 20, 0.04)');
  sg.addColorStop(0.55, `rgba(8, 12, 20, ${dimAlpha * 0.55})`);
  sg.addColorStop(1, `rgba(6, 10, 18, ${dimAlpha})`);
  ctx.fillStyle = sg;
  ctx.fillRect(0, 0, W, H);

  // Return [lat, lon] -> [canvasX, canvasY] projector
  return (lat, lon) => [
    ((lon - west) / spanLon) * W,
    ((north - lat) / spanLat) * H,
  ];
}

/**
 * Highlights a [lat, lon] polygon (e.g. GEO_BORDERS.north_korea or GEO_BORDERS.usa)
 * using Ziro's top-to-bottom frontline clip-mask sweep!
 */
export function drawGeoTerritory(ctx, project, latLonPoly, {
  fill = 'rgba(220, 38, 38, 0.50)',
  stroke = '#FEF08A',
  lineWidth = 4.5,
  progress = 1,
  dashed = false,
} = {}) {
  if (!latLonPoly || latLonPoly.length < 3) return;
  const pts = latLonPoly.map(([lat, lon]) => project(lat, lon));
  let minX = Infinity, maxX = -Infinity, minY = Infinity, maxY = -Infinity;
  for (const [x, y] of pts) {
    if (x < minX) minX = x;
    if (x > maxX) maxX = x;
    if (y < minY) minY = y;
    if (y > maxY) maxY = y;
  }

  const trace = () => {
    ctx.beginPath();
    pts.forEach(([x, y], i) => (i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y)));
    ctx.closePath();
  };

  ctx.save();
  if (progress > 0) {
    ctx.save();
    trace();
    ctx.clip();
    ctx.fillStyle = fill;
    ctx.fillRect(minX - 10, minY - 10, (maxX - minX) + 20, ((maxY - minY) + 20) * easeOutCubic(clamp(progress)));
    ctx.restore();
  }
  trace();
  if (dashed) ctx.setLineDash([14, 10]);
  ctx.lineWidth = lineWidth;
  ctx.strokeStyle = stroke;
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
}

/**
 * Draws a geopolitical dividing line (e.g. 38th Parallel in Korea, 17th Parallel, DMZ)
 */
export function drawLatitudeLine(ctx, project, lat, lonStart, lonEnd, label = '', p = 1, color = '#FACC15') {
  if (p <= 0) return;
  const [x0, y0] = project(lat, lonStart);
  const [x1, y1] = project(lat, lonEnd);
  const cx = lerp(x0, x1, easeOutCubic(clamp(p)));
  const cy = lerp(y0, y1, easeOutCubic(clamp(p)));

  ctx.save();
  ctx.strokeStyle = '#0F172A';
  ctx.lineWidth = 9;
  ctx.setLineDash([18, 12]);
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(cx, cy); ctx.stroke();

  ctx.strokeStyle = color;
  ctx.lineWidth = 5;
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(cx, cy); ctx.stroke();
  ctx.setLineDash([]);

  if (label && p > 0.6) {
    ctx.font = `900 24px ${FONT}`;
    ctx.textAlign = 'center';
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#0F172A';
    ctx.strokeText(label, (x0 + x1) / 2, y0 - 18);
    ctx.fillStyle = color;
    ctx.fillText(label, (x0 + x1) / 2, y0 - 18);
  }
  ctx.restore();
}

export function tracePolygon(ctx, poly, cx, cy, sc = 1) {
  ctx.beginPath();
  poly.forEach(([px, py], i) => {
    const x = cx + px * sc, y = cy + py * sc;
    if (i === 0) ctx.moveTo(x, y);
    else ctx.lineTo(x, y);
  });
  ctx.closePath();
}

export function drawSatelliteStage(ctx, W, H, satImg, {
  spotX = 960,
  spotY = 520,
  spotR = 460,
  dimAlpha = 0.68,
} = {}) {
  ctx.fillStyle = '#0B1320';
  ctx.fillRect(0, 0, W, H);

  if (satImg) {
    ctx.save();
    ctx.filter = 'saturate(0.85) contrast(1.08)';
    drawImageCover(ctx, satImg, 0, 0, W, H);
    ctx.filter = 'none';
    ctx.restore();
  }

  const sg = ctx.createRadialGradient(spotX, spotY, spotR * 0.32, spotX, spotY, spotR * 1.45);
  sg.addColorStop(0, 'rgba(8, 12, 20, 0.05)');
  sg.addColorStop(0.55, `rgba(8, 12, 20, ${dimAlpha * 0.55})`);
  sg.addColorStop(1, `rgba(6, 10, 18, ${dimAlpha})`);
  ctx.fillStyle = sg;
  ctx.fillRect(0, 0, W, H);
}

export function drawClipMaskTerritory(ctx, poly, cx, cy, sc, {
  fill = 'rgba(220, 38, 38, 0.52)',
  stroke = '#FEF08A',
  lineWidth = 5,
  progress = 1,
  dashed = false,
} = {}) {
  ctx.save();
  tracePolygon(ctx, poly, cx, cy, sc);
  if (progress > 0) {
    ctx.save();
    ctx.clip();
    const minY = cy - 220 * sc;
    const maxH = 440 * sc * easeOutCubic(clamp(progress));
    ctx.fillStyle = fill;
    ctx.fillRect(cx - 320 * sc, minY, 640 * sc, maxH);
    ctx.restore();
  }
  tracePolygon(ctx, poly, cx, cy, sc);
  if (dashed) ctx.setLineDash([14, 10]);
  ctx.lineWidth = lineWidth;
  ctx.strokeStyle = stroke;
  ctx.stroke();
  ctx.setLineDash([]);
  ctx.restore();
}

export function drawRadarPin(ctx, x, y, label, t, color = '#EF4444') {
  ctx.save();
  for (let r = 0; r < 3; r++) {
    const rp = ((t * 0.9 + r * 0.33) % 1);
    ctx.beginPath();
    ctx.arc(x, y, 12 + rp * 65, 0, Math.PI * 2);
    ctx.strokeStyle = `rgba(239, 68, 68, ${1 - rp})`;
    ctx.lineWidth = 3;
    ctx.stroke();
  }
  ctx.beginPath();
  ctx.arc(x, y, 10, 0, Math.PI * 2);
  ctx.fillStyle = color;
  ctx.fill();
  ctx.lineWidth = 3;
  ctx.strokeStyle = '#FFF';
  ctx.stroke();

  if (label) {
    ctx.font = `900 26px ${FONT}`;
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.lineJoin = 'round';
    ctx.lineWidth = 6;
    ctx.strokeStyle = '#0F172A';
    ctx.strokeText(label, x + 20, y + 2);
    ctx.fillStyle = '#FFFFFF';
    ctx.fillText(label, x + 20, y + 2);
  }
  ctx.restore();
}

export function drawEmpireArrow(ctx, { bt, t0, label, x0, y0, x1, y1, col = '#EF4444' }) {
  const ep = easeOutBack(prog(bt, t0, 0.55));
  if (ep <= 0) return;
  const cx = lerp(x0, x1, ep);
  const cy = lerp(y0, y1, ep);

  ctx.save();
  ctx.strokeStyle = '#0F172A';
  ctx.lineWidth = 15;
  ctx.lineCap = 'round';
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(cx, cy); ctx.stroke();

  ctx.strokeStyle = col;
  ctx.lineWidth = 10;
  ctx.beginPath(); ctx.moveTo(x0, y0); ctx.lineTo(cx, cy); ctx.stroke();

  const ang = Math.atan2(y1 - y0, x1 - x0);
  ctx.translate(cx, cy);
  ctx.rotate(ang);
  ctx.fillStyle = col;
  ctx.strokeStyle = '#0F172A';
  ctx.lineWidth = 3;
  ctx.beginPath();
  ctx.moveTo(18, 0); ctx.lineTo(-22, -18); ctx.lineTo(-22, 18); ctx.closePath();
  ctx.fill(); ctx.stroke();
  ctx.restore();

  if (label) {
    ctx.save();
    ctx.font = `900 22px ${FONT}`;
    const tw = ctx.measureText(label).width + 30;
    roundRect(ctx, x0 - tw / 2, y0 - 23, tw, 46, 10);
    ctx.fillStyle = '#0F172A';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = col;
    ctx.stroke();
    ctx.fillStyle = '#FFF';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(label, x0, y0);
    ctx.restore();
  }
}
