// Ziro-History-Studio-v3 — Channel Brand Host Mascot ("Giáo Sư Áo Hoodie Đỏ")
// Features:
// - Bold 5px ink outline (#18181C), seamless neck-to-collar anatomy, crimson hoodie (#D93829)
// - Automatic 30fps Audio Lip-Sync (mouth = 0..3 from timeline_<cluster>.json)
// - Natural 3.4s eye blinking + 5 facial moods + comic FX (sweat, angryVein, idea, question)
// - 6 Expressive Poses (idle, point_right, point_left, magnifier, shrug, drop_pointer)
import { FONT, clamp, lerp, easeOutBack, easeOutCubic, roundRect } from './helpers.js';

export function getMouthAt(mouth30fps, t, fps = 30) {
  if (!Array.isArray(mouth30fps) || mouth30fps.length === 0) return 0;
  const idx = Math.floor(Math.max(0, t) * fps);
  return idx < mouth30fps.length ? mouth30fps[idx] : 0;
}

export function drawBrandHost(ctx, x, y, scale = 1, opts = {}) {
  const {
    t = 0,
    mouth = 0,          // 0: closed, 1: slight, 2: medium D-mouth, 3: wide open
    mood = 'normal',    // 'normal' | 'skeptical' | 'shocked' | 'happy' | 'serious'
    pose = 'idle',      // 'idle' | 'point_right' | 'point_left' | 'magnifier' | 'shrug' | 'crossed' | 'drop_pointer'
    flip = 1,           // 1: default, -1: mirror horizontally
    dropElapsed = 0,    // seconds since 'drop_pointer' triggered
    sweat = false,
    angryVein = false,
    question = false,
    idea = false,
    pop = 1,
  } = opts;

  if (pop <= 0) return;

  const INK = '#18181C';
  const HOODIE = '#D93829';
  const HOODIE_DARK = '#A82418';
  const SKIN = '#FADEC8';
  const HAIR = '#2B211B';
  const PANTS = '#262932';

  // Subtle idle breathing bob
  const breathe = Math.sin(t * 2.8) * 2.2;
  const sPop = pop < 1 ? easeOutBack(pop) : 1;

  // Automatic natural blink every 3.4s (unless shocked)
  const blinkCycle = (t + 0.7) % 3.4;
  const isBlinking = mood !== 'shocked' && blinkCycle > 3.26;

  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale * sPop * flip, scale * sPop);
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';

  // Ground shadow
  ctx.fillStyle = 'rgba(0, 0, 0, 0.16)';
  ctx.beginPath();
  ctx.ellipse(0, 148, 56, 13, 0, 0, Math.PI * 2);
  ctx.fill();

  // Legs & Sneakers
  ctx.lineWidth = 5;
  ctx.strokeStyle = INK;
  ctx.fillStyle = PANTS;
  roundRect(ctx, -30, 68, 22, 72, 8);
  ctx.fill(); ctx.stroke();
  roundRect(ctx, 8, 68, 22, 72, 8);
  ctx.fill(); ctx.stroke();

  // Red-and-white sneakers
  const drawShoe = (sx, dir) => {
    ctx.beginPath();
    ctx.moveTo(sx - 12, 134);
    ctx.lineTo(sx + 16 * dir, 134);
    ctx.quadraticCurveTo(sx + 26 * dir, 136, sx + 24 * dir, 146);
    ctx.lineTo(sx - 12, 146);
    ctx.closePath();
    ctx.fillStyle = '#F8FAFC';
    ctx.fill();
    ctx.lineWidth = 4.5;
    ctx.strokeStyle = INK;
    ctx.stroke();
    ctx.fillStyle = HOODIE;
    ctx.fillRect(sx - 6, 137, 12, 5);
  };
  drawShoe(-19, -1);
  drawShoe(19, 1);

  ctx.save();
  ctx.translate(0, breathe);

  // Back Hood Collar (behind neck/shoulders)
  ctx.beginPath();
  ctx.ellipse(0, -28, 54, 24, 0, 0, Math.PI * 2);
  ctx.fillStyle = HOODIE_DARK;
  ctx.fill();
  ctx.lineWidth = 5;
  ctx.strokeStyle = INK;
  ctx.stroke();

  // Back Arm (if pointing left, draw behind or mirror)
  const drawArmAndHand = (ax, ay, ex, ey, hx, hy) => {
    ctx.strokeStyle = INK;
    ctx.lineWidth = 22;
    ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ex, ey); ctx.lineTo(hx, hy); ctx.stroke();
    ctx.strokeStyle = HOODIE;
    ctx.lineWidth = 12;
    ctx.beginPath(); ctx.moveTo(ax, ay); ctx.lineTo(ex, ey); ctx.lineTo(hx, hy); ctx.stroke();

    // Hand
    ctx.beginPath();
    ctx.arc(hx, hy, 11, 0, Math.PI * 2);
    ctx.fillStyle = SKIN;
    ctx.fill();
    ctx.lineWidth = 4.5;
    ctx.strokeStyle = INK;
    ctx.stroke();
  };

  // Left arm (viewer's left: -42, -16)
  if (pose === 'point_left') {
    drawArmAndHand(-40, -14, -78, -26, -112, -42);
    // Pointer stick extending left
    ctx.strokeStyle = INK; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(-116, -44); ctx.lineTo(-195, -76); ctx.stroke();
    ctx.beginPath(); ctx.arc(-198, -77, 8, 0, Math.PI * 2);
    ctx.fillStyle = HOODIE; ctx.fill(); ctx.lineWidth = 3.5; ctx.stroke();
  } else if (pose === 'shrug') {
    drawArmAndHand(-40, -14, -68, 8, -86, -24);
  } else if (pose === 'drop_pointer') {
    const wave = Math.sin(t * 14) * 5;
    drawArmAndHand(-40, -14, -70, -48, -82 + wave, -88);
  } else if (pose !== 'crossed') {
    drawArmAndHand(-40, -14, -54, 24, -48, 56);
  }

  // Crimson Hoodie Torso
  ctx.beginPath();
  ctx.moveTo(-42, -26);
  ctx.quadraticCurveTo(-52, 26, -46, 76);
  ctx.quadraticCurveTo(0, 84, 46, 76);
  ctx.quadraticCurveTo(52, 26, 42, -26);
  ctx.closePath();
  ctx.fillStyle = HOODIE;
  ctx.fill();
  ctx.lineWidth = 5;
  ctx.strokeStyle = INK;
  ctx.stroke();

  // Kangaroo Pocket
  ctx.beginPath();
  ctx.moveTo(-26, 42);
  ctx.lineTo(26, 42);
  ctx.lineTo(32, 70);
  ctx.lineTo(-32, 70);
  ctx.closePath();
  ctx.fillStyle = HOODIE_DARK;
  ctx.fill();
  ctx.lineWidth = 3.5;
  ctx.strokeStyle = INK;
  ctx.stroke();

  // Seamless Neck tucked deep into V-collar (0% gap!)
  roundRect(ctx, -14, -50, 28, 28, 8);
  ctx.fillStyle = SKIN;
  ctx.fill();
  ctx.lineWidth = 4.5;
  ctx.strokeStyle = INK;
  ctx.stroke();

  // White Hoodie Drawstrings
  ctx.strokeStyle = '#FFFFFF';
  ctx.lineWidth = 4;
  ctx.beginPath();
  ctx.moveTo(-12, -24); ctx.lineTo(-14, 14);
  ctx.moveTo(12, -24); ctx.lineTo(14, 10);
  ctx.stroke();

  // Right Arm (viewer's right: +40, -14) & Props
  if (pose === 'point_right') {
    const bob = Math.sin(t * 5) * 3;
    drawArmAndHand(40, -14, 78, -24, 112, -40 + bob);
    // Sleek telescopic pointer stick
    ctx.strokeStyle = INK; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(116, -42 + bob); ctx.lineTo(198, -76 + bob); ctx.stroke();
    ctx.beginPath(); ctx.arc(200, -77 + bob, 8.5, 0, Math.PI * 2);
    ctx.fillStyle = '#FACC15'; ctx.fill(); ctx.lineWidth = 3.5; ctx.stroke();
  } else if (pose === 'magnifier') {
    drawArmAndHand(40, -14, 72, -10, 88, -46);
    // Brass Magnifying Glass
    ctx.strokeStyle = '#78350F'; ctx.lineWidth = 7;
    ctx.beginPath(); ctx.moveTo(88, -46); ctx.lineTo(104, -68); ctx.stroke();
    ctx.beginPath(); ctx.arc(118, -88, 26, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(186, 230, 253, 0.55)'; ctx.fill();
    ctx.lineWidth = 6; ctx.strokeStyle = '#D97706'; ctx.stroke();
    ctx.lineWidth = 3; ctx.strokeStyle = INK; ctx.stroke();
  } else if (pose === 'shrug') {
    drawArmAndHand(40, -14, 68, 8, 86, -24);
  } else if (pose === 'crossed') {
    drawArmAndHand(-38, -12, -44, 24, 24, 20);
    drawArmAndHand(38, -12, 44, 24, -24, 24);
  } else if (pose === 'drop_pointer') {
    const wave = -Math.sin(t * 14) * 5;
    drawArmAndHand(40, -14, 70, -48, 82 + wave, -88);
    // Falling & bouncing pointer stick (Ziro's 03:57 "Drop the Spear" gag!)
    const dt = clamp(dropElapsed / 0.65);
    const py = dt < 0.7
      ? lerp(-40, 142, (dt / 0.7) * (dt / 0.7))
      : lerp(142, 126, Math.sin(((dt - 0.7) / 0.3) * Math.PI));
    const prot = lerp(-0.4, 1.48, easeOutCubic(dt));
    ctx.save();
    ctx.translate(115 + dt * 28, py - breathe);
    ctx.rotate(prot);
    ctx.strokeStyle = INK; ctx.lineWidth = 6;
    ctx.beginPath(); ctx.moveTo(-45, 0); ctx.lineTo(45, 0); ctx.stroke();
    ctx.beginPath(); ctx.arc(47, 0, 8, 0, Math.PI * 2);
    ctx.fillStyle = '#FACC15'; ctx.fill(); ctx.lineWidth = 3.5; ctx.stroke();
    ctx.restore();
  } else {
    drawArmAndHand(40, -14, 54, 24, 48, 56);
  }

  // Head (Slightly oversized charming Ziro proportion)
  ctx.beginPath();
  ctx.arc(0, -88, 48, 0, Math.PI * 2);
  ctx.fillStyle = SKIN;
  ctx.fill();
  ctx.lineWidth = 5;
  ctx.strokeStyle = INK;
  ctx.stroke();

  // Ears
  ctx.beginPath();
  ctx.arc(-48, -86, 9, Math.PI * 0.5, Math.PI * 1.5);
  ctx.fillStyle = SKIN; ctx.fill(); ctx.stroke();
  ctx.beginPath();
  ctx.arc(48, -86, 9, -Math.PI * 0.5, Math.PI * 0.5);
  ctx.fillStyle = SKIN; ctx.fill(); ctx.stroke();

  // Signature Stylized Historian Hair + Tuft
  ctx.beginPath();
  ctx.moveTo(-47, -96);
  ctx.bezierCurveTo(-52, -136, -16, -148, 12, -144);
  ctx.lineTo(8, -156);
  ctx.lineTo(26, -142);
  ctx.bezierCurveTo(50, -134, 52, -108, 46, -94);
  ctx.quadraticCurveTo(22, -118, -8, -114);
  ctx.quadraticCurveTo(-32, -112, -47, -96);
  ctx.closePath();
  ctx.fillStyle = HAIR;
  ctx.fill();
  ctx.lineWidth = 4.5;
  ctx.strokeStyle = INK;
  ctx.stroke();

  // Round Historian Glasses + Eyes
  const drawEye = (ex) => {
    // Lens frame
    ctx.beginPath();
    ctx.arc(ex, -88, 15, 0, Math.PI * 2);
    ctx.fillStyle = 'rgba(255, 255, 255, 0.55)';
    ctx.fill();
    ctx.lineWidth = 3.8;
    ctx.strokeStyle = INK;
    ctx.stroke();

    if (isBlinking) {
      ctx.beginPath();
      ctx.moveTo(ex - 9, -88);
      ctx.lineTo(ex + 9, -88);
      ctx.lineWidth = 3.8;
      ctx.stroke();
    } else if (mood === 'shocked') {
      ctx.beginPath();
      ctx.arc(ex, -88, 3.2, 0, Math.PI * 2);
      ctx.fillStyle = INK;
      ctx.fill();
    } else {
      ctx.beginPath();
      ctx.arc(ex + 1.5, -88, 5, 0, Math.PI * 2);
      ctx.fillStyle = INK;
      ctx.fill();
      ctx.beginPath();
      ctx.arc(ex - 0.5, -90, 1.8, 0, Math.PI * 2);
      ctx.fillStyle = '#FFF';
      ctx.fill();
    }
  };
  drawEye(-19);
  drawEye(19);
  // Glasses bridge
  ctx.beginPath();
  ctx.moveTo(-4, -89); ctx.lineTo(4, -89);
  ctx.lineWidth = 3.8; ctx.strokeStyle = INK; ctx.stroke();

  // Expressive Eyebrows
  ctx.lineWidth = 4.2;
  ctx.strokeStyle = INK;
  ctx.beginPath();
  if (mood === 'skeptical') {
    ctx.moveTo(-31, -108); ctx.lineTo(-10, -106);
    ctx.moveTo(9, -112); ctx.quadraticCurveTo(20, -118, 31, -110);
  } else if (mood === 'serious') {
    ctx.moveTo(-31, -112); ctx.lineTo(-9, -105);
    ctx.moveTo(31, -112); ctx.lineTo(9, -105);
  } else if (mood === 'shocked') {
    ctx.moveTo(-30, -114); ctx.quadraticCurveTo(-19, -122, -8, -114);
    ctx.moveTo(8, -114); ctx.quadraticCurveTo(19, -122, 30, -114);
  } else {
    ctx.moveTo(-29, -109); ctx.lineTo(-10, -110);
    ctx.moveTo(10, -110); ctx.lineTo(29, -109);
  }
  ctx.stroke();

  // 30fps Audio-Driven Lip-Sync Mouth (0..3)
  ctx.save();
  ctx.translate(0, -60);
  ctx.lineWidth = 3.8;
  ctx.strokeStyle = INK;
  if (mouth === 0) {
    ctx.beginPath();
    if (mood === 'shocked') {
      ctx.arc(0, 2, 5.5, 0, Math.PI * 2);
      ctx.fillStyle = '#7F1D1D'; ctx.fill(); ctx.stroke();
    } else if (mood === 'serious' || mood === 'skeptical') {
      ctx.moveTo(-9, 2); ctx.lineTo(9, 0); ctx.stroke();
    } else {
      ctx.arc(0, -3, 10, 0.2, Math.PI - 0.2);
      ctx.stroke();
    }
  } else if (mouth === 1) {
    ctx.beginPath();
    ctx.ellipse(0, 2, 9, 5.5, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#450A0A'; ctx.fill(); ctx.stroke();
  } else if (mouth === 2) {
    // Classic Ziro D-Mouth with coral tongue
    ctx.beginPath();
    ctx.moveTo(-13, -3);
    ctx.lineTo(13, -3);
    ctx.bezierCurveTo(14, 13, -14, 13, -13, -3);
    ctx.closePath();
    ctx.fillStyle = '#450A0A'; ctx.fill(); ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, 7, 7, Math.PI, 0);
    ctx.fillStyle = '#EF4444'; ctx.fill();
  } else {
    // Wide open vowel peak + teeth + tongue
    ctx.beginPath();
    ctx.ellipse(0, 4, 15, 12, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#450A0A'; ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#FFFFFF';
    ctx.fillRect(-10, -6, 20, 5);
    ctx.beginPath();
    ctx.arc(0, 11, 8.5, Math.PI, 0);
    ctx.fillStyle = '#EF4444'; ctx.fill();
    ctx.beginPath();
    ctx.ellipse(0, 4, 15, 12, 0, 0, Math.PI * 2);
    ctx.stroke();
  }
  ctx.restore();

  // Optional Ziro Comic Particles (Sweat drop, Angry Vein, Question marks, Idea Bulb)
  if (sweat) {
    const sy = -102 + ((t * 24) % 14);
    ctx.beginPath();
    ctx.moveTo(38, sy - 10);
    ctx.quadraticCurveTo(46, sy + 2, 38, sy + 8);
    ctx.quadraticCurveTo(30, sy + 2, 38, sy - 10);
    ctx.fillStyle = '#38BDF8'; ctx.fill();
    ctx.lineWidth = 2.5; ctx.strokeStyle = INK; ctx.stroke();
  }

  if (angryVein) {
    ctx.save();
    ctx.translate(32, -122);
    const sc = 1 + Math.sin(t * 12) * 0.12;
    ctx.scale(sc, sc);
    ctx.strokeStyle = '#EF4444';
    ctx.lineWidth = 4;
    ctx.beginPath();
    ctx.moveTo(-8, -2); ctx.quadraticCurveTo(-2, -2, -2, -8);
    ctx.moveTo(8, -2); ctx.quadraticCurveTo(2, -2, 2, -8);
    ctx.moveTo(-8, 2); ctx.quadraticCurveTo(-2, 2, -2, 8);
    ctx.moveTo(8, 2); ctx.quadraticCurveTo(2, 2, 2, 8);
    ctx.stroke();
    ctx.restore();
  }

  if (question) {
    ctx.save();
    ctx.scale(flip, 1); // keep text unflipped!
    ctx.fillStyle = '#DC2626';
    ctx.font = `900 42px ${FONT}`;
    ctx.textAlign = 'center';
    ctx.fillText('?', 56 * flip, -132 + Math.sin(t * 7) * 5);
    ctx.restore();
  }

  if (idea) {
    ctx.save();
    ctx.translate(0, -172 + Math.sin(t * 6) * 4);
    ctx.beginPath(); ctx.arc(0, 0, 18, 0, Math.PI * 2);
    ctx.fillStyle = '#FDE047'; ctx.fill();
    ctx.lineWidth = 3.5; ctx.strokeStyle = INK; ctx.stroke();
    ctx.fillStyle = '#94A3B8'; ctx.fillRect(-7, 16, 14, 8); ctx.strokeRect(-7, 16, 14, 8);
    ctx.restore();
  }

  ctx.restore();
  ctx.restore();
}
