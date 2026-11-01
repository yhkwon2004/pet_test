#!/usr/bin/env node
/* INFU RETRO IR 덱을 PowerPoint 파일로 내보냅니다.

   웹 덱(index.html)의 모든 장을 그대로 찍어(2560×1440) 16:9 슬라이드마다 꽉 차게 깔고, 시연 영상은 같은 자리에 진짜
   동영상 개체로 얹어 슬라이드쇼에서 저절로 재생되게 하며, 장마다 발표 노트에 대본을 넣습니다. 글자 · 그래프 · 사진이
   어느 컴퓨터의 PowerPoint에서든 웹 덱과 똑같이 보이고(서체가 없어도), 내용은 index.html 한 곳에서만 고칩니다.

     node scripts/build-pptx.cjs [덱 폴더] [출력 파일.pptx]

   필요: Node 18+ · playwright(크로미움 포함) · pptxgenjs · sharp
         (전역 설치 뒤 NODE_PATH=$(npm root -g) 로 실행하거나, 같은 저장소에 npm i playwright pptxgenjs sharp)
*/
'use strict';
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require('playwright');
const PptxGenJS = require('pptxgenjs');
const sharp = require('sharp');
const JSZip = require('jszip');

const ROOT = path.dirname(__dirname);
const DECK = path.resolve(process.argv[2] || (fs.existsSync(path.join(ROOT, 'public', 'infutech')) ? path.join(ROOT, 'public', 'infutech') : ROOT));
const OUT = path.resolve(process.argv[3] || path.join(ROOT, 'export', 'INFU-RETRO_IR_WON-SHOT.pptx'));
const W_IN = 13.333, H_IN = 7.5;      // LAYOUT_WIDE, 16:9
const BASE_W = 1920, BASE_H = 1080;   // the viewport the deck was laid out and checked in
const OUT_W = 2560, OUT_H = 1440;     // each slide's picture — crisp on a 4K projector, modest file size
const SETTLE_MS = 2000;               // the build-in animations finish well within this

const MIME = { '.html': 'text/html; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg',
  '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.webmanifest': 'application/manifest+json', '.js': 'text/javascript', '.css': 'text/css' };

// a tiny static server, so the deck loads exactly as it does online (byte ranges for the videos)
function serve(dir) {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split('?')[0]);
      if (p.endsWith('/')) p += 'index.html';
      const file = path.join(dir, path.normalize(p));
      if (!file.startsWith(dir) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
      const size = fs.statSync(file).size, type = MIME[path.extname(file)] || 'application/octet-stream';
      const m = /bytes=(\d*)-(\d*)/.exec(req.headers.range || '');
      if (m) {
        const start = m[1] ? +m[1] : 0, end = m[2] ? +m[2] : size - 1;
        res.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${start}-${end}/${size}`, 'Content-Length': end - start + 1, 'Accept-Ranges': 'bytes' });
        return fs.createReadStream(file, { start, end }).pipe(res);
      }
      res.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes' });
      fs.createReadStream(file).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

// PowerPoint plays a video by itself only when the slide's timing tree says so; pptxgenjs writes none, so add the
// standard "start automatically" tree: one playFrom(0) call per video, started with the slide, muted like the web deck
async function autoplay(file, media) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const bySlide = new Map();
  media.forEach(m => bySlide.set(m.slide, [...(bySlide.get(m.slide) || []), m]));
  for (const [n, list] of bySlide) {
    const name = `ppt/slides/slide${n}.xml`;
    let xml = await zip.file(name).async('string');
    const ids = [...xml.matchAll(/<p:cNvPr id="(\d+)" name="Media \d+"/g)].map(m => m[1]);
    if (ids.length !== list.length) throw new Error(`slide ${n}: ${ids.length} media shapes for ${list.length} videos`);
    let id = 3;
    const grp = id++, sub = id++;
    const calls = ids.map(spid =>
      `<p:par><p:cTn id="${id++}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="withEffect">` +
      `<p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr>` +
      `<p:cTn id="${id++}" dur="1" fill="hold"/><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par>`).join('');
    const nodes = ids.map((spid, i) =>
      `<p:video><p:cMediaNode vol="80000" mute="1"><p:cTn id="${id++}" fill="hold" display="0"${list[i].loop ? ' repeatCount="indefinite"' : ''}>` +
      `<p:stCondLst><p:cond delay="indefinite"/></p:stCondLst>` +
      `<p:endCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:endCondLst></p:cTn>` +
      `<p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cMediaNode></p:video>`).join('');
    const timing =
      `<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst>` +
      `<p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst>` +
      `<p:par><p:cTn id="${grp}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst>` +
      `<p:childTnLst><p:par><p:cTn id="${sub}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>${calls}</p:childTnLst></p:cTn></p:par></p:childTnLst>` +
      `</p:cTn></p:par></p:childTnLst></p:cTn>` +
      `<p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst>` +
      `<p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>` +
      `${nodes}</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>`;
    zip.file(name, xml.replace('</p:sld>', timing + '</p:sld>'));
  }
  // pptxgenjs writes a note as one run with raw line feeds; PowerPoint wants real line breaks between the lines
  for (const name of Object.keys(zip.files).filter(n => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(n))) {
    const xml = await zip.file(name).async('string');
    zip.file(name, xml.replace(/<a:t>([^<]*)<\/a:t>/g, (m, t) => m.includes('\n')
      ? '<a:t>' + t.split('\n').join('</a:t></a:r><a:br/><a:r><a:rPr lang="ko-KR" dirty="0"/><a:t>') + '</a:t>' : m));
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE', compressionOptions: { level: 6 } }));
}

(async () => {
  const html = fs.readFileSync(path.join(DECK, 'index.html'), 'utf8');
  const SECTIONS = JSON.parse(/const SECTIONS = (\[[^\]]*\])/.exec(html)[1].replace(/'/g, '"'));
  const ax = /const APPX = (\d+)/.exec(html); const APPX = ax ? +ax[1] : SECTIONS.length;   // a deck without an appendix

  const srv = await serve(DECK);
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: BASE_W, height: BASE_H }, deviceScaleFactor: OUT_W / BASE_W * 1.5 })).newPage();
  await page.goto(`http://127.0.0.1:${srv.address().port}/`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  const slides = await page.evaluate(() => [...document.querySelectorAll('.slide')].map(s => ({
    id: s.id, title: s.dataset.title, sec: +s.dataset.sec, time: s.dataset.time || '',
    note: [...s.querySelectorAll('.note p')].map(p => p.textContent.trim()).join('\n'),
  })));
  const mainCount = slides.filter(s => s.sec !== APPX).length;

  const pres = new PptxGenJS();
  pres.layout = 'LAYOUT_WIDE';
  pres.title = 'INFU RETRO — AI 자이로 센서 기반 반려동물 약물 투약 이상감지 솔루션';
  pres.subject = '2026 NEXT WAVE-UP 아이디어 리그 · 일반·기술 트랙';
  pres.author = 'WON SHOT';
  pres.company = 'WON SHOT';

  const media = [];
  let section = '', total = 0;
  for (const [k, s] of slides.entries()) {
    await page.evaluate(id => { location.hash = id; }, s.id);
    await page.waitForTimeout(SETTLE_MS);
    // the videos show their first frame (the picture underneath), the control bar stays hidden
    const videos = await page.evaluate(id => {
      document.querySelector('#chrome')?.classList.add('idle');
      return [...document.querySelectorAll(`#${CSS.escape(id)} video`)].map(v => {
        v.pause(); try { v.currentTime = 0; } catch {}
        const r = v.getBoundingClientRect();
        let { x, y, width: w, height: h } = r;
        if (getComputedStyle(v).objectFit === 'contain' && v.videoWidth) {   // the box the frames really fill
          const sc = Math.min(w / v.videoWidth, h / v.videoHeight), ww = v.videoWidth * sc, hh = v.videoHeight * sc;
          x += (w - ww) / 2; y += (h - hh) / 2; w = ww; h = hh;
        }
        return { src: v.getAttribute('src'), poster: v.getAttribute('poster'), loop: v.loop, x, y, w, h };
      });
    }, s.id);
    await page.waitForTimeout(300);
    const png = await page.screenshot({ type: 'png' });
    const jpg = await sharp(png).resize(OUT_W, OUT_H).jpeg({ quality: 92, chromaSubsampling: '4:4:4', mozjpeg: true }).toBuffer();
    total += jpg.length;

    const title = (s.sec >= 1 && s.sec < APPX - 1 ? String(s.sec).padStart(2, '0') + ' ' : '') + SECTIONS[s.sec];
    if (title !== section) { pres.addSection({ title }); section = title; }
    const slide = pres.addSlide({ sectionTitle: title });
    slide.addImage({ data: 'image/jpeg;base64,' + jpg.toString('base64'), x: 0, y: 0, w: W_IN, h: H_IN, altText: s.title });
    for (const v of videos) {
      const poster = await sharp(path.join(DECK, v.poster)).png().toBuffer();
      slide.addMedia({ type: 'video', path: path.join(DECK, v.src), cover: 'image/png;base64,' + poster.toString('base64'),
        x: v.x / BASE_W * W_IN, y: v.y / BASE_H * H_IN, w: v.w / BASE_W * W_IN, h: v.h / BASE_H * H_IN });
      media.push({ slide: k + 1, loop: v.loop });
    }
    const label = s.sec === APPX ? `부록 A${k - mainCount + 1}` : `${k + 1} / ${mainCount}`;
    slide.addNotes(`${label}${s.time ? ` · 대본 약 ${s.time}초` : ''}\n${s.note}`);
    console.log(`${String(k + 1).padStart(2)} ${s.id.padEnd(10)} ${String(Math.round(jpg.length / 1024)).padStart(5)} KB${videos.length ? ' · 영상 ' + videos.length : ''}`);
  }
  await browser.close();
  srv.close();

  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  await pres.writeFile({ fileName: OUT });
  await autoplay(OUT, media);
  console.log(`${OUT} · ${slides.length}장 · ${(fs.statSync(OUT).size / 1048576).toFixed(1)} MB (슬라이드 이미지 ${(total / 1048576).toFixed(1)} MB)`);
})().catch(e => { console.error(e); process.exit(1); });
