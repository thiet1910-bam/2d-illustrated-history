// Ziro-History-Studio-v3 — Authentic Ziro Kinetic Typography, Counters, Icon Grids & Master Scroll
// STRICT RULE: Zero bottom karaoke subtitles! Zero top news HUD banners!
// All on-screen text is concise 1–5 word director callouts typed next to objects.
import { FONT, clamp, lerp, prog, easeOutCubic, easeOutBack, roundRect, fitText } from './helpers.js';

export function drawZiroGreyStage(ctx, W, H, baseHex = '#CCCCCC', vignette = 0.16) {
  ctx.fillStyle = baseHex;
  ctx.fillRect(0, 0, W, H);

  if (vignette > 0) {
    const vg = ctx.createRadialGradient(W / 2, H / 2, H * 0.35, W / 2, H / 2, W * 0.68);
    vg.addColorStop(0, 'rgba(0,0,0,0)');
    vg.addColorStop(1, `rgba(0,0,0,${vignette})`);
    ctx.fillStyle = vg;
    ctx.fillRect(0, 0, W, H);
  }
}

export function drawTypewriter(ctx, text, x, y, bt, startT = 0, opts = {}) {
  const {
    dur = Math.max(0.28, text.length * 0.032),
    size = 44,
    maxWidth = 860,
    weight = '900',
    color = '#18181C',
    outline = '',
    outlineWidth = 6,
    align = 'left',
    shadow = false,
  } = opts;

  if (bt < startT || !text) return;
  const p = clamp((bt - startT) / Math.max(0.05, dur));
  const chars = Math.max(1, Math.round(text.length * p));
  const sub = text.slice(0, chars);

  ctx.save();
  fitText(ctx, text, maxWidth, size, weight);
  ctx.textAlign = align;
  ctx.textBaseline = 'middle';

  if (shadow) {
    ctx.shadowColor = 'rgba(0,0,0,0.35)';
    ctx.shadowBlur = 10;
    ctx.shadowOffsetY = 3;
  }
  if (outline) {
    ctx.lineJoin = 'round';
    ctx.lineWidth = outlineWidth;
    ctx.strokeStyle = outline;
    ctx.strokeText(sub, x, y);
  }
  ctx.fillStyle = color;
  ctx.fillText(sub, x, y);
  ctx.restore();
}

export function drawOdometerCounter(ctx, {
  from = 0,
  to = 100,
  prefix = '',
  suffix = '',
  x = 960,
  y = 540,
  p = 1,
  size = 86,
  color = '#DC2626',
  outline = '#FFFFFF',
  align = 'center',
  decimals = 0,
  commas = true,
}) {
  if (p <= 0) return;
  const ep = easeOutCubic(clamp(p));
  const val = lerp(from, to, ep);
  const numStr = decimals > 0
    ? val.toFixed(decimals)
    : (commas ? Math.round(val).toLocaleString('en-US') : String(Math.round(val)));
  const full = `${prefix}${numStr}${suffix}`;

  ctx.save();
  const popScale = p < 0.25 ? lerp(0.82, 1.0, p / 0.25) : 1.0;
  ctx.translate(x, y);
  ctx.scale(popScale, popScale);
  ctx.font = `900 ${size}px ${FONT}`;
  ctx.textAlign = align;
  ctx.textBaseline = 'middle';
  ctx.lineJoin = 'round';

  if (outline) {
    ctx.lineWidth = Math.max(6, Math.round(size * 0.12));
    ctx.strokeStyle = outline;
    ctx.strokeText(full, 0, 0);
  }
  ctx.fillStyle = color;
  ctx.fillText(full, 0, 0);
  ctx.restore();
}

export function drawIconGrid(ctx, {
  count = 20,
  cols = 10,
  x = 600,
  y = 320,
  gapX = 64,
  gapY = 64,
  bt = 0,
  startT = 0,
  dur = 1.2,
  drawItem,
}) {
  if (bt < startT) return 0;
  const shown = Math.min(count, Math.floor(clamp((bt - startT) / Math.max(0.1, dur)) * count) + 1);
  for (let i = 0; i < shown; i++) {
    const r = Math.floor(i / cols);
    const c = i % cols;
    const itemT = startT + (i / count) * dur;
    const ip = easeOutBack(clamp((bt - itemT) / 0.22));
    ctx.save();
    ctx.translate(x + c * gapX, y + r * gapY);
    ctx.scale(ip, ip);
    drawItem(ctx, i);
    ctx.restore();
  }
  return shown;
}

export function drawChecklist(ctx, {
  title = '',
  items = [],       // [{ t0: 0.5, text: 'Áo choàng đỏ' }, ...]
  x = 980,
  y = 240,
  w = 680,
  rowH = 74,
  bt = 0,
  dark = false,
}) {
  const pCard = easeOutBack(prog(bt, 0, 0.4));
  if (pCard <= 0) return;

  const h = (title ? 86 : 28) + items.length * rowH + 24;
  ctx.save();
  ctx.translate(x + w / 2, y + h / 2);
  ctx.scale(pCard, pCard);
  ctx.translate(-(x + w / 2), -(y + h / 2));

  ctx.shadowColor = 'rgba(0,0,0,0.22)';
  ctx.shadowBlur = 22;
  ctx.shadowOffsetY = 8;
  roundRect(ctx, x, y, w, h, 16);
  ctx.fillStyle = dark ? '#1E293B' : '#FCFBF7';
  ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.lineWidth = 4;
  ctx.strokeStyle = '#18181C';
  ctx.stroke();

  let curY = y + 36;
  if (title) {
    fitText(ctx, title, w - 56, 34, '900');
    ctx.fillStyle = dark ? '#FACC15' : '#18181C';
    ctx.textAlign = 'left';
    ctx.textBaseline = 'middle';
    ctx.fillText(title, x + 32, y + 48);
    ctx.strokeStyle = dark ? 'rgba(255,255,255,0.15)' : 'rgba(0,0,0,0.12)';
    ctx.lineWidth = 2;
    ctx.beginPath(); ctx.moveTo(x + 28, y + 80); ctx.lineTo(x + w - 28, y + 80); ctx.stroke();
    curY = y + 98;
  }

  items.forEach((it) => {
    const bx = x + 34, by = curY + 10;
    roundRect(ctx, bx, by, 40, 40, 8);
    ctx.fillStyle = dark ? '#0F172A' : '#FFFFFF';
    ctx.fill();
    ctx.lineWidth = 3.5;
    ctx.strokeStyle = '#18181C';
    ctx.stroke();

    if (bt >= it.t0) {
      const tp = easeOutBack(prog(bt, it.t0, 0.28));
      ctx.save();
      ctx.translate(bx + 20, by + 20);
      ctx.scale(tp, tp);
      ctx.strokeStyle = '#16A34A';
      ctx.lineWidth = 6;
      ctx.lineCap = 'round';
      ctx.lineJoin = 'round';
      ctx.beginPath();
      ctx.moveTo(-11, 1); ctx.lineTo(-2, 10); ctx.lineTo(13, -10);
      ctx.stroke();
      ctx.restore();

      drawTypewriter(ctx, it.text, bx + 58, by + 21, bt, it.t0 + 0.08, {
        size: 30,
        maxWidth: w - 115,
        weight: '800',
        color: dark ? '#F8FAFC' : '#18181C',
      });
    }
    curY += rowH;
  });

  ctx.restore();
}

export function drawMasterScroll(ctx, {
  acts = [
    { roman: 'I', label: 'Khởi nguồn' },
    { roman: 'II', label: 'Bước ngoặt' },
    { roman: 'III', label: 'Xung đột' },
    { roman: 'IV', label: 'Bùng nổ' },
    { roman: 'V', label: 'Hệ quả' },
  ],
  activeIdx = 0,
  bt = 0,
  W = 1920,
  H = 1080,
}) {
  drawZiroGreyStage(ctx, W, H, '#24211D', 0.45);
  const unfurl = easeOutCubic(prog(bt, 0.02, 0.48));
  const sw = lerp(220, 1680, unfurl);
  const sh = 420;
  const cx = W / 2, cy = H / 2;

  ctx.save();
  // Parchment body
  ctx.shadowColor = 'rgba(0,0,0,0.5)';
  ctx.shadowBlur = 35;
  roundRect(ctx, cx - sw / 2, cy - sh / 2, sw, sh, 12);
  const pg = ctx.createLinearGradient(0, cy - sh / 2, 0, cy + sh / 2);
  pg.addColorStop(0, '#F6E7C1');
  pg.addColorStop(0.5, '#EED7A1');
  pg.addColorStop(1, '#DFC17B');
  ctx.fillStyle = pg;
  ctx.fill();
  ctx.shadowColor = 'transparent';
  ctx.lineWidth = 5;
  ctx.strokeStyle = '#5C3A18';
  ctx.stroke();

  // Clip inner chapter nodes
  ctx.save();
  roundRect(ctx, cx - sw / 2 + 16, cy - sh / 2 + 16, Math.max(10, sw - 32), sh - 32, 8);
  ctx.clip();

  const step = 1320 / Math.max(1, acts.length - 1);
  const startX = cx - 660;

  // Connecting dotted trail
  ctx.strokeStyle = '#854D0E';
  ctx.lineWidth = 4;
  ctx.setLineDash([12, 10]);
  ctx.beginPath();
  ctx.moveTo(startX, cy - 10);
  ctx.lineTo(startX + (acts.length - 1) * step, cy - 10);
  ctx.stroke();
  ctx.setLineDash([]);

  acts.forEach((act, idx) => {
    const nx = startX + idx * step;
    const isAct = idx === activeIdx;
    const pulse = isAct ? 1 + Math.sin(bt * 8) * 0.08 : 1;

    ctx.save();
    ctx.translate(nx, cy - 10);
    ctx.scale(pulse, pulse);
    if (isAct) {
      ctx.shadowColor = '#DC2626';
      ctx.shadowBlur = 24;
    }
    ctx.beginPath();
    ctx.arc(0, 0, isAct ? 56 : 45, 0, Math.PI * 2);
    ctx.fillStyle = isAct ? '#DC2626' : (idx < activeIdx ? '#78350F' : '#FEF3C7');
    ctx.fill();
    ctx.shadowColor = 'transparent';
    ctx.lineWidth = isAct ? 5 : 3.5;
    ctx.strokeStyle = '#451A03';
    ctx.stroke();

    ctx.fillStyle = isAct || idx < activeIdx ? '#FFFFFF' : '#451A03';
    ctx.font = `900 ${isAct ? 30 : 21}px ${FONT}`;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(`HỒI ${act.roman}`, 0, 1);
    ctx.restore();

    ctx.fillStyle = isAct ? '#991B1B' : '#451A03';
    fitText(ctx, act.label, step - 16, isAct ? 23 : 19, isAct ? '900' : '700');
    ctx.textAlign = 'center';
    ctx.fillText(act.label, nx, cy + 78);
  });

  ctx.restore();

  // Wooden scroll rollers on left & right edges
  for (const rx of [cx - sw / 2, cx + sw / 2]) {
    roundRect(ctx, rx - 18, cy - sh / 2 - 24, 36, sh + 48, 14);
    ctx.fillStyle = '#78350F';
    ctx.fill();
    ctx.lineWidth = 4.5;
    ctx.strokeStyle = '#291305';
    ctx.stroke();
  }
  ctx.restore();
}
