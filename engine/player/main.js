// Ziro-History-Studio-v3 — Dynamic Cluster Scene Host (Full HD 1920x1080 @ 30fps + Auto 30fps Lip-Sync)
const params = new URLSearchParams(location.search);
const W = Number(params.get('w')) || 1920;
const H = Number(params.get('h')) || 1080;
const scale = Number(params.get('scale')) || 1;
const dur = Number(params.get('dur')) || 60;
const episode = params.get('episode');
const cluster = params.get('cluster');

if (!episode || !cluster) {
  throw new Error('Missing ?episode=<id>&cluster=<id> query parameters');
}

const canvas = document.getElementById('c');
canvas.width = Math.max(2, 2 * Math.round(W * scale / 2));
canvas.height = Math.max(2, 2 * Math.round(H * scale / 2));
const ctx = canvas.getContext('2d');

let timeline = null;
try {
  const res = await fetch(`/assets/timelines/timeline_${encodeURIComponent(cluster)}.json`);
  if (res.ok) timeline = await res.json();
} catch {}

const mouthArr = timeline?.mouth_30fps || [];
const tlFps = timeline?.fps || 30;

const mod = await import(`/episodes/${episode}/3_scenes/${cluster}.js`);
await mod.init?.({ W, H, scale, episode, cluster, timeline });
await document.fonts.ready;

window.renderFrame = async t => {
  const fIdx = Math.floor(Math.max(0, t) * tlFps);
  const mouth = fIdx < mouthArr.length ? mouthArr[fIdx] : 0;

  ctx.setTransform(1, 0, 0, 1, 0, 0);
  ctx.fillStyle = '#CCCCCC';
  ctx.fillRect(0, 0, canvas.width, canvas.height);
  ctx.save();
  ctx.setTransform(canvas.width / W, 0, 0, canvas.height / H, 0, 0);
  await mod.draw(ctx, t, { W, H, scale, dur, t, timeline, mouth });
  ctx.restore();
};

window.grab = (type = 'image/jpeg', quality = 0.96) => canvas.toDataURL(type, quality);
window.__ready = true;
