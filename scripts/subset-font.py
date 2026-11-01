#!/usr/bin/env python3
"""INFU RETRO IR 덱 index.html에 쓰인 글자만 담은 Pretendard 서브셋을 만들어 index.html 안에 넣습니다.

서체 파일을 따로 두지 않고 HTML 안(<style id="pitch-font">)에 넣어 두므로, 인터넷이 느리거나 끊겨도, 파일을 바로
열어도, 어느 컴퓨터에서든 같은 서체로 보입니다. 그래프(charts/*.svg)는 글자를 윤곽선으로 담고 있어 이 서체가 필요 없습니다.

덱 문구를 고쳐 새 글자가 생기면 다시 실행합니다. Pretendard에 없는 글자(한자 등)가 문구에 있으면 멈추고 알려 줍니다
— 그런 글자는 컴퓨터마다 다른 서체로 그려지기 때문입니다.

  pip install fonttools brotli
  python3 scripts/subset-pitch-font.py      # 서체: node_modules의 PretendardVariable.ttf, 없으면 PRETENDARD_TTF=<경로>
"""
import base64, io, os, re, string, sys
from fontTools import subset
from fontTools.ttLib import TTFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(ROOT, 'public', 'infutech') if os.path.isdir(os.path.join(ROOT, 'public', 'infutech')) else ROOT
path = os.path.join(DECK, 'index.html')
src = os.environ.get('PRETENDARD_TTF') or os.path.join(ROOT, 'node_modules', 'pretendard', 'dist', 'public', 'variable', 'PretendardVariable.ttf')
if not os.path.exists(src):
    sys.exit('PretendardVariable.ttf가 없습니다 — npm ci 하거나 PRETENDARD_TTF=<PretendardVariable.ttf 경로>')

html = open(path, encoding='utf-8').read()
BLOCK = re.compile(r'<style id="pitch-font">.*?</style>', re.S)
if not BLOCK.search(html):
    sys.exit('index.html에 <style id="pitch-font"> 블록이 없습니다')
used = {c for c in BLOCK.sub('', html) if c.isprintable() and not c.isspace()}

cmap = TTFont(src).getBestCmap()
missing = sorted(c for c in used if ord(c) not in cmap)
if missing:
    sys.exit('Pretendard에 없는 글자가 있습니다(컴퓨터마다 다른 서체로 보임) — 문구를 바꿔 주세요: '
             + ' '.join(f'{c} U+{ord(c):04X}' for c in missing))
# spare punctuation so small wording edits do not fall outside the subset
chars = used | {c for c in string.printable + '·—–…“”‘’「」→←↔↓↑×−±①②③※%' if not c.isspace() and ord(c) in cmap} | {' ', ' '}

opts = subset.Options()
opts.flavor = 'woff2'
opts.layout_features = ['*']
opts.name_IDs = ['*']
opts.notdef_outline = True
font = subset.load_font(src, opts)
sub = subset.Subsetter(opts)
sub.populate(unicodes=sorted(ord(c) for c in chars))
sub.subset(font)
buf = io.BytesIO()
subset.save_font(font, buf, opts)

data = base64.b64encode(buf.getvalue()).decode('ascii')
block = ('<style id="pitch-font">@font-face { font-family: "Pretendard Pitch"; '
         f'src: url("data:font/woff2;base64,{data}") format("woff2"); font-weight: 100 900; font-display: block; }}</style>')
open(path, 'w', encoding='utf-8').write(BLOCK.sub(lambda m: block, html, count=1))
print(path, len(chars), 'glyphs', len(buf.getvalue()) // 1024, 'KB woff2 embedded')
