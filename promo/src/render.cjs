// Renders scenes.html frame by frame (deterministic seek(t)) and pipes the frames straight into ffmpeg.
//   opaque scenes            → edit/media/scene_<id>.mp4    (H.264, full picture)
//   scenes over real footage → edit/media/gfx_<id>.mov      (QuickTime Animation, with transparency)
// usage: node render.cjs [sceneId ...]      (no ids = all scenes)
const { chromium } = require('playwright');
const { spawn } = require('child_process');
const path = require('path'), fs = require('fs');
const FPS = +(process.env.FPS || 120), SCALE = +(process.env.SCALE || 2);   // 4K (1920×1080 CSS × 2) at 120 fps
const OVER_FOOTAGE = new Set(['reveal', 'demo']);           // these scenes have a hole for video underneath
const HERE = __dirname, OUT = path.join(HERE, '..', 'edit', 'media');
fs.mkdirSync(OUT, { recursive: true });

function encoder(file, alpha) {
  const args = ['-v', 'error', '-y', '-f', 'image2pipe', '-framerate', String(FPS), '-c:v', 'png', '-i', '-'];
  if (alpha) args.push('-c:v', 'qtrle', '-pix_fmt', 'argb', file);
  else args.push('-c:v', 'libx264', '-preset', 'medium', '-crf', '13', '-pix_fmt', 'yuv420p', '-movflags', '+faststart', file);
  const p = spawn('ffmpeg', args, { stdio: ['pipe', 'inherit', 'inherit'] });
  return p;
}
const write = (p, buf) => new Promise(r => p.stdin.write(buf) ? r() : p.stdin.once('drain', r));

(async () => {
  const only = process.argv.slice(2);
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: 1920, height: 1080 }, deviceScaleFactor: SCALE })).newPage();
  await page.goto('file://' + path.join(HERE, 'scenes.html'));
  await page.evaluate(() => document.fonts.ready);
  await page.evaluate(() => Promise.all([...document.images].map(i => i.decode().catch(() => {}))));
  const scenes = await page.evaluate(() => window.SCENES);
  for (const s of scenes) {
    if (only.length && !only.includes(s.id)) continue;
    const alpha = OVER_FOOTAGE.has(s.id);
    const file = path.join(OUT, (alpha ? 'gfx_' : 'scene_') + s.id + (alpha ? '.mov' : '.mp4'));
    const enc = encoder(file, alpha);
    const n = Math.round((s.t1 - s.t0) * FPS);
    const t0 = Date.now();
    for (let i = 0; i < n; i++) {
      await page.evaluate(t => window.seek(t), s.t0 + i / FPS);
      await write(enc, await page.screenshot({ type: 'png', omitBackground: alpha }));
    }
    enc.stdin.end(); await new Promise(r => enc.on('close', r));
    console.log(s.id, n, 'frames', ((Date.now() - t0) / 1000).toFixed(0) + 's', path.basename(file), (fs.statSync(file).size / 1e6).toFixed(1) + ' MB');
  }
  fs.writeFileSync(path.join(OUT, 'scenes.json'), JSON.stringify(scenes, null, 1));
  await browser.close();
})();
