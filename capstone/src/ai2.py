# Figure 2 (slide 12) — journal-style: (a) state coding & 4×4 input, (b) CNN branch, (c) RNN branch, (d) fusion; eqs (11)–(15)
import math, sys
from mathtxt import M
K, G, LG, LLG, NV, NV2, VM, OR, GN = '#1A1A1A', '#5F6670', '#BFC5CE', '#E8EBF0', '#1E3A8A', '#8CA0CF', '#D55E00', '#E69F00', '#009E73'
W, H = 1700, 725
O = []; A = O.append
def T(x, y, s, fs=16, fw=500, col=K, anc='start'):
    A(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="{fw}" fill="{col}" text-anchor="{anc}">{s}</text>')
def EQ(x, y, s, n, xr, fs=17):
    A(f'<text x="{x:.1f}" y="{y:.1f}" font-size="{fs}" font-weight="500" fill="{K}">{M(s, fs)}</text>'); T(xr, y, f'({n})', 15, 500, G, 'end')
def ARW(x1, y1, x2, y2, col=K, sw=1.4):
    A(f'<path d="M{x1:.1f} {y1:.1f} L{x2:.1f} {y2:.1f}" stroke="{col}" stroke-width="{sw}" fill="none" marker-end="url(#f2a)"/>')
def PANEL(x, y, l, title):
    T(x, y, l, 26, 800, K); T(x + 30, y - 1, title, 17, 700, K)
SC = {-1: NV, 0: '#FFFFFF', 1: NV2}
# ---------- a — coding
PANEL(0, 26, 'a', '상태 부호화와 4×4 입력')
px, py, pw, ph = 52, 62, 330, 120
vn = .55; tau = .18
yv = lambda v: py + ph - v * ph
A(f'<rect x="{px}" y="{yv(vn * (1 + tau)):.1f}" width="{pw}" height="{(yv(vn * (1 - tau)) - yv(vn * (1 + tau))):.1f}" fill="{LLG}"/>')
A(f'<line x1="{px}" y1="{yv(vn):.1f}" x2="{px + pw}" y2="{yv(vn):.1f}" stroke="{G}" stroke-width="1" stroke-dasharray="5 4"/>')
A(f'<path d="M{px} {py} L{px} {py + ph} L{px + pw} {py + ph}" stroke="{K}" stroke-width="1.1" fill="none"/>')
T(px - 8, py + 10, M('*v*', 14), 15, 500, G, 'end'); T(px + pw, py + ph + 18, M('*k*', 14), 15, 500, G, 'end')
T(px + pw + 6, yv(vn) + 5, M('*v*_{n}', 13), 14, 500, G); T(px + pw + 6, yv(vn * (1 + tau)) + 4, M('±*τ*', 13), 14, 500, G)
vals = [.56, .6, .52, .58, .55, .62, .49, .57, .41, .38, .34, .3, .27, .25, .22, .2]
pts = ' L'.join(f'{px + 10 + i * (pw - 20) / 15:.1f} {yv(v):.1f}' for i, v in enumerate(vals))
A(f'<path d="M{pts}" stroke="{NV}" stroke-width="1.8" fill="none"/>')
for i, v in enumerate(vals):
    A(f'<circle cx="{px + 10 + i * (pw - 20) / 15:.1f}" cy="{yv(v):.1f}" r="3" fill="{NV}"/>')
st = [(-1 if v < vn * (1 - tau) else 1 if v > vn * (1 + tau) else 0) for v in vals]
cw = (pw - 20) / 16
for i, sv in enumerate(st):
    A(f'<rect x="{px + 10 + i * cw - cw / 2 + (pw - 20) / 30:.1f}" y="{py + ph + 30}" width="{cw - 2:.1f}" height="20" fill="{SC[sv]}" stroke="{G}" stroke-width=".8"/>')
T(px - 8, py + ph + 45, M('*s*_{*k*}', 14), 15, 500, G, 'end')
ARW(px + pw + 40, py + 70, px + pw + 80, py + 70)
gx, gy, gc = px + pw + 90, py + 10, 30
for i, sv in enumerate(st):
    r, q = divmod(i, 4)
    A(f'<rect x="{gx + q * gc}" y="{gy + r * gc}" width="{gc}" height="{gc}" fill="{SC[sv]}" stroke="{G}" stroke-width=".8"/>')
T(gx + 60, gy + 4 * gc + 22, M('*X*_{*k*}  (4×4)', 14), 14, 600, K, 'middle')
for i, (sv, lab) in enumerate(((-1, '−1 느림'), (0, '0 정상'), (1, '+1 빠름'))):
    A(f'<rect x="{gx + 140}" y="{gy + 6 + i * 24}" width="14" height="14" fill="{SC[sv]}" stroke="{G}" stroke-width=".8"/>'); T(gx + 160, gy + 18 + i * 24, lab, 14, 500, G)
EQ(0, 296, '*v*_{n} = (*W*_{I} − *W*_{f})/*T*,   *r*_{*k*} = (*v*_{*k*} − *v*_{n})/*v*_{n}', 11, 690)
EQ(0, 326, '*s*_{*k*} = −1 (*r*_{*k*} < −*τ*),  +1 (*r*_{*k*} > *τ*),  0 (그 외)', 12, 690)
EQ(0, 356, '*X*_{*k*} = reshape(*s*_{*k*−15:*k*}, 4×4)', 13, 690)
# ---------- b — CNN
bx = 760
A(f'<line x1="{bx - 30}" y1="0" x2="{bx - 30}" y2="370" stroke="{LG}" stroke-width="1"/>')
PANEL(bx, 26, 'b', 'CNN 분기 — 순간 패턴의 모양')
def stack(x, y, s, n, off, lab, dim, par):
    for i in range(n - 1, -1, -1):
        A(f'<rect x="{x + i * off}" y="{y - i * off}" width="{s}" height="{s}" fill="#FFFFFF" stroke="{NV}" stroke-width="1"/>')
    cx = x + (n - 1) * off / 2 + s / 2
    T(cx, 92, lab, 14, 700, K, 'middle'); T(cx, 250, dim, 15, 500, G, 'middle'); T(cx, 272, par, 14, 500, G, 'middle')
    return x + (n - 1) * off + s
e = stack(bx + 10, 150, 72, 1, 0, '입력', '4×4×1', '')
ARW(e + 10, 186, e + 50, 186)
e = stack(e + 60, 162, 72, 8, 6, 'Conv2D 3×3, 8', '4×4×8', '80 params')
ARW(e + 10, 186, e + 50, 186)
e = stack(e + 60, 186, 36, 8, 6, 'MaxPool 2×2', '2×2×8', '0')
ARW(e + 10, 186, e + 50, 186)
fx = e + 64
A(f'<rect x="{fx}" y="{118}" width="18" height="136" fill="#FFFFFF" stroke="{NV}" stroke-width="1"/>')
T(fx + 9, 92, 'Flatten', 14, 700, K, 'middle'); T(fx + 9, 272, '32', 15, 500, G, 'middle')
ARW(fx + 26, 186, fx + 60, 186)
for j in range(8):
    A(f'<circle cx="{fx + 80}" cy="{124 + j * 18}" r="6" fill="{NV}"/>')
T(fx + 80, 92, 'Dense 16', 14, 700, K, 'middle'); T(fx + 80, 272, '528', 14, 500, G, 'middle')
ARW(fx + 96, 186, fx + 130, 186)
T(fx + 138, 192, M('*f*_{C}', 18), 18, 600, NV)
T(bx, 318, '고립된 한 칸 = 순간 흔들림  ·  뭉친 덩어리 = 지속 이상', 15, 500, G)
T(bx, 344, '논문 단독 분류기: Dense 3 (51) 추가 → 총 659 파라미터', 14, 500, G)
# ---------- c — RNN
YB = 420
A(f'<line x1="0" y1="{YB - 34}" x2="{W}" y2="{YB - 34}" stroke="{LG}" stroke-width="1"/>')
PANEL(0, YB, 'c', 'RNN 분기 — 시간에 따른 흐름')
xs = [60, 220, 380, 600]
labs = ['*k*−3', '*k*−2', '*k*−1', '*k*']
for i, (x, l) in enumerate(zip(xs, labs)):
    A(f'<circle cx="{x}" cy="{YB + 92}" r="26" fill="#FFFFFF" stroke="{OR}" stroke-width="1.6"/>')
    T(x, YB + 99, M(f'*h*_{{{l}}}', 17), 17, 600, K, 'middle')
    A(f'<rect x="{x - 26}" y="{YB + 170}" width="52" height="34" fill="#FFFFFF" stroke="{G}" stroke-width="1"/>')
    T(x, YB + 193, M(f'*v*_{{{l}}}', 16), 16, 500, K, 'middle')
    ARW(x, YB + 168, x, YB + 122, OR)
for a, b in zip(xs, xs[1:]):
    if b - a > 200:
        T((a + b) / 2, YB + 98, '···', 18, 700, G, 'middle'); ARW(a + 28, YB + 92, a + 70, YB + 92, OR); ARW(b - 70, YB + 92, b - 28, YB + 92, OR)
    else:
        ARW(a + 28, YB + 92, b - 28, YB + 92, OR)
ARW(626, YB + 92, 670, YB + 92, OR); T(678, YB + 99, M('*h*_{*k*}', 18), 18, 600, OR)
EQ(0, YB + 250, '*h*_{*k*} = tanh(*W*_{h}*h*_{*k*−1} + *W*_{v}*v*_{*k*} + *b*)', 14, 690)
T(0, YB + 278, '점점 느려짐 · 멈춤 · 급감 추세를 순서대로 기억', 15, 500, G)
# ---------- d — fusion
dx = 760
A(f'<line x1="{dx - 30}" y1="{YB - 34}" x2="{dx - 30}" y2="{H}" stroke="{LG}" stroke-width="1"/>')
PANEL(dx, YB, 'd', '결합 판정 — 5종')
for j in range(6):
    A(f'<rect x="{dx + 20}" y="{YB + 40 + j * 22}" width="22" height="22" fill="{NV if j < 4 else "#FFFFFF"}" stroke="{NV if j < 4 else OR}" stroke-width="1.2"/>')
T(dx + 54, YB + 70, M('*f*_{C}', 16), 16, 600, NV); T(dx + 54, YB + 158, M('*h*_{*k*}', 16), 16, 600, OR)
T(dx + 31, YB + 196, '연결 [ ; ]', 14, 500, G, 'middle')
ARW(dx + 100, YB + 106, dx + 170, YB + 106)
A(f'<rect x="{dx + 176}" y="{YB + 70}" width="170" height="72" fill="#FFFFFF" stroke="{K}" stroke-width="1.2"/>')
T(dx + 261, YB + 100, M('*W*_{o}, *b*_{o}', 16), 16, 600, K, 'middle'); T(dx + 261, YB + 126, 'softmax', 15, 500, G, 'middle')
ARW(dx + 346, YB + 106, dx + 400, YB + 106)
classes = [('정상', GN), ('흔들림', NV2), ('당겨짐', NV), ('줄 분리', VM), ('소진', OR)]
for i, (c, col) in enumerate(classes):
    y = YB + 30 + i * 38
    A(f'<rect x="{dx + 410}" y="{y}" width="16" height="16" fill="{col}"/>'); T(dx + 436, y + 14, c, 16, 600, K)
    A(f'<line x1="{dx + 400}" y1="{YB + 106}" x2="{dx + 408}" y2="{y + 8}" stroke="{LG}" stroke-width="1"/>')
EQ(dx, YB + 250, '*ŷ*_{*k*} = argmax softmax(*W*_{o}[*f*_{C}(*X*_{*k*}); *h*_{*k*}] + *b*_{o})', 15, 1700)
T(dx, YB + 278, 'ESP32 온디바이스 추론 · 판정 → 알림 · 기록', 15, 500, G)
defs = f'<defs><marker id="f2a" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="7" markerHeight="7" orient="auto"><path d="M0 1L9 5L0 9z" fill="context-stroke"/></marker></defs>'
svg = (f'<svg class="r-tsvg cp-a2" viewBox="0 0 {W} {H}" role="img" aria-label="그림 2. (a) 유속 v_k를 기준 v_n과 허용 오차 τ로 −1·0·+1 상태 s_k로 부호화하고 연속 16개를 4×4 입력 X_k로 만든다(식 11–13). (b) CNN 분기: Conv2D 3×3·8, MaxPool 2×2, Flatten 32, Dense 16 → 특징 f_C. (c) RNN 분기: h_k = tanh(W_h h_k−1 + W_v v_k + b)(식 14). (d) f_C와 h_k를 연결해 softmax로 정상·흔들림·당겨짐·줄 분리·소진 5종 판정(식 15).">'
       + defs + ''.join(O) + '</svg>')
open(sys.argv[1], 'w').write(svg); print('ok', len(svg))
