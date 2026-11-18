# Stage 5: slide 10 = circuit evolution with the team's real board images (design → real PCB → mounted module → V3)
import re
DST = '/home/user/pet_test/capstone/index.html'
s = open(DST, encoding='utf-8').read()
m = re.search(r'<section [^>]*id="s-hw"[^>]*>.*?</section>\n', s, re.S); assert m
new = '''<section class="slide rf " id="s-hw" data-sec="6" data-time="22" data-title="회로는 계속 개선되고 있습니다 — 설계 · 실물 · 탑재 · V3">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Design · 회로 설계</p><h2 class="r-t b">회로는 <em>계속 개선</em>되고 있습니다 — 설계 → 실물 → 탑재 → V3</h2></header>
    <ol class="cp-ev b">
      <li><figure><img src="media/pcb-layout.webp" alt="회로 설계 레이아웃 — 60×35 mm 단일 보드" data-zoom></figure><i>STEP 1</i><b>회로 설계</b><p>60 × 35 mm 단일 보드</p><p>24-bit 로드셀 전용 ADC · 전원 분리 · RC 필터</p></li>
      <li><figure><img src="media/pcb-real.webp" alt="실물 PCB 앞면과 뒷면" data-zoom></figure><i>STEP 2</i><b>실물 PCB 제작</b><p>앞 · 뒷면 실물 보드</p><p>설계한 회로를 실물로 제작해 검증</p></li>
      <li><figure><img src="media/mod-inside.webp" alt="모듈 내부 — 로드셀, 회로기판, 배터리를 탑재한 시제품" data-zoom></figure><i>STEP 3</i><b>모듈 탑재</b><p>로드셀 4개 · 회로기판 · 배터리 일체</p><p>기존 폴대 걸이부에 그대로 장착</p></li>
      <li class="now"><div class="v3"><span>V3</span><small>최신 설계</small></div><i>STEP 4 · NOW</i><b>하우징 맞춤 V3 보드</b><p>X자 하우징에 맞춘 곡면 보드 · 폴대 주위 배치</p><p>ESP32 + 24-bit ADC 2개 · 로드셀 4채널(LC1–LC4) · USB-C 충전</p></li>
    </ol>
    <p class="r-src c b">회로 설계 · 실물 PCB · 모듈 내부 – INFUTECH 시제품 · 발명신고서(2026) · V3 – INFUTECH KiCad · 3D 설계(2026)</p>
  </div>
  <div class="note" hidden><p>회로는 계속 개선하고 있습니다. 60×35밀리미터 단일 보드로 시작해 24비트 로드셀 전용 ADC와 전원 분리, RC 필터로 미세한 무게 변화를 읽었고, 실물 PCB로 만들어 모듈에 탑재했습니다.</p><p>최신 V3는 X자 하우징에 맞춘 곡면 보드로, ESP32와 24비트 ADC 두 개로 로드셀 네 채널을 읽고 USB-C로 충전합니다.</p></div>
</section>
'''
s = s[:m.start()] + new + s[m.end():]
s = s.replace("'구조 · PCB 설계',", "'회로 설계',")
css = '''
#s-hw .cp-ev { flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(4, 1fr); gap: 1.4em; counter-reset: st; }
#s-hw .cp-ev > li { position: relative; display: flex; flex-direction: column; gap: .35em; padding: 1em 1em 1.3em; border: 1px solid #E5E7EB; border-radius: .7em; background: #FFFFFF; }
#s-hw .cp-ev > li + li::before { content: "→"; position: absolute; left: -1.05em; top: 9em; font-size: 1.3em; font-weight: 800; color: #8CA0CF; }
#s-hw .cp-ev figure, #s-hw .cp-ev .v3 { flex: 1; min-height: 0; margin: 0 0 .7em; border-radius: .5em; overflow: hidden; background: #F3F4F6; display: flex; align-items: center; justify-content: center; }
#s-hw .cp-ev figure img { width: 100%; height: 100%; object-fit: contain; }
#s-hw .cp-ev > li:nth-child(3) figure img { object-fit: cover; }
#s-hw .cp-ev > li > i { font-style: normal; font-size: .95em; font-weight: 800; letter-spacing: .06em; color: #1E3A8A; }
#s-hw .cp-ev > li > b { font-size: 1.6em; font-weight: 700; color: #111418; letter-spacing: -.02em; }
#s-hw .cp-ev > li > p { font-size: 1.05em; font-weight: 500; color: #3F4651; line-height: 1.45; }
#s-hw .cp-ev > li > p + p { margin-top: .1em; }
#s-hw .cp-ev li.now { background: #1E3A8A; border-color: #1E3A8A; }
#s-hw .cp-ev li.now > i { color: #D7DEEA; } #s-hw .cp-ev li.now > b { color: #FFFFFF; } #s-hw .cp-ev li.now > p { color: #D7DEEA; }
#s-hw .cp-ev .v3 { flex-direction: column; gap: .3em; background: rgba(255, 255, 255, .08); border: 1px solid rgba(255, 255, 255, .25); }
#s-hw .cp-ev .v3 span { font-size: 6em; font-weight: 800; letter-spacing: -.04em; color: #FFFFFF; line-height: 1; }
#s-hw .cp-ev .v3 small { font-size: 1.1em; font-weight: 600; color: #D7DEEA; letter-spacing: .08em; }
#s-hw .r-src.c { margin-top: 1em; }
#s-hw .cp-ev > li { display: grid; grid-template-rows: 1fr auto auto 2.9em 2.9em; row-gap: .35em; }
#s-hw .cp-ev > li > p { font-size: 1.02em; }
#s-hw .cp-ev figure, #s-hw .cp-ev .v3 { height: 100%; }
'''
s = s.replace('</style>\n</head>', css + '</style>\n</head>', 1) if '</style>\n</head>' in s else s.replace('</head>', f'<style id="cap-ev">{css}</style>\n</head>', 1)
open(DST, 'w', encoding='utf-8').write(s); print('slide 10 circuit ok')
