# Figure 1 (slide 11) — journal-style: (a) correction pipeline with eqs (1)–(10), (b) virtual-gyro training, (c) measured errors
import math, sys
from mathtxt import M
K, G, LG, LLG, NV, NV2, VM, OR, GN = '#1A1A1A', '#5F6670', '#BFC5CE', '#E8EBF0', '#1E3A8A', '#8CA0CF', '#D55E00', '#E69F00', '#009E73'
W, H = 1700, 650
O = []; A = O.append
def T(x, y, s, fs=16, fw=500, col=K, anc='start', it=False):
    A(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="{fw}" fill="{col}" text-anchor="{anc}"{" font-style=\"italic\"" if it else ""}>{s}</text>')
def EQ(x, y, s, n=None, fs=17, xr=None):
    A(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="500" fill="{K}">{M(s, fs)}</text>')
    if n is not None and xr is not None: T(xr, y, f'({n})', 15, 500, G, 'end')
def ARW(x1, y1, x2, y2, col=K, dash=False, sw=1.4):
    A(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="{sw}" fill="none" marker-end="url(#f1a)"{" stroke-dasharray=\"5 4\"" if dash else ""}/>')
def PANEL(x, y, l, title):
    T(x, y, l, 26, 800, K); T(x + 30, y - 1, title, 17, 700, K)
def sig(f, x, y, w, h, col, sw=1.6, dash=False, n=160, lo=0.0, hi=1.0):
    pts = []
    for i in range(n):
        u = i / (n - 1); v = (f(u) - lo) / (hi - lo)
        pts.append(f'{x + u * w:.1f} {y + h - v * h:.1f}')
    A(f'<path d="M{" L".join(pts)}" stroke="{col}" stroke-width="{sw}" fill="none" stroke-linejoin="round"{" stroke-dasharray=\"5 4\"" if dash else ""}/>')
def AX(x, y, w, h, yl, xl='t'):
    A(f'<path d="M{x} {y} L{x} {y + h} L{x + w} {y + h}" stroke="{K}" stroke-width="1.1" fill="none"/>')
    A(f'<text x="{x - 8}" y="{y + 10}" font-size="14" font-weight="500" fill="{G}" text-anchor="end">{M(yl, 14)}</text>')
    T(x + w, y + h + 18, xl, 15, 500, G, 'end', True)
# signals (normalized, schematic)
true = lambda u: 0.82 - 0.5 * u
sway = lambda u: 0.11 * math.sin(u * 13) * math.exp(-((u - .55) / .28) ** 2)
noise = lambda u: 0.035 * (math.sin(u * 211) + .6 * math.sin(u * 377 + 1.3) + .4 * math.sin(u * 523 + .2))
raw = lambda u: true(u) + sway(u) + noise(u)
kal = lambda u: true(u) + sway(u) + 0.004 * math.sin(u * 211)
cor = lambda u: true(u) + 0.12 * sway(u)
# ---------- panel a
PANEL(0, 26, 'a', '신호 보정 파이프라인 — 측정 · 칼만 필터 · 가상 자이로 · PID')
cols = [0, 430, 860, 1290]; CW = 400; Y0 = 62
heads = ['① 측정 모델', '② 칼만 필터', '③ 가상 자이로', '④ PID 보정 · 출력']
for k, x in enumerate(cols):
    T(x, Y0, heads[k], 17, 700, NV)
    A(f'<line x1="{x}" y1="{Y0 + 9}" x2="{x + CW}" y2="{Y0 + 9}" stroke="{LG}" stroke-width="1"/>')
xr = lambda k: cols[k] + CW
EQ(0, Y0 + 40, '*z*_{*k*} = *w*_{*k*} + *n*_{*k*}', 1, 18, xr(0))
T(0, Y0 + 66, M('*w*_{*k*}: 수액 무게,  *n*_{*k*}: 측정 잡음 · 외란', 14), 15, 500, G)
T(0, Y0 + 88, '4채널 · 24-bit ADC · 샘플 주기 Δ<tspan font-style="italic">t</tspan>', 15, 500, G)
x = cols[1]
T(x, Y0 + 34, M('*x*_{*k*} = [*w*_{*k*}, *ẇ*_{*k*}]^{T},  *H* = [1  0]', 14), 15, 500, G)
EQ(x, Y0 + 58, '*x̂*_{*k*}^{−} = *F x̂*_{*k*−1},   *P*_{*k*}^{−} = *FP*_{*k*−1}*F*^{T} + *Q*', 2, 16, xr(1))
EQ(x, Y0 + 84, '*K*_{*k*} = *P*_{*k*}^{−}*H*^{T}(*HP*_{*k*}^{−}*H*^{T} + *R*)^{−1}', 3, 16, xr(1))
EQ(x, Y0 + 110, '*x̂*_{*k*} = *x̂*_{*k*}^{−} + *K*_{*k*}(*z*_{*k*} − *Hx̂*_{*k*}^{−})', 4, 16, xr(1))
x = cols[2]
EQ(x, Y0 + 40, '(*θ̂*_{*k*}, Δ*ŵ*_{*k*}) = *g*_{*φ*}(*z*_{*k*−*N*+1:*k*})', 5, 17, xr(2))
T(x, Y0 + 66, M('*θ̂* = (*θ*_{x}, *θ*_{y}, *θ*_{z}):  자이로 없이 추정한 기울기', 14), 15, 500, G)
T(x, Y0 + 88, '최근 N개 로드셀 값 → 경량 신경망 (ESP32)', 15, 500, G)
x = cols[3]
EQ(x, Y0 + 34, '*e*_{*k*} = Δ*ŵ*_{*k*}', 6, 16, xr(3))
EQ(x, Y0 + 58, '*u*_{*k*} = *K*_{P}*e*_{*k*} + *K*_{I}Σ*e*_{*i*}Δ*t* + *K*_{D}(*e*_{*k*} − *e*_{*k*−1})/Δ*t*', 7, 15, xr(3))
EQ(x, Y0 + 84, '*w̃*_{*k*} = *ŵ*_{*k*} − *u*_{*k*}', 8, 16, xr(3))
EQ(x, Y0 + 110, '*v*_{*k*} = −(*w̃*_{*k*} − *w̃*_{*k*−1})/Δ*t*', 10, 16, xr(3))
# mini plots
PY, PH, PW = 200, 108, 330
for k, x in enumerate(cols):
    AX(x + 52, PY, PW, PH, ['*z*', '*ŵ*', '*θ̂*', '*w̃*'][k])
sig(raw, cols[0] + 52, PY, PW, PH, '#8A9099', 1.2, lo=.1, hi=1)
sig(raw, cols[1] + 52, PY, PW, PH, LLG, 1.2, lo=.1, hi=1); sig(kal, cols[1] + 52, PY, PW, PH, NV, 1.8, lo=.1, hi=1)
for ph, col in ((0, OR), (1.1, '#C98A00'), (2.2, '#F2C46B')):
    sig(lambda u, ph=ph: .5 + 2.6 * 0.11 * math.sin(u * 13 + ph * .25) * math.exp(-((u - .55) / .28) ** 2) * (1 - .25 * ph / 2.2), cols[2] + 52, PY, PW, PH, col, 1.6)
sig(true, cols[3] + 52, PY, PW, PH, K, 1.2, True, lo=.1, hi=1); sig(cor, cols[3] + 52, PY, PW, PH, NV, 1.9, lo=.1, hi=1)
# legends
def LEG(x, y, items):
    for i, (col, lab, dash) in enumerate(items):
        yy = y + i * 18
        A(f'<line x1="{x}" y1="{yy - 5}" x2="{x + 22}" y2="{yy - 5}" stroke="{col}" stroke-width="2"{" stroke-dasharray=\"4 3\"" if dash else ""}/>')
        A(f'<text x="{x + 28}" y="{yy}" font-size="13" font-weight="500" fill="{G}">{M(lab, 13)}</text>')
LEG(cols[1] + 230, PY + 4, [(LLG, '원신호 *z*', False), (NV, '칼만 추정 *ŵ*', False)])
LEG(cols[2] + 260, PY + 4, [(OR, '*θ*_{x}', False), ('#C98A00', '*θ*_{y}', False), ('#F2C46B', '*θ*_{z}', False)])
LEG(cols[3] + 230, PY + 4, [(NV, '보정 *w̃*', False), (K, '기준 무게', True)])
for k in range(3):
    ARW(cols[k] + CW - 8, PY + PH / 2, cols[k + 1] + 20, PY + PH / 2)
T(cols[3] + 382, PY + PH + 38, '→ 그림 2 (CNN · RNN 분석)', 14, 600, NV, 'end')
T(0, PY + PH + 38, '모식도 · 정규화 신호', 14, 500, G)
# ---------- panel b — training
YB = 400
A(f'<line x1="0" y1="{YB - 32}" x2="{W}" y2="{YB - 32}" stroke="{LG}" stroke-width="1"/>')
PANEL(0, YB, 'b', '가상 자이로 학습 (출시 전 1회)')
def BOX(x, y, w, h, l1, l2, fill='#FFFFFF', stroke=K):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" fill="{fill}" stroke="{stroke}" stroke-width="1.2"/>')
    A(f'<text x="{x + w / 2}" y="{y + h / 2 - 4}" font-size="16" font-weight="700" fill="{K}" text-anchor="middle">{M(l1, 16)}</text>')
    A(f'<text x="{x + w / 2}" y="{y + h / 2 + 18}" font-size="14" font-weight="500" fill="{G}" text-anchor="middle">{M(l2, 14)}</text>')
BOX(0, YB + 34, 230, 70, '프로세서 A', '로드셀 + 자이로 → *w*^{A}_{*k*}')
BOX(0, YB + 140, 230, 70, '프로세서 B', '로드셀 단일 → *z*^{B}_{*k*}')
ARW(230, YB + 69, 300, YB + 114); ARW(230, YB + 175, 300, YB + 130)
BOX(304, YB + 87, 200, 70, 'Δ*w*_{*k*} = *w*^{B}_{*k*} − *w*^{A}_{*k*}', '편차 = 학습 정답', '#FFFFFF', VM)
ARW(504, YB + 122, 560, YB + 122)
# tiny network
nx, ny = 580, YB + 70
layers = [3, 5, 5, 2]
pos = [[(nx + li * 70, ny + 14 + j * (104 / (n - 1) if n > 1 else 0)) for j in range(n)] for li, n in enumerate(layers)]
for li in range(3):
    for a in pos[li]:
        for b in pos[li + 1]:
            A(f'<line x1="{a[0]}" y1="{a[1]}" x2="{b[0]}" y2="{b[1]}" stroke="{LG}" stroke-width=".8"/>')
drop = {(1, 1), (2, 3)}
for li, lay in enumerate(pos):
    for j, (cx, cy) in enumerate(lay):
        if (li, j) in drop:
            A(f'<circle cx="{cx}" cy="{cy}" r="7" fill="#FFFFFF" stroke="{G}" stroke-width="1" stroke-dasharray="2 2"/>')
        else:
            A(f'<circle cx="{cx}" cy="{cy}" r="7" fill="{NV if li in (1, 2) else "#FFFFFF"}" stroke="{NV}" stroke-width="1.2"/>')
T(nx + 105, YB + 226, M('*g*_{*φ*} · 점선 = 드롭아웃', 14), 14, 600, G, 'middle')
ARW(nx + 222, YB + 122, nx + 262, YB + 122)
A(f'<rect x="{nx + 266}" y="{YB + 82}" width="340" height="80" fill="#FFFFFF" stroke="{K}" stroke-width="1.2"/>')
EQ(nx + 282, YB + 114, 'min_{*φ*} Σ_{*k*} ‖*g*_{*φ*}(*z*^{B}) − Δ*w*_{*k*}‖^{2}', 9, 17, nx + 596)
T(nx + 282, YB + 144, '역전파 · 수렴까지 반복 → 가중치 φ를 ESP32에 탑재', 14, 500, G)
# ---------- panel c — measured bars
cx0 = 1240
PANEL(cx0, YB, 'c', '잔량 최대 오차 · 정상 중 오경보')
groups = [('최대 오차', (14.2, 2.4, 2.9)), ('오경보', (12.3, 1.0, 0.7))]
cols3 = ('#B9BFC8', NV2, NV); labs = ('로드셀 단일', '4센서', '가상 자이로')
bx, by, bh = cx0 + 40, YB + 40, 160; ymax = 16
A(f'<path d="M{bx} {by} L{bx} {by + bh} L{bx + 420} {by + bh}" stroke="{K}" stroke-width="1.1" fill="none"/>')
for v in (0, 5, 10, 15):
    yy = by + bh - v / ymax * bh
    A(f'<line x1="{bx - 5}" y1="{yy:.1f}" x2="{bx}" y2="{yy:.1f}" stroke="{K}" stroke-width="1"/>'); T(bx - 9, yy + 5, f'{v}', 14, 500, G, 'end')
T(bx - 30, by - 10, '%', 13, 600, G)
for gi, (gl, vals) in enumerate(groups):
    gx = bx + 30 + gi * 205
    for i, v in enumerate(vals):
        h = v / ymax * bh; x = gx + i * 52
        A(f'<rect x="{x}" y="{by + bh - h:.1f}" width="40" height="{h:.1f}" fill="{cols3[i]}"/>')
        T(x + 20, by + bh - h - 6, f'{v}', 13, 700 if i == 2 else 500, NV if i == 2 else G, 'middle')
    T(gx + 72, by + bh + 22, gl, 14, 600, K, 'middle')
for i, l in enumerate(labs):
    A(f'<rect x="{cx0 + 40 + i * 140}" y="{by + bh + 40}" width="14" height="14" fill="{cols3[i]}"/>'); T(cx0 + 60 + i * 140, by + bh + 52, l, 14, 500, G)
defs = f'<defs><marker id="f1a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1L9 5L0 9z" fill="{K}"/></marker></defs>'
svg = (f'<svg class="r-tsvg cp-t2" viewBox="0 0 {W} {H}" role="img" aria-label="그림 1. (a) 신호 보정 파이프라인: 측정 모델 z=w+n, 칼만 필터 예측·갱신, 가상 자이로 g_φ로 기울기·오차 추정, PID 보정 및 유속 계산(식 1–10). (b) 가상 자이로 학습: 프로세서 A(로드셀+자이로)와 B(로드셀 단일)의 편차를 정답으로 지도학습(식 9). (c) 잔량 최대 오차 14.2·2.4·2.9%, 정상 중 오경보 12.3·1.0·0.7%(로드셀 단일·4센서·가상 자이로).">'
       + defs + ''.join(O) + '</svg>')
open(sys.argv[1], 'w').write(svg); print('ok', len(svg))
