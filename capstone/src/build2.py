# Stage 2 (2026-11-16): law/record-burden slide, precise signal-processing slide 10, CNN + RNN slide 11,
# team aligned to the 2026-2 캡스톤디자인 참가신청서, team mark INFUTECH, rewritten script and timing.
import re, os
S = os.path.dirname(os.path.abspath(__file__))
SRC = '/home/user/pet_test/index.html'; DST = '/home/user/pet_test/capstone/index.html'
s = open(DST, encoding='utf-8').read(); src = open(SRC, encoding='utf-8').read()
def sec(txt, id_):
    m = re.search(r'<section [^>]*id="%s"[^>]*>.*?</section>\n' % re.escape(id_), txt, re.S); assert m, id_; return m
def put(id_, new):
    global s; m = sec(s, id_); s = s[:m.start()] + new + s[m.end():]
def rep(a, b, txt, n=1):
    assert txt.count(a) == n, (txt.count(a), a[:80]); return txt.replace(a, b)
def note(t, paras):
    return re.sub(r'<div class="note" hidden>.*?</div>', '<div class="note" hidden>' + ''.join(f'<p>{p}</p>' for p in paras) + '</div>', t, count=1, flags=re.S)
# ---------- law / record burden (after s-onevet), from the IR deck's s-demand
t = sec(src, 's-demand').group(0)
t = t.replace('id="s-demand" data-sec="2" data-time="24" data-title="처치 기록은 법정 의무, 분쟁 시 사본 발급도 입법 중"',
              'id="s-law" data-sec="2" data-time="20" data-title="기록 · 정보 제공까지 의무가 되면, 1인 수의사의 부담은 더 커집니다"')
t = rep('<header class="r-hd"><h2 class="r-t lg2 b">처치 기록은 법정 의무,<br><em>분쟁 시 사본 발급도 입법 중</em></h2></header>',
        '<header class="r-hd"><p class="r-kick b">Pain Point ③ · 기록 · 정보 제공 의무</p><h2 class="r-t b">기록 · 정보 제공까지 의무가 되면, <em>1인 수의사의 부담</em>은 더 커집니다</h2></header>', t)
t = t.replace('<div class="r-2 w64 b">', '<div class="r-2 w64 cp-law b">', 1)
t = re.sub(r'(</div>\n    </div>\n)(  </div>\n  <div class="note")',
           r'\1    <p class="r-foot b">감시에 기록까지 혼자 — 그래서 <b>이상을 먼저 알리고 자동으로 기록하는 장치</b>가 꼭 필요합니다 · 현장 26곳에서도 같은 요구 확인</p>\n\2', t, count=1)
t = note(t, ['여기에 기록 부담까지 커지고 있습니다. 진료부 처치 기록은 이미 수의사법상 의무이고, 분쟁 때 진료기록 사본을 발급하는 법안도 농해수위를 통과했습니다.',
             '기록이 있으면 분쟁 해결률도 1.5배 높았습니다. 1인 수의사가 감시와 기록을 모두 손으로 해야 하는 셈이라, 이상을 먼저 알리고 자동으로 기록하는 장치가 꼭 필요합니다.'])
m = sec(s, 's-onevet'); s = s[:m.end()] + t + s[m.end():]
# ---------- slide 10: signal processing
t = sec(s, 's-tech').group(0)
tech = open(f'{S}/tech2.svg').read()
t = re.sub(r'<header class="r-hd">.*?</header>', '<header class="r-hd"><p class="r-kick b">Core Tech ① · 신호 처리</p><h2 class="r-t b"><em>칼만 필터 · 가상 자이로 · PID</em>로, 흔들려도 정확한 무게 신호를 만듭니다</h2></header>', t, count=1, flags=re.S)
t = re.sub(r'<div class="r-card r-tc b">.*?</div>\n', f'<div class="r-card r-tc cp-tc b">{tech}</div>\n', t, count=1, flags=re.S)
t = re.sub(r'<p class="r-tk b">.*?</p>', '<p class="r-src c b">칼만 필터 – INFUTECH 사업계획서 · 가상 자이로 지도학습 · PID(LoRA + 유전 알고리즘 튜닝) – INFUTECH 설계 · 최대 오차 2.9% – 내부 모의시험(모의 병실 1,000회)</p>', t, count=1, flags=re.S)
t = re.sub(r'data-title="[^"]*"', 'data-title="칼만 필터 · 가상 자이로 · PID — 흔들려도 정확한 무게 신호"', t, count=1)
t = note(t, ['이제 핵심 기술입니다. 로드셀 원신호에는 흔들림과 센서 잡음이 섞여 있어, 먼저 칼만 필터로 잡음을 1차로 걸러 냅니다.',
             '다음으로 가상 자이로가 로드셀만으로 기울기를 추정하고, PID 제어가 그 오차를 상쇄합니다. 가상 자이로는 자이로를 단 프로세서와 로드셀만 단 프로세서의 편차를 정답으로 지도학습했고, PID 게인은 LoRA와 유전 알고리즘으로 자동 튜닝합니다.',
             '이렇게 얻은 보정 하중과 유속을 다음 단계에서 분석합니다.'])
put('s-tech', t)
# ---------- slide 11: CNN + RNN
ai = open(f'{S}/ai2.svg').read()
t = f'''<section class="slide rf " id="s-cnn" data-sec="7" data-time="26" data-title="CNN과 RNN으로 — 모양과 흐름을 함께 분석해 판정합니다">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Core Tech ② · AI 분석</p><h2 class="r-t b">보정된 신호를 <em>CNN과 RNN</em>으로 — 모양과 흐름을 함께 분석합니다</h2></header>
    <div class="r-card cp-cnn b">{ai}</div>
    <ul class="cp-why b">
      <li><i>①</i><div><b>CNN · 순간 패턴의 '모양'</b><span>고립된 한 칸은 흔들림, 뭉친 덩어리는 지속 이상</span></div></li>
      <li><i>②</i><div><b>RNN · 시간에 따른 '흐름'</b><span>점점 느려짐 · 멈춤 · 급감 추세를 순서대로 기억</span></div></li>
      <li class="pp"><i>③</i><div><b>우수논문 2편 · 특허 출원 3건</b><span>국제 AIT 2026 · 국내 한국혁신산업학회 2026</span></div></li>
    </ul>
    <p class="r-src c b">CNN 구조(Conv2D 3×3 · 8 → MaxPool 2×2 → Dense 16) – 한우진 외, 「상태 패턴 분석 기반 수액 이상 감지 알고리즘」 · 판정 5종 – 2026-2 캡스톤디자인 참가신청서 · RNN 시계열 분석 – INFUTECH 설계</p>
  </div>
  <div class="note" hidden><p>보정된 신호는 두 가지 AI로 분석합니다. CNN은 16개 상태를 4×4 그림으로 만들어, 고립된 한 칸은 순간 흔들림, 뭉친 덩어리는 지속 이상으로 모양을 봅니다.</p><p>RNN은 유속을 순서대로 기억해 점점 느려지거나 멈추는 추세를 봅니다. 두 결과를 종합해 정상, 흔들림, 당겨짐, 줄 분리, 소진 다섯 가지로 판정하고, 이 알고리즘으로 우수논문 2편과 특허 3건을 냈습니다.</p></div>
</section>
'''
put('s-cnn', t)
# ---------- team aligned to the 참가신청서
t = sec(s, 's-team').group(0)
t = re.sub(r'data-title="[^"]*"', 'data-title="팀 INFUTECH — 소프트웨어와 임상병리가 함께"', t, count=1)
t = rep('<header class="r-hd"><h2 class="r-t b">인퓨테크 · 팀 WON SHOT, <em>개발과 의료 실증 두 축</em></h2></header>',
        '<header class="r-hd"><h2 class="r-t b">팀 INFUTECH — <em>소프트웨어와 임상병리</em>가 함께 만들었습니다</h2></header>', t)
t = re.sub(r'<div class="r-tgrp b">.*?\n    </div>\n', '''<div class="r-tgrp b">
      <div class="tg dev"><p class="gl"><b>개발</b>컴퓨터소프트웨어공학과 <span>4명</span></p><ul class="r-ppl"><li><img src="media/team-kwon.webp" alt="권용현"><b>권용현</b><span>PCB 설계 · F/W</span></li><li><img src="media/team-jeong.webp" alt="정익상"><b>정익상</b><span>알고리즘 · IR</span></li><li><img src="media/team-han-woojin.webp" alt="한우진"><b>한우진</b><span>3D 설계 · F/W</span></li><li><img src="media/team-choi-iji.webp" alt="최이지"><b>최이지</b><span>백엔드 · 서버 · DB</span></li></ul></div>
      <div class="tg cli"><p class="gl"><b>임상</b>임상병리학과 <span>1명</span></p><ul class="r-ppl"><li><img src="media/team-kim-eungang.webp" alt="김은강"><b>김은강</b><span>임상 자문 · 실증 지원</span></li></ul></div>
    </div>
''', t, count=1, flags=re.S)
t = note(t, ['팀 인퓨테크는 컴퓨터소프트웨어공학과 4명과 임상병리학과 1명입니다. PCB와 펌웨어, 알고리즘, 3D 설계, 서버, 임상 실증을 나눠 맡았고, 전남대 수의과대학과 원광대 간호학과가 실증을 함께합니다.'])
put('s-team', t)
# ---------- team mark, cover topic, closing
s = s.replace('content: "WON SHOT"', 'content: "INFUTECH"')
s = rep('<p class="r-cv-k b">동물병원 입원실 수액 이상감지 솔루션</p>', '<p class="r-cv-k b">가상의 자이로 AI 모델을 활용한 동물용 약물이상감지 시스템</p>', s)
s = s.replace('현장 인터뷰(WON SHOT)', '현장 인터뷰(INFUTECH)')
s = rep('<p class="r-st-s b">2026 캡스톤 디자인 · WON SHOT · 감사합니다</p>', '<p class="r-st-s b">2026 캡스톤 디자인 · INFUTECH · 감사합니다</p>', s)
s = re.sub(r'<meta name="description" content="[^"]*">', '<meta name="description" content="2026 캡스톤 디자인 · 팀 INFUTECH — 가상의 자이로 AI 모델을 활용한 동물용 약물이상감지 시스템 INFU RETRO 발표 자료">', s, count=1)
s = re.sub(r"const SECTIONS = \[.*?\];", "const SECTIONS = ['오프닝', '문제 ① 순회 사이 공백', '문제 ② 1인 수의사 · 기록 부담', '기존 장비의 한계', '현장 수요', '제품 소개', '구조 · PCB 설계', '핵심 기술 · AI 분석', '시험 · 검증', '수요 검증', '팀', '클로징', '부록'];", s, flags=re.S)
s = s.replace('<p>본문 15장 + 부록 · 대본 약 4분 40초 · 2026 캡스톤 디자인</p>', '<p>본문 16장 + 부록 · 대본 약 4분 40초 · 2026 캡스톤 디자인</p>')
# ---------- script (all main slides)
NOTES = {
 's-opening': ['안녕하십니까, 2026 캡스톤 디자인 팀 인퓨테크입니다.', '저희 작품은 가상의 자이로 AI 모델을 활용한 동물용 약물 이상 감지 시스템, INFU RETRO입니다.'],
 's-hook': ['먼저 질문입니다. 전국 동물병원 5,312곳의 입원실 수액 카테터, 몇 개 중 하나꼴로 사고가 날까요?', '100개 중 1개, 20개 중 1개, 4개 중 1개 중에 골라 보시죠.'],
 's-background': ['정답은 4개 중 1개, 26.7퍼센트입니다.', '문제는 발견 시점입니다. 수액은 1~2시간마다 확인하도록 권고되지만, 그 사이에 줄이 빠지거나 막히면 다음 순회 때까지 아무도 모릅니다.'],
 's-onevet': ['더 큰 문제는 구조입니다. 동물병원 10곳 중 7곳은 수의사가 1명입니다.', '진료와 수술, 상담을 하면서 입원실까지 봐야 하니, 순회 간격은 길어지고 사고는 늦게 발견됩니다.'],
 's-rivals': ['하지만 지금 장비는 비싸거나 바꿔야 합니다.', '인퓨전펌프는 1줄에 110만 원, 스마트 폴대는 300만 원이 넘고 폴대째 교체해야 합니다.'],
 's-field': ['그래서 MVP를 들고 현장 26곳을 찾았습니다. 병원이 원한 건 새 장비가 아니라, 쓰던 폴대 그대로 알림과 기록만 자동화하는 것이었습니다.', '시연하고, 고치고, 다시 찾아간 결과가 지금의 제품입니다.'],
 's-match': ['그래서 만든 것이 INFU RETRO입니다. 쓰던 폴대에 끼우면 갈고리 4개가 수액백 4개를 동시에 잽니다.', '줄 분리와 소진은 5초 안에 휴대폰으로 알리고, 기록은 자동으로 남습니다.'],
 's-solution': ['폴대에 끼우고 수액백을 걸면 끝입니다. 줄이 분리되면 원장님 휴대폰으로 알림이 가고, 조치 시각까지 기록됩니다.'],
 's-hw': ['하드웨어는 구조와 PCB에 집중했습니다. 스크류와 마그네틱으로 기존 폴대에 조립하고, 체결부와 로드셀, 걸이부가 일직선으로 하중을 받습니다.', 'PCB에는 24비트 로드셀 전용 ADC를 넣고, 로드셀 값을 4×4 배열로 받아 ESP32가 빠르게 처리합니다.'],
 's-edge': ['모의 병실에서 1,000회를 시험했습니다. 흔들고 당겨도 잔량 최대 오차는 2.9퍼센트, 정상 중 오경보는 0.7퍼센트였습니다.', '줄 분리와 소진은 250번 모두 평균 2.8초에 판정했습니다.'],
 's-entry': ['현장 수요는 계약으로 확인했습니다. 유통사 두 곳과 공급 약정, 구매의향 협약 1억 100만 원 규모를 맺었고, 전남대 수의과대학과는 실증 LOI를 맺었습니다.', '약정은 KC 인증 후 효력이고 협약은 비구속이라, 확정 매출은 아닙니다.'],
 's-end': ['폴대는 그대로, 수액은 놓치지 않게. 지금까지 팀 인퓨테크였습니다. 감사합니다.'],
}
for k, v in NOTES.items():
    t = sec(s, k).group(0); put(k, note(t, v))
s_out = s
open(DST, 'w', encoding='utf-8').write(s_out)
print('ok', len(re.findall(r'data-time=', s_out)), 'main slides')
TIMES = {'s-opening': 13, 's-hook': 13, 's-background': 15, 's-onevet': 14, 's-law': 27, 's-rivals': 11, 's-field': 16, 's-match': 14, 's-solution': 9, 's-hw': 22, 's-tech': 36, 's-cnn': 31, 's-edge': 16, 's-entry': 19, 's-team': 17, 's-end': 7}
s = open(DST, encoding='utf-8').read()
for k, v in TIMES.items():
    s, n = re.subn(r'(<section [^>]*id="%s"[^>]*data-time=")\d+' % k, r'\g<1>%d' % v, s); assert n == 1, k
open(DST, 'w', encoding='utf-8').write(s); print('timed', sum(TIMES.values()))
# ---------- copy every media file the deck references
import shutil
ROOT = '/home/user/pet_test'
refs = set(re.findall(r'(?:src|href|poster)="(media/[^"#?]+)"', s))
for r in refs:
    d = os.path.join(ROOT, 'capstone', r)
    if not os.path.exists(d):
        for base in (ROOT, os.path.join(ROOT, 'festa')):
            if os.path.exists(os.path.join(base, r)):
                os.makedirs(os.path.dirname(d), exist_ok=True); shutil.copy2(os.path.join(base, r), d); break
        else: print('MISSING', r)
print('media ok', len(refs))
