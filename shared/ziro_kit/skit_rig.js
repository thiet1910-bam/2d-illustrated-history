// Ziro-History-Studio-v3 — Universal Two-Actor Sitcom Skit Engine & Global Costume Rig
// Features:
// 1. Full-screen illustrated 2D stage (NO top HUD, NO bottom subtitle, NO foot labels!)
// 2. Turn-Taking Lip-Sync Lock: ONLY the currently speaking actor moves their mouth (0..3)
// 3. Overhead Speech Captions: Active speaker's line types above their head at 100% opacity;
//    when the partner replies, the previous line stays visible dimmed to 38% (0.38)!
// 4. Universal Multi-Era / Multi-Country Archetypes:
//    - 'president_suit'   (US/Western President, Diplomat, Wall Street Banker, Politician)
//    - 'general_military' (North Korean / Soviet / US Military General with Officer Cap & Medals)
//    - 'soldier_helmet'   (Modern / Cold War Infantry Soldier with Steel Helmet)
//    - 'supreme_leader'   (Authoritarian State Tunic + Swept Hair / Glasses)
//    - 'scientist_coat'   (Nuclear / Tech / Economist Expert in White Lab Coat)
//    - 'king_ancient'     (Universal Ancient Emperor / Monarch with Crown & Royal Robe)
//    - 'warrior_ancient'  (Universal Ancient Scout / Soldier with Tunic & Cap/Helmet)
//    - 'citizen_modern'   (Everyday Citizen / Voter / Worker in Casual Jacket)
import { FONT, clamp, easeOutBack, roundRect } from './helpers.js';

export function drawOverheadCaptions(ctx, turns, t) {
  for (const turn of turns) {
    if (t < turn.t0 || (turn.hideAt && t >= turn.hideAt)) continue;

    const isDimmed = turn.dimAt !== undefined && t >= turn.dimAt;
    const alpha = isDimmed ? 0.38 : 1.0;

    const lines = turn.text.split('\n');
    const totalChars = turn.text.length;
    const typeDur = Math.min(1.1, Math.max(0.25, totalChars * 0.024));
    const shownChars = isDimmed
      ? totalChars
      : Math.max(1, Math.round(totalChars * clamp((t - turn.t0) / typeDur)));

    ctx.save();
    ctx.globalAlpha = alpha;

    const lineH = 38;
    const baseSize = turn.size || 30;
    let maxW = 0;
    ctx.font = `800 ${baseSize}px ${FONT}`;
    for (const ln of lines) maxW = Math.max(maxW, ctx.measureText(ln).width);

    if (turn.backdrop !== false) {
      roundRect(
        ctx,
        turn.x - maxW / 2 - 22,
        turn.y - (lines.length * lineH) / 2 - 12,
        maxW + 44,
        lines.length * lineH + 24,
        14
      );
      ctx.fillStyle = turn.darkStage ? 'rgba(15, 20, 30, 0.78)' : 'rgba(252, 250, 245, 0.88)';
      ctx.fill();
    }

    let rem = shownChars;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    const startY = turn.y - ((lines.length - 1) * lineH) / 2;

    for (let i = 0; i < lines.length; i++) {
      if (rem <= 0) break;
      const sub = lines[i].slice(0, rem);
      rem -= lines[i].length + 1;
      const ly = startY + i * lineH;

      ctx.lineJoin = 'round';
      ctx.lineWidth = 5;
      ctx.strokeStyle = turn.darkStage ? '#090D16' : '#FFFFFF';
      ctx.strokeText(sub, turn.x, ly);
      ctx.fillStyle = turn.color || (turn.darkStage ? '#F8FAFC' : '#18181C');
      ctx.fillText(sub, turn.x, ly);
    }

    const tickTop = turn.y + (lines.length * lineH) / 2 + 16;
    ctx.strokeStyle = turn.darkStage ? '#FACC15' : '#18181C';
    ctx.lineWidth = 3.5;
    ctx.lineCap = 'round';
    ctx.beginPath();
    ctx.moveTo(turn.x, tickTop);
    ctx.lineTo(turn.x + (turn.tickDX || 0), tickTop + 16);
    ctx.stroke();

    ctx.restore();
  }
}

/**
 * Standalone 30fps Ziro Mouth Drawer — attachable to ANY custom character in 1 line!
 */
export function drawActorMouth(ctx, mx, my, mState = 0, mood = 'normal') {
  const INK = '#18181C';
  ctx.save();
  ctx.translate(mx, my);
  ctx.lineWidth = 3.6;
  ctx.strokeStyle = INK;
  if (mState === 0) {
    ctx.beginPath();
    if (mood === 'proud') ctx.arc(0, -3, 10, 0.15, Math.PI - 0.15);
    else if (mood === 'shocked') {
      ctx.arc(0, 2, 6, 0, Math.PI * 2);
      ctx.fillStyle = '#450A0A';
      ctx.fill();
    } else {
      ctx.moveTo(-9, 1);
      ctx.lineTo(9, 0);
    }
    ctx.stroke();
  } else if (mState === 1) {
    ctx.beginPath();
    ctx.ellipse(0, 2, 9, 5, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#450A0A';
    ctx.fill();
    ctx.stroke();
  } else if (mState === 2) {
    ctx.beginPath();
    ctx.moveTo(-12, -2);
    ctx.lineTo(12, -2);
    ctx.bezierCurveTo(13, 12, -13, 12, -12, -2);
    ctx.fillStyle = '#450A0A';
    ctx.fill();
    ctx.stroke();
    ctx.beginPath();
    ctx.arc(0, 7, 6.5, Math.PI, 0);
    ctx.fillStyle = '#EF4444';
    ctx.fill();
  } else {
    ctx.beginPath();
    ctx.ellipse(0, 4, 14, 11, 0, 0, Math.PI * 2);
    ctx.fillStyle = '#450A0A';
    ctx.fill();
    ctx.stroke();
    ctx.fillStyle = '#FFF';
    ctx.fillRect(-9, -5, 18, 4);
    ctx.beginPath();
    ctx.arc(0, 10, 8, Math.PI, 0);
    ctx.fillStyle = '#EF4444';
    ctx.fill();
    ctx.beginPath();
    ctx.ellipse(0, 4, 14, 11, 0, 0, Math.PI * 2);
    ctx.stroke();
  }
  ctx.restore();
}

export function drawSkitActor(ctx, x, y, scale = 1, opts = {}) {
  const {
    role = 'president_suit',
    t = 0,
    mouth = 0,              // 0..3 (ONLY > 0 when this character is speaking!)
    mood = 'normal',        // 'normal' | 'shocked' | 'skeptical' | 'proud' | 'sweat'
    gesture = 'idle',       // 'idle' | 'point' | 'scroll' | 'salute' | 'hand_chin'
    primaryColor = '',      // Optional custom coat/suit/armor color override
    accentColor = '',       // Optional tie/trim/cap color override
    skinColor = '#F5D5B8',  // Customizable skin tone (or '#FFFFFF' for pure Ziro white head)
    glasses = false,
    flip = 1,
    pop = 1,
  } = opts;

  if (pop <= 0) return;
  const INK = '#18181C';
  const sPop = pop < 1 ? easeOutBack(pop) : 1;
  const breathe = Math.sin(t * 2.6 + x * 0.01) * 2;
  const isBlinking = mood !== 'shocked' && ((t + x * 0.003) % 3.6) > 3.46;

  ctx.save();
  ctx.translate(x, y);
  ctx.scale(scale * sPop * flip, scale * sPop);
  ctx.lineJoin = 'round';
  ctx.lineCap = 'round';

  // Ground shadow
  ctx.fillStyle = 'rgba(0,0,0,0.2)';
  ctx.beginPath();
  ctx.ellipse(0, 148, 56, 13, 0, 0, Math.PI * 2);
  ctx.fill();

  ctx.save();
  ctx.translate(0, breathe);

  // Determine archetype family
  const coatMap = {
    president_suit: primaryColor || '#1E293B',
    diplomat: primaryColor || '#1E3A8A',
    general_military: primaryColor || '#3F4E3A',
    soldier_helmet: primaryColor || '#4B553A',
    supreme_leader: primaryColor || '#27272A',
    scientist_coat: primaryColor || '#F8FAFC',
    king_ancient: primaryColor || '#581C87',
    warrior_ancient: primaryColor || '#0F766E',
    citizen_modern: primaryColor || '#2563EB',
  };
  const bodyCol = coatMap[role] || primaryColor || '#334155';
  const trimCol = accentColor || (role === 'president_suit' ? '#DC2626' : '#FACC15');

  // Optional Royal Cape for Ancient Monarchs
  if (role === 'king_ancient') {
    ctx.beginPath();
    ctx.moveTo(-46, -24); ctx.lineTo(-68, 138); ctx.lineTo(64, 138); ctx.lineTo(46, -24);
    ctx.closePath();
    ctx.fillStyle = '#7F1D1D'; ctx.fill();
    ctx.lineWidth = 5; ctx.strokeStyle = INK; ctx.stroke();
  }

  // Legs
  ctx.fillStyle = role === 'scientist_coat' ? '#334155' : '#1E2028';
  ctx.lineWidth = 5;
  ctx.strokeStyle = INK;
  roundRect(ctx, -28, 74, 21, 66, 8); ctx.fill(); ctx.stroke();
  roundRect(ctx, 7, 74, 21, 66, 8); ctx.fill(); ctx.stroke();

  // Left resting arm
  ctx.strokeStyle = INK; ctx.lineWidth = 20;
  ctx.beginPath(); ctx.moveTo(-38, -12); ctx.lineTo(-52, 42); ctx.stroke();
  ctx.strokeStyle = bodyCol; ctx.lineWidth = 12; ctx.stroke();

  // Torso / Jacket / Tunic
  roundRect(ctx, -42, -26, 84, 108, 14);
  ctx.fillStyle = bodyCol;
  ctx.lineWidth = 5;
  ctx.strokeStyle = INK;
  ctx.fill();
  ctx.stroke();

  // Costume-specific torso details
  if (role === 'president_suit' || role === 'diplomat') {
    // White shirt V-neck + Tie + Flag lapel pin
    ctx.beginPath();
    ctx.moveTo(-18, -26); ctx.lineTo(0, 26); ctx.lineTo(18, -26); ctx.closePath();
    ctx.fillStyle = '#FFFFFF'; ctx.fill(); ctx.lineWidth = 3.5; ctx.stroke();
    ctx.beginPath();
    ctx.moveTo(-5, -24); ctx.lineTo(5, -24); ctx.lineTo(8, 22); ctx.lineTo(0, 34); ctx.lineTo(-8, 22); ctx.closePath();
    ctx.fillStyle = trimCol; ctx.fill(); ctx.lineWidth = 2.5; ctx.stroke();
    ctx.fillStyle = '#FACC15'; ctx.fillRect(18, -8, 12, 8);
  } else if (role === 'general_military') {
    // Gold epaulets + Brass buttons + Medal ribbons
    ctx.fillStyle = '#FACC15';
    roundRect(ctx, -46, -28, 22, 10, 4); ctx.fill(); ctx.stroke();
    roundRect(ctx, 24, -28, 22, 10, 4); ctx.fill(); ctx.stroke();
    for (let b = 0; b < 4; b++) {
      ctx.beginPath(); ctx.arc(0, -8 + b * 22, 4.5, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
    }
    ctx.fillStyle = '#EF4444'; ctx.fillRect(12, -6, 20, 8);
    ctx.fillStyle = '#38BDF8'; ctx.fillRect(12, 4, 20, 8);
  } else if (role === 'supreme_leader') {
    // High buttoned collar + Center button seam + Red lapel badge
    ctx.strokeStyle = INK; ctx.lineWidth = 3;
    ctx.beginPath(); ctx.moveTo(0, -26); ctx.lineTo(0, 80); ctx.stroke();
    for (let b = 0; b < 4; b++) {
      ctx.beginPath(); ctx.arc(0, -8 + b * 22, 3.5, 0, Math.PI * 2);
      ctx.fillStyle = '#52525B'; ctx.fill(); ctx.stroke();
    }
    ctx.fillStyle = '#DC2626'; ctx.fillRect(12, -8, 14, 9);
  } else if (role === 'scientist_coat') {
    // Inner blue shirt + Tie + Pocket pens
    ctx.fillStyle = '#DBEAFE'; ctx.fillRect(-12, -26, 24, 96); ctx.strokeRect(-12, -26, 24, 96);
    ctx.fillStyle = '#1D4ED8'; ctx.fillRect(-4, -24, 8, 48);
    ctx.strokeRect(16, 4, 18, 22);
  } else if (role === 'king_ancient') {
    ctx.fillStyle = '#FACC15';
    ctx.fillRect(-10, -24, 20, 104); ctx.strokeRect(-10, -24, 20, 104);
  } else if (role === 'soldier_helmet' || role === 'warrior_ancient') {
    ctx.fillStyle = '#92400E';
    ctx.fillRect(-42, 34, 84, 16); ctx.strokeRect(-42, 34, 84, 16);
  }

  // Right Gesture Arm
  ctx.strokeStyle = INK; ctx.lineWidth = 20;
  ctx.beginPath();
  if (gesture === 'point') { ctx.moveTo(38, -10); ctx.lineTo(80, -26); ctx.lineTo(114, -36); }
  else if (gesture === 'salute') { ctx.moveTo(38, -10); ctx.lineTo(68, -42); ctx.lineTo(44, -92); }
  else if (gesture === 'scroll') { ctx.moveTo(38, -10); ctx.lineTo(66, 8); ctx.lineTo(86, -12); }
  else if (gesture === 'hand_chin') { ctx.moveTo(38, -10); ctx.lineTo(60, 12); ctx.lineTo(24, -44); }
  else { ctx.moveTo(38, -10); ctx.lineTo(54, 34); ctx.lineTo(48, 62); }
  ctx.stroke();
  ctx.strokeStyle = bodyCol; ctx.lineWidth = 12; ctx.stroke();

  if (gesture === 'scroll') {
    roundRect(ctx, 74, -44, 34, 52, 6);
    ctx.fillStyle = '#FEF3C7'; ctx.fill(); ctx.lineWidth = 3.5; ctx.strokeStyle = INK; ctx.stroke();
  }

  // Seamless Neck + Round Head
  roundRect(ctx, -13, -48, 26, 26, 8);
  ctx.fillStyle = skinColor; ctx.lineWidth = 4.5; ctx.strokeStyle = INK; ctx.fill(); ctx.stroke();
  ctx.beginPath(); ctx.arc(0, -86, 45, 0, Math.PI * 2);
  ctx.fillStyle = skinColor; ctx.lineWidth = 5; ctx.fill(); ctx.stroke();

  // Headgear / Hair per Archetype
  if (role === 'general_military') {
    // Officer Peaked Visor Cap with Red Band & Gold Star
    ctx.beginPath();
    ctx.moveTo(-46, -110); ctx.lineTo(-56, -142); ctx.quadraticCurveTo(0, -162, 56, -142); ctx.lineTo(46, -110);
    ctx.closePath();
    ctx.fillStyle = bodyCol; ctx.fill(); ctx.stroke();
    ctx.fillStyle = '#DC2626'; ctx.fillRect(-46, -118, 92, 12); ctx.strokeRect(-46, -118, 92, 12);
    ctx.fillStyle = '#18181C'; ctx.fillRect(-44, -106, 88, 7);
    ctx.fillStyle = '#FACC15'; ctx.beginPath(); ctx.arc(0, -132, 7, 0, Math.PI * 2); ctx.fill(); ctx.stroke();
  } else if (role === 'soldier_helmet') {
    // Curved Steel Combat Helmet
    ctx.beginPath();
    ctx.arc(0, -96, 49, Math.PI * 1.03, -Math.PI * 0.03);
    ctx.closePath();
    ctx.fillStyle = '#3F4E3A'; ctx.fill(); ctx.lineWidth = 5; ctx.stroke();
  } else if (role === 'king_ancient') {
    // Gold Royal Crown
    ctx.beginPath();
    ctx.moveTo(-44, -116); ctx.lineTo(-48, -158); ctx.lineTo(-24, -144); ctx.lineTo(0, -164);
    ctx.lineTo(24, -144); ctx.lineTo(48, -158); ctx.lineTo(44, -116); ctx.closePath();
    ctx.fillStyle = '#FACC15'; ctx.fill(); ctx.lineWidth = 5; ctx.stroke();
  } else if (role === 'supreme_leader') {
    // Tall squared side-shaved haircut
    roundRect(ctx, -40, -138, 80, 32, 10);
    ctx.fillStyle = '#18181C'; ctx.fill();
  } else {
    // Clean parted hair
    ctx.beginPath();
    ctx.arc(0, -96, 45, Math.PI * 1.08, -Math.PI * 0.08);
    ctx.fillStyle = role === 'scientist_coat' ? '#94A3B8' : '#29221E';
    ctx.fill(); ctx.lineWidth = 4.5; ctx.stroke();
  }

  // Eyes & Optional Glasses
  for (const ex of [-15, 15]) {
    if (glasses || role === 'scientist_coat') {
      ctx.beginPath(); ctx.arc(ex, -88, 12, 0, Math.PI * 2);
      ctx.fillStyle = 'rgba(255,255,255,0.65)'; ctx.fill();
      ctx.lineWidth = 3.5; ctx.strokeStyle = INK; ctx.stroke();
    }
    if (isBlinking) {
      ctx.beginPath(); ctx.moveTo(ex - 7, -88); ctx.lineTo(ex + 7, -88); ctx.lineWidth = 4; ctx.stroke();
    } else {
      ctx.beginPath(); ctx.arc(ex, -88, 5, 0, Math.PI * 2); ctx.fillStyle = INK; ctx.fill();
    }
  }
  if (glasses || role === 'scientist_coat') {
    ctx.beginPath(); ctx.moveTo(-3, -88); ctx.lineTo(3, -88); ctx.lineWidth = 3.5; ctx.stroke();
  }

  // Expressive Brows
  ctx.lineWidth = 4.2;
  ctx.beginPath();
  if (mood === 'skeptical') {
    ctx.moveTo(-27, -104); ctx.lineTo(-8, -102);
    ctx.moveTo(8, -110); ctx.lineTo(27, -104);
  } else if (mood === 'shocked') {
    ctx.moveTo(-27, -112); ctx.lineTo(-8, -116);
    ctx.moveTo(8, -116); ctx.lineTo(27, -112);
  } else {
    ctx.moveTo(-27, -105); ctx.lineTo(-8, -103);
    ctx.moveTo(8, -103); ctx.lineTo(27, -105);
  }
  ctx.stroke();

  // 30fps Lip-Sync Mouth
  drawActorMouth(ctx, 0, -61, mouth, mood);

  // Nervous Sweat Drop
  if (mood === 'sweat') {
    const sy = -96 + ((t * 24) % 14);
    ctx.beginPath();
    ctx.moveTo(-36, sy - 8);
    ctx.quadraticCurveTo(-44, sy + 2, -36, sy + 8);
    ctx.quadraticCurveTo(-28, sy + 2, -36, sy - 8);
    ctx.fillStyle = '#38BDF8'; ctx.fill(); ctx.lineWidth = 2.5; ctx.stroke();
  }

  ctx.restore();
  ctx.restore();
}
