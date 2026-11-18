# Slide 10 — signal processing chain: load cell → Kalman → virtual gyro → PID (+ learning stage), template palette
import math, sys
from mathtxt import M
RI, RI2, RP, RL, RK, RK2, RM, RLN, RY, RR, GN = '#4B48E0', '#7471F0', '#AEB2FB', '#ECEBFE', '#1D1C2B', '#4A4A5C', '#8B8B9C', '#DCDCE6', '#FFD84D', '#F0506E', '#2E9E6A'
W, H = 1700, 600
O = []; A = O.append
def t(x, y, s, fs=17, fw=700, col=RK2, anc='start', extra=''):
    A(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="{fw}" fill="{col}" text-anchor="{anc}"{extra}>{s}</text>')
def eq(x, y, n, s, fs=17, col=RK):
    A(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="600" fill="{col}">{M(s, fs)}</text>')
    if n: A(f'<text x="{x + 0:.0f}" y="{y:.0f}" font-size="13" font-weight="700" fill="{RM}" text-anchor="end" dx="-6">({n})</text>')
def box(x, y, w, h, fill='#FFFFFF', stroke=RLN, rx=18, sw=1.5):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{fill}" stroke="{stroke}" stroke-width="{sw}"/>')
def arrow(x1, y1, x2, y2, col=RI, dash=''):
    d = f' stroke-dasharray="{dash}"' if dash else ''
    A(f'<path d="M{x1} {y1} L{x2} {y2}" stroke="{col}" stroke-width="3" fill="none" stroke-linecap="round" marker-end="url(#t2a)"{d}/>')
def wave(x0, y0, w, amp, noise, col, sw=2.6, n=70, seed=1, base=0):
    pts = []
    for i in range(n):
        u = i / (n - 1)
        v = math.sin(u * 6.3) * amp * 0.35 + base * u
        v += noise * (math.sin(i * 2.7 + seed) * 0.6 + math.sin(i * 5.1 + seed * 2) * 0.4)
        pts.append(f'{x0 + u * w:.1f} {y0 + v:.1f}')
    A(f'<path d="M{" L".join(pts)}" stroke="{col}" stroke-width="{sw}" fill="none" stroke-linejoin="round"/>')
def chip(x, y, s, fill=RI, col='#FFFFFF', fs=15):
    w = sum(fs * (1.0 if '\uac00' <= ch <= '\ud7a3' else 0.6) for ch in s) + 28
    A(f'<rect x="{x}" y="{y}" width="{w:.0f}" height="28" rx="14" fill="{fill}"/>'); t(x + w / 2, y + 19.5, s, fs, 850, col, 'middle')
    return w
# ---------- stage cards (top)
Y, HH = 40, 300
cards = [(0, 360), (420, 360), (840, 360), (1260, 440)]
heads = [('① 측정 모델', '로드셀 원신호'), ('② 칼만 필터', '측정 잡음 1차 제거'), ('③ 가상 자이로', '로드셀만으로 기울기 · 오차 추정'), ('④ PID 보정', '외란 오차 상쇄')]
for k, ((x, w), (h1, h2)) in enumerate(zip(cards, heads)):
    box(x, Y, w, HH, '#FFFFFF' if k < 3 else RL, RLN if k < 3 else RP, 22, 1.6)
    t(x + 22, Y + 40, h1, 22, 900, RI if k else RK)
    t(x + 22, Y + 66, h2, 15, 700, RM)
    if k < 3: arrow(x + w + 6, Y + HH / 2, cards[k + 1][0] - 8, Y + HH / 2)
SUB = lambda c: f'<tspan font-size="12" baseline-shift="sub">{c}</tspan>'
# ① load cell
eq(48, Y + 112, 1, 'z_k = w_k + n_k', 20)
A(f'<text x="48" y="{Y + 140}" font-size="14" font-weight="600" fill="{RM}">{M("w_k: 실제 수액 무게 · n_k: 측정 잡음 · 외란", 14)}</text>')
wave(22, Y + 210, 316, 50, 14, '#9A9AAC', 2.2, 80, 1)
t(22, Y + 272, '4채널 · 24bit ADC · 샘플 주기 Δt', 15, 700, RM)
# ② Kalman (state x = [w, ẇ]ᵀ, H = [1 0])
x = 462
A(f'<text x="{x - 20}" y="{Y + 98}" font-size="14" font-weight="700" fill="{RM}">{M("상태 x_k = [w_k, ẇ_k]^{T},  H = [1 0]", 14)}</text>')
eq(x, Y + 132, 2, 'x̂_k^{−} = F x̂_{k−1},  P_k^{−} = F P_{k−1} F^{T} + Q', 16)
eq(x, Y + 164, 3, 'K_k = P_k^{−}H^{T}(H P_k^{−}H^{T} + R)^{−1}', 16)
eq(x, Y + 196, 4, 'x̂_k = x̂_k^{−} + K_k(z_k − H x̂_k^{−})', 16)
wave(x - 20, Y + 240, 316, 30, 1.6, RI, 2.6, 80, 1)
A(f'<text x="{x - 20}" y="{Y + 272}" font-size="15" font-weight="700" fill="{RM}">{M("ŵ_k = H x̂_k : 잡음을 뺀 무게 추정", 15)}</text>')
# ③ virtual gyro
x = 882
eq(x, Y + 112, 5, '(θ̂_k, Δŵ_k) = g_{φ}(z_{k−N+1:k})', 17)
t(x - 20, Y + 140, '최근 N개 로드셀 값만으로 기울기 · 오차 추정', 14, 600, RM)
for k, (lab, val) in enumerate((('θ̂x', '가상 기울기'), ('θ̂y', '가상 기울기'), ('θ̂z', '가상 회전'))):
    yy = Y + 160 + k * 36
    A(f'<rect x="{x + 120}" y="{yy}" width="196" height="30" rx="7" fill="{RL}"/>')
    t(x + 134, yy + 21, lab, 16, 800, RI); t(x + 176, yy + 21, val, 15, 600, RK2)
A(f'<g transform="rotate(-12 {x + 40} {Y + 210})"><line x1="{x + 40}" y1="{Y + 160}" x2="{x + 40}" y2="{Y + 262}" stroke="{RK2}" stroke-width="4" stroke-linecap="round"/><rect x="{x + 18}" y="{Y + 154}" width="44" height="12" rx="5" fill="{RP}"/><rect x="{x + 28}" y="{Y + 172}" width="24" height="32" rx="6" fill="#FFFFFF" stroke="{RK2}" stroke-width="2.2"/></g>')
t(x - 20, Y + 284, '자이로 없이 학습된 모델이 추정 (출시 제품)', 15, 700, RM)
# ④ PID
x = 1302
eq(x, Y + 106, 6, 'e_k = Δŵ_k', 17)
eq(x, Y + 140, 7, 'u_k = K_{P}e_k + K_{I} Σ_{i≤k} e_i Δt + K_{D}(e_k − e_{k−1}) / Δt', 16)
eq(x, Y + 174, 8, 'w̃_k = ŵ_k − u_k', 17)
A(f'<path d="M{x - 20} {Y + 222} C{x + 100} {Y + 204} {x + 240} {Y + 234} {x + 396} {Y + 216}" stroke="{GN}" stroke-width="3" fill="none"/>')
A(f'<rect x="{x - 20}" y="{Y + 248}" width="416" height="36" rx="8" fill="#FFFFFF" stroke="{RP}" stroke-width="1.2"/>')
t(x - 6, Y + 272, f'게인 (K{SUB("P")}, K{SUB("I")}, K{SUB("D")}) · LoRA · 유전 알고리즘 튜닝', 15, 700, RK2)
# ---------- bottom: learning stage + output bridge
YB = 380
box(0, YB, 1110, 210, '#FFFFFF', RLN, 22)
chip(22, YB + 18, '가상 자이로 학습 · 제품 출시 전')
# processor A / B
for k, (lab, sub, col) in enumerate((('프로세서 A', '로드셀 + 자이로', RI), ('프로세서 B', '로드셀 단일', RK))):
    yy = YB + 64 + k * 70
    A(f'<rect x="22" y="{yy}" width="300" height="58" rx="14" fill="{RL if k == 0 else "#F4F4F8"}"/>')
    chip(36, yy + 15, lab, col, '#FFFFFF', 14)
    t(150, yy + 36, sub, 18, 850, RK)
arrow(330, YB + 93, 400, YB + 128, RI); arrow(330, YB + 163, 400, YB + 136, RK2)
A(f'<rect x="406" y="{YB + 96}" width="210" height="76" rx="14" fill="#FFF0F3" stroke="{RR}" stroke-width="1.6"/>')
A(f'<text x="511" y="{YB + 128}" font-size="18" font-weight="700" fill="{RR}" text-anchor="middle">{M("Δw_k = w_k^{B} − w_k^{A}", 18)}</text>'); t(511, YB + 156, '편차 = 학습 정답', 14, 700, RK2, 'middle')
arrow(622, YB + 134, 680, YB + 134, RR)
A(f'<rect x="686" y="{YB + 80}" width="230" height="108" rx="14" fill="{RL}"/>')
t(801, YB + 108, '지도학습 (9)', 17, 800, RI, 'middle'); A(f'<text x="801" y="{YB + 140}" font-size="15" font-weight="600" fill="{RK}" text-anchor="middle">{M("min_{φ} Σ‖g_{φ}(z^{B}) − Δw‖²", 15)}</text>'); t(801, YB + 166, '드롭아웃 · 역전파 반복', 14, 600, RK2, 'middle')
arrow(922, YB + 134, 980, YB + 134, RI)
A(f'<rect x="986" y="{YB + 96}" width="104" height="76" rx="14" fill="{RI}"/>')
t(1038, YB + 128, 'ESP32', 17, 900, '#FFFFFF', 'middle'); t(1038, YB + 152, '가중치 탑재', 14, 700, '#E5E4FF', 'middle')
A(f'<path d="M1038 {YB + 94} L1038 {Y + HH + 8}" stroke="{RI}" stroke-width="2.4" fill="none" stroke-dasharray="7 6" marker-end="url(#t2a)"/>')
t(1046, YB - 12, '학습된 가중치', 14, 800, RI)
# output bridge
A(f'<rect x="1150" y="{YB}" width="550" height="210" rx="22" fill="url(#t2g)"/>')
t(1176, YB + 44, '출력', 16, 850, '#E5E4FF')
A(f'<text x="1176" y="{YB + 90}" font-size="24" font-weight="700" fill="#FFFFFF">{M("w̃_k ,  v_k = −(w̃_k − w̃_{k−1}) / Δt", 24)}</text>'); t(1660, YB + 90, '(10)', 13, 700, '#D7DEEA', 'end')
t(1176, YB + 126, '보정 하중 · 유속 → 잔량 최대 오차 2.9% (내부 모의시험 1,000회)', 15, 600, '#E5E4FF')
A(f'<rect x="1176" y="{YB + 148}" width="498" height="42" rx="21" fill="{RY}"/>')
t(1425, YB + 176, '다음 장 ▶ CNN · RNN이 이 신호를 분석', 18, 900, RK, 'middle')
A(f'<path d="M1480 {Y + HH + 4} L1480 {YB - 6}" stroke="{RI}" stroke-width="3" fill="none" marker-end="url(#t2a)"/>')
defs = (f'<defs><marker id="t2a" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{RI}"/></marker>'
        f'<linearGradient id="t2g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{RI2}"/><stop offset="1" stop-color="{RI}"/></linearGradient></defs>')
svg = (f'<svg class="r-tsvg cp-t2" viewBox="0 0 {W} {H}" role="img" aria-label="신호 처리 흐름 — ① 로드셀 4채널 · 24bit ADC 원신호, ② 칼만 필터로 측정 잡음 1차 제거, ③ 가상 자이로가 로드셀만으로 기울기를 추정, ④ PID가 흔들림 · 당김 오차를 상쇄(게인은 LoRA + 유전 알고리즘으로 자동 튜닝). 학습 단계에서는 로드셀 + 자이로(프로세서 A)와 로드셀 단일(프로세서 B)의 편차를 정답으로 지도학습해 ESP32에 탑재합니다. 출력은 보정 하중 · 유속이며, 다음 장에서 CNN · RNN이 분석합니다.">' + defs + ''.join(O) + '</svg>')
open(sys.argv[1], 'w').write(svg); print('ok', len(svg))
