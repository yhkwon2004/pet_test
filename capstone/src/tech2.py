# Slide 10 — signal processing chain: load cell → Kalman → virtual gyro → PID (+ learning stage), template palette
import math, sys
RI, RI2, RP, RL, RK, RK2, RM, RLN, RY, RR, GN = '#4B48E0', '#7471F0', '#AEB2FB', '#ECEBFE', '#1D1C2B', '#4A4A5C', '#8B8B9C', '#DCDCE6', '#FFD84D', '#F0506E', '#2E9E6A'
W, H = 1700, 600
O = []; A = O.append
def t(x, y, s, fs=17, fw=700, col=RK2, anc='start', extra=''):
    A(f'<text x="{x:.0f}" y="{y:.0f}" font-size="{fs}" font-weight="{fw}" fill="{col}" text-anchor="{anc}"{extra}>{s}</text>')
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
heads = [('① 로드셀 원신호', '4채널 · 24bit ADC'), ('② 칼만 필터', '측정 잡음 1차 제거'), ('③ 가상 자이로', '로드셀만으로 기울기 추정'), ('④ PID 보정', '흔들림 · 당김 오차 상쇄')]
for k, ((x, w), (h1, h2)) in enumerate(zip(cards, heads)):
    box(x, Y, w, HH, '#FFFFFF' if k < 3 else RL, RLN if k < 3 else RP, 22, 1.6)
    t(x + 22, Y + 40, h1, 22, 900, RI if k else RK)
    t(x + 22, Y + 66, h2, 16, 700, RM)
    if k < 3: arrow(x + w + 6, Y + HH / 2, cards[k + 1][0] - 8, Y + HH / 2)
# ① raw noisy signal + hook icon
wave(22, Y + 200, 316, 60, 16, '#9A9AAC', 2.2, 80, 1)
t(22, Y + 272, '흔들림 · 당김 · 센서 잡음이 섞인 무게', 15, 700, RM)
for k in range(4):
    A(f'<rect x="{230 + k * 30}" y="{Y + 92}" width="20" height="30" rx="5" fill="{RL}" stroke="{RP}" stroke-width="1.5"/>')
t(290, Y + 140, '갈고리 4개', 14, 800, RI, 'middle')
# ② Kalman
x = 442
wave(x, Y + 210, 316, 60, 16, '#D5D5DE', 2, 80, 1)
wave(x, Y + 210, 316, 60, 2.2, RI, 3, 80, 1)
t(x, Y + 106, '예측', 15, 800, RM); t(x + 52, Y + 106, 'x̂ₖ⁻ = x̂ₖ₋₁', 20, 800, RK)
t(x, Y + 138, '보정', 15, 800, RM); t(x + 52, Y + 138, 'x̂ₖ = x̂ₖ⁻ + Kₖ(zₖ − x̂ₖ⁻)', 20, 800, RK)
t(x, Y + 272, '측정값 z와 예측을 칼만 이득 K로 섞어 매끈하게', 15, 700, RM)
# ③ virtual gyro (tilted pole + xyz)
x = 862
A(f'<g transform="rotate(-12 {x + 70} {Y + 200})"><line x1="{x + 70}" y1="{Y + 110}" x2="{x + 70}" y2="{Y + 250}" stroke="{RK2}" stroke-width="5" stroke-linecap="round"/><rect x="{x + 40}" y="{Y + 100}" width="60" height="16" rx="6" fill="{RP}"/><rect x="{x + 56}" y="{Y + 122}" width="28" height="40" rx="7" fill="#FFFFFF" stroke="{RK2}" stroke-width="2.5"/></g>')
A(f'<path d="M{x + 18} {Y + 150} Q{x + 8} {Y + 180} {x + 18} {Y + 210}" stroke="{RR}" stroke-width="3" fill="none" stroke-linecap="round"/>')
for k, (lab, val) in enumerate((('θx', '기울기'), ('θy', '기울기'), ('θz', '회전'))):
    yy = Y + 110 + k * 46
    A(f'<rect x="{x + 160}" y="{yy}" width="176" height="36" rx="10" fill="{RL}"/>')
    t(x + 176, yy + 25, lab, 18, 900, RI); t(x + 214, yy + 25, f'가상 {val}', 16, 700, RK2)
t(x, Y + 272, '자이로 없이 학습된 모델이 추정 → 오차 e 계산', 15, 700, RM)
# ④ PID
x = 1282
SUB = lambda c: f'<tspan font-size="14" baseline-shift="sub">{c}</tspan>'
t(x, Y + 112, f'u(t) = K{SUB("P")}·e + K{SUB("I")}∫e dt + K{SUB("D")}·de/dt', 22, 850, RK)
t(x, Y + 142, 'e = 가상 자이로가 추정한 흔들림 오차', 15, 700, RK2)
wave(x, Y + 200, 396, 60, 16, '#D5D5DE', 2, 80, 3)
A(f'<path d="M{x} {Y + 214} C{x + 120} {Y + 190} {x + 260} {Y + 226} {x + 396} {Y + 206}" stroke="{GN}" stroke-width="3.4" fill="none"/>')
A(f'<rect x="{x}" y="{Y + 246}" width="396" height="36" rx="10" fill="#FFFFFF" stroke="{RP}" stroke-width="1.5"/>')
t(x + 14, Y + 270, f'게인 K{SUB("P")} · K{SUB("I")} · K{SUB("D")}', 15, 850, RI); t(x + 150, Y + 270, '← LoRA · 유전 알고리즘 튜닝', 15, 700, RK2)
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
t(511, YB + 128, '편차 Δw', 20, 900, RR, 'middle'); t(511, YB + 154, '= 학습 정답', 15, 800, RK2, 'middle')
arrow(622, YB + 134, 680, YB + 134, RR)
A(f'<rect x="686" y="{YB + 80}" width="230" height="108" rx="14" fill="{RL}"/>')
t(801, YB + 112, '지도학습', 19, 900, RI, 'middle'); t(801, YB + 140, '입력 = 단일 신호', 15, 700, RK2, 'middle'); t(801, YB + 164, '드롭아웃 · 역전파 반복', 15, 700, RK2, 'middle')
arrow(922, YB + 134, 980, YB + 134, RI)
A(f'<rect x="986" y="{YB + 96}" width="104" height="76" rx="14" fill="{RI}"/>')
t(1038, YB + 128, 'ESP32', 17, 900, '#FFFFFF', 'middle'); t(1038, YB + 152, '가중치 탑재', 14, 700, '#E5E4FF', 'middle')
A(f'<path d="M1038 {YB + 94} L1038 {Y + HH + 8}" stroke="{RI}" stroke-width="2.4" fill="none" stroke-dasharray="7 6" marker-end="url(#t2a)"/>')
t(1046, YB - 12, '학습된 가중치', 14, 800, RI)
# output bridge
A(f'<rect x="1150" y="{YB}" width="550" height="210" rx="22" fill="url(#t2g)"/>')
t(1176, YB + 44, '출력', 16, 850, '#E5E4FF')
t(1176, YB + 90, '보정 하중 w(t) · 유속 v(t)', 28, 900, '#FFFFFF')
t(1176, YB + 126, '흔들려도 오차 최대 2.9% · 내부 모의시험', 16, 700, '#E5E4FF')
A(f'<rect x="1176" y="{YB + 148}" width="498" height="42" rx="21" fill="{RY}"/>')
t(1425, YB + 176, '다음 장 ▶ CNN · RNN이 이 신호를 분석', 18, 900, RK, 'middle')
A(f'<path d="M1480 {Y + HH + 4} L1480 {YB - 6}" stroke="{RI}" stroke-width="3" fill="none" marker-end="url(#t2a)"/>')
defs = (f'<defs><marker id="t2a" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5.5" markerHeight="5.5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{RI}"/></marker>'
        f'<linearGradient id="t2g" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{RI2}"/><stop offset="1" stop-color="{RI}"/></linearGradient></defs>')
svg = (f'<svg class="r-tsvg cp-t2" viewBox="0 0 {W} {H}" role="img" aria-label="신호 처리 흐름 — ① 로드셀 4채널 · 24bit ADC 원신호, ② 칼만 필터로 측정 잡음 1차 제거, ③ 가상 자이로가 로드셀만으로 기울기를 추정, ④ PID가 흔들림 · 당김 오차를 상쇄(게인은 LoRA + 유전 알고리즘으로 자동 튜닝). 학습 단계에서는 로드셀 + 자이로(프로세서 A)와 로드셀 단일(프로세서 B)의 편차를 정답으로 지도학습해 ESP32에 탑재합니다. 출력은 보정 하중 · 유속이며, 다음 장에서 CNN · RNN이 분석합니다.">' + defs + ''.join(O) + '</svg>')
open(sys.argv[1], 'w').write(svg); print('ok', len(svg))
