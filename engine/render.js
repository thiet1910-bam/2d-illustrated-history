#!/usr/bin/env node
// Ziro-History-Studio-v3 — Fast HTML5 Canvas + Vector Renderer (Full HD 1920x1080 @ 30fps)
// Usage:
//   Peak QA frames: node engine/render.js --episode EP01_Demo --cluster cum_01_Hoi_I --peaks "1.8,11.2,21.1"
//   Full cluster:   node engine/render.js --episode EP01_Demo --cluster cum_01_Hoi_I
import http from 'node:http';
import { spawn, execFileSync } from 'node:child_process';
import { createRequire } from 'node:module';
import { once } from 'node:events';
import { readFile, stat, mkdir, writeFile } from 'node:fs/promises';
import { existsSync } from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const engineDir = path.dirname(fileURLToPath(import.meta.url));
const studioRoot = path.resolve(engineDir, '..');
const a = process.argv.slice(2);
const opt = (k, d = '') => { const i = a.indexOf('--' + k); return i < 0 ? d : a[i + 1]; };

const episode = opt('episode');
const cluster = opt('cluster');
if (!episode || !cluster) {
  throw new Error('Usage: node engine/render.js --episode <EP_ID> --cluster <CLUSTER_ID> [--from 0 --to N --peaks "t1,t2"]');
}

const timelinePath = path.join(studioRoot, 'episodes', episode, '2_assets', 'timelines', `timeline_${cluster}.json`);
let defaultDur = 60;
if (existsSync(timelinePath)) {
  const tl = JSON.parse(await readFile(timelinePath, 'utf8'));
  defaultDur = Number(tl.total_duration_sec) || defaultDur;
}

const from = Number(opt('from', 0));
const to = Number(opt('to', defaultDur));
const fps = Number(opt('fps', 30));
const scale = Number(opt('scale', 1));
const peaksArg = opt('peaks', '');

const cfgPath = path.join(studioRoot, '.mvd', 'config.json');
const cfg = existsSync(cfgPath) ? JSON.parse(await readFile(cfgPath, 'utf8')) : {};
let ffmpeg = process.env.MVD_FFMPEG || (cfg.ffmpeg && existsSync(cfg.ffmpeg) ? cfg.ffmpeg : '');
if (!ffmpeg) {
  try {
    ffmpeg = execFileSync('python', [path.join(engineDir, 'bins.py'), 'ffmpeg'], { encoding: 'utf8' }).trim();
  } catch {
    ffmpeg = 'ffmpeg';
  }
}

const req = createRequire(path.join(studioRoot, 'package.json'));
const { chromium } = req('playwright');

const mime = {
  '.html': 'text/html', '.js': 'text/javascript', '.mjs': 'text/javascript',
  '.json': 'application/json', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.woff2': 'font/woff2'
};

// Serve /engine/player/, /shared/, /episodes/<ep>/3_scenes/, and alias /assets/ -> /episodes/<ep>/2_assets/
const server = http.createServer(async (request, response) => {
  try {
    const u = decodeURIComponent(new URL(request.url, 'http://localhost').pathname);
    if (u.split('/').some(s => s.startsWith('.'))) throw Error('Forbidden');
    let f;
    if (u.startsWith('/assets/')) {
      f = path.resolve(studioRoot, 'episodes', episode, '2_assets', '.' + u.slice('/assets'.length));
    } else if (['/engine/player/', '/shared/', `/episodes/${episode}/`].some(p => u.startsWith(p))) {
      f = path.resolve(studioRoot, '.' + u);
    } else {
      throw Error('Forbidden');
    }
    if (!f.startsWith(studioRoot + path.sep) || (await stat(f)).isDirectory()) throw Error('Forbidden');
    response.writeHead(200, { 'Content-Type': mime[path.extname(f).toLowerCase()] || 'application/octet-stream' });
    response.end(await readFile(f));
  } catch {
    response.writeHead(404);
    response.end('Not found');
  }
});

let browser, encoder, encodeResult;
try {
  await new Promise((resolve, reject) => { server.once('error', reject); server.listen(0, '127.0.0.1', resolve); });
  browser = await chromium.launch({ headless: true });
  const page = await browser.newPage();
  const errors = [];
  page.on('pageerror', e => errors.push(e.message));
  const url = `http://127.0.0.1:${server.address().port}/engine/player/index.html?episode=${encodeURIComponent(episode)}&cluster=${encodeURIComponent(cluster)}&dur=${to}&scale=${scale}`;
  await page.goto(url);
  await page.waitForFunction(() => window.__ready === true, {}, { timeout: 30000 });

  if (peaksArg) {
    const peaksOut = path.resolve(opt('out', path.join(studioRoot, '.cache', episode, cluster, 'peaks')));
    await mkdir(peaksOut, { recursive: true });
    const times = peaksArg.split(',').map(Number);
    for (let idx = 0; idx < times.length; idx++) {
      await page.evaluate(t => window.renderFrame(t), times[idx]);
      if (errors.length) throw Error(errors.join('\n'));
      const data = await page.evaluate(() => window.grab('image/png'));
      const bytes = Buffer.from(data.slice(data.indexOf(',') + 1), 'base64');
      await writeFile(path.join(peaksOut, `peak_${String(idx + 1).padStart(2, '0')}.png`), bytes);
    }
    console.log(`[QA PEAKS] Captured ${times.length} PNG frames -> ${peaksOut}`);
  } else {
    const count = Math.ceil((to - from) * fps - 1e-8);
    const outDir = path.resolve(opt('out', path.join(studioRoot, 'episodes', episode, '4_output', 'clusters')));
    await mkdir(outDir, { recursive: true });
    const outName = opt('name', cluster);
    const dest = path.join(outDir, outName + '.mp4');

    const defaultAudio = path.join(studioRoot, '.cache', episode, cluster, `mixed_${cluster}.wav`);
    const fallbackVoice = path.join(studioRoot, '.cache', episode, cluster, `voice_${cluster}.wav`);
    const audioPath = opt('audio', existsSync(defaultAudio) ? defaultAudio : (existsSync(fallbackVoice) ? fallbackVoice : ''));

    const args = ['-hide_banner', '-y', '-f', 'image2pipe', '-vcodec', 'mjpeg', '-framerate', String(fps), '-i', 'pipe:0'];
    if (audioPath && existsSync(path.resolve(audioPath))) {
      args.push('-ss', String(from), '-t', String(to - from), '-i', path.resolve(audioPath));
      args.push('-map', '0:v:0', '-map', '1:a:0', '-af', 'apad', '-c:a', 'aac', '-b:a', '192k', '-ar', '48000');
    } else {
      args.push('-map', '0:v:0');
    }
    args.push('-c:v', 'libx264', '-preset', 'fast', '-crf', '19', '-pix_fmt', 'yuv420p', '-frames:v', String(count), '-t', String(count / fps), '-movflags', '+faststart', dest);

    encoder = spawn(ffmpeg, args, { stdio: ['pipe', 'inherit', 'inherit'] });
    encodeResult = new Promise((resolve, reject) => {
      encoder.once('error', reject);
      encoder.once('close', code => code === 0 ? resolve() : reject(Error('FFmpeg exited ' + code)));
    });
    encodeResult.catch(() => {});
    encoder.stdin.on('error', () => {});

    for (let i = 0; i < count; i++) {
      await page.evaluate(t => window.renderFrame(t), from + i / fps);
      if (errors.length) throw Error(errors.join('\n'));
      const data = await page.evaluate(() => window.grab('image/jpeg', 0.96));
      const bytes = Buffer.from(data.slice(data.indexOf(',') + 1), 'base64');
      if (!encoder.stdin.write(bytes)) {
        await Promise.race([once(encoder.stdin, 'drain'), encodeResult.then(() => { throw Error('Encoder ended early'); })]);
      }
    }
    encoder.stdin.end();
    await encodeResult;
    console.log(`[RENDER PASS] ${count} frames (${(count / fps).toFixed(2)}s) -> ${dest}`);
  }
} finally {
  if (encoder && encoder.exitCode === null) encoder.kill();
  if (browser) await browser.close();
  await new Promise(resolve => server.close(resolve));
}
