# Stage 7: two slides at the very front of the appendix
#   s-ax-mkt3  시장 규모 TAM · SAM · SOM + 호남 → 전국 → 해외 확장 계획
#   s-ax-cust  타겟 고객 B2B · B2G — 대형병원 / 1인 동물병원 / 공공
# Figures follow the IR deck's market slide (IMARC 2025 · GIA · 농식품부 2025.6) and the deck's own facts.
DST = '/home/user/pet_test/capstone/index.html'
s = open(DST, encoding='utf-8').read()

MKT = '''<section class="slide rf appx" id="s-ax-mkt3" data-sec="12" data-title="부록 — 시장 규모 TAM · SAM · SOM · 확장 계획">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Appendix · 시장 규모</p><h2 class="r-t b">호남에서 시작해 <em>전국, 그리고 해외</em>로</h2></header>
    <div class="mk-wrap b">
      <div class="mk-nest">
        <div class="t"><p>TAM</p><b>69조 원</b><span>세계 동물 의료시장<br>USD 495억 · 2025</span></div>
        <div class="s"><p>SAM</p><b>4,400억 원</b><span>세계 동물용 인퓨전펌프<br>USD 3.15억</span></div>
        <div class="o"><p>SOM</p><b>316억 원</b><span>국내 동물병원 5,312곳</span></div>
      </div>
      <ol class="mk-road">
        <li class="on"><i>1</i><div><time>지금 · 1차 시장</time><b>호남권 — 전남 · 전북</b><p>동물병원 약 300곳 · 18억 원</p><p>전남대 수의과대학 실증 · 대학 · 액셀러레이터 인프라</p><p class="k">약정 · 협약 1억 100만 원 → 다음 목표 4.5억 원</p></div></li>
        <li><i>2</i><div><time>2030~ · 2차 시장</time><b>전국 확장</b><p>동물병원 5,312곳 · 316억 원</p><p>실증 데이터 · 학회 · 유통사 2곳 전국 판로</p></div></li>
        <li><i>3</i><div><time>수출 인증 후 · 3차 시장</time><b>해외 확장</b><p>세계 동물용 인퓨전펌프 4,400억 원</p><p>USD 3.15억 → 4.67억(2032, 연 5.8%)</p></div></li>
      </ol>
    </div>
    <p class="r-src c b">TAM – IMARC 세계 동물 의료(Veterinary Healthcare) 시장 2025 · SAM – GIA 세계 동물용 인퓨전펌프 · SOM = 동물병원 5,312곳(농식품부 2025.6) × 5대 × (35만 + 구독 84만) 상한 · 1달러 1,400원</p>
  </div>
  <div class="note" hidden><p>시장 규모입니다. 전체 시장은 세계 동물 의료시장 69조 원, 저희가 직접 겨냥하는 세계 동물용 인퓨전펌프 시장이 4,400억 원, 국내 동물병원 5,312곳이 316억 원입니다.</p><p>첫 진입은 호남권 전남 · 전북 약 300곳, 18억 원 시장이고, 2030년부터 전국으로, 수출 인증 뒤에는 해외로 확장합니다.</p></div>
</section>
'''

CUST = '''<section class="slide rf appx" id="s-ax-cust" data-sec="12" data-title="부록 — 타겟 고객 B2B · B2G">
  <div class="frame">
    <header class="r-hd"><p class="r-kick b">Appendix · 타겟 고객</p><h2 class="r-t b">B2B · B2G — <em>병원 규모마다 다른 가치</em>를 드립니다</h2></header>
    <div class="cxr b">
      <div class="cxc cxa">
        <p class="cxt">B2B · 대형 동물병원</p><b>여러 케이지 · 여러 동물을<br>한 화면에서</b>
        <ul><li><em>문제</em>입원 케이지가 많아 순회만으로는 동시 관리가 어려움</li>
            <li><em>가치</em>폴대 1대에 수액백 4개 동시 측정 · 케이지별 대시보드</li>
            <li><em>가치</em>스테이션 · 휴대폰 통합 알림 — 어느 케이지인지 바로 확인</li></ul>
        <div class="cxk"><b>4</b><span>수액백 동시 측정 / 폴대 1대<br>케이지 수만큼 확장</span></div>
        <p class="cxp">다수 관리 편의성 · 야간 인력 효율</p></div>
      <div class="cxc cxb">
        <p class="cxt">B2B · 1인 동물병원</p><b>진료 중에도 입원실을<br>대신 지켜봅니다</b>
        <ul><li><em>문제</em>수의사 1명이 진료 · 수술 · 입원실을 혼자 — 전국 10곳 중 7곳</li>
            <li><em>가치</em>알림 · 조치 시각 자동 기록 → 진료부 첨부 (수의사법 제13조 기록 의무)</li>
            <li><em>가치</em>줄 분리 · 소진 5초 안에 판정 → 사고 예방</li></ul>
        <div class="cxk"><b>5초</b><span>줄 분리 · 소진 기기 판정<br>평균 2.8초 · 250/250 감지</span></div>
        <p class="cxp">기록 편의성 · 사고 예방</p></div>
      <div class="cxc cxg">
        <p class="cxt">B2G · 공공</p><b>국립대 동물병원 ·<br>지자체 동물보호센터</b>
        <ul><li><em>문제</em>보호 · 입원 동물은 많고 관리 인력은 한정</li>
            <li><em>가치</em>실증 데이터 · 표준 기록으로 공공 관리 품질 향상</li>
            <li><em>근거</em>전남대 수의과대학 실증 LOI</li></ul>
        <div class="cxk"><b>LOI</b><span>전남대 수의과대학<br>수의 임상 실증 협의</span></div>
        <p class="cxp">실증 · 공공 조달 연계</p></div>
    </div>
    <p class="cxf b">공통 · 쓰던 폴대에 끼우기만 — 35만 원 구매 + 선택 구독 월 7만 원</p>
    <p class="r-src c b">1인 병원 비율 – 농식품부 2025.6(5,312곳 중 3,815곳) · 기록 의무 – 수의사법 제13조 · 판정 시간 – 내부 모의시험 · 가격 – INFUTECH 사업계획서</p>
  </div>
  <div class="note" hidden><p>타겟 고객은 B2B와 B2G입니다. 대형 동물병원에는 여러 케이지와 여러 동물을 한 화면에서 관리하는 편의성을, 1인 동물병원에는 기록 자동화와 사고 예방을 드립니다.</p><p>공공 부문에서는 국립대 동물병원과 지자체 동물보호센터를 대상으로, 전남대 수의과대학 실증 LOI를 근거로 확장합니다.</p></div>
</section>
'''

anchor = '<section class="slide rf appx" id="s-a-test"'
assert s.count(anchor) == 1
s = s.replace(anchor, MKT + CUST + anchor, 1)

CSS = '''
/* appendix: market size + target customers */
#s-ax-mkt3 .mk-wrap { flex: 1; min-height: 0; display: grid; grid-template-columns: 1fr 1.1fr; gap: 3em; align-items: center; }
#s-ax-mkt3 .mk-nest { position: relative; justify-self: center; width: 31em; height: 31em; }
#s-ax-mkt3 .mk-nest > div { position: absolute; left: 50%; bottom: 0; transform: translateX(-50%); border-radius: 50%; display: flex; flex-direction: column; align-items: center; text-align: center; }
#s-ax-mkt3 .mk-nest .t { width: 31em; height: 31em; background: #EEF2F8; padding-top: 2.6em; color: #1E3A8A; }
#s-ax-mkt3 .mk-nest .s { width: 21em; height: 21em; background: #D6E2F7; padding-top: 2.2em; color: #1E3A8A; }
#s-ax-mkt3 .mk-nest .o { width: 12em; height: 12em; background: linear-gradient(160deg, #2F5BD3, #1E3A8A); justify-content: center; color: #FFFFFF; }
#s-ax-mkt3 .mk-nest p { font-size: 1em; font-weight: 800; letter-spacing: .14em; }
#s-ax-mkt3 .mk-nest b { font-size: 2.5em; font-weight: 850; letter-spacing: -.03em; line-height: 1.15; }
#s-ax-mkt3 .mk-nest .o b { font-size: 2.1em; }
#s-ax-mkt3 .mk-nest span { margin-top: .2em; font-size: .95em; font-weight: 600; line-height: 1.35; opacity: .85; }
#s-ax-mkt3 .mk-road { list-style: none; display: flex; flex-direction: column; gap: 1.2em; }
#s-ax-mkt3 .mk-road li { display: grid; grid-template-columns: 2.4em 1fr; gap: 1em; padding: 1.1em 1.5em; border-radius: 1em; border: 1px solid #E3E8F0; background: #FFFFFF; }
#s-ax-mkt3 .mk-road li.on { border-color: #1E3A8A; box-shadow: 0 .8em 2em rgba(30, 58, 138, .12); }
#s-ax-mkt3 .mk-road i { font-style: normal; width: 1.7em; height: 1.7em; border-radius: 50%; background: #1E3A8A; color: #FFFFFF; display: grid; place-items: center; font-size: 1.2em; font-weight: 800; }
#s-ax-mkt3 .mk-road li:not(.on) i { background: #8FA3CC; }
#s-ax-mkt3 .mk-road time { font-size: .95em; font-weight: 750; color: #0E7490; }
#s-ax-mkt3 .mk-road b { display: block; margin-top: .1em; font-size: 1.55em; font-weight: 850; color: #111418; }
#s-ax-mkt3 .mk-road p { margin-top: .2em; font-size: 1.05em; font-weight: 550; color: #3F4651; }
#s-ax-mkt3 .mk-road p.k { margin-top: .4em; font-weight: 800; color: #1E3A8A; }
#s-ax-cust .cxr { flex: 1; min-height: 0; display: grid; grid-template-columns: repeat(3, 1fr); gap: 1.4em; }
#s-ax-cust .cxc { display: flex; flex-direction: column; padding: 1.6em 1.6em 1.4em; border-radius: 1em; border: 1px solid #E3E8F0; background: #FFFFFF; }
#s-ax-cust .cxc .cxt { align-self: flex-start; padding: .25em .8em; border-radius: 99em; font-size: .95em; font-weight: 800; color: #FFFFFF; background: #1E3A8A; }
#s-ax-cust .cxc.cxg .cxt { background: #0E7490; }
#s-ax-cust .cxc > b { margin-top: .7em; font-size: 1.6em; font-weight: 850; line-height: 1.3; color: #111418; letter-spacing: -.02em; }
#s-ax-cust .cxc ul { list-style: none; margin-top: 1em; display: grid; gap: .7em; }
#s-ax-cust .cxc li { font-size: 1.05em; font-weight: 550; color: #3F4651; line-height: 1.45; }
#s-ax-cust .cxc li em { font-style: normal; display: inline-block; margin-right: .5em; padding: 0 .45em; border-radius: .3em; font-size: .85em; font-weight: 800; color: #1E3A8A; background: #E6EEFF; }
#s-ax-cust .cxc .cxp { margin-top: auto; padding-top: 1em; border-top: 1px solid #E3E8F0; font-size: 1.2em; font-weight: 850; color: #1E3A8A; }
#s-ax-cust .cxc.cxg .cxp { color: #0E7490; }
#s-ax-cust .cxk { margin-top: auto; display: flex; align-items: center; gap: .8em; padding: 1em 1.1em; border-radius: .8em; background: #F4F7FB; }
#s-ax-cust .cxk b { font-size: 2.6em; font-weight: 850; color: #1E3A8A; letter-spacing: -.04em; line-height: 1; }
#s-ax-cust .cxg .cxk b { color: #0E7490; }
#s-ax-cust .cxk span { font-size: .98em; font-weight: 600; color: #3F4651; line-height: 1.4; }
#s-ax-cust .cxc .cxp { margin-top: 1em; }
#s-ax-cust .cxf { margin-top: 1.1em; text-align: center; font-size: 1.2em; font-weight: 750; color: #111418; }
'''
s = s.replace('</head>', f'<style id="cap-appx-mkt">{CSS}</style>\n</head>', 1)
open(DST, 'w', encoding='utf-8').write(s)
print('appendix market + customers ok')
