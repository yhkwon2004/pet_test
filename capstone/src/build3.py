# Stage 3: apply the verified review findings (story continuity, measured-vs-claimed alert time,
# paper/patent attribution, animal-first field evidence, wording), then the speaker-script timing.
import re, os
DST = '/home/user/pet_test/capstone/index.html'
s = open(DST, encoding='utf-8').read()
def rep(a, b, n=1):
    global s; assert s.count(a) == n, (s.count(a), a[:90]); s = s.replace(a, b)
def sec(id_):
    m = re.search(r'<section [^>]*id="%s"[^>]*>.*?</section>\n' % re.escape(id_), s, re.S); assert m, id_; return m
def note(id_, paras):
    global s; m = sec(id_); t = re.sub(r'<div class="note" hidden>.*?</div>', '<div class="note" hidden>' + ''.join(f'<p>{p}</p>' for p in paras) + '</div>', m.group(0), count=1, flags=re.S)
    s = s[:m.start()] + t + s[m.end():]
# ---- s-field: continue the pain points, animal-first evidence, no 'AX 전환'
rep('data-title="현장 26곳 — 병원은 쓰던 폴대 그대로의 AX 전환을 원했습니다"', 'data-title="현장의 답 — 먼저 알려 주는 장치는 필요하다, 단 쓰던 폴대 그대로"')
rep('<h2 class="r-t b">병원이 원한 건 새 장비가 아니라, <em>쓰던 폴대 그대로의 AX 전환</em>이었습니다</h2>',
    '<h2 class="r-t b">현장의 답 — <em>먼저 알려 주는 장치</em>는 필요하다, 단 쓰던 폴대 그대로</h2>')
rep('<li><i>01</i><div><b>비용 부담</b><p>스마트 폴대 300만 원+ · 센서값만 90만 원+</p></div></li>',
    '<li><i>01</i><div><b>순회 사이 공백</b><p>진료 · 수술 중엔 입원실을 볼 수 없음</p></div></li>')
rep('<li><i>02</i><div><b>기존 자산은 그대로</b><p>쓰던 폴대 · 수액 세트 · 입원장을 바꾸지 않고</p></div></li>',
    '<li><i>02</i><div><b>비용 부담</b><p>스마트 폴대 300만 원+ · 센서값만 90만 원+</p></div></li>')
rep('<li><i>03</i><div><b>그래도 AX 전환</b><p>알림 · 투여 기록은 사람 손 대신 디지털로</p></div></li>',
    '<li><i>03</i><div><b>쓰던 폴대 그대로</b><p>폴대 · 수액 세트 · 입원장은 바꾸지 않고, 알림 · 기록만 자동으로</p></div></li>')
rep('<span>전북 지역 병원</span>', '<span>전북 병원 · 수액 운용 비교</span>')
rep('<p>스마트 폴대의 고질적인 <b>높은 센서 비용</b>은 줄이고, <b>쓰던 폴대를 그대로 활용</b>하는 모델이 필요하다</p>',
    '<p>이상 순간을 <b>먼저 알리되</b>, <b>센서 비용</b>은 줄이고 <b>쓰던 폴대를 그대로 활용</b>하는 모델이 필요하다</p>')
note('s-field', ['그래서 MVP를 들고 호남권 반려동물병원 16곳을 중심으로, 비교를 위해 전북 병원 10곳까지 모두 26곳을 찾았습니다.',
                 '답은 같았습니다. 먼저 알려 주는 장치는 필요하지만, 폴대를 통째로 바꾸거나 비싼 장비를 들일 여유는 없다는 것이었습니다. 시연하고 고치고 다시 찾아간 결과가 지금의 제품입니다.'])
# ---- alert time: only the device decision is measured
rep('<b>줄 분리 · 소진 5초 안에 휴대폰 알림</b>', '<b>줄 분리 · 소진 5초 안에 판정 → 휴대폰 알림</b>')
note('s-match', ['그래서 만든 것이 INFU RETRO입니다. 쓰던 폴대에 끼우면 갈고리 4개가 수액백 4개를 동시에 잽니다.',
                 '줄 분리와 소진은 기기가 5초 안에 판정해 휴대폰으로 알리고, 기록은 자동으로 남습니다.'])
rep('<tr><th>이상 → 휴대폰 알림</th><td class="c">5초 이내</td><td class="arr">→</td><td class="t">3초 이내</td><td class="m">라인 막힘 · 급속 주입 발생 후 Push 도달</td></tr>',
    '<tr><th>이상 → 기기 판정</th><td class="c">5초 이내(평균 2.8초)</td><td class="arr">→</td><td class="t">3초 이내</td><td class="m">라인 막힘 · 급속 주입 발생 후 판정 · 휴대폰 도착은 실측 예정</td></tr>')
rep('<div class="note" hidden><p>양산형 목표는 잔량 오차 1.5퍼센트, 알림 3초,', '<div class="note" hidden><p>양산형 목표는 잔량 오차 1.5퍼센트, 판정 3초,')
# ---- s-cnn: correct paper / patent attribution
rep('<li class="pp"><i>③</i><div><b>우수논문 2편 · 특허 출원 3건</b><span>국제 AIT 2026 · 국내 한국혁신산업학회 2026</span></div></li>',
    '<li class="pp"><i>③</i><div><b>학회 검증 · 특허 출원</b><span>CNN 논문 국내 우수논문상 · 이중 트랙 알고리즘 국제 AIT 2026 · 특허 3건</span></div></li>')
rep(' · RNN 시계열 분석 – INFUTECH 설계</p>', ' · RNN 시계열 분석 – INFUTECH 설계 · AIT 2026 – 「Design of a Dual-Track Algorithm for Real-Time IV Monitoring Based on Load Cell」 · 특허는 이중 트랙 신호처리 대상</p>')
note('s-cnn', ['보정된 신호는 두 가지 AI로 분석합니다. CNN은 16개 상태를 4×4 그림으로 만들어, 고립된 한 칸은 순간 흔들림, 뭉친 덩어리는 지속 이상으로 모양을 봅니다.',
               'RNN은 유속을 순서대로 기억해 점점 느려지거나 멈추는 추세를 봅니다. 두 결과를 종합해 정상, 흔들림, 당겨짐, 줄 분리, 소진 다섯 가지로 판정합니다.',
               '이 CNN 논문은 국내 우수논문상을, 함께 쓰는 이중 트랙 알고리즘은 국제 AIT 우수논문상을 받았고, 특허 3건을 출원하고 있습니다.'])
# ---- s-rivals: human-ward interview labelled as reference
rep('<figcaption>병동 현장 인터뷰</figcaption>', '<figcaption>사람 병원 인터뷰 · 참고</figcaption>')
rep('· 병동 · 전남대 수의과대학 현장 인터뷰(INFUTECH)', '· 사람 병원 · 전남대 수의과대학 현장 인터뷰(INFUTECH)')
# ---- s-entry: distributors, not hospitals; not a contract
note('s-entry', ['현장의 수요는 유통사 약정과 협약으로 확인했습니다. 유통사 두 곳과 공급 약정, 구매의향 협약 1억 100만 원 규모를 맺었고, 전남대 수의과대학과는 실증 LOI를 맺었습니다.',
                 '약정은 KC 인증 후 효력이고 협약은 비구속이라, 확정 매출은 아닙니다.'])
open(DST, 'w', encoding='utf-8').write(s); print('stage3 ok')
# ---- tighten the three longest scripts to keep ~5 syllables/s in 280 s
s = open(DST, encoding='utf-8').read()
note('s-law', ['여기에 기록 부담까지 커집니다. 처치 기록은 이미 수의사법상 의무이고, 진료기록 사본 발급 법안도 농해수위를 통과했습니다. 기록이 있으면 분쟁 해결률도 1.5배 높았습니다.',
               '감시와 기록을 혼자 해야 하는 1인 수의사에게, 먼저 알리고 자동으로 기록하는 장치가 꼭 필요한 이유입니다.'])
note('s-tech', ['핵심 기술입니다. 로드셀 원신호의 잡음을 칼만 필터로 1차로 걸러 내고, 가상 자이로가 로드셀만으로 기울기를 추정하면 PID 제어가 그 오차를 상쇄합니다.',
                '가상 자이로는 자이로를 단 프로세서와 로드셀만 단 프로세서의 편차로 학습했고, PID 게인은 LoRA와 유전 알고리즘으로 자동 튜닝합니다. 이 보정 신호를 다음 단계에서 분석합니다.'])
note('s-cnn', ['보정된 신호는 두 가지 AI로 분석합니다. CNN은 4×4 그림의 모양으로 순간 흔들림과 지속 이상을 가르고, RNN은 유속을 순서대로 기억해 느려지거나 멈추는 추세를 봅니다.',
               '두 결과를 종합해 정상, 흔들림, 당겨짐, 줄 분리, 소진 다섯 가지로 판정합니다. 이 알고리즘들로 국내와 국제 학회에서 우수논문상을 받았습니다.'])
open(DST, 'w', encoding='utf-8').write(s); print('scripts tightened')
TIMES = {'s-opening': 14, 's-hook': 13, 's-background': 15, 's-onevet': 14, 's-law': 24, 's-rivals': 11, 's-field': 25, 's-match': 16, 's-solution': 9, 's-hw': 23, 's-tech': 29, 's-cnn': 27, 's-edge': 16, 's-entry': 20, 's-team': 17, 's-end': 7}
s = open(DST, encoding='utf-8').read()
for k, v in TIMES.items():
    s, n = re.subn(r'(<section [^>]*id="%s"[^>]*data-time=")\d+' % k, r'\g<1>%d' % v, s); assert n == 1, k
open(DST, 'w', encoding='utf-8').write(s); print('timed', sum(TIMES.values()))
