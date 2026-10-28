// Template: Two-Actor Sitcom Skit Cluster (SKIT_CHAM_BIEM) — Authentic Ziro Style
// Full-screen 2D illustrated stage + Turn-Taking Lip-Sync + 38% Dimmed Overhead Captions!
import { lerp, loadImg, withCamera, drawImageCover } from '../../../shared/ziro_kit/helpers.js';
import { drawSkitActor, drawOverheadCaptions } from '../../../shared/ziro_kit/skit_rig.js';

let imgs = {};

export async function init() {
  const [stageBg] = await Promise.all([
    loadImg('/assets/backgrounds/skit1_stage.jpg'),
  ]);
  imgs = { stageBg };
}

export function draw(ctx, t, { W, H, mouth }) {
  // Actor A speaks on [0..4.5s), Actor B replies on [4.5..8.5s)
  const aSpeaking = t < 4.5;
  const bSpeaking = t >= 4.5;

  withCamera(ctx, W, H, { zoom: lerp(1.0, 1.04, t / 8.5), t }, () => {
    drawImageCover(ctx, imgs.stageBg, 0, 0, W, H);

    // Left Actor: Military General (ONLY moves mouth while aSpeaking!)
    drawSkitActor(ctx, 520, 740, 1.38, {
      role: 'general_military',
      t,
      mouth: aSpeaking ? mouth : 0,
      mood: bSpeaking ? 'sweat' : 'normal',
      gesture: aSpeaking ? 'salute' : 'idle',
    });

    // Right Actor: President / Diplomat (ONLY moves mouth while bSpeaking!)
    drawSkitActor(ctx, 1380, 740, 1.38, {
      role: 'president_suit',
      flip: -1,
      t,
      mouth: bSpeaking ? mouth : 0,
      mood: bSpeaking ? 'skeptical' : 'normal',
      gesture: bSpeaking ? 'point' : 'hand_chin',
    });

    // Overhead Captions: Line 1 dims automatically to 38% when Actor B replies at t=4.5s!
    drawOverheadCaptions(ctx, [
      {
        t0: 0.15, dimAt: 4.50,
        x: 520, y: 330,
        text: 'Thưa Ngài, kế hoạch này chắc chắn\nthành công 100% trên giấy tờ!',
      },
      {
        t0: 4.55,
        x: 1380, y: 330,
        text: 'Trên giấy tờ thôi hả?\nCòn ngoài thực địa thì sao?!',
      },
    ], t);
  });
}
