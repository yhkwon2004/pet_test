import re, sys
SRC='/home/user/pet_test/index.html'; DST='/home/user/pet_test/capstone/index.html'
import os; S=os.path.dirname(os.path.abspath(__file__))
s=open(SRC,encoding='utf-8').read()
def sec(id_):
    m=re.search(r'<section [^>]*id="%s"[^>]*>.*?</section>\n'%re.escape(id_), s, re.S); assert m, id_; return m
def get(id_): return sec(id_).group(0)
def put(id_, new):
    global s; m=sec(id_); s=s[:m.start()]+new+s[m.end():]
def drop(id_): put(id_,'')
def rep(a,b,txt):
    assert txt.count(a)==1,(txt.count(a),a[:80]); return txt.replace(a,b)
def setattrs(t, sec_n, time=None, title=None):
    t=re.sub(r'data-sec="\d+"', f'data-sec="{sec_n}"', t, count=1)
    if time is None: t=re.sub(r' data-time="\d+"','',t,count=1)
    else: t=re.sub(r'data-time="\d+"', f'data-time="{time}"', t, count=1)
    if title: t=re.sub(r'data-title="[^"]*"', f'data-title="{title}"', t, count=1)
    return t
def note(t, paras):
    return re.sub(r'<div class="note" hidden>.*?</div>', '<div class="note" hidden>'+''.join(f'<p>{p}</p>' for p in paras)+'</div>', t, count=1, flags=re.S)
APPX=12
# ---------- drop business / law slides
for d in ['s-demand','s-compare','s-paper','s-bm','s-market','s-path','s-plan','s-funding','s-invest','s-future','s-ax-mkt','s-ax-swot','s-ax-risk']: drop(d)
# ---------- cover
t=get('s-opening')
t=rep('<p class="r-cv-k b">반려동물 약물투약 사고를 방지하기 위한 이상감지 솔루션</p>','<p class="r-cv-cap b">2026 캡스톤 디자인</p>\n        <p class="r-cv-k b">동물병원 입원실 수액 이상감지 솔루션</p>',t)
t=setattrs(t,0,16,'2026 캡스톤 디자인 — 동물병원 입원실 수액 이상감지 솔루션')
t=note(t,['안녕하십니까, 2026 캡스톤 디자인 팀 WON SHOT입니다.','저희가 만든 INFU RETRO는 자이로 센서를 AI로 구현한 하중센서 모듈로, 동물병원 입원실의 수액 이상을 감지합니다.'])
put('s-opening',t)
# ---------- hook
t=get('s-hook'); t=setattrs(t,0,16)
t=note(t,['먼저 질문 하나 드리겠습니다. 전국 동물병원은 5,312곳입니다.','입원실 수액 카테터, 몇 개 중 하나꼴로 사고가 날까요? 100개 중 1개, 20개 중 1개, 아니면 4개 중 1개일까요?'])
put('s-hook',t)
# ---------- background -> 순회 사이 공백
gap_svg=open(f'{S}/gap.svg').read()
t=f'''<section class="slide rf " id="s-background" data-sec="1" data-time="20" data-title="정답은 4개 중 1개 — 사고는 순회와 순회 사이에서 납니다">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Pain Point ① · 순회 사이 공백</p><h2 class="r-t b">정답은 <em>4개 중 1개</em>, 그런데 사고는 <em>순회와 순회 사이</em>에서 납니다</h2></header>
    <div class="r-2 cp-gap b">
      <div class="r-card r-pc cp-pie"><div class="r-pie" style="--p:26.7"><span>정답 C</span></div><p class="r-cap"><span>26.7%</span> 카테터 합병증</p><p class="r-src">Haskey 2024 · 영국 19개 기관 · 정맥염 포함</p></div>
      <div class="r-card cp-tl"><p class="r-ct">순회 확인만으로는 <b>사고 순간</b>을 볼 수 없습니다 <span>예시</span></p>{gap_svg}<p class="r-src">AAHA 2024 · 수액은 1~2시간마다 눈금 확인 권고 → 그 사이에 생긴 이상은 다음 순회에서야 발견</p></div>
    </div>
    <p class="r-foot b">이 중 <b>빠짐 · 막힘 · 꼬임</b>은 수액 무게가 줄어드는 속도에 나타납니다 · 정맥염은 대상 아님</p>
  </div>
  <div class="note" hidden><p>정답은 C, 4개 중 1개입니다. 영국 19개 기관 연구에서 카테터 합병증은 26.7퍼센트였습니다.</p><p>문제는 발견 시점입니다. 수액은 1~2시간마다 눈금을 확인하도록 권고되지만, 그 사이에 줄이 빠지거나 막히면 다음 순회 때까지 아무도 모릅니다.</p></div>
</section>
'''
put('s-background',t)
# ---------- new: 1인 수의사 구조 (insert after background)
onevet=f'''<section class="slide rf " id="s-onevet" data-sec="2" data-time="20" data-title="10곳 중 7곳은 수의사 1명 — 진료하는 동안 입원실은 비어 있습니다">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Pain Point ② · 1인 수의사 구조</p><h2 class="r-t b">10곳 중 7곳은 <em>수의사 1명</em> — 진료하는 동안 입원실은 비어 있습니다</h2></header>
    <div class="r-2 cp-one b">
      <div class="r-card r-pc cp-pie"><div class="r-pie" style="--p:71.8"></div><p class="r-cap"><span>10곳 중 7곳</span> 수의사 1명</p><p class="r-src">농식품부 2025.6 · 전국 동물병원 5,312곳 중 3,815곳</p></div>
      <div class="r-card cp-day">
        <p class="r-ct">수의사 1명이 동시에 맡는 일 <span>예시</span></p>
        <ul class="cp-tasks">
          <li><i><svg viewBox="0 0 48 48"><path d="M10 40V18l14-9 14 9v22z" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linejoin="round"/><path d="M24 20v12M18 26h12" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/></svg></i><b>외래 진료</b></li>
          <li><i><svg viewBox="0 0 48 48"><path d="M12 36l20-20M28 12l8 8M10 38l4-4" fill="none" stroke="currentColor" stroke-width="3.4" stroke-linecap="round"/><circle cx="34" cy="14" r="4" fill="none" stroke="currentColor" stroke-width="3"/></svg></i><b>수술 · 처치</b></li>
          <li><i><svg viewBox="0 0 48 48"><path d="M8 12h24v16H18l-8 7v-7H8z" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linejoin="round"/><path d="M36 20h4v14h-2v5l-6-5H22" fill="none" stroke="currentColor" stroke-width="3" stroke-linejoin="round"/></svg></i><b>보호자 상담</b></li>
          <li class="iv"><i><svg viewBox="0 0 48 48"><rect x="16" y="6" width="16" height="22" rx="5" fill="none" stroke="currentColor" stroke-width="3.2"/><path d="M24 28v8M24 36c0 4 6 4 6 8" fill="none" stroke="currentColor" stroke-width="3.2" stroke-linecap="round"/></svg></i><b>입원실 수액 확인</b><small>틈날 때만</small></li>
        </ul>
        <div class="cp-res"><p>진료 · 수술 중엔 입원실을 볼 수 없음</p><i>→</i><p>순회 간격은 길어지고</p><i>→</i><p class="r">사고는 늦게 발견</p></div>
      </div>
    </div>
    <p class="r-foot b">사람이 계속 지켜볼 수 없다면, <b>이상이 생긴 순간 먼저 알려 주는 장치</b>가 필요합니다</p>
  </div>
  <div class="note" hidden><p>더 큰 문제는 구조입니다. 전국 동물병원 10곳 중 7곳은 수의사가 1명입니다.</p><p>한 사람이 진료와 수술, 보호자 상담을 하면서 입원실까지 봐야 하니, 순회 간격은 길어지고 사고는 늦게 발견됩니다. 계속 지켜볼 수 없다면, 이상이 생긴 순간 먼저 알려 주는 장치가 필요합니다.</p></div>
</section>
'''
m=sec('s-background'); s=s[:m.end()]+onevet+s[m.end():]
# ---------- rivals
t=get('s-rivals'); t=setattrs(t,3,20)
t=note(t,['지금 쓸 수 있는 장비는 비싸거나, 바꿔야 하거나, 거부감이 있습니다.','인퓨전펌프는 1줄에 110만 원, 스마트 폴대는 300만 원이 넘고 폴대째 바꿔야 합니다. 방울 감지는 오차가 크고, CCTV는 거부감이 큽니다.'])
put('s-rivals',t)
# ---------- field
t=get('s-field'); t=setattrs(t,4,22)
t=note(t,['그래서 MVP를 들고 전북 병원 10곳, 호남권 반려동물병원 16곳, 모두 26곳을 찾았습니다.','병원이 원한 건 비싼 새 장비가 아니라, 쓰던 폴대 그대로 알림과 기록만 디지털로 바꾸는 것이었습니다. 시연하고, 고치고, 다시 찾아간 결과가 지금의 제품입니다.'])
put('s-field',t)
# ---------- match
t=get('s-match'); t=setattrs(t,5,20)
t=note(t,['그래서 만든 것이 INFU RETRO입니다. 쓰던 표준 폴대 위에 끼우기만 하면 됩니다.','갈고리마다 로드셀이 하나씩 달려 수액백 4개를 동시에 재고, 줄 분리와 소진은 5초 안에 휴대폰으로 알립니다. 알림과 조치 시각은 자동으로 기록됩니다.'])
put('s-match',t)
# ---------- solution
t=get('s-solution'); t=setattrs(t,5,18)
t=rep('<b>기록 예시 · 1인 병원 야간</b>','<b>기록 예시 · 1인 병원</b>',t)
t=note(t,['사용법은 간단합니다. 폴대에 끼우고 수액백을 걸면 됩니다. 영상은 2.5배속입니다.','줄이 분리되자 원장님 휴대폰으로 알림이 갔고, 재연결 시각까지 기록이 남습니다.'])
put('s-solution',t)
# ---------- new: HW design (after solution)
hw=f'''<section class="slide rf " id="s-hw" data-sec="6" data-time="20" data-title="구조 · PCB 설계 — 폴대 교체 없이 끼우고, 칩이 빠르게 읽도록">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Design · 구조 · PCB 설계</p><h2 class="r-t b">폴대 교체 없이 끼우고, <em>칩이 빠르게 읽도록</em> 설계했습니다</h2></header>
    <ol class="cp-hw b">
      <li><figure><img src="media/hanger-real.webp" alt="기존 링거폴대 상단에 결합한 INFU RETRO 모듈 실물" decoding="async" data-zoom></figure><i>01</i><b>스크류 · 마그네틱 결합</b><p>기존 폴대 상단에 조립 · <em>폴대 교체 없음</em></p></li>
      <li><figure><img src="media/hanger-drawing.webp" alt="체결부 · 로드셀 · 걸이부로 이어지는 모듈 설계 도면" decoding="async" data-zoom></figure><i>02</i><b>일직선 하중 구조</b><p>체결부 – <em>로드셀</em> – 걸이부 · 갈고리마다 1개</p></li>
      <li><figure><img src="media/pcb-layout.webp" alt="24비트 로드셀 전용 ADC를 올린 PCB 설계 레이아웃" decoding="async" data-zoom></figure><i>03</i><b>24비트 로드셀 전용 ADC</b><p>전원 분리 · RC 필터 → <em>방울 단위에 가까운</em> 변화</p></li>
      <li><div class="cp-arr"><span class="g4">{''.join('<b class="%s"></b>'%c for c in 'zpzmpzzzzmpzmzzp')}</span><p>로드셀 값 16개 → 4×4 배열</p></div><i>04</i><b>4×4 배열로 받아 처리</b><p>단일 로드셀 값을 묶어 <em>ESP32가 빠르게</em> 판정</p></li>
    </ol>
    <p class="r-src c b">결합 구조 · 4×4 배열 처리 – INFUTECH 설계 · 24비트 ADC · 전원 분리 · RC 필터 – INFUTECH 발명신고서(2026)</p>
  </div>
  <div class="note" hidden><p>하드웨어는 두 가지에 집중했습니다. 먼저 구조입니다. 스크류와 마그네틱으로 기존 폴대 상단에 조립하고, 체결부와 로드셀, 걸이부가 일직선으로 하중을 받습니다.</p><p>PCB에는 24비트 로드셀 전용 ADC와 전원 분리, RC 필터를 넣었고, 단일 로드셀 값을 4×4 배열로 묶어 ESP32가 빠르게 판정하도록 설계했습니다.</p></div>
</section>
'''
m=sec('s-solution'); s=s[:m.end()]+hw+s[m.end():]
# ---------- tech
t=get('s-tech'); t=setattrs(t,7,24)
t=note(t,['핵심 기술은 가상 AI 자이로입니다. 같은 흔들림을 로드셀과 자이로를 단 프로세서 A, 로드셀만 단 프로세서 B가 동시에 기록하고, 두 값의 편차를 정답으로 지도학습했습니다.','그래서 제품에는 자이로 없이 로드셀 하나만 넣고도 흔들림을 보정합니다. 모델은 약 660개 파라미터, 10KB로 ESP32 안에서 돌아갑니다.'])
put('s-tech',t)
# ---------- new: CNN (after tech)
cnn_svg=open(f'{S}/cnn-cap.svg').read()
cnn=f'''<section class="slide rf " id="s-cnn" data-sec="7" data-time="24" data-title="4×4 상태 패턴을 경량 2D CNN으로 — 학회에서 검증한 감지 알고리즘">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Algorithm · 논문 · 특허</p><h2 class="r-t b">16번 잰 결과를 <em>4×4 그림</em>으로 — 경량 2D CNN이 판정합니다</h2></header>
    <div class="r-card cp-cnn b">{cnn_svg}</div>
    <ul class="cp-why b">
      <li><i>①</i><div><b>흔들림과 이상을 '모양'으로 구분</b><span>순간 흔들림은 고립된 한 칸, 지속 이상은 뭉친 덩어리</span></div></li>
      <li><i>②</i><div><b>칩 안에서 바로 실행</b><span>파라미터 659개 · 약 10KB · ESP32</span></div></li>
      <li class="pp"><i>③</i><div><b>우수논문 2편 · 특허 출원 3건</b><span>국제 AIT 2026 · 국내 한국혁신산업학회 2026</span></div></li>
    </ul>
    <p class="r-src c b">모델 구조 · 총 파라미터(약 660개) – 한우진 외, 「상태 패턴 분석 기반 수액 이상 감지 알고리즘」 · 패딩 · 층별 파라미터는 총 파라미터에서 역산 · ①은 설계 근거(정성)</p>
  </div>
  <div class="note" hidden><p>판정은 경량 2D CNN이 합니다. 기준 유속 대비 편차를 느림, 정상, 빠름으로 부호화하고, 연속 16개 상태를 4×4 그림으로 만듭니다.</p><p>순간 흔들림은 고립된 한 칸, 지속되는 이상은 뭉친 덩어리로 나타나 모양으로 구분됩니다. 파라미터 659개, 약 10KB라 칩 안에서 바로 판정하고, 이 알고리즘으로 우수논문 2편과 특허 3건을 냈습니다.</p></div>
</section>
'''
m=sec('s-tech'); s=s[:m.end()]+cnn+s[m.end():]
# ---------- edge
t=get('s-edge'); t=setattrs(t,8,18)
t=note(t,['원광대 간호학과 모의 병실에서 1,000회를 시험했습니다. 흔들고 당겨도 잔량 오차는 3퍼센트 이내였습니다.','정상 중 오경보는 17분의 1로 줄었고, 줄 분리와 소진은 250번 모두 평균 2.8초에 판정했습니다.'])
put('s-edge',t)
# ---------- entry
t=get('s-entry'); t=setattrs(t,9,18,'현장의 답 — 약정 · 협약 1억 100만 원으로 수요를 확인했습니다')
t=rep('<h2 class="r-t b"><em>약정 · 협약</em>으로 가설을 검증했고, 1등급 신고 경로로 들어갑니다</h2>','<p class="r-kick b">Demand · 수요 검증</p><h2 class="r-t b">현장의 답 — <em>약정 · 협약 1억 100만 원</em>으로 수요를 확인했습니다</h2>',t)
t=note(t,['현장의 수요는 계약으로 확인했습니다. 유통사 ㈜씨엔과 5,100만 원 공급 약정, ㈜에스케이엠엔엠과 5,000만 원 구매의향 협약을 맺었고, 전남대 수의과대학과는 실증 LOI를 맺었습니다.','약정은 KC 인증 후 효력이고 협약은 비구속이라 확정 매출은 아닙니다.'])
put('s-entry',t)
# ---------- team / end
t=get('s-team'); t=setattrs(t,10,14)
t=note(t,['저희는 개발팀 5명과 임상 실증팀 2명, 두 축으로 움직입니다. 전남대 수의과대학과 원광대 간호학과가 실증을, 유통사 두 곳이 판로를 함께합니다.'])
put('s-team',t)
t=get('s-end'); t=setattrs(t,11,8)
t=rep('<p class="r-st-s b">WON SHOT · 감사합니다</p>','<p class="r-st-s b">2026 캡스톤 디자인 · WON SHOT · 감사합니다</p>',t)
t=note(t,['폴대는 그대로, 수액은 놓치지 않게. 지금까지 팀 WON SHOT이었습니다. 감사합니다.'])
put('s-end',t)
# ---------- appendix: renumber, move internal test report to appendix
for aid in ['s-kpi','s-ax-cost','s-ax-target','s-ax-field','s-ax-field2','s-ax-docs','s-ax-paper','s-ax-hw','s-ax-hw2']:
    t=get(aid); t=setattrs(t,APPX); put(aid,t)
t=get('s-a-test'); t=setattrs(t,APPX,None,'부록 — 내부 시험 성적서 · 모의 병실 1,000회')
t=t.replace('class="slide rf"','class="slide rf appx"',1); m=sec('s-a-test'); s=s[:m.start()]+s[m.end():]
k=s.index('<section class="slide rf appx" id="s-kpi"'); s=s[:k]+t+s[k:]
# ---------- sections / meta
s=re.sub(r"const SECTIONS = \[.*?\];", "const SECTIONS = ['오프닝', '문제 ① 순회 사이 공백', '문제 ② 1인 수의사 구조', '기존 장비의 한계', '현장 수요', '제품 소개', '구조 · PCB 설계', '핵심 기술 · 알고리즘', '시험 · 검증', '수요 검증', '팀', '클로징', '부록'];", s, flags=re.S)
s=re.sub(r'<title>.*?</title>','<title>INFU RETRO — 2026 캡스톤 디자인</title>',s,count=1)
s=re.sub(r'<meta name="description" content="[^"]*">','<meta name="description" content="2026 캡스톤 디자인 · 팀 WON SHOT — 동물병원 입원실 수액 이상감지 솔루션 INFU RETRO 발표 자료">',s,count=1)
s=re.sub(r'<p>19장 \+ 부록 A1 · 대본 4분 30초 · STARTRUN Flow 20 Step 구성</p>','<p>본문 15장 + 부록 · 대본 약 4분 40초 · 2026 캡스톤 디자인</p>',s)
s=re.sub(r'<meta name="pptx-title" content="[^"]*">','<meta name="pptx-title" content="INFU RETRO — 2026 캡스톤 디자인">',s)
# ---------- CSS
css=open(f'{S}/cap.css').read()
s=s.replace('</head>', f'<style id="cap-css">\n{css}\n</style>\n</head>',1)
open(DST,'w',encoding='utf-8').write(s)
print('sections:', len(re.findall(r'<section class="slide',s)), 'main time:', sum(int(x) for x in re.findall(r'data-time="(\d+)"',s)))
# ---------- per-slide timing from the spoken script (stime.py, 280 s total)
TIMES={'s-opening':15,'s-hook':14,'s-background':20,'s-onevet':22,'s-rivals':17,'s-field':21,'s-match':19,'s-solution':14,'s-hw':27,'s-tech':27,'s-cnn':28,'s-edge':17,'s-entry':21,'s-team':12,'s-end':6}
s=open(DST,encoding='utf-8').read()
for k,v in TIMES.items():
    s,n=re.subn(r'(<section [^>]*id="%s"[^>]*data-time=")\d+'%k, r'\g<1>%d'%v, s); assert n==1,k
open(DST,'w',encoding='utf-8').write(s)
print('timed', sum(TIMES.values()))
