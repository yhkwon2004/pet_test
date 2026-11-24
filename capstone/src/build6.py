# Stage 6: national engineering award — 청년 뉴턴(NEW:TURN) 2026 창의적종합설계경진대회 최우수상(산업통상부장관상), 공동 2위
# Fact base: 산업통상부 보도자료 2026.11.19 (서울 SETEC, 전국 73개 대학 149팀, 대상 1팀 = 국무총리상) + team's stage photo
import re
DST = '/home/user/pet_test/capstone/index.html'
s = open(DST, encoding='utf-8').read()

# cover: the award leads the badge row (own line), the three existing badges follow
old = '<ul class="r-cv-bd b">\n'
assert s.count(old) == 1
s = s.replace(old, old + '          <li class="aw"><b>산업통상부장관상</b><span>전국 창의적종합설계경진대회 · 최우수상 · 공동 2위</span></li>\n          <li class="brk" aria-hidden="true"></li>\n', 1)

# team slide: award first in the list, stage photo first among the pictures
old = '<ul><li><b>2026 WON+ PBL 챌린지</b>'
assert s.count(old) == 1
s = s.replace(old, '<ul><li class="top"><b>창의적종합설계경진대회</b> · 산업통상부장관상(최우수상) · 공동 2위</li><li><b>2026 WON+ PBL 챌린지</b>', 1)
old = '<div class="r-awi">'
assert s.count(old) == 1
s = s.replace(old, old + '<figure class="nt"><img src="media/award-newturn.webp" alt="청년 뉴턴(NEW:TURN) 2026 창의적종합설계경진대회 산업통상부장관상 최우수상 시상 — 서울 SETEC" data-zoom><figcaption>청년 뉴턴 2026 · 최우수상</figcaption></figure>', 1)
old = '<div class="lg2">'
assert s.count(old) == 1
s = s.replace(old, '<p class="r-src aw-src">청년 뉴턴(NEW:TURN) 2026 · 산업통상부 · 2026.11.19 서울 SETEC · 전국 73개 대학 149팀</p>' + old, 1)

# appendix KPI: four awards now
for a, b in (('수상 <b>3건</b>', '수상 <b>4건</b>'), ('수상 3건이 더해집니다', '수상 4건이 더해집니다')):
    assert s.count(a) == 1, a; s = s.replace(a, b, 1)
# slide 10 card text: one line each, no orphans
for a, b in (('<p>24-bit 로드셀 전용 ADC · 전원 분리 · RC 필터</p>', '<p>24-bit ADC · 전원 분리 · RC 필터</p>'),
             ('<p>X자 하우징에 맞춘 곡면 보드 · 폴대 주위 배치</p>', '<p>X자 하우징 맞춤 곡면 보드</p>'),
             ('<p>ESP32 + 24-bit ADC 2개 · 로드셀 4채널(LC1–LC4) · USB-C 충전</p>', '<p>ESP32 + ADC 2개 · 로드셀 4채널</p>')):
    assert s.count(a) == 1, a; s = s.replace(a, b, 1)
# speaker notes (kept inside each slide's data-time at ~5 syllables/s)
m = re.search(r'(<section [^>]*id="s-team".*?<div class="note" hidden>).*?(</div>)', s, re.S); assert m
s = s[:m.end(1)] + '<p>팀 인퓨테크는 소프트웨어와 임상병리 다섯 명이 회로부터 서버, 임상 실증까지 나눠 맡았습니다.</p><p>이 작품으로 전국 149팀이 겨룬 창의적종합설계경진대회에서 산업통상부장관상, 공동 2위를 받았습니다.</p>' + s[m.start(2):]
m = re.search(r'(<section [^>]*id="s-hw".*?<div class="note" hidden>).*?(</div>)', s, re.S); assert m
s = s[:m.end(1)] + '<p>회로는 계속 개선하고 있습니다. 단일 보드에 24비트 로드셀 전용 ADC와 전원 분리, RC 필터를 넣어 미세한 무게 변화를 읽었고, 실물 PCB로 만들어 모듈에 탑재했습니다.</p><p>개선형 PCB는 X자 하우징에 맞춘 곡면 보드로, 로드셀 네 채널을 읽고 USB-C로 충전합니다.</p>' + s[m.start(2):]
s = s.replace('<figcaption>글로벌 피우다 · 장려상</figcaption>', '<figcaption>피우다 · 장려상</figcaption>', 1)

css = '''
#s-opening .r-cv-bd li.brk { flex-basis: 100%; height: 0; padding: 0 !important; margin: -.45em 0 0; border: 0 !important; background: none !important; box-shadow: none !important; }
#s-opening .r-cv-bd li.aw { background: #1E3A8A !important; border-color: #1E3A8A !important; padding: .7em 1.3em; }
#s-opening .r-cv-bd li.aw b { color: #FFFFFF !important; font-size: 1.35em; }
#s-opening .r-cv-bd li.aw span { color: #D7DEEA !important; font-size: 1em; }
#s-team .r-tm2 { grid-template-columns: 1fr 1.32fr; gap: 2.4em; }
#s-team .r-tm2 ul li { line-height: 1.5; }
#s-team .r-tm2 ul li.top { color: #1E3A8A; } #s-team .r-tm2 ul li.top b { color: #1E3A8A; }
#s-team .r-awi { grid-template-columns: auto 1fr auto; grid-template-rows: auto; gap: 0 .9em; }
#s-team .r-tm2 .r-awi .nt { grid-row: 1; grid-column: 1; height: 10.4em; aspect-ratio: 700 / 375; }
#s-team .r-awi .nt img { width: 100%; height: 100%; object-fit: cover; }
#s-team .r-tm2 .r-awi .pic { grid-row: 1; grid-column: 2; }
#s-team .r-tm2 .r-awi .cert { grid-row: 1; grid-column: 3; }
#s-team .r-awi { row-gap: .45em; }
#s-team .r-awi .aw-src { grid-row: 2; grid-column: 1 / -1; margin: 0; text-align: center; white-space: nowrap; }
#s-opening .r-cv-bd li.aw { box-sizing: border-box; height: 3.6em; width: 35.55em; justify-content: center; padding: 0 1.1em; }
#s-hw .cp-ev .v3 { grid-template-rows: minmax(0, 1fr) minmax(0, 1fr) !important; }
#s-hw .cp-ev .v3 figure:first-child { background: linear-gradient(#CBCBE6, #66667F) !important; }
'''
s = s.replace('</head>', f'<style id="cap-award">{css}</style>\n</head>', 1)
open(DST, 'w', encoding='utf-8').write(s); print('award ok')
