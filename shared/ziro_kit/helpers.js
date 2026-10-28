// Ziro-History-Studio-v3 — Shared 2D Vector & Motion Kit (Full HD 1920x1080, Vietnamese-safe Typography)
export const FONT = "'Segoe UI', 'Arial', sans-serif";

export const clamp = (v, a = 0, b = 1) => Math.max(a, Math.min(b, v));
export const lerp = (a, b, p) => a + (b - a) * p;
export const prog = (t, start, dur) => clamp((t - start) / Math.max(0.0001, dur));

export const easeOutCubic = x => 1 - Math.pow(1 - clamp(x), 3);
export const easeInOutCubic = x => {
  const p = clamp(x);
  return p < 0.5 ? 4 * p * p * p : 1 - Math.pow(-2 * p + 2, 3) / 2;
};
export const easeOutBack = x => {
  const p = clamp(x);
  const c1 = 1.70158, c3 = c1 + 1;
  return 1 + c3 * Math.pow(p - 1, 3) + c1 * Math.pow(p - 1, 2);
};
export const easeOutQuart = x => 1 - Math.pow(1 - clamp(x), 4);

export function loadImg(src) {
  return new Promise((resolve, reject) => {
    const img = new Image();
    img.onload = () => resolve(img);
    img.onerror = () => reject(new Error('Failed to load image: ' + src));
    img.src = src;
  });
}

export function roundRect(ctx, x, y, w, h, r) {
  const rr = Math.min(r, Math.abs(w) / 2, Math.abs(h) / 2);
  ctx.beginPath();
  ctx.moveTo(x + rr, y);
  ctx.arcTo(x + w, y, x + w, y + h, rr);
  ctx.arcTo(x + w, y + h, x, y + h, rr);
  ctx.arcTo(x, y + h, x, y, rr);
  ctx.arcTo(x, y, x + w, y, rr);
  ctx.closePath();
}

export function drawZiroStage(ctx, W, H, topCol = '#D4CFC7', botCol = '#BEB7AC', vignette = 0.28, dark = false) {
  const g = ctx.createLinearGradient(0, 0, 0, H);
  g.addColorStop(0, topCol);
  g.addColorStop(1, botCol);
  ctx.fillStyle = g;
  ctx.fillRect(0, 0, W, H);

  ctx.save();
  ctx.strokeStyle = dark ? 'rgba(255,255,255,0.035)' : 'rgba(30,25,20,0.04)';
  ctx.lineWidth = 1;
  for (let x = 120; x < W; x += 120) {
    ctx.beginPath(); ctx.moveTo(x, 0); ctx.lineTo(x, H); ctx.stroke();
  }
  for (let y = 120; y < H; y += 120) {
    ctx.beginPath(); ctx.moveTo(0, y); ctx.lineTo(W, y); ctx.stroke();
  }

  const vg = ctx.createRadialGradient(W / 2, H * 0.48, H * 0.28, W / 2, H * 0.5, W * 0.68);
  vg.addColorStop(0, 'rgba(0,0,0,0)');
  vg.addColorStop(1, `rgba(0,0,0,${vignette})`);
  ctx.fillStyle = vg;
  ctx.fillRect(0, 0, W, H);
  ctx.restore();
}

export function withCamera(ctx, W, H, { zoom = 1, panX = 0, panY = 0, shake = 0, t = 0 }, fn) {
  ctx.save();
  const sx = shake > 0 ? Math.sin(t * 67.3) * shake : 0;
  const sy = shake > 0 ? Math.cos(t * 53.9) * shake * 0.8 : 0;
  const driftX = Math.sin(t * 0.9) * 2.5;
  const driftY = Math.cos(t * 0.7) * 1.8;
  ctx.translate(W / 2 + panX + driftX + sx, H / 2 + panY + driftY + sy);
  ctx.scale(zoom, zoom);
  ctx.translate(-W / 2, -H / 2);
  fn();
  ctx.restore();
}

export function fitText(ctx, text, maxWidth, baseSize, weight = '800') {
  let sz = baseSize;
  ctx.font = `${weight} ${sz}px ${FONT}`;
  while (ctx.measureText(text).width > maxWidth && sz > 14) {
    sz -= 1;
    ctx.font = `${weight} ${sz}px ${FONT}`;
  }
  return sz;
}

export function drawHudBanner(ctx, W, text, p, accent = '#C92A2A', dark = false) {
  if (p <= 0 || !text) return;
  ctx.save();
  const ep = easeOutCubic(p);
  const y = lerp(34, 62, ep);
  ctx.globalAlpha = clamp(p * 1.4);

  fitText(ctx, text, W - 260, 34, '800');
  const tw = ctx.measureText(text).width;
  const padX = 34, boxW = tw + padX * 2, boxH = 58;
  const bx = (W - boxW) / 2, by = y - boxH / 2;

  ctx.shadowColor = 'rgba(0,0,0,0.22)';
  ctx.shadowBlur = 18;
  ctx.shadowOffsetY = 5;
  roundRect(ctx, bx, by, boxW, boxH, 14);
  ctx.fillStyle = dark ? 'rgba(22, 25, 34, 0.92)' : 'rgba(252, 250, 245, 0.94)';
  ctx.fill();
  ctx.shadowColor = 'transparent';

  ctx.lineWidth = 2.5;
  ctx.strokeStyle = dark ? 'rgba(255,255,255,0.16)' : 'rgba(25,25,25,0.14)';
  ctx.stroke();

  roundRect(ctx, bx + 8, by + 10, 7, boxH - 20, 3.5);
  ctx.fillStyle = accent;
  ctx.fill();

  ctx.fillStyle = dark ? '#F8F9FA' : '#1E2024';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, W / 2 + 4, y + 1);
  ctx.restore();
}

export function drawSubtitle(ctx, W, H, text, alpha = 1) {
  if (!text || alpha <= 0) return;
  ctx.save();
  ctx.globalAlpha = alpha;
  fitText(ctx, text, W - 200, 27, '700');
  const tw = ctx.measureText(text).width;
  const bw = tw + 52, bh = 50;
  const bx = (W - bw) / 2, by = H - 76;

  roundRect(ctx, bx, by, bw, bh, 25);
  ctx.fillStyle = 'rgba(15, 17, 23, 0.84)';
  ctx.fill();
  ctx.lineWidth = 1.5;
  ctx.strokeStyle = 'rgba(255, 212, 112, 0.35)';
  ctx.stroke();

  ctx.fillStyle = '#FFF9EC';
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, W / 2, by + bh / 2 + 1);
  ctx.restore();
}

export function drawImageCover(ctx, img, x, y, w, h) {
  if (!img) return;
  const ir = img.width / img.height;
  const br = w / h;
  let sx = 0, sy = 0, sw = img.width, sh = img.height;
  if (ir > br) {
    sw = img.height * br;
    sx = (img.width - sw) / 2;
  } else {
    sh = img.width / br;
    sy = (img.height - sh) / 2;
  }
  ctx.drawImage(img, sx, sy, sw, sh, x, y, w, h);
}

export function drawPolaroid(ctx, { img, cx, cy, w, h, rot = 0, tag = '', caption = '', tagCol = '#1C64F2', pop = 1, mystery = false }) {
  if (pop <= 0) return;
  ctx.save();
  const s = easeOutBack(pop);
  ctx.translate(cx, cy);
  ctx.rotate(rot);
  ctx.scale(s, s);

  const pad = 16, botPad = caption ? 64 : 26;
  const fw = w + pad * 2, fh = h + pad + botPad;

  ctx.shadowColor = 'rgba(0,0,0,0.34)';
  ctx.shadowBlur = 28;
  ctx.shadowOffsetY = 12;
  roundRect(ctx, -fw / 2, -fh / 2, fw, fh, 10);
  ctx.fillStyle = '#FCFBF7';
  ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = '#242424';
  ctx.stroke();

  const ix = -w / 2, iy = -fh / 2 + pad;
  ctx.save();
  roundRect(ctx, ix, iy, w, h, 5);
  ctx.clip();
  if (img && !mystery) {
    drawImageCover(ctx, img, ix, iy, w, h);
  } else {
    const mg = ctx.createLinearGradient(ix, iy, ix + w, iy + h);
    mg.addColorStop(0, '#343A46');
    mg.addColorStop(1, '#1E222B');
    ctx.fillStyle = mg;
    ctx.fillRect(ix, iy, w, h);
    ctx.fillStyle = '#FFD166';
    ctx.font = `900 112px ${FONT}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('?', 0, iy + h / 2);
  }
  ctx.restore();

  ctx.strokeStyle = 'rgba(0,0,0,0.22)';
  ctx.lineWidth = 1.5;
  ctx.strokeRect(ix, iy, w, h);

  ctx.beginPath();
  ctx.arc(0, -fh / 2 + 5, 11, 0, Math.PI * 2);
  ctx.fillStyle = '#E03131';
  ctx.fill();
  ctx.lineWidth = 2.5;
  ctx.strokeStyle = '#1E1E1E';
  ctx.stroke();
  ctx.beginPath();
  ctx.arc(-3, -fh / 2 + 2, 3.5, 0, Math.PI * 2);
  ctx.fillStyle = '#FFA8A8';
  ctx.fill();

  if (tag) {
    ctx.font = `800 19px ${FONT}`;
    const tw = ctx.measureText(tag).width + 26;
    roundRect(ctx, ix + 12, iy + 12, tw, 34, 7);
    ctx.fillStyle = tagCol;
    ctx.fill();
    ctx.strokeStyle = '#111';
    ctx.lineWidth = 2;
    ctx.stroke();
    ctx.fillStyle = '#FFF';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(tag, ix + 25, iy + 29);
  }

  if (caption) {
    fitText(ctx, caption, w - 12, 22, '700');
    ctx.fillStyle = '#22252A';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(caption, 0, iy + h + botPad / 2 + 2);
  }
  ctx.restore();
}

export function drawRubberStamp(ctx, x, y, text, color = '#C92A2A', rot = -0.1, p = 1) {
  if (p <= 0) return;
  ctx.save();
  const ep = easeOutCubic(clamp(p * 1.6));
  const sc = lerp(2.1, 1.0, ep);
  ctx.globalAlpha = clamp(p * 2.2);
  ctx.translate(x, y);
  ctx.rotate(rot);
  ctx.scale(sc, sc);

  fitText(ctx, text, 680, 32, '900');
  const tw = ctx.measureText(text).width;
  const bw = tw + 46, bh = 58;

  roundRect(ctx, -bw / 2, -bh / 2, bw, bh, 8);
  ctx.fillStyle = 'rgba(255, 250, 245, 0.93)';
  ctx.fill();
  ctx.lineWidth = 5;
  ctx.strokeStyle = color;
  ctx.stroke();

  roundRect(ctx, -bw / 2 + 6, -bh / 2 + 6, bw - 12, bh - 12, 4);
  ctx.lineWidth = 2;
  ctx.stroke();

  ctx.fillStyle = color;
  ctx.textAlign = 'center';
  ctx.textBaseline = 'middle';
  ctx.fillText(text, 0, 1);
  ctx.restore();
}

export function drawZiroChar(ctx, x, y, scale = 1, opts = {}) {
  const {
    role = 'citizen',
    mood = 'neutral',
    walk = 0,
    color = '#3B82F6',
    flip = 1,
    armRaise = 0,
    phone = false,
  } = opts;

  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale * flip, scale);
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';

  ctx.fillStyle = 'rgba(0,0,0,0.18)';
  ctx.beginPath();
  ctx.ellipse(0, 62, 34, 9, 0, 0, Math.PI * 2);
  ctx.fill();

  const legSwing = Math.sin(walk) * 16;

  if (role === 'chador') {
    ctx.beginPath();
    ctx.moveTo(0, -68);
    ctx.bezierCurveTo(34, -64, 48, 8, 44, 58);
    ctx.quadraticCurveTo(0, 66, -44, 58);
    ctx.bezierCurveTo(-48, 8, -34, -64, 0, -68);
    ctx.fillStyle = '#181A20';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#0B0C0E';
    ctx.stroke();

    roundRect(ctx, -18, -48, 36, 20, 8);
    ctx.fillStyle = '#EAC8A8';
    ctx.fill();
    ctx.fillStyle = '#111';
    ctx.beginPath();
    ctx.arc(-7, -38, 2.8, 0, Math.PI * 2);
    ctx.arc(7, -38, 2.8, 0, Math.PI * 2);
    ctx.fill();
    ctx.restore();
    return;
  }

  ctx.strokeStyle = '#1F2328';
  ctx.lineWidth = 6.5;
  ctx.beginPath();
  ctx.moveTo(-11, 22);
  ctx.lineTo(-13 + legSwing, 58);
  ctx.lineTo(-4 + legSwing, 58);
  ctx.moveTo(11, 22);
  ctx.lineTo(13 - legSwing, 58);
  ctx.lineTo(22 - legSwing, 58);
  ctx.stroke();

  if (role === 'spartan') {
    ctx.beginPath();
    ctx.moveTo(-24, -18);
    ctx.quadraticCurveTo(-46, 18, -36, 52);
    ctx.lineTo(32, 50);
    ctx.quadraticCurveTo(42, 16, 24, -18);
    ctx.closePath();
    ctx.fillStyle = '#B91C1C';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#1E1E1E';
    ctx.stroke();
  }

  if (role === 'cleric') {
    ctx.beginPath();
    ctx.moveTo(-24, -22);
    ctx.quadraticCurveTo(-36, 22, -32, 54);
    ctx.lineTo(32, 54);
    ctx.quadraticCurveTo(36, 22, 24, -22);
    ctx.closePath();
    ctx.fillStyle = '#252830';
    ctx.fill();
    ctx.lineWidth = 3.5;
    ctx.strokeStyle = '#111';
    ctx.stroke();
    ctx.strokeStyle = '#D4AF37';
    ctx.lineWidth = 2;
    ctx.beginPath();
    ctx.moveTo(0, -20);
    ctx.lineTo(0, 52);
    ctx.stroke();
  } else if (role === 'spartan') {
    roundRect(ctx, -23, -22, 46, 42, 12);
    ctx.fillStyle = '#F2B885';
    ctx.fill();
    ctx.lineWidth = 3.2;
    ctx.strokeStyle = '#1F1F1F';
    ctx.stroke();
    ctx.strokeStyle = 'rgba(130,70,30,0.65)';
    ctx.lineWidth = 2;
    for (let row = 0; row < 3; row++) {
      ctx.strokeRect(-11, -4 + row * 7, 10, 6);
      ctx.strokeRect(1, -4 + row * 7, 10, 6);
    }
    roundRect(ctx, -24, 16, 48, 18, 6);
    ctx.fillStyle = '#EF233C';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#1F1F1F';
    ctx.stroke();
  } else if (role === 'woman70s') {
    ctx.beginPath();
    ctx.moveTo(-18, -22);
    ctx.lineTo(18, -22);
    ctx.lineTo(28, 28);
    ctx.lineTo(-28, 28);
    ctx.closePath();
    ctx.fillStyle = color;
    ctx.fill();
    ctx.lineWidth = 3.2;
    ctx.strokeStyle = '#1E1E1E';
    ctx.stroke();
  } else {
    roundRect(ctx, -22, -22, 44, 48, 12);
    ctx.fillStyle = color;
    ctx.fill();
    ctx.lineWidth = 3.2;
    ctx.strokeStyle = '#1E1E1E';
    ctx.stroke();
  }

  if (role === 'woman70s') {
    ctx.beginPath();
    ctx.moveTo(-26, -54);
    ctx.bezierCurveTo(-40, -34, -38, -8, -26, -4);
    ctx.lineTo(26, -4);
    ctx.bezierCurveTo(38, -8, 40, -34, 26, -54);
    ctx.closePath();
    ctx.fillStyle = '#3B2314';
    ctx.fill();
    ctx.lineWidth = 2.8;
    ctx.strokeStyle = '#1A110B';
    ctx.stroke();
  }

  ctx.strokeStyle = '#1F2328';
  ctx.lineWidth = 6;
  ctx.beginPath();
  ctx.moveTo(-21, -14);
  if (role === 'spartan') {
    ctx.lineTo(-38, -18);
    ctx.lineTo(-32, -38);
    ctx.moveTo(21, -14);
    ctx.lineTo(38, -18);
    ctx.lineTo(32, -38);
  } else if (phone) {
    ctx.lineTo(-32, 6);
    ctx.moveTo(21, -14);
    ctx.lineTo(34, -8 - armRaise * 18);
  } else {
    ctx.lineTo(-32 - legSwing * 0.6, 12 - armRaise * 26);
    ctx.moveTo(21, -14);
    ctx.lineTo(32 + legSwing * 0.6, 10 - armRaise * 26);
  }
  ctx.stroke();

  if (phone) {
    roundRect(ctx, 28, -24 - armRaise * 18, 15, 24, 3);
    ctx.fillStyle = '#111827';
    ctx.fill();
    ctx.strokeStyle = '#38BDF8';
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  ctx.beginPath();
  ctx.arc(0, -46, 23, 0, Math.PI * 2);
  ctx.fillStyle = '#F7D6B5';
  ctx.fill();
  ctx.lineWidth = 3.2;
  ctx.strokeStyle = '#1E1E1E';
  ctx.stroke();

  if (role === 'cleric') {
    ctx.beginPath();
    ctx.moveTo(-15, -34);
    ctx.quadraticCurveTo(0, 4, 15, -34);
    ctx.fillStyle = '#E5E7EB';
    ctx.fill();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#374151';
    ctx.stroke();
    roundRect(ctx, -26, -74, 52, 22, 11);
    ctx.fillStyle = '#111318';
    ctx.fill();
    ctx.lineWidth = 3;
    ctx.strokeStyle = '#000';
    ctx.stroke();
  } else if (role === 'youth') {
    ctx.beginPath();
    ctx.moveTo(-26, -58);
    ctx.lineTo(0, -72);
    ctx.lineTo(26, -58);
    ctx.lineTo(0, -48);
    ctx.closePath();
    ctx.fillStyle = '#1E293B';
    ctx.fill();
    ctx.lineWidth = 2.5;
    ctx.strokeStyle = '#0F172A';
    ctx.stroke();
  } else if (role === 'spartan') {
    ctx.beginPath();
    ctx.arc(0, -60, 26, Math.PI, 0);
    ctx.fillStyle = '#DC2626';
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, -52, 23, Math.PI * 1.05, -0.05);
    ctx.fillStyle = '#D97706';
    ctx.fill();
    ctx.stroke();
  } else if (role === 'weaver') {
    roundRect(ctx, -22, -72, 44, 18, 8);
    ctx.fillStyle = '#7C2D12';
    ctx.fill();
    ctx.stroke();
  } else if (role === 'woman70s') {
    ctx.beginPath();
    ctx.arc(0, -50, 23, Math.PI * 1.08, -0.08);
    ctx.fillStyle = '#3B2314';
    ctx.fill();
  }

  ctx.fillStyle = '#18181B';
  ctx.beginPath();
  ctx.arc(-8, -47, 3.2, 0, Math.PI * 2);
  ctx.arc(8, -47, 3.2, 0, Math.PI * 2);
  ctx.fill();

  ctx.strokeStyle = '#18181B';
  ctx.lineWidth = 2.6;
  if (mood === 'stern' || mood === 'weary') {
    ctx.beginPath();
    ctx.moveTo(-14, -55); ctx.lineTo(-4, -52);
    ctx.moveTo(14, -55); ctx.lineTo(4, -52);
    ctx.stroke();
  }
  ctx.beginPath();
  if (mood === 'happy' || mood === 'proud') {
    ctx.arc(0, -40, 7, 0.15, Math.PI - 0.15);
  } else if (mood === 'shocked') {
    ctx.arc(0, -37, 4.5, 0, Math.PI * 2);
  } else {
    ctx.moveTo(-6, -37);
    ctx.lineTo(6, -37);
  }
  ctx.stroke();

  ctx.restore();
}

export function drawPersianCarpet(ctx, cx, cy, w, h, p = 1) {
  if (p <= 0) return;
  ctx.save();
  const curW = w * easeOutCubic(p);
  ctx.translate(cx, cy);

  ctx.strokeStyle = '#EAB308';
  ctx.lineWidth = 3;
  for (let ty = -h / 2 + 8; ty <= h / 2 - 8; ty += 12) {
    ctx.beginPath();
    ctx.moveTo(-curW / 2 - 14, ty); ctx.lineTo(-curW / 2, ty);
    ctx.moveTo(curW / 2, ty); ctx.lineTo(curW / 2 + 14, ty);
    ctx.stroke();
  }

  ctx.shadowColor = 'rgba(0,0,0,0.38)';
  ctx.shadowBlur = 24;
  ctx.shadowOffsetY = 10;
  roundRect(ctx, -curW / 2, -h / 2, curW, h, 8);
  ctx.fillStyle = '#881337';
  ctx.fill();
  ctx.shadowColor = 'transparent';

  ctx.save();
  roundRect(ctx, -curW / 2, -h / 2, curW, h, 8);
  ctx.clip();

  ctx.strokeStyle = '#FACC15';
  ctx.lineWidth = 4;
  ctx.strokeRect(-curW / 2 + 12, -h / 2 + 12, curW - 24, h - 24);
  ctx.strokeStyle = '#FCA5A5';
  ctx.lineWidth = 2;
  ctx.strokeRect(-curW / 2 + 24, -h / 2 + 24, curW - 48, h - 48);

  ctx.beginPath();
  ctx.moveTo(0, -h * 0.28);
  ctx.lineTo(w * 0.22, 0);
  ctx.lineTo(0, h * 0.28);
  ctx.lineTo(-w * 0.22, 0);
  ctx.closePath();
  ctx.fillStyle = '#1E3A8A';
  ctx.fill();
  ctx.lineWidth = 3.5;
  ctx.strokeStyle = '#FDE047';
  ctx.stroke();

  ctx.beginPath();
  ctx.arc(0, 0, Math.min(w, h) * 0.11, 0, Math.PI * 2);
  ctx.fillStyle = '#D97706';
  ctx.fill();
  ctx.stroke();

  const corners = [[-w * 0.34, -h * 0.26], [w * 0.34, -h * 0.26], [-w * 0.34, h * 0.26], [w * 0.34, h * 0.26]];
  for (const [qx, qy] of corners) {
    ctx.beginPath();
    ctx.arc(qx, qy, 18, 0, Math.PI * 2);
    ctx.fillStyle = '#B45309';
    ctx.fill();
    ctx.strokeStyle = '#FEF08A';
    ctx.lineWidth = 2;
    ctx.stroke();
  }

  ctx.restore();
  ctx.restore();
}
