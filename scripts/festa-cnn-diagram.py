# A4 — lightweight 2D CNN architecture diagram (reference-style: stacked feature maps, braces, FC nodes)
import sys
NV, NV2, NV3, CY, K, K2, MU = '#0B2466', '#1C3A8A', '#4A5E91', '#1CE8F2', '#0F1A38', '#3F4A66', '#7A84A0'
GR, RR, OR = '#1F9D63', '#E5484D', '#E07B2E'
W, H = 1700, 420
O = []; A = O.append
def txt(x, y, t, fs=17, fw=700, col=K2, anc='middle', extra=''):
    A(f'<text x="{x:.0f}" y="{y:.0f}" text-anchor="{anc}" font-size="{fs}" font-weight="{fw}" fill="{col}"{extra}>{t}</text>')
def brace(x1, x2, y, title, l2, l3=None):
    m = (x1 + x2) / 2
    A(f'<path d="M{x1} {y+14} Q{x1} {y} {x1+14} {y} L{m-10} {y} Q{m} {y} {m} {y-12} Q{m} {y} {m+10} {y} L{x2-14} {y} Q{x2} {y} {x2} {y+14}" fill="none" stroke="{K2}" stroke-width="2.2"/>')
    yy = y - 22
    if l3: txt(m, yy, l3, 15, 600, MU); yy -= 20
    txt(m, yy, l2, 16, 700, K2); yy -= 22
    txt(m, yy, title, 19, 900, NV, extra=' text-decoration="underline"')
# grid cells of input (anomaly example)
pat = '00--0---00------'
CY0 = 262  # vertical centre of maps
# ---- INPUT
ix, isz = 30, 128
iy = CY0 - isz / 2; c = isz / 4
A(f'<rect x="{ix}" y="{iy}" width="{isz}" height="{isz}" fill="#FFFFFF" stroke="{K2}" stroke-width="2"/>')
for k, ch in enumerate(pat):
    r, q = divmod(k, 4)
    col = {'-': NV, '+': '#8FA2D4', '0': '#E3E8F4'}[ch]
    A(f'<rect x="{ix+q*c+3:.1f}" y="{iy+r*c+3:.1f}" width="{c-6:.1f}" height="{c-6:.1f}" rx="3" fill="{col}"/>')
A(f'<rect x="{ix+1}" y="{iy+1}" width="{3*c-2:.1f}" height="{3*c-2:.1f}" fill="none" stroke="{OR}" stroke-width="3" stroke-dasharray="6 4"/>')
txt(ix + isz/2, iy + isz + 34, 'INPUT', 19, 900, K)
txt(ix + isz/2, iy + isz + 58, '(4 × 4 × 1)', 16, 700, K2)
txt(ix + isz/2, iy + isz + 80, '16개 상태 패턴', 15, 600, MU)
# ---- stacks
def stack(x0, size, n, off, grid, label_dim, label_ch, fill='#C9D6F2'):
    y0 = CY0 - size / 2 + (n - 1) * off / 2
    for i in range(n - 1, -1, -1):
        x, y = x0 + i * off, y0 - i * off
        A(f'<rect x="{x:.1f}" y="{y:.1f}" width="{size}" height="{size}" fill="{fill}" stroke="{NV3}" stroke-width="1.4"/>')
    # grid on front layer
    g = size / grid
    for t in range(1, grid):
        A(f'<path d="M{x0+t*g:.1f} {y0} V{y0+size}M{x0} {y0+t*g:.1f} H{x0+size}" stroke="{NV3}" stroke-opacity=".45" stroke-width="1"/>')
    bx2 = x0 + (n - 1) * off + size
    txt((x0 + bx2) / 2, y0 + size + 34, label_ch, 16, 700, K2)
    txt((x0 + bx2) / 2, y0 + size + 58, label_dim, 16, 800, NV)
    return x0, y0, size, bx2
# conv
cx0, cy0, cs, cbx = stack(300, 128, 8, 9, 4, '(4 × 4 × 8)', '8 channels')
# projection from input 3x3 window to conv front cell
tx, ty = cx0 + cs/4 * 0.5, cy0 + cs/4 * 0.5
for (px, py) in ((ix + 3*c, iy), (ix + 3*c, iy + 3*c)):
    A(f'<path d="M{px:.1f} {py:.1f} L{tx:.1f} {ty:.1f}" stroke="{OR}" stroke-width="1.6" stroke-dasharray="5 4"/>')
A(f'<circle cx="{tx:.1f}" cy="{ty:.1f}" r="5" fill="{OR}"/>')
brace(300, cbx, 70, 'Conv2D', '3 × 3 kernel · 8 filters', 'same padding')
# pool
px0, py0, ps, pbx = stack(610, 64, 8, 9, 2, '(2 × 2 × 8)', '8 channels', fill='#DCE3F2')
A(f'<rect x="{cx0+2}" y="{cy0+2}" width="{cs/2-4:.1f}" height="{cs/2-4:.1f}" fill="none" stroke="{NV}" stroke-width="2.4"/>')
A(f'<path d="M{cx0+cs/2:.1f} {cy0+cs/4:.1f} L{px0+ps/4:.1f} {py0+ps/4:.1f}" stroke="{NV}" stroke-width="1.6" stroke-dasharray="5 4"/>')
A(f'<circle cx="{px0+ps/4:.1f}" cy="{py0+ps/4:.1f}" r="4.5" fill="{NV}"/>')
brace(610, pbx, 70, 'Max-Pooling', '(2 × 2)')
# flatten bar
fx, fw, fh = 830, 46, 250
fy = CY0 - fh / 2
A(f'<rect x="{fx}" y="{fy}" width="{fw}" height="{fh}" rx="8" fill="#FBE3CC" stroke="{OR}" stroke-width="2"/>')
txt(fx + fw/2 + 6, CY0, 'Flatten · 32', 18, 800, '#A04E10', extra=f' transform="rotate(-90 {fx+fw/2} {CY0})"')
A(f'<path d="M{pbx+8} {CY0} L{fx-8} {CY0}" stroke="{K2}" stroke-width="2" marker-end="url(#ca)"/>')
txt(fx + fw/2, fy + fh + 34, '32 values', 16, 700, K2)
# dense 16
dxn = 1040; nodes = [CY0 - 150 + i * 42 for i in range(6)] + [CY0 + 150]
outs = [(1250, CY0 - 90, '정상'), (1250, CY0, '급속'), (1250, CY0 + 90, '폐색')]
for y in nodes:
    for t in range(6):
        sy = fy + 18 + t * (fh - 36) / 5
        A(f'<path d="M{fx+fw} {sy:.0f} L{dxn-18} {y}" stroke="#9AA7C7" stroke-opacity=".55" stroke-width="1"/>')
    for (ox, oy, _) in outs:
        A(f'<path d="M{dxn+18} {y} L{ox-24} {oy}" stroke="#9AA7C7" stroke-opacity=".55" stroke-width="1"/>')
for k, y in enumerate(nodes):
    A(f'<circle cx="{dxn}" cy="{y}" r="17" fill="{GR}"/>')
txt(dxn, CY0 + 112, '⋮', 26, 900, GR)
txt(dxn, CY0 + 196, "16 units", 16, 800, NV)
brace(dxn - 60, dxn + 60, 70, 'Fully-Connected', 'Dense 16')
for (ox, oy, lab) in outs:
    col = {'정상': GR, '급속': OR, '폐색': RR}[lab]
    A(f'<circle cx="{ox}" cy="{oy}" r="23" fill="{col}"/>')
    txt(ox + 38, oy + 7, lab, 21, 900, K, anc='start')
txt(1270, CY0 + 196, 'OUTPUT', 16, 900, K)
brace(1215, 1330, 70, 'Softmax', 'Dense 3')
# params summary
sx = 1400
A(f'<rect x="{sx}" y="70" width="290" height="330" rx="20" fill="{NV}"/>')
txt(sx + 145, 112, '층별 파라미터', 18, 800, '#C9D4F0')
rows = [('Conv2D', '80'), ('Max-Pooling', '0'), ('Dense 16', '528'), ('Dense 3', '51')]
for k, (a, b) in enumerate(rows):
    y = 152 + k * 40
    txt(sx + 30, y, a, 18, 700, '#FFFFFF', anc='start'); txt(sx + 260, y, b, 20, 800, CY, anc='end')
A(f'<path d="M{sx+26} 300 H{sx+264}" stroke="#FFFFFF" stroke-opacity=".25" stroke-width="2"/>')
txt(sx + 30, 338, '합계', 19, 800, '#FFFFFF', anc='start'); txt(sx + 260, 340, '659개', 32, 900, CY, anc='end')
txt(sx + 145, 378, '≈ 약 10KB · ESP32 실시간 추론', 15, 700, '#C9D4F0')
defs = f'<defs><marker id="ca" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="6" markerHeight="6" orient="auto"><path d="M0 0L10 5L0 10z" fill="{K2}"/></marker></defs>'
svg = (f'<svg class="cnnsvg" viewBox="0 -34 {W} {H+84}" role="img" aria-label="경량 2D CNN 구조 — 입력 4×4×1 상태 패턴, Conv2D 3×3 커널 8필터(4×4×8), Max-Pooling 2×2(2×2×8), Flatten 32, Dense 16, 출력 Dense 3 Softmax(정상·급속·폐색). 파라미터 Conv 80, Dense16 528, Dense3 51, 합계 659개.">' + defs + ''.join(O) + '</svg>')
open(sys.argv[1], 'w').write(svg); print('ok', len(svg))
