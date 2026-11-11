# 공학페스티벌 비즈니스 모델 구조도 v3 — value chain (생산 → INFUTECH → 유통 → 병원) + SaaS/데이터/B2G loops
import sys
NV, NV2, CY, RR, GR, K, K2, MU = '#0B2466', '#1C3A8A', '#1CE8F2', '#E5484D', '#1F9D63', '#0F1A38', '#3F4A66', '#7A84A0'
def tw(s, fs):
    w = 0
    for ch in s:
        o = ord(ch)
        if 0xAC00 <= o <= 0xD7A3: w += 0.98
        elif ch == ' ': w += 0.28
        elif ch == '·': w += 0.36
        elif ch in '()/,.+→㈜': w += 0.62
        elif ch.isdigit(): w += 0.6
        elif ch.isupper(): w += 0.68
        else: w += 0.56
    return w * fs
W, H = 1728, 486
O = []; A = O.append; boxes = []; pills = []
A('<defs>')
for k, c in (('ga', NV2), ('gm', RR), ('gd', GR)):
    A(f'<marker id="{k}" viewBox="0 0 10 10" refX="8.5" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M0 0L10 5L0 10z" fill="{c}"/></marker>')
A(f'<linearGradient id="ghub" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="{NV2}"/><stop offset="1" stop-color="{NV}"/></linearGradient>')
A('<filter id="gsh" x="-10%" y="-10%" width="120%" height="140%"><feDropShadow dx="0" dy="8" stdDeviation="10" flood-color="#0B2466" flood-opacity=".12"/></filter>')
A('</defs>')
def node(x, y, w, h, img, tag, tagc, title, sub, cid, fill, s=60, iconbg='#FFFFFF'):
    A(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="22" fill="{fill}" stroke="#DCE2EE" stroke-width="1.6" filter="url(#gsh)"/>')
    ix, iy = x + 22, y + (h - s) / 2
    A(f'<clipPath id="{cid}"><rect x="{ix}" y="{iy}" width="{s}" height="{s}" rx="14"/></clipPath><rect x="{ix}" y="{iy}" width="{s}" height="{s}" rx="14" fill="{iconbg}"/>')
    if img == 'truck':
        A(f'<g transform="translate({ix + s/2 - 20} {iy + s/2 - 14})" fill="none" stroke="#FFFFFF" stroke-width="3.2" stroke-linejoin="round" stroke-linecap="round"><path d="M1 3h22v18H1z"/><path d="M23 9h8l7 7v5H23z"/><circle cx="9" cy="24" r="4" fill="{iconbg}"/><circle cx="31" cy="24" r="4" fill="{iconbg}"/></g>')
    else:
        A(f'<image href="media/{img}" x="{ix}" y="{iy}" width="{s}" height="{s}" preserveAspectRatio="xMidYMid slice" clip-path="url(#{cid})"/>')
    tx = ix + s + 18; cy = y + h / 2
    tgw = tw(tag, 15) + 20
    A(f'<rect x="{tx}" y="{cy-50}" width="{tgw:.0f}" height="25" rx="12.5" fill="{tagc}"/><text x="{tx + tgw/2:.0f}" y="{cy-32}" text-anchor="middle" font-size="15" font-weight="850" fill="#FFFFFF">{tag}</text>')
    A(f'<text x="{tx}" y="{cy+10}" font-size="26" font-weight="850" fill="{K}">{title}</text>')
    A(f'<text x="{tx}" y="{cy+40}" font-size="17" font-weight="650" fill="{K2}">{sub}</text>')
    right = tx + max(tw(title, 26), tw(sub, 17), tgw)
    assert right <= x + w - 14, (title, right, x + w)
    boxes.append((x, y, x + w, y + h))
def pill(cx, cy, label, col, fs=18):
    w = tw(label, fs) + 28; h = 32
    A(f'<rect x="{cx - w/2:.0f}" y="{cy - h/2:.0f}" width="{w:.0f}" height="{h}" rx="16" fill="#FFFFFF" stroke="{col}" stroke-opacity=".55" stroke-width="1.6"/>')
    A(f'<text x="{cx:.0f}" y="{cy + 6:.0f}" text-anchor="middle" font-size="{fs}" font-weight="800" fill="{col}">{label}</text>')
    pills.append((cx - w/2, cy - h/2, cx + w/2, cy + h/2))
def flow(pts, kind, label=None, at=None):
    col, mk, dash, sw = {'p': (NV2, 'ga', '', 3.2), 'm': (RR, 'gm', ' stroke-dasharray="10 7"', 3), 'd': (GR, 'gd', ' stroke-dasharray="1 8" stroke-linecap="round"', 4.2)}[kind]
    A(f'<path d="M{" L".join(f"{x:.0f} {y:.0f}" for x, y in pts)}" stroke="{col}" stroke-width="{sw}" fill="none" stroke-linejoin="round"{dash} marker-end="url(#{mk})"/>')
    if label:
        cx, cy = at if at else ((pts[0][0] + pts[-1][0]) / 2, (pts[0][1] + pts[-1][1]) / 2)
        pill(cx, cy, label, col)
# ---- main row
Y0, NH = 104, 168; CYM = Y0 + NH / 2
xs = [(0, 268), (444, 300), (920, 332), (1426, 302)]
(px, pw), (hx, hw), (dx, dw), (bx, bw) = xs
node(px, Y0, pw, NH, 'pcb-real.webp', '생산', '#6B7590', '생산 파트너', 'PCB · 금형 · 사출', 'gp', '#FFFFFF', s=64)
# hub
A(f'<rect x="{hx}" y="{Y0-10}" width="{hw}" height="{NH+20}" rx="28" fill="url(#ghub)" filter="url(#gsh)"/>'); boxes.append((hx, Y0-10, hx+hw, Y0+NH+10))
hcx = hx + hw / 2
A(f'<clipPath id="ghc"><circle cx="{hcx}" cy="{Y0+50}" r="44"/></clipPath><circle cx="{hcx}" cy="{Y0+50}" r="44" fill="#FFFFFF"/><image href="media/product.png" x="{hcx-41}" y="{Y0+10}" width="82" height="123" preserveAspectRatio="xMidYMin meet" clip-path="url(#ghc)"/><circle cx="{hcx}" cy="{Y0+50}" r="44" fill="none" stroke="{CY}" stroke-width="4"/>')
A(f'<text x="{hcx}" y="{Y0+130}" text-anchor="middle" font-size="34" font-weight="900" fill="#FFFFFF" letter-spacing="1">INFUTECH</text>')
A(f'<text x="{hcx}" y="{Y0+160}" text-anchor="middle" font-size="17" font-weight="700" fill="#C9D4F0">모듈 · 이상 감지 AI · 관제 SaaS</text>')
node(dx, Y0, dw, NH, 'truck', '유통 파트너', '#E07B2E', '의료기기 유통업체', '㈜에스케이엠엔엠', 'gd1', '#FFF7EE', s=64, iconbg='#E07B2E')
node(bx, Y0, bw, NH, 'ic-hosp.png', 'B2B 고객', NV, '병원', '병상별 설치 · 관제', 'gh1', '#EEF2FB', s=64, iconbg=NV)
# main row flows (product forward above, money back below)
YF, YB = CYM - 26, CYM + 30
def gap(a, b): return a[0] + a[1] + 8, b[0] - 8
for (a, b), fwd, back in (((xs[0], xs[1]), '모듈 납품', '제조비'), ((xs[1], xs[2]), '모듈 공급', '공급 대금'), ((xs[2], xs[3]), '판매 · 설치', '대당 25만 원')):
    l, r = gap(a, b)
    if a == xs[0]:
        flow([(l, YF), (r, YF)], 'p', fwd); flow([(r, YB), (l, YB)], 'm', back)
    else:
        flow([(l, YF), (r, YF)], 'p', fwd); flow([(r, YB), (l, YB)], 'm', back)
# SaaS loop over the top (INFUTECH ↔ 병원 direct)
bcx = bx + bw / 2
flow([(hcx - 50, Y0 - 16), (hcx - 50, 22), (bcx + 60, 22), (bcx + 60, Y0 - 8)], 'p', '관제 SaaS · 유지보수', at=(1180, 22))
flow([(bcx - 60, Y0 - 8), (bcx - 60, 62), (hcx + 50, 62), (hcx + 50, Y0 - 16)], 'm', '월 관리 구독료', at=(1180, 62))
# data loop under the row
YD = Y0 + NH + 52
flow([(bcx, Y0 + NH + 8), (bcx, YD), (hcx + 70, YD), (hcx + 70, Y0 + NH + 16)], 'd', '수액 투여 데이터 → AI 고도화', at=(1176, YD))
# B2G under producer
GX, GY, GW, GH = 0, 352, 300, 128
node(GX, GY, GW, GH, 'ic-gov.png', 'B2G', GR, '공공 · 정부', '스마트 의료 인프라', 'gg1', '#EDF8F2', s=58, iconbg=GR)
YG1, YG2 = GY + 40, GY + 92
flow([(hcx - 70, Y0 + NH + 16), (hcx - 70, YG1), (GX + GW + 8, YG1)], 'p', '관제 인프라 · 데이터', at=(GX + GW + 104, YG1))
flow([(GX + GW + 8, YG2), (hcx - 10, YG2), (hcx - 10, Y0 + NH + 16)], 'm', '보조금 사업 연계', at=(GX + GW + 104, YG2))
# legend
LX, LY = 1236, 462
for i, (k, t) in enumerate((('p', '제품 · 서비스'), ('m', '매출 · 비용'), ('d', '데이터'))):
    x = LX + i * 168
    col, dash, sw = {'p': (NV2, '', 3.2), 'm': (RR, ' stroke-dasharray="10 7"', 3), 'd': (GR, ' stroke-dasharray="1 8" stroke-linecap="round"', 4.2)}[k]
    A(f'<path d="M{x} {LY} L{x+40} {LY}" stroke="{col}" stroke-width="{sw}"{dash}/><text x="{x+50}" y="{LY+6}" font-size="17" font-weight="700" fill="{MU}">{t}</text>')
def ov(a, b): return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])
for i, p in enumerate(pills):
    assert 0 <= p[0] and p[2] <= W and p[1] >= 0 and p[3] <= H, p
    for q in pills[i+1:]: assert not ov(p, q), (p, q)
    for b in boxes: assert not ov(p, b), ('pill on node', p, b)
for (a, b) in ((xs[0], xs[1]), (xs[1], xs[2]), (xs[2], xs[3])):
    l, r = gap(a, b)
    for p in pills:
        if l - 1 <= p[0] and p[2] <= r + 1: pass
        elif p[1] >= Y0 - 10 and p[3] <= Y0 + NH + 10 and not (p[2] <= l or p[0] >= r): raise AssertionError(('pill wider than gap', p, l, r))
svg = (f'<svg class="bmsvg" viewBox="-26 -4 {W+52} {H+26}" overflow="visible" role="img" aria-label="비즈니스 모델 구조도 — 생산 파트너가 모듈을 납품하고, INFUTECH가 의료기기 유통업체 ㈜에스케이엠엔엠에 모듈을 공급하면 유통업체가 병원에 대당 25만 원에 판매·설치합니다. INFUTECH는 병원에 관제 SaaS와 유지보수를 제공해 월 관리 구독료를 받고, 수액 투여 데이터로 AI를 고도화합니다. 공공·정부에는 관제 인프라와 데이터를 제공하고 보조금 사업과 연계합니다.">' + ''.join(O) + '</svg>')
open(sys.argv[1], 'w').write(svg); print('ok', len(svg), len(pills), 'pills')
