#!/usr/bin/env node
/* INFU RETRO IR 덱을 "편집할 수 있는" PowerPoint 파일로 내보냅니다.

   장마다
     ① 배경층: 글자 · 사진 · 그림(SVG)을 숨긴 채 찍은 화면(그라데이션 · 카드 · 막대 · 원형 도형)을 배경 그림으로,
     ② 사진: <img>를 같은 자리 · 같은 크기의 그림 개체로(원형은 원형 자르기),
     ③ 그림(SVG): 글자를 뺀 채 투명 배경 PNG로,
     ④ 글자: 화면에 보이는 모든 글자(SVG 그림 안 글자 포함)를 PowerPoint 텍스트 상자로 — 서체 · 크기 · 굵기 · 색 · 자간 그대로,
     ⑤ 시연 영상: 진짜 동영상 개체(자동 재생), 발표 노트: 대본
   으로 올립니다. 글자는 PowerPoint에서 바로 고칠 수 있습니다(서체: Pretendard — 없으면 PowerPoint가 비슷한 서체로 바꿉니다).

     NODE_PATH=... node scripts/build-pptx-editable.cjs [덱 폴더] [출력.pptx]
   필요: playwright(크로미움) · pptxgenjs · sharp · jszip
*/
'use strict';
const fs = require('fs'), path = require('path'), http = require('http');
const { chromium } = require('playwright');
const PptxGenJS = require('pptxgenjs');
const sharp = require('sharp');
const JSZip = require('jszip');

const ROOT = path.dirname(__dirname);
const DECK = path.resolve(process.argv[2] || ROOT);
const OUT = path.resolve(process.argv[3] || path.join(ROOT, 'export', 'INFU-RETRO_IR_WON-SHOT_editable.pptx'));
const W_IN = 13.333, H_IN = 7.5, BW = 1920, BH = 1080;
const PX = W_IN / BW;               // inch per css px
const PT = 72 * PX;                 // pt per css px (= 0.5)
const SCALE = 2;                    // background / svg raster scale
const FONT = 'Pretendard';

const MIME = { '.html': 'text/html; charset=utf-8', '.webp': 'image/webp', '.png': 'image/png', '.jpg': 'image/jpeg', '.gif': 'image/gif',
  '.svg': 'image/svg+xml', '.mp4': 'video/mp4', '.webmanifest': 'application/manifest+json' };
function serve(dir) {
  return new Promise(resolve => {
    const srv = http.createServer((req, res) => {
      let p = decodeURIComponent(req.url.split('?')[0]); if (p.endsWith('/')) p += 'index.html';
      const file = path.join(dir, path.normalize(p));
      if (!file.startsWith(dir) || !fs.existsSync(file) || fs.statSync(file).isDirectory()) { res.writeHead(404); return res.end(); }
      const size = fs.statSync(file).size, type = MIME[path.extname(file)] || 'application/octet-stream';
      const m = /bytes=(\d*)-(\d*)/.exec(req.headers.range || '');
      if (m) { const s = m[1] ? +m[1] : 0, e = m[2] ? +m[2] : size - 1;
        res.writeHead(206, { 'Content-Type': type, 'Content-Range': `bytes ${s}-${e}/${size}`, 'Content-Length': e - s + 1, 'Accept-Ranges': 'bytes' });
        return fs.createReadStream(file, { start: s, end: e }).pipe(res); }
      res.writeHead(200, { 'Content-Type': type, 'Content-Length': size, 'Accept-Ranges': 'bytes' }); fs.createReadStream(file).pipe(res);
    });
    srv.listen(0, '127.0.0.1', () => resolve(srv));
  });
}

// ---- in-page extraction (runs in the browser) ----
function extract(id) {
  const sec = document.getElementById(id), frame = sec.querySelector('.frame');
  const fr = frame.getBoundingClientRect();
  const hex = c => { const m = c.match(/rgba?\(([^)]+)\)/); if (!m) return null; const p = m[1].split(/[ ,/]+/).filter(Boolean).map(Number);
    return { hex: p.slice(0, 3).map(v => Math.round(v).toString(16).padStart(2, '0')).join('').toUpperCase(), a: p.length > 3 ? p[3] : 1 }; };
  const visible = el => { for (let e = el; e && e !== sec; e = e.parentElement) { const cs = getComputedStyle(e);
    if (cs.display === 'none' || cs.visibility === 'hidden' || +cs.opacity === 0) return false; } return true; };
  const opac = el => { let o = 1; for (let e = el; e && e !== sec; e = e.parentElement) o *= +getComputedStyle(e).opacity; return o; };
  const isInline = el => { const d = getComputedStyle(el).display; return d === 'inline' || d === 'contents'; };
  const out = { texts: [], imgs: [], svgs: [], videos: [], chips: [] };
  const isRound = (el, w, h) => { const br = getComputedStyle(el).borderTopLeftRadius; if (!br) return false;
    const v = parseFloat(br); if (br.includes('%')) return v >= 49; return v >= Math.min(w, h) / 2 - 1 && Math.abs(w - h) < 2; };

  // ① text containers: non-inline elements with their own (non-whitespace) text, gathering inline descendants
  const all = [...sec.querySelectorAll('.frame *')].filter(el => !el.closest('.note') && !el.closest('svg') && !['SCRIPT', 'STYLE', 'VIDEO', 'IMG'].includes(el.tagName));
  for (const el of all) {
    if (isInline(el)) continue;
    const own = [...el.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()) ||
      [...el.children].some(c => isInline(c) && c.textContent.trim());
    if (!own || !visible(el)) continue;
    const runs = [], rects = [];
    const walk = (node, inh) => {
      for (const n of node.childNodes) {
        if (n.nodeType === 3) {
          const t = n.textContent.replace(/\s+/g, ' ');
          if (!t.trim() && !t) continue;
          const pe = n.parentElement, cs = getComputedStyle(pe);
          const r = document.createRange(); r.selectNodeContents(n); for (const q of r.getClientRects()) if (q.width > 0) rects.push(q);
          const c = hex(cs.color);
          runs.push({ text: t, size: parseFloat(cs.fontSize), weight: +cs.fontWeight, color: c ? c.hex : '000000', alpha: (c ? c.a : 1) * opac(pe),
            italic: cs.fontStyle === 'italic', ls: parseFloat(cs.letterSpacing) || 0, sub: pe.tagName === 'SUB', sup: pe.tagName === 'SUP',
            family: cs.fontFamily });
        } else if (n.nodeType === 1) {
          if (n.tagName === 'BR') { runs.push({ br: true }); continue; }
          if (n.tagName === 'SVG' || n.tagName === 'IMG' || n.tagName === 'svg') continue;
          if (!isInline(n)) {                   // its own container — or an empty inline-block (legend swatch): keep its width as spaces
            const ncs = getComputedStyle(n);
            if (ncs.display === 'inline-block' && !n.textContent.trim() && n.offsetWidth > 0) {
              const fs = parseFloat(getComputedStyle(node).fontSize), wd = n.offsetWidth + parseFloat(ncs.marginLeft) + parseFloat(ncs.marginRight);
              const pcs = getComputedStyle(n.parentElement), c = hex(pcs.color);
              runs.push({ text: '\u00A0'.repeat(Math.max(1, Math.round(wd / (fs * .26)))), size: fs, weight: 400, color: c ? c.hex : '000000', alpha: 1, ls: 0 });
            }
            continue;
          }
          if (!visible(n)) continue;
          walk(n);
        }
      }
    };
    walk(el);
    // trim leading/trailing whitespace runs
    while (runs.length && !runs[0].br && !runs[0].text.trim()) runs.shift();
    while (runs.length && !runs[runs.length - 1].br && !runs[runs.length - 1].text.trim()) runs.pop();
    if (!runs.length || !rects.length) continue;
    if (runs[0].text) runs[0].text = runs[0].text.replace(/^\s+/, '');
    const last = runs[runs.length - 1]; if (last.text) last.text = last.text.replace(/\s+$/, '');
    const x1 = Math.min(...rects.map(r => r.left)), y1 = Math.min(...rects.map(r => r.top)), x2 = Math.max(...rects.map(r => r.right)), y2 = Math.max(...rects.map(r => r.bottom));
    const cs = getComputedStyle(el);
    const lines = new Set(rects.map(r => Math.round(r.top / 4))).size;
    let align = cs.textAlign; if (align === 'start') align = 'left'; if (align === 'end') align = 'right'; if (align === 'justify') align = 'left';
    // flex/grid containers center their text by alignment, not text-align
    if (/flex|grid/.test(cs.display) && (cs.justifyContent === 'center' || cs.alignItems === 'center') && align === 'left' && lines === 1) {
      const er = el.getBoundingClientRect(); if (Math.abs((x1 + x2) / 2 - (er.left + er.right) / 2) < 3) align = 'center'; }
    out.texts.push({ x: x1 - fr.left, y: y1 - fr.top, w: x2 - x1, h: y2 - y1, align, lines, lh: parseFloat(cs.lineHeight) || parseFloat(cs.fontSize) * 1.3, runs });
  }

  // ② svg <text>
  for (const t of sec.querySelectorAll('.frame svg text')) {
    if (!visible(t.ownerSVGElement)) continue;
    const r = t.getBoundingClientRect(); if (!r.width) continue;
    const cs = getComputedStyle(t), c = hex(cs.fill) || { hex: '1D1C2B', a: 1 };
    const svgr = t.ownerSVGElement.getBoundingClientRect(), vb = t.ownerSVGElement.viewBox.baseVal;
    const sc = vb && vb.width ? svgr.width / vb.width : 1;
    const anchor = t.getAttribute('text-anchor') || cs.textAnchor;
    out.texts.push({ x: r.left - fr.left, y: r.top - fr.top, w: r.width, h: r.height, align: anchor === 'middle' ? 'center' : anchor === 'end' ? 'right' : 'left', lines: 1,
      lh: r.height, runs: [{ text: t.textContent, size: parseFloat(cs.fontSize) * sc, weight: +cs.fontWeight || 400, color: c.hex, alpha: (+cs.fillOpacity || 1) * c.a * opac(t.ownerSVGElement), ls: 0 }] });
  }

  // ③ images
  for (const im of sec.querySelectorAll('.frame img')) {
    if (!visible(im)) continue;
    const cs = getComputedStyle(im);
    if (cs.maskImage && cs.maskImage !== 'none' || cs.webkitMaskImage && cs.webkitMaskImage !== 'none') continue; // stays in the background layer
    const r = im.getBoundingClientRect(); if (r.width < 2) continue;
    // clip to the nearest overflow-hidden ancestor (cropped photos inside rounded frames)
    let clip = null, clipEl = null;
    for (let e = im.parentElement; e && e !== sec; e = e.parentElement) { if (getComputedStyle(e).overflow === 'hidden') { clip = e.getBoundingClientRect(); clipEl = e; break; } }
    const tr = cs.transform; let rot = 0; if (tr && tr !== 'none') { const m = tr.match(/matrix\(([^)]+)\)/); if (m) { const v = m[1].split(',').map(Number); rot = Math.round(Math.atan2(v[1], v[0]) * 180 / Math.PI); } }
    const w = rot ? im.offsetWidth : r.width, h = rot ? im.offsetHeight : r.height, cx = r.left + r.width / 2, cy = r.top + r.height / 2;
    out.imgs.push({ src: im.getAttribute('src'), x: cx - w / 2 - fr.left, y: cy - h / 2 - fr.top, w, h, rot, fit: cs.objectFit, pos: cs.objectPosition,
      nw: im.naturalWidth, nh: im.naturalHeight, round: isRound(im, w, h) || (clip && Math.abs(clip.width - clip.height) < 2 && isRound(clipEl, clip.width, clip.height)),
      clip: clip && !rot ? { x: clip.left - fr.left, y: clip.top - fr.top, w: clip.width, h: clip.height } : null, alpha: opac(im) });
  }
  // ④ svgs (charts, icons, diagrams)
  [...sec.querySelectorAll('.frame svg')].forEach((s, i) => {
    if (s.parentElement.closest('svg') || !visible(s)) return;
    const r = s.getBoundingClientRect(); if (r.width < 4) return;
    s.setAttribute('data-px', i);
    out.svgs.push({ i, x: r.left - fr.left, y: r.top - fr.top, w: r.width, h: r.height });
  });
  // ⑤ videos
  for (const v of sec.querySelectorAll('.frame video')) {
    v.pause(); try { v.currentTime = 0; } catch {}
    const r = v.getBoundingClientRect();
    let c = r; for (let e = v.parentElement; e && e !== sec; e = e.parentElement) { if (getComputedStyle(e).overflow === 'hidden') { c = e.getBoundingClientRect(); break; } }
    const L = Math.max(r.left, c.left), T = Math.max(r.top, c.top), R = Math.min(r.right, c.right), B = Math.min(r.bottom, c.bottom);
    const crop = { l: (L - r.left) / r.width, t: (T - r.top) / r.height, r: (r.right - R) / r.width, b: (r.bottom - B) / r.height };
    out.videos.push({ src: v.getAttribute('src'), poster: v.getAttribute('poster'), loop: v.loop, x: L - fr.left, y: T - fr.top, w: R - L, h: B - T, crop });
  }
  // overlay chips (badges / captions on top of photos): their fill must sit above the photo, not in the background layer
  const media = [...sec.querySelectorAll('.frame img, .frame video')].filter(visible).map(e => e.getBoundingClientRect());
  for (const el of sec.querySelectorAll('.frame *')) {
    if (el.closest('svg') || el.closest('.note') || ['IMG', 'VIDEO'].includes(el.tagName) || !visible(el)) continue;
    const cs = getComputedStyle(el); if (cs.position !== 'absolute') continue;
    const bgc = hex(cs.backgroundColor), grad = cs.backgroundImage && cs.backgroundImage.includes('gradient');
    if ((!bgc || bgc.a < .05) && !grad) continue;
    const r = el.getBoundingClientRect(); if (r.width < 4 || r.width > fr.width * .5) continue;
    if (!media.some(m => r.left < m.right && r.right > m.left && r.top < m.bottom && r.bottom > m.top)) continue;
    let col = bgc && bgc.a >= .05 ? bgc : null;
    if (!col && grad) { const m = cs.backgroundImage.match(/rgba?\([^)]+\)/); col = m ? hex(m[0]) : null; }
    if (!col) continue;
    out.chips.push({ x: r.left - fr.left, y: r.top - fr.top, w: r.width, h: r.height, color: col.hex, alpha: col.a * opac(el), rad: parseFloat(cs.borderTopLeftRadius) || 0 });
  }
  // brand corner + page number (pseudo-elements)
  for (const [pseudo, txt] of [['::before', 'WON SHOT'], ['::after', frame.dataset.pg]]) {
    const cs = getComputedStyle(frame, pseudo); if (cs.content === 'none' || cs.display === 'none' || !txt) continue;
    const c = hex(cs.color) || { hex: '777777', a: 1 }, fs = parseFloat(cs.fontSize);
    const right = parseFloat(cs.right), top = parseFloat(cs.top), bottom = parseFloat(cs.bottom), left = parseFloat(cs.left);
    const w = 400, h = fs * 1.4;
    const x = !isNaN(right) && cs.right !== 'auto' ? fr.width - right - w : left;
    const y = cs.top !== 'auto' && !isNaN(top) ? top : fr.height - bottom - h;
    out.texts.push({ x, y, w, h, align: cs.right !== 'auto' ? 'right' : 'left', lines: 1, lh: h, runs: [{ text: txt, size: fs, weight: +cs.fontWeight, color: c.hex, alpha: c.a, ls: parseFloat(cs.letterSpacing) || 0 }] });
  }
  return out;
}

const HIDE_ALL_TEXT = `.slide.on, .slide.on *, .slide.on *::before, .slide.on *::after { color: transparent !important; -webkit-text-fill-color: transparent !important; text-shadow: none !important; }
.slide.on .frame::before, .slide.on .frame::after { color: transparent !important; }
.slide.on img:not(.r-cv-bg), .slide.on video, .slide.on svg { visibility: hidden !important; }
#chrome, .chrome, .bar-line { display: none !important; }`;
const ISOLATE = `html, body, .deck, .slide.on { background: transparent !important; }
.slide.on::before, .slide.on::after, .slide.on .frame::before, .slide.on .frame::after { display: none !important; }
.slide.on * { visibility: hidden !important; background: transparent !important; box-shadow: none !important; border-color: transparent !important; }
.slide.on svg[data-iso], .slide.on svg[data-iso] * { visibility: visible !important; }
.slide.on svg[data-iso] text { fill: transparent !important; }
#chrome, .chrome, .bar-line { display: none !important; }`;

const imgCache = new Map();
async function toPng(file) {
  if (imgCache.has(file)) return imgCache.get(file);
  const m0 = await sharp(file, { animated: false }).metadata();
  const alpha = !!m0.hasAlpha && (await sharp(file, { animated: false }).stats()).channels[3]?.min < 255;   // opaque photos → JPEG (smaller file)
  const buf = alpha ? await sharp(file, { animated: false }).png().toBuffer() : await sharp(file, { animated: false }).flatten({ background: '#ffffff' }).jpeg({ quality: 88, mozjpeg: true }).toBuffer();
  const v = { data: (alpha ? 'image/png' : 'image/jpeg') + ';base64,' + buf.toString('base64'), w: m0.width, h: m0.height, buf, alpha };
  imgCache.set(file, v); return v;
}
// crop an image like CSS object-fit: cover/contain with object-position inside a w×h box → buffer at the box aspect
async function fitImage(file, im) {
  const src = await toPng(file);
  const boxW = im.w, boxH = im.h;
  if (im.fit !== 'cover') return { data: src.data, x: im.x, y: im.y, w: im.w, h: im.h, contain: im.fit === 'contain', nw: src.w, nh: src.h };
  const sc = Math.max(boxW / src.w, boxH / src.h);
  const cw = Math.round(boxW / sc), ch = Math.round(boxH / sc);
  const [px, py] = (im.pos || '50% 50%').split(' ').map(v => v.endsWith('%') ? parseFloat(v) / 100 : .5);
  const left = Math.max(0, Math.min(src.w - cw, Math.round((src.w - cw) * px))), top = Math.max(0, Math.min(src.h - ch, Math.round((src.h - ch) * (isNaN(py) ? .5 : py))));
  const cut = sharp(src.buf).extract({ left, top, width: Math.min(cw, src.w), height: Math.min(ch, src.h) });
  const out = src.alpha ? await cut.png().toBuffer() : await cut.jpeg({ quality: 88, mozjpeg: true }).toBuffer();
  return { data: (src.alpha ? 'image/png' : 'image/jpeg') + ';base64,' + out.toString('base64'), x: im.x, y: im.y, w: im.w, h: im.h };
}

// post-process: unique shape ids, one <a:pPr> per paragraph, Korean language tags, video crop + autoplay
async function finish(file, media) {
  const zip = await JSZip.loadAsync(fs.readFileSync(file));
  const bySlide = new Map(); media.forEach(m => bySlide.set(m.slide, [...(bySlide.get(m.slide) || []), m]));
  const slideFiles = Object.keys(zip.files).filter(n => /^ppt\/slides\/slide\d+\.xml$/.test(n));
  for (const name of slideFiles) {
    const n = +/slide(\d+)\.xml$/.exec(name)[1];
    let xml = await zip.file(name).async('string');
    // ① unique ids (pptxgenjs reuses ids for media)
    let next = 2; const mediaIds = [];
    xml = xml.replace(/<p:cNvPr id="\d+" name="([^"]*)"/g, (m, nm) => { const id = next++; if (/^Media \d+$/.test(nm)) mediaIds.push(id); return `<p:cNvPr id="${id}" name="${nm}"`; });
    // ② a paragraph has one pPr, first
    xml = xml.replace(/<a:p>([\s\S]*?)<\/a:p>/g, (m, body) => {
      let first = true;
      body = body.replace(/<a:pPr\b[^>]*?(?:\/>|>[\s\S]*?<\/a:pPr>)/g, pp => { if (first) { first = false; return pp; } return ''; });
      return `<a:p>${body}</a:p>`;
    });
    // ③ Korean
    xml = xml.replace(/lang="en-US"/g, 'lang="ko-KR" altLang="en-US"').replace(/(<a:ea typeface="[^"]*" pitchFamily="\d+") charset="-122"/g, '$1 charset="-127"');
    // ④ videos: crop to their frame, autoplay muted
    const list = bySlide.get(n) || [];
    if (list.length) {
      let mi = 0;
      xml = xml.replace(/<p:pic>[\s\S]*?<\/p:pic>/g, pic => {
        if (!/name="Media \d+"/.test(pic)) return pic; const c = (list[mi++] || {}).crop; if (!c) return pic;
        const f = v => Math.max(0, Math.round(v * 100000));
        if (!(f(c.l) || f(c.t) || f(c.r) || f(c.b))) return pic;
        return pic.replace(/(<a:blip [^>]*?(?:\/>|>[\s\S]*?<\/a:blip>))/, `$1<a:srcRect l="${f(c.l)}" t="${f(c.t)}" r="${f(c.r)}" b="${f(c.b)}"/>`);
      });
      let id = 3; const grp = id++, sub = id++;
      const calls = mediaIds.map(spid => `<p:par><p:cTn id="${id++}" presetID="1" presetClass="mediacall" presetSubtype="0" fill="hold" nodeType="withEffect"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst><p:cmd type="call" cmd="playFrom(0.0)"><p:cBhvr><p:cTn id="${id++}" dur="1" fill="hold"/><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cBhvr></p:cmd></p:childTnLst></p:cTn></p:par>`).join('');
      const nodes = mediaIds.map((spid, i) => `<p:video><p:cMediaNode vol="80000" mute="1"><p:cTn id="${id++}" fill="hold" display="0"${list[i] && list[i].loop ? ' repeatCount="indefinite"' : ''}><p:stCondLst><p:cond delay="indefinite"/></p:stCondLst><p:endCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:endCondLst></p:cTn><p:tgtEl><p:spTgt spid="${spid}"/></p:tgtEl></p:cMediaNode></p:video>`).join('');
      const timing = `<p:timing><p:tnLst><p:par><p:cTn id="1" dur="indefinite" restart="never" nodeType="tmRoot"><p:childTnLst><p:seq concurrent="1" nextAc="seek"><p:cTn id="2" dur="indefinite" nodeType="mainSeq"><p:childTnLst><p:par><p:cTn id="${grp}" fill="hold"><p:stCondLst><p:cond delay="indefinite"/><p:cond evt="onBegin" delay="0"><p:tn val="2"/></p:cond></p:stCondLst><p:childTnLst><p:par><p:cTn id="${sub}" fill="hold"><p:stCondLst><p:cond delay="0"/></p:stCondLst><p:childTnLst>${calls}</p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn></p:par></p:childTnLst></p:cTn><p:prevCondLst><p:cond evt="onPrev" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:prevCondLst><p:nextCondLst><p:cond evt="onNext" delay="0"><p:tgtEl><p:sldTgt/></p:tgtEl></p:cond></p:nextCondLst></p:seq>${nodes}</p:childTnLst></p:cTn></p:par></p:tnLst></p:timing>`;
      xml = xml.replace('</p:sld>', timing + '</p:sld>');
    }
    zip.file(name, xml);
  }
  for (const name of Object.keys(zip.files).filter(n => /^ppt\/notesSlides\/notesSlide\d+\.xml$/.test(n))) {
    const xml = await zip.file(name).async('string');
    zip.file(name, xml.replace(/<a:t>([^<]*)<\/a:t>/g, (m, t) => m.includes('\n') ? '<a:t>' + t.split('\n').join('</a:t></a:r><a:br/><a:r><a:rPr lang="ko-KR" dirty="0"/><a:t>') + '</a:t>' : m));
  }
  fs.writeFileSync(file, await zip.generateAsync({ type: 'nodebuffer', compression: 'DEFLATE', compressionOptions: { level: 6 } }));
}

(async () => {
  const html = fs.readFileSync(path.join(DECK, 'index.html'), 'utf8');
  const SECTIONS = JSON.parse(/const SECTIONS = (\[[^\]]*\])/.exec(html)[1].replace(/'/g, '"'));
  const APPX = +(/const APPX = (\d+)/.exec(html) || [0, SECTIONS.length])[1] || SECTIONS.length - 1;
  const srv = await serve(DECK);
  const browser = await chromium.launch();
  const page = await (await browser.newContext({ viewport: { width: BW, height: BH }, deviceScaleFactor: SCALE })).newPage();
  await page.goto(`http://127.0.0.1:${srv.address().port}/`, { waitUntil: 'networkidle' });
  await page.waitForTimeout(800);
  const slides = await page.evaluate(() => [...document.querySelectorAll('.slide')].map(s => ({ id: s.id, title: s.dataset.title, sec: +s.dataset.sec, time: s.dataset.time || '',
    note: [...s.querySelectorAll('.note p')].map(p => p.textContent.trim()).join('\n') })));
  const mainCount = slides.filter(s => s.sec !== APPX).length;

  const pres = new PptxGenJS(); pres.layout = 'LAYOUT_WIDE';
  pres.title = 'INFU RETRO — 반려동물 약물투약 사고를 방지하기 위한 이상감지 솔루션'; pres.author = 'WON SHOT'; pres.company = 'WON SHOT';
  pres.theme = { headFontFace: FONT, bodyFontFace: FONT };
  const media = []; let section = '', stats = { t: 0, i: 0, s: 0 };

  for (const [k, s] of slides.entries()) {
    await page.evaluate(id => { location.hash = id; }, s.id);
    await page.waitForTimeout(2200);
    await page.evaluate(() => document.querySelector('#chrome')?.classList.add('idle'));
    const data = await page.evaluate(extract, s.id);
    const frameBox = await page.evaluate(id => { const r = document.querySelector('#' + CSS.escape(id) + ' .frame').getBoundingClientRect(); return { x: r.left, y: r.top, w: r.width, h: r.height }; }, s.id);

    // background layer
    const st1 = await page.addStyleTag({ content: HIDE_ALL_TEXT });
    await page.waitForTimeout(150);
    const bg = await page.screenshot({ type: 'png', clip: { x: frameBox.x, y: frameBox.y, width: frameBox.w, height: frameBox.h } });
    await st1.evaluate(n => n.remove());
    const bgJpg = await sharp(bg).resize(Math.round(BW * 1.5), Math.round(BH * 1.5)).jpeg({ quality: 90, mozjpeg: true }).toBuffer();

    // svg rasters
    const svgPics = [];
    for (const sv of data.svgs) {
      await page.evaluate(([id, i]) => document.querySelector(`#${CSS.escape(id)} svg[data-px="${i}"]`).setAttribute('data-iso', ''), [s.id, sv.i]);
      const st = await page.addStyleTag({ content: ISOLATE });
      await page.waitForTimeout(60);
      const png = await page.screenshot({ type: 'png', omitBackground: true, clip: { x: frameBox.x + sv.x, y: frameBox.y + sv.y, width: sv.w, height: sv.h } });
      await st.evaluate(n => n.remove());
      await page.evaluate(([id, i]) => document.querySelector(`#${CSS.escape(id)} svg[data-px="${i}"]`).removeAttribute('data-iso'), [s.id, sv.i]);
      svgPics.push({ ...sv, data: 'image/png;base64,' + png.toString('base64') });
    }

    const title = (s.sec >= 1 && s.sec < APPX - 1 ? String(s.sec).padStart(2, '0') + ' ' : '') + SECTIONS[s.sec];
    if (title !== section) { pres.addSection({ title }); section = title; }
    const slide = pres.addSlide({ sectionTitle: title });
    slide.background = { data: 'image/jpeg;base64,' + bgJpg.toString('base64') };

    // images
    for (const im of data.imgs) {
      const file = path.join(DECK, im.src);
      if (!fs.existsSync(file)) continue;
      let box = im;
      if (im.clip && (im.clip.w < im.w - 1 || im.clip.h < im.h - 1)) {   // image larger than its frame (zoomed crops)
        const ix = Math.max(im.x, im.clip.x), iy = Math.max(im.y, im.clip.y), ix2 = Math.min(im.x + im.w, im.clip.x + im.clip.w), iy2 = Math.min(im.y + im.h, im.clip.y + im.clip.h);
        box = { ...im, x: ix, y: iy, w: ix2 - ix, h: iy2 - iy, fit: 'cover' };
      }
      const f = await fitImage(file, box);
      const opt = { data: f.data, x: box.x * PX, y: box.y * PX, w: box.w * PX, h: box.h * PX, rotate: im.rot || undefined, rounding: !!im.round, altText: path.basename(im.src) };
      if (f.contain) opt.sizing = { type: 'contain', w: box.w * PX, h: box.h * PX };
      if (im.alpha < .99) opt.transparency = Math.round((1 - im.alpha) * 100);
      slide.addImage(opt); stats.i++;
    }
    for (const sv of svgPics) { slide.addImage({ data: sv.data, x: sv.x * PX, y: sv.y * PX, w: sv.w * PX, h: sv.h * PX }); stats.s++; }
    for (const v of data.videos) {
      const poster = await sharp(path.join(DECK, v.poster)).png().toBuffer();
      slide.addMedia({ type: 'video', path: path.join(DECK, v.src), cover: 'image/png;base64,' + poster.toString('base64'), x: v.x * PX, y: v.y * PX, w: v.w * PX, h: v.h * PX });
      media.push({ slide: k + 1, loop: v.loop, crop: v.crop });
    }
    for (const c of data.chips) {
      slide.addShape(pres.shapes.ROUNDED_RECTANGLE, { x: c.x * PX, y: c.y * PX, w: c.w * PX, h: c.h * PX, rectRadius: Math.min(c.rad, c.h / 2) * PX,
        fill: { color: c.color, transparency: c.alpha < .99 ? Math.round((1 - c.alpha) * 100) : 0 }, line: { type: 'none' } });
    }
    // text boxes
    for (const t of data.texts) {
      const runs = t.runs.map(r => r.br ? { text: '', options: { breakLine: true } } : {
        text: r.text, options: { fontFace: FONT, fontSize: +(r.size * PT).toFixed(1), bold: r.weight >= 600, italic: !!r.italic, color: r.color,
          transparency: r.alpha < .99 ? Math.round((1 - r.alpha) * 100) : undefined, charSpacing: r.ls ? +(r.ls * PT).toFixed(2) : undefined,
          subscript: !!r.sub || undefined, superscript: !!r.sup || undefined } });
      // merge break markers into the previous run (pptxgenjs breakLine)
      const rr = []; for (const r of runs) { if (r.options.breakLine && !r.text) { if (rr.length) rr[rr.length - 1].options = { ...rr[rr.length - 1].options, breakLine: true }; } else rr.push(r); }
      if (!rr.length) continue;
      const maxSize = Math.max(...t.runs.filter(r => !r.br).map(r => r.size));
      const padW = t.w * .06 + maxSize * .5, padH = maxSize * .25;
      let x = t.x, w = t.w + padW;
      if (t.align === 'center') x -= padW / 2; else if (t.align === 'right') x -= padW;
      const lineSp = t.lines > 1 ? +(t.lh * PT).toFixed(1) : undefined;
      slide.addText(rr, { x: x * PX, y: (t.y - padH / 2) * PX, w: w * PX, h: (t.h + padH) * PX, align: t.align, valign: 'top', margin: 0, inset: 0,
        wrap: t.lines > 1, lineSpacing: lineSp, paraSpaceBefore: 0, paraSpaceAfter: 0, fit: 'none' });
      stats.t++;
    }
    const label = s.sec === APPX ? `부록 A${k - mainCount + 1}` : `${k + 1} / ${mainCount}`;
    slide.addNotes(`${label}${s.time ? ` · 대본 약 ${s.time}초` : ''}\n${s.note}`);
    console.log(`${String(k + 1).padStart(2)} ${s.id.padEnd(13)} 글자 ${String(data.texts.length).padStart(3)} · 사진 ${data.imgs.length} · 그림 ${data.svgs.length}${data.videos.length ? ' · 영상 ' + data.videos.length : ''}`);
  }
  await browser.close(); srv.close();
  fs.mkdirSync(path.dirname(OUT), { recursive: true });
  await pres.writeFile({ fileName: OUT });
  await finish(OUT, media);
  console.log(`${OUT} · ${slides.length}장 · 텍스트 상자 ${stats.t} · 사진 ${stats.i} · 그림 ${stats.s} · ${(fs.statSync(OUT).size / 1048576).toFixed(1)} MB`);
})().catch(e => { console.error(e); process.exit(1); });
