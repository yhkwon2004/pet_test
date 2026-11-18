# Slide 11 — the corrected signal analysed two ways: CNN (4×4 shape) + RNN (time trend) → combined decision (5 states)
import sys, math
from mathtxt import M
RI, RI2, RP, RL, RK, RK2, RM, RLN, RY, RR, GN, OR = '#4B48E0', '#7471F0', '#AEB2FB', '#ECEBFE', '#1D1C2B', '#4A4A5C', '#8B8B9C', '#DCDCE6', '#FFD84D', '#F0506E', '#2E9E6A', '#E07B2E'
W, H = 1700, 716
O = []; A = O.append
def t(x, y, s, fs=17, fw=700, col=RK2, anc='start'):
    A(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="{fw}" fill="{col}" text-anchor="{anc}">{s}</text>')
def arrow(pts, col=RI, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    A(f'<path d="M{" L".join(f"{x:.0f} {y:.0f}" for x, y in pts)}" stroke="{col}" stroke-width="3" fill="none" stroke-linejoin="round" stroke-linecap="round" marker-end="url(#a2a)"{d}/>')
SUB = lambda c: f'<tspan font-size="13" baseline-shift="sub">{c}</tspan>'
# ---- input
A(f'<rect x="0" y="200" width="210" height="160" rx="20" fill="url(#a2g)"/>')
t(20, 236, '10장 출력', 15, 800, '#E5E4FF'); t(20, 272, '보정 하중 w(t)', 22, 900, '#FFFFFF'); t(20, 304, '유속 v(t)', 22, 900, '#FFFFFF')
pts = ' L'.join(f'{20 + i * 2.4:.1f} {338 + math.sin(i / 6) * 6:.1f}' for i in range(72))
A(f'<path d="M{pts}" stroke="{RY}" stroke-width="2.6" fill="none"/>')
YA, YBn = 120, 430   # lane centres
arrow([(214, 260), (244, 260), (244, YA), (262, YA)]); arrow([(214, 300), (244, 300), (244, YBn), (262, YBn)])
# ---- lane A: CNN
A(f'<rect x="266" y="{YA - 104}" width="960" height="208" rx="22" fill="#FFFFFF" stroke="{RLN}" stroke-width="1.6"/>')
A(f'<rect x="286" y="{YA - 88}" width="74" height="28" rx="14" fill="{RI}"/>'); t(323, YA - 68, 'CNN', 16, 900, '#FFFFFF', 'middle')
t(372, YA - 67, '순간 패턴 = 모양으로 분석', 18, 850, RK)
# encode chip
A(f'<rect x="286" y="{YA - 40}" width="190" height="120" rx="14" fill="{RL}"/>')
t(381, YA - 10, '상태 부호화', 17, 850, RI, 'middle')
for k, (lab, col) in enumerate((('−1 느림', RP), ('0 정상', '#FFFFFF'), ('+1 빠름', RI))):
    A(f'<rect x="{298 + k * 58}" y="{YA + 8}" width="52" height="56" rx="8" fill="{col}" stroke="{RP}" stroke-width="1.2"/>')
    t(324 + k * 58, YA + 32, lab.split()[0], 16, 900, '#FFFFFF' if col == RI else RK, 'middle'); t(324 + k * 58, YA + 54, lab.split()[1], 13, 700, '#FFFFFF' if col == RI else RK2, 'middle')
arrow([(480, YA + 20), (512, YA + 20)])
# 4x4 grid
pat = '00--0---00------'; gx, gy, c = 518, YA - 40, 30
for k, ch in enumerate(pat):
    r, q = divmod(k, 4)
    col = {'-': RI, '+': RP, '0': '#EFEFF4'}[ch]
    A(f'<rect x="{gx + q * c}" y="{gy + r * c}" width="{c - 4}" height="{c - 4}" rx="4" fill="{col}"/>')
t(gx + 58, YA + 98, '4×4 패턴', 15, 800, RK2, 'middle')
arrow([(642, YA + 20), (676, YA + 20)])
# conv stack
for i in range(5, -1, -1):
    A(f'<rect x="{682 + i * 7}" y="{YA - 30 - i * 7}" width="96" height="96" fill="#DCDBFB" stroke="{RI2}" stroke-width="1.3"/>')
t(756, YA + 98, 'Conv2D 3×3 · 8', 15, 800, RK2, 'middle')
arrow([(830, YA + 20), (862, YA + 20)])
for i in range(5, -1, -1):
    A(f'<rect x="{868 + i * 6}" y="{YA - 6 - i * 6}" width="50" height="50" fill="{RL}" stroke="{RI2}" stroke-width="1.3"/>')
t(912, YA + 98, 'MaxPool 2×2', 15, 800, RK2, 'middle')
arrow([(958, YA + 20), (990, YA + 20)])
for k in range(5):
    A(f'<circle cx="1010" cy="{YA - 44 + k * 26}" r="9" fill="{GN}"/>')
t(1010, YA + 98, 'Dense 16', 15, 800, RK2, 'middle')
t(1048, YA - 30, '고립 칸', 15, 800, RK2); t(1048, YA - 10, '= 순간 흔들림', 15, 700, RM)
t(1048, YA + 22, '뭉친 덩어리', 15, 800, RR); t(1048, YA + 42, '= 지속 이상', 15, 700, RM)
# ---- lane B: RNN
A(f'<rect x="266" y="{YBn - 104}" width="960" height="208" rx="22" fill="#FFFFFF" stroke="{RLN}" stroke-width="1.6"/>')
A(f'<rect x="286" y="{YBn - 88}" width="74" height="28" rx="14" fill="{OR}"/>'); t(323, YBn - 68, 'RNN', 16, 900, '#FFFFFF', 'middle')
t(372, YBn - 67, '시간 흐름 = 추세로 분석', 18, 850, RK)
labs = [f'v{SUB("1")}', f'v{SUB("2")}', f'v{SUB("3")}', '…', f'v{SUB("t")}']
hx = [330, 470, 610, 740, 860]
for k, (x, lab) in enumerate(zip(hx, labs)):
    if lab == '…':
        t(x, YBn + 6, '…', 26, 900, RM, 'middle'); continue
    A(f'<rect x="{x - 30}" y="{YBn + 42}" width="60" height="36" rx="10" fill="#FFF4EA" stroke="{OR}" stroke-width="1.4"/>'); t(x, YBn + 66, lab, 16, 850, '#A04E10', 'middle')
    arrow([(x, YBn + 40), (x, YBn + 22)], OR)
    A(f'<rect x="{x - 40}" y="{YBn - 30}" width="80" height="50" rx="12" fill="{OR}"/>'); t(x, YBn + 2, f'h{SUB(lab[1] if lab[0]=="v" and len(lab)<3 else lab.split(">")[1][0])}', 18, 900, '#FFFFFF', 'middle')
for a, b in ((330, 470), (470, 610), (610, 714), (766, 860)):
    arrow([(a + 42, YBn - 5), (b - 44, YBn - 5)], OR)
t(1048, YBn - 30, '점점 느려짐', 15, 800, RK2); t(1048, YBn - 10, '멈춤 · 급감 추세', 15, 800, RK2)
t(1048, YBn + 22, '순서대로 기억해', 15, 700, RM); t(1048, YBn + 42, '변화를 판단', 15, 700, RM)
arrow([(902, YBn - 5), (1036, YBn - 5)], OR) if False else None
# ---- merge + outputs
arrow([(1228, YA), (1262, YA), (1262, 268), (1290, 268)]); arrow([(1228, YBn), (1262, YBn), (1262, 292), (1290, 292)], OR)
A(f'<rect x="1296" y="214" width="150" height="132" rx="20" fill="url(#a2g)"/>')
t(1371, 264, '종합 판정', 21, 900, '#FFFFFF', 'middle'); t(1371, 292, 'Softmax', 15, 800, '#E5E4FF', 'middle'); t(1371, 318, 'ESP32 온디바이스', 13, 700, '#E5E4FF', 'middle')
outs = [('정상', GN), ('흔들림', RP), ('당겨짐', RI2), ('줄 분리', RR), ('소진', OR)]
for k, (lab, col) in enumerate(outs):
    y = 120 + k * 80
    A(f'<path d="M1446 280 L{1500} {y}" stroke="#C9C8F8" stroke-width="1.6"/>')
    A(f'<circle cx="1518" cy="{y}" r="20" fill="{col}"/>'); t(1552, y + 7, lab, 21, 900, RK)
t(1600, 548, '판정 5종 · 식 (15)', 15, 800, RM, 'middle')

# ---- equation band (numbered, continues 11장's (1)–(10))
YE = 584
A(f'<rect x="0" y="{YE}" width="{W}" height="130" rx="16" fill="#F6F7F9" stroke="{RLN}" stroke-width="1.2"/>')
EQS = [(11, 'v_{n} = (W_{I} − W_{f}) / T,   r_k = (v_k − v_{n}) / v_{n}', '정상 유속 기준 자가측정 · 상대 편차'),
       (12, 's_k = −1 (r_k < −τ),  +1 (r_k > τ),  0 (그 외)', '허용 오차 τ로 3상태 부호화'),
       (13, 'X_k = reshape(s_{k−15:k}, 4×4)', '연속 16상태 → 4×4 입력 (원소 −1 · 0 · +1)'),
       (14, 'h_k = tanh(W_{h}h_{k−1} + W_{v}v_k + b)', 'RNN 은닉 상태'),
       (15, 'ŷ_k = argmax softmax(W_{o}[f_{C}(X_k); h_k] + b_{o})', 'CNN 특징 f_C와 결합 → 5종 판정')]
cw = W / 3
for i, (n, e, d) in enumerate(EQS):
    col, row = (i % 3, i // 3) if i < 3 else (i - 3, 1)
    x = 24 + col * cw if i < 3 else 24 + (i - 3) * (W / 2)
    y = YE + 42 + row * 58
    A(f'<text x="{x:.0f}" y="{y}" font-size="13" font-weight="700" fill="{RM}">({n})</text>')
    A(f'<text x="{x + 40:.0f}" y="{y}" font-size="18" font-weight="600" fill="{RK}">{M(e, 18)}</text>')
    A(f'<text x="{x + 40:.0f}" y="{y + 20}" font-size="13" font-weight="600" fill="{RM}">{d}</text>')
defs = (f'<defs><marker id="a2a" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="context-stroke"/></marker>'
        f'<linearGradient id="a2g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{RI2}"/><stop offset="1" stop-color="{RI}"/></linearGradient></defs>')
svg = (f'<svg class="r-tsvg cp-a2" viewBox="0 0 {W} {H}" role="img" aria-label="AI 분석 — 10장의 보정 하중 · 유속을 두 갈래로 분석합니다. CNN은 −1 · 0 · +1 상태 부호화와 4×4 패턴을 Conv2D 3×3 · 8, MaxPool 2×2, Dense 16으로 분석해 순간 흔들림(고립 칸)과 지속 이상(덩어리)을 구분하고, RNN은 유속 v1…vt를 순서대로 기억해 점점 느려짐 · 멈춤 · 급감 추세를 봅니다. 두 결과를 종합해 정상 · 흔들림 · 당겨짐 · 줄 분리 · 소진 5종으로 판정합니다.">' + defs + ''.join(O) + '</svg>')
open(sys.argv[1], 'w').write(svg); print('ok', len(svg))
