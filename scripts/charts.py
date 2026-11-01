#!/usr/bin/env python3
"""INFU RETRO IR 덱 그래프를 Python(NumPy)으로 계산하고 Matplotlib으로 그려 고정된 SVG로 내보냅니다.

글자까지 모두 윤곽선(path)으로 저장하므로 서체 · 브라우저 · 화면 크기가 달라도 똑같이 보이고, 확대해도 선명합니다.

  pip install numpy matplotlib
  python3 scripts/infutech-charts.py          # 서체: node_modules의 Pretendard, 없으면 PRETENDARD_DIR

  charts/gyro.svg       부록 A7 — 학습 장비의 자이로 신호와 무게 편차, 자이로로 보정한 뒤의 잔차
  charts/gyro-mini.svg  8장 — 같은 신호를 한 칸에: 보정 전 편차와 보정 뒤 편차 (본 발표용으로 글자를 크게)
  charts/filter.svg   7장 · 흔들림 구간 원신호와 칼만필터 출력 (썸네일)
  charts/cnn-pattern.svg  7장 · CNN이 보는 4×4 상태 패턴 — 정상 · 이상 (썸네일)

자료 그래프(덱의 막대 · 점 그래프는 모두 여기서 그린다 — HTML로 그리지 않는다)
  charts/clinic-24h.svg      3장 · 서울 동물병원 100곳 중 24시간 운영 약 8곳
  charts/dispute.svg         4장 · 동물병원 피해구제 접수 건수 2021 ~ 2026.6
  charts/resolve.svg         4장 · 진료기록 유무별 분쟁 해결률 (이름 · 숫자 · 막대 · 건수까지 한 장)
  charts/causes.svg          4장 · 피해구제 신청 사유(128건) — 진료상 과실의 네 갈래, 1위 처치 미흡
  charts/market.svg          17장 · 시장 규모 TAM · SAM · SOM (곳 수와 금액까지 한 장)
  charts/grade.svg           14장 · 동물용 의료기기 등급 사다리 — INFU RETRO 구조는 1등급(신고)
  charts/dispute-split.svg   부록 A15 · 상담 → 신청 → 처리 → 해결 흐름과 진료부 확보 여부별 해결 · 미해결
  charts/causes-all.svg      부록 A15 · 신청 사유 100% 누적 막대 (진료상 과실 75% + 그 외 25%)
  charts/pivc.svg            부록 A16 · 수액 카테터 합병증 발생률 — 연구 3편 (영국 · 미국 · 이탈리아)
  charts/treat-cost.svg      부록 A17 · 최근 2년 치료비 2023 → 2025 조사 (전체 가구 · 치료비를 쓴 가구)
  charts/signals.svg         부록 A16 · 무게 곡선 예시(모의 신호) — 정상 · 막힘 · 빠짐이 기대 추세에서 벗어나는 모습
  charts/petcost.svg         부록 A17 · 1마리 월 양육비 12.1만 원 중 병원비 3.7만 원(그중 치료 1.4만 원)
  charts/revenue.svg         부록 A17 · 병원 1곳(5대) 연 매출 — 1년차 장비 + 구독, 2년차부터 구독
  charts/visit.svg           12장 · 양육가구 최근 1년 동물병원 이용률 2021 → 2025 (출처의 두 해만)
  charts/cagr.svg            12장 · 동물용 인퓨전펌프 시장 CAGR 조사기관별 전망
  charts/rx.svg · rx-large.svg   12장 · 부록 A13 · 동물병원 의료용 마약류 처방량 2022 ~ 2025
  charts/epoch.svg           11장 · CNN 검증 정확도 최근 6 epoch
  charts/cost-vs.svg · cost-stack.svg · entry.svg   15장 · 제작비 비교 · 원가 구조 · 입원장 5대 도입비
  charts/bm.svg              18장 · 비즈니스 모델 — 제품 · 돈 흐름, 제공 서비스, 판매 대상과 확대 목표
  charts/t-arch.svg · t-signal.svg · t-cnn.svg   부록 · 시스템 구성 · 판별 파이프라인(논문 식 · 그림) · 경량 CNN 구조
  charts/t-chain.svg         부록 · 하드웨어 신호 경로와 잡음 대책 (PCB 레이아웃 사진의 ①~⑥과 같은 번호)
  charts/t-data.svg          부록 · 데이터 구축 → 전이학습 → 파인튜닝 → 실측 교차 검증 → 기기 배포, 검증 정확도 최근 6 epoch
  charts/t-gyroflow.svg · t-gyroscatter.svg   부록 · 자이로 상관 분석을 학습한 AI 자이로로 보정 — 단계와 상관 산점도(학습 장비 모의 신호)
  charts/v-kaha.svg · v-rank.svg   부록 · 현장의 목소리 — 진료수의사 근무 어려움(한국동물병원협회) · 동물병원 서비스 40개 시장 중 37위(한국소비자원)
  charts/petins.svg          부록 A19 · 펫보험 보유계약 2022 → 2025 (손해보험업계 집계, 3년 새 3.5배)

그림 크기(인치)는 덱에서 차지하는 자리(1080p 기준 px ÷ 96)에 맞춰, 글자가 덱 본문과 같은 크기로 보이게 한다.
막대는 한 기준선에서 자라고, 값 쪽 끝만 둥글게(기준선 쪽은 각지게) 그린다 — 막대 사이 · 조각 사이는 2px 틈으로 가른다.

모든 신호는 모의 데이터입니다. 실측 로그(CSV)가 있으면 simulate() 대신 그 값을 넣으면 같은 차트가 나옵니다.
"""
import glob, math, os, re
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager
from matplotlib.ft2font import LoadFlags
from matplotlib.patches import Ellipse, FancyBboxPatch, PathPatch, Polygon
from matplotlib.path import Path

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DECK = os.path.join(ROOT, 'public', 'infutech') if os.path.isdir(os.path.join(ROOT, 'public', 'infutech')) else ROOT
OUT = os.path.join(DECK, 'charts')

INK, INK2, MUTE, HONEY, ALERT, SAGE, RAW = '#2A1F18', '#5B4B3F', '#76665A', '#AD6229', '#D04E2D', '#4C8744', '#A39282'
GRID, LINE = '#EFE7DC', '#CDBFAF'


def simulate(kind, seed):
    """1 Hz 무게 → 칼만필터(흔들림 게이팅) → 초기 감소량 기대 추세 → 이상 점수."""
    s = seed & 0xFFFFFFFF
    def rnd():
        nonlocal s
        s = (s * 1664525 + 1013904223) & 0xFFFFFFFF
        return s / 4294967296
    def gauss():
        u = 0.0
        while not u:
            u = rnd()
        return math.sqrt(-2 * math.log(u)) * math.cos(2 * math.pi * rnd())
    N, W0, q0, T = 3600, 520, 290 / 3600, 1800
    w = W0; ph = rnd() * 6; raw = []
    for t in range(N):
        q = q0
        # 유속 저하: 줄이 꺾이거나 막혀 1분에 걸쳐 38%로 줄어듦
        if kind == 'drop' and t >= T: q = q0 * (1 - 0.62 * min(1, (t - T) / 60))
        # 줄 빠짐: 카테터에서 분리된 줄로 수액이 계속 새어 나감 — 정맥압이 없어 오히려 조금 빨라짐
        if kind == 'line' and t >= T: q = q0 * 1.35
        # 공기 유입 · 역류: 2분 동안 혈액이 줄을 타고 거꾸로 올라옴
        if kind == 'air' and T <= t < T + 120: q = -q0 * 0.5
        w -= q
        m = w + gauss() * 1.4
        if kind == 'shake' and 720 <= t < 1320:
            env = math.sin(math.pi * (t - 720) / 600)
            m += env * (24 * math.sin(2 * math.pi * 0.43 * t + ph) + gauss() * 10)
            if rnd() < 0.012: m += (rnd() - 0.5) * 110
        # 줄 빠짐: 당겨지는 순간의 장력이 몇 초간 무게처럼 더해짐
        if kind == 'line' and T <= t < T + 6: m += 34 * math.exp(-(t - T) / 2.2) + gauss() * 6
        raw.append(m)
    # constant-velocity Kalman filter; large innovations are down-weighted unless they persist (a real level change)
    x0, x1, P00, P01, P11, run, sgn = raw[0], -q0, 25.0, 0.0, 1e-4, 0, 0
    Qw, Qv, R0, kw = 0.004, 4e-6, 1.96, []
    for t in range(N):
        x0 += x1; P00 += 2 * P01 + P11 + Qw; P01 += P11; P11 += Qv
        inn = raw[t] - x0; z = abs(inn) / math.sqrt(P00 + R0)
        sg = (inn > 0) - (inn < 0)
        run = run + 1 if z > 2 and sg == sgn else (1 if z > 2 else 0); sgn = sg
        R = R0 * (z / 3) ** 4 if z > 3 and run < 6 else R0
        S = P00 + R; K0 = P00 / S; K1 = P01 / S
        x0 += K0 * inn; x1 += K1 * inn
        P00, P01, P11 = (1 - K0) * P00, (1 - K0) * P01, P11 - K1 * P01
        kw.append(x0)
    tt = np.arange(30, 301); rate, b = np.polyfit(tt, np.array(kw)[30:301], 1)
    exp = b + rate * np.arange(N)
    # anomaly score: stands in for the CNN classifier's response to each situation
    score, e = [], 0.06
    for t in range(N):
        tgt = 0.07
        if kind == 'shake' and 720 <= t < 1320: tgt += 0.27 * math.sin(math.pi * (t - 720) / 600) ** 1.5
        if kind == 'drop' and t >= T + 15: tgt = 0.07 + 0.86 * (1 - math.exp(-(t - T - 15) / 35))
        if kind == 'line' and t >= T + 2: tgt = 0.93   # 장력 스파이크 2~3샘플을 보고 판별
        if kind == 'air' and t >= T: tgt = 0.84 if t < T + 120 else 0.08
        tau = 1.6 if kind in ('line', 'air') and T <= t < T + 120 else 18
        e += (tgt - e) / tau
        score.append(max(0.01, min(0.99, e + gauss() * 0.018)))
    return np.array(raw), np.array(kw), exp, np.array(score)


def use_font():
    dirs = [os.environ.get('PRETENDARD_DIR', ''), os.path.join(ROOT, 'node_modules', 'pretendard', 'dist', 'public', 'static')]
    files = [f for d in dirs if d for f in glob.glob(os.path.join(d, 'Pretendard-*.otf'))]
    if not files:
        raise SystemExit('Pretendard OTF가 없습니다 — npm ci 하거나 PRETENDARD_DIR=<Pretendard-*.otf 폴더>')
    for f in files:
        font_manager.fontManager.addfont(f)
    plt.rcParams.update({
        'font.family': 'Pretendard', 'font.size': 9, 'axes.unicode_minus': False,
        'svg.fonttype': 'path', 'svg.hashsalt': 'infu-retro',  # 글자는 윤곽선으로, 결과는 매번 같게
        'axes.edgecolor': LINE, 'axes.linewidth': .8, 'axes.labelcolor': INK2,
        'xtick.color': LINE, 'ytick.color': LINE, 'xtick.labelcolor': MUTE, 'ytick.labelcolor': MUTE,
        'xtick.major.size': 3, 'ytick.major.size': 3,
    })


def save(fig, name, fills=None, blurs=None):
    """fills: {gid: (x1, y1, x2, y2, [(offset, colour, opacity), ...])} — that patch gets an SVG linear gradient
    (bounding-box units, like CSS); blurs: {gid: σ px} — that patch is blurred into a soft shadow"""
    path = os.path.join(OUT, name)
    fig.savefig(path, format='svg', transparent=True, metadata={'Date': None, 'Creator': None})
    plt.close(fig)
    if fills or blurs:
        svg, defs = open(path, encoding='utf-8').read(), []
        for gid, (x1, y1, x2, y2, stops) in (fills or {}).items():
            defs.append(f'<linearGradient id="{gid}-fill" x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}">'
                        + ''.join(f'<stop offset="{o}" stop-color="{c}" stop-opacity="{a}"/>' for o, c, a in stops)
                        + '</linearGradient>')
            svg, n = re.subn(rf'(<g id="{gid}">\s*<path [^>]*?style="fill: )#[0-9a-f]{{6}}', rf'\1url(#{gid}-fill)', svg, count=1)
            assert n == 1, gid
        for gid, sd in (blurs or {}).items():
            defs.append(f'<filter id="{gid}-blur" x="-40%" y="-80%" width="180%" height="260%">'
                        f'<feGaussianBlur stdDeviation="{sd * .75:g}"/></filter>')  # px → pt, the SVG's units
            assert f'<g id="{gid}">' in svg, gid
            svg = svg.replace(f'<g id="{gid}">', f'<g id="{gid}" filter="url(#{gid}-blur)">', 1)
        svg = svg.replace('<defs>', '<defs>\n  ' + '\n  '.join(defs), 1)
        open(path, 'w', encoding='utf-8').write(svg)
    print(path, os.path.getsize(path) // 1024, 'KB')


def gyro_signals():
    # training rig, 12 s at 20 Hz: two pushes on the pole; the load cell's deviation follows the gyro rate
    rng = np.random.default_rng(7)
    t = np.arange(0, 12, 1 / 20)
    env = np.exp(-((t - 3) ** 2) / 1.6) + .7 * np.exp(-((t - 8.2) ** 2) / 1.1)
    gyro = 38 * env * np.sin(2 * np.pi * 1.15 * t) + rng.normal(0, 1.2, t.size)            # deg/s
    lag = 2
    dev = .2 * np.roll(gyro, lag) + .006 * np.gradient(gyro, t) + rng.normal(0, .55, t.size)  # g
    dev[:lag] = rng.normal(0, .55, lag)
    # learn the gyro → deviation relation by least squares on lagged gyro and its derivative
    X = np.column_stack([np.roll(gyro, k) for k in range(4)] + [np.gradient(gyro, t), np.ones_like(t)])
    coef, *_ = np.linalg.lstsq(X[4:], dev[4:], rcond=None)
    res = dev - X @ coef
    r = float(np.corrcoef(np.roll(gyro, lag)[4:], dev[4:])[0, 1])
    rms0, rms1 = float(np.sqrt(np.mean(dev[4:] ** 2))), float(np.sqrt(np.mean(res[4:] ** 2)))
    return t, gyro, dev, res, r, rms0, rms1


def chart_gyro():
    t, gyro, dev, res, r, rms0, rms1 = gyro_signals()
    lim = float(max(abs(dev).max(), abs(res).max()) * 1.15)
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(7.2, 4.4), gridspec_kw=dict(hspace=.62))
    rows = [(gyro, SAGE, '자이로 각속도 (°/s)', '흔들림 두 번', MUTE),
            (dev, HONEY, '같은 시각 무게 편차 (g)', f'r = {r:.2f} · 자이로와 상관', HONEY),
            (res, INK, '자이로로 보정한 뒤 (g)', f'편차 RMS {rms0:.1f} g → {rms1:.1f} g', INK)]
    for ax, (y, col, left, right, rc) in zip(axs, rows):
        ax.plot(t, y, color=col, lw=1.3, solid_joinstyle='round')
        ax.set_title(left, loc='left', fontsize=10.5, fontweight='semibold', color=INK2, pad=5)
        ax.set_title(right, loc='right', fontsize=10.5, fontweight='bold', color=rc, pad=5)
        ax.grid(axis='y', color=GRID, lw=.8)
        ax.set_axisbelow(True)
        for side in ('top', 'right'):
            ax.spines[side].set_visible(False)
        ax.tick_params(labelsize=10.5)
    axs[0].set_ylim(-46, 46); axs[0].set_yticks([-40, 0, 40])
    for ax in axs[1:]:
        ax.set_ylim(-lim, lim); ax.set_yticks([-5, 0, 5])
    axs[2].set_xlim(0, 12); axs[2].set_xticks(range(0, 13, 2))
    axs[2].set_xlabel('시간 (s) · 20 Hz 샘플링', fontsize=10.5, color=INK2, labelpad=4)
    fig.subplots_adjust(left=.075, right=.985, top=.93, bottom=.11)
    return fig, (r, rms0, rms1)


def chart_gyro_mini():
    # one panel for the main talk: the deviation the shaking leaves, before and after the learned correction
    t, gyro, dev, res, r, rms0, rms1 = gyro_signals()
    fig, ax = plt.subplots(figsize=(5.6, 2.5))
    ax.plot(t, dev, color=HONEY, lw=1.6, label=f'보정 전 · RMS {rms0:.1f} g')
    ax.plot(t, res, color=INK, lw=1.6, label=f'보정 후 · RMS {rms1:.1f} g')
    ax.set_title('흔들림이 만든 무게 편차 (g)', loc='left', fontsize=11, fontweight='semibold', color=INK2, pad=6)
    ax.set_title(f'자이로와 상관 r = {r:.2f}', loc='right', fontsize=11, fontweight='bold', color=HONEY, pad=6)
    lim = float(max(abs(dev).max(), abs(res).max()) * 1.15)
    ax.set_ylim(-lim, lim * 1.6); ax.set_yticks([-5, 0, 5])  # headroom above the traces for the legend
    ax.set_xlim(0, 12); ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel('시간 (s) · 학습 장비 20 Hz', fontsize=11, color=INK2, labelpad=3)
    ax.grid(axis='y', color=GRID, lw=.8); ax.set_axisbelow(True)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=11)
    leg = ax.legend(loc='upper right', ncol=2, fontsize=11, frameon=False, handlelength=1.4, columnspacing=1.2, borderaxespad=.1)
    for txt, col in zip(leg.get_texts(), (HONEY, INK)):
        txt.set_color(col)
    fig.subplots_adjust(left=.075, right=.985, top=.86, bottom=.22)
    return fig


BAR_OFF, BAR_DIM = '#E3D8CB', '#D9CBBA'


def px(w, h):
    """figure size for a box of w × h px on the 1080p stage (SVG renders 1 in = 96 px)"""
    return (w / 96, h / 96)


def chart_clinic24h():
    # 100 dots, 8 lit: 24-hour clinics in Seoul (7.95%)
    fig = plt.figure(figsize=px(300, 71))
    ax = fig.add_axes([0, 0, 1, 1])
    k = np.arange(100)
    ax.scatter(k % 20, -(k // 20), s=58, c=[HONEY if i < 8 else '#E6DCCF' for i in k], linewidths=0)
    ax.set_xlim(-.6, 19.6); ax.set_ylim(-4.6, .6); ax.axis('off')
    return fig


def chart_dispute():
    vals = [9, 20, 11, 16, 27, 45]
    labs = ['2021', '2022', '2023', '2024', '2025', '2026\n1~6월']
    return columns(vals, labs, (300, 380), {5}, lambda v: f'{v}', value_px=17, label_px=14, bar_px=32)


# ---- figures laid out in px like the deck's HTML: text runs on a baseline, rounded boxes, pills ----
PT = .75  # 1 px on the 1080p stage = .75 pt
WEIGHT = {400: 'regular', 500: 'medium', 600: 'semibold', 700: 'bold', 800: 'extra bold'}


def canvas(w, h):
    """w × h px figure whose data coordinates are px from its top-left corner"""
    fig = plt.figure(figsize=px(w, h))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, w); ax.set_ylim(h, 0); ax.axis('off')
    return fig, ax


def advance(s, size, weight):
    """advance width in px of s set at size px — what the browser lays out, so runs can follow each other"""
    font = font_manager.get_font(font_manager.findfont(font_manager.FontProperties(family='Pretendard', weight=WEIGHT[weight])))
    font.set_size(size, 72)
    return sum(font.load_char(ord(c), flags=LoadFlags.NO_HINTING).linearHoriAdvance / 65536 for c in s)


def say(ax, x, y, runs, ha='left', z=3):
    """one line with its baseline at y: runs of (text, size px, weight, colour[, letter-spacing em, gap em]);
    letter-spacing is set glyph by glyph as CSS does. Returns the line's width."""
    runs = [r + (0, 0)[len(r) - 4:] if len(r) < 6 else r for r in runs]
    width = sum(g * sz + advance(t, sz, w) + tr * sz * len(t) for t, sz, w, _, tr, g in runs)
    x0 = x - width if ha == 'right' else x - width / 2 if ha == 'center' else x
    for t, sz, w, col, tr, g in runs:
        x0 += g * sz
        for piece in (t if tr else [t]):
            ax.text(x0, y, piece, fontsize=sz * PT, fontweight=WEIGHT[w], color=col, ha='left', va='baseline', zorder=z)
            x0 += advance(piece, sz, w) + tr * sz * len(piece)
    return width


def rbox(ax, x, y, w, h, r, z=1, gid=None, **kw):
    p = FancyBboxPatch((x, y), w, h, boxstyle=f'round,pad=0,rounding_size={r}', zorder=z, gid=gid, **kw)
    ax.add_patch(p)
    return p


def shape(x0, y0, x1, y1, tl=0, tr=0, br=0, bl=0):
    """rectangle (px, y down) with its own radius on each corner — bars round only their data end"""
    v = [(x0 + tl, y0), (x1 - tr, y0), (x1, y0), (x1, y0 + tr), (x1, y1 - br), (x1, y1), (x1 - br, y1),
         (x0 + bl, y1), (x0, y1), (x0, y1 - bl), (x0, y0 + tl), (x0, y0), (x0 + tl, y0), (x0 + tl, y0)]
    c = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3,
         Path.LINETO, Path.CURVE3, Path.CURVE3, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.CLOSEPOLY]
    return Path(v, c)


def columns(values, labels, size, hl, fmt, value_px=20, label_px=16, bar_px=56, fill=BAR_OFF):
    """vertical bars from one baseline (rounded data end, square on the baseline), the value on each cap and the
    category under it; bars in hl are honey, the others `fill`"""
    W, H = size
    fig, ax = canvas(W, H)
    lines = max(l.count('\n') + 1 for l in labels)
    base = H - 10 - label_px * 1.25 * lines   # the category labels sit under the baseline
    room = base - value_px * 1.9                # the tallest bar leaves room for its value
    band = W / len(values)
    ax.plot([0, W], [base, base], color=LINE, lw=PT, solid_capstyle='butt', zorder=3)
    for k, (v, lab) in enumerate(zip(values, labels)):
        xc, top, on = band * (k + .5), base - room * v / max(values), k in hl
        r = min(6, bar_px / 2)
        ax.add_patch(PathPatch(shape(xc - bar_px / 2, top, xc + bar_px / 2, base, tl=r, tr=r), facecolor=HONEY if on else fill, lw=0, zorder=2))
        say(ax, xc, top - value_px * .45, [(fmt(v), value_px, 700, HONEY if on else INK2)], ha='center')
        for i, line in enumerate(lab.split('\n')):
            say(ax, xc, base + 8 + label_px * (.95 + 1.25 * i), [(line, label_px, 400, MUTE)], ha='center')
    return fig


def hbars(rows, size, label_w=None, value_px=17, label_px=16, bar_px=24):
    """horizontal bars from one left baseline with a rounded data end, one row per
    (label, value, text, colour, label colour, hatch). The label sits left of the bar (label_w px wide)
    or, with label_w=None, on its own line above it so the bars get the full width."""
    W, H = size
    fig, ax = canvas(W, H)
    n, vmax = len(rows), max(r[1] for r in rows)
    x0 = label_w or 0
    room = W - x0 - max(advance(r[2], value_px, 700) for r in rows) - 12
    for k, (lab, v, txt, col, lcol, hatch) in enumerate(rows):
        row = H / n
        weight = 700 if lcol == HONEY else 500
        if label_w:
            cy = row * (k + .5)
            say(ax, x0 - 14, cy + .36 * label_px, [(lab, label_px, weight, lcol)], ha='right')
        else:
            cy = row * k + label_px * 1.3 + bar_px / 2
            say(ax, 0, row * k + label_px * .95, [(lab, label_px, weight, lcol)])
        end = x0 + room * v / vmax
        r = min(6, bar_px / 2)
        ax.add_patch(PathPatch(shape(x0, cy - bar_px / 2, end, cy + bar_px / 2, tr=r, br=r), facecolor=col,
                               edgecolor='#FFFFFF' if hatch else 'none', hatch=hatch, lw=0, zorder=2))
        say(ax, end + 10, cy + .36 * value_px, [(txt, value_px, 700, HONEY if lcol == HONEY else INK)])
    return fig


def pill(ax, right, cy, text, size, col, bg, z):
    """CSS pill: padding .22em .75em, fully rounded, text right edge at right − padding"""
    w = advance(text, size, 800)
    h = size * 1.2 + size * .44
    rbox(ax, right - w - size * 1.5, cy - h / 2, w + size * 1.5, h, h / 2, z=z, color=bg, lw=0)
    say(ax, right - size * .75, cy + size * .37, [(text, size, 800, col)], ha='right', z=z + .1)


def chart_resolve():
    # 진료기록 유무별 분쟁 해결률: 위아래 두 줄 (IR 6장 가운데 카드 오른쪽, 약 300 × 230 px)
    W, H = 300, 230
    fig, ax = canvas(W, H)
    for k, (lab, rate, cases, bar, num) in enumerate([('기록 있음', 30, '80건 중 24건', HONEY, HONEY),
                                                    ('기록 없음', 19.5, '41건 중 8건', '#B8A797', INK2)]):
        y = k * 118
        say(ax, 0, y + 18, [(lab, 16, 700, INK2)])
        say(ax, 0, y + 70, [(f'{rate:g}', 50, 800, num, -.04), ('%', 22, 700, num, 0, .06)])
        say(ax, W, y + 70, [(cases, 14.5, 500, MUTE)], ha='right')
        rbox(ax, 0, y + 84, W, 13, 6.5, color='#F2E5D9' if k == 0 else '#F0ECE7', lw=0)
        rbox(ax, 0, y + 84, W * rate / 100, 13, 6.5, z=2, color=bar, lw=0)
    return fig


# 한국소비자원 동물병원 소비자피해 분석(2026.9, 2021~2026.6): 피해구제 128건 기준 신청 사유 — 진료상 과실 96건(75%)
CAUSES = [('처치 미흡', 32.0), ('수술 부작용', 26.6), ('진단 과실', 10.2), ('안전사고', 6.2)]


def chart_causes():
    # 4장 오른쪽 카드 아래(폭 575 px): 진료상 과실의 네 갈래 — 1위 처치 미흡만 honey
    rows = [(lab, v, f'{v:.1f}%', HONEY if k == 0 else BAR_DIM, HONEY if k == 0 else INK2, None) for k, (lab, v) in enumerate(CAUSES)]
    return hbars(rows, (575, 124), label_w=104, value_px=16.5, label_px=16, bar_px=15)


def chart_dispute_split():
    # 부록 A15 (529 × 606 px): 위 — 상담에서 해결까지 네 단계, 아래 — 처리 완료 121건을 진료부 확보 여부로 나눈 해결 · 미해결
    W, H = 529, 606
    fig, ax = canvas(W, H)
    steps = [('1,941', '상담'), ('128', '피해구제 신청'), ('121', '처리 완료'), ('32', '분쟁 해결')]
    bw, gap = 112, (W - 4 * 112) / 3
    for k, (num, lab) in enumerate(steps):
        x, last = k * (bw + gap), k == len(steps) - 1
        rbox(ax, x, 0, bw, 84, 12, color='#FBEBDD' if last else '#F4EEE7', lw=0)
        say(ax, x + bw / 2, 42, [(num, 27, 800, HONEY if last else INK)], ha='center')
        say(ax, x + bw / 2, 68, [(lab, 14.5, 600, HONEY if last else MUTE)], ha='center')
        if not last:  # arrow to the next step
            ax.annotate('', xy=(x + bw + gap - 3, 42), xytext=(x + bw + 3, 42),
                        arrowprops=dict(arrowstyle='-|>', color=LINE, lw=1.4, mutation_scale=11, shrinkA=0, shrinkB=0))
    say(ax, 0, 146, [('처리 완료 121건 — 진료부 확보 여부별', 17, 700, INK)])
    for k, (lab, col) in enumerate((('해결', HONEY), ('해결 못 함', '#E6DBCD'))):  # legend
        x = 0 if k == 0 else 74
        rbox(ax, x, 166, 13, 13, 3, color=col, lw=0)
        say(ax, x + 20, 178, [(lab, 14.5, 500, INK2)])
    rows = [('전체', 121, 32), ('진료부 확보', 80, 24), ('진료부 미확보', 41, 8)]
    room = W - advance('해결 26.4%', 17, 700) - 14
    for k, (lab, n, ok) in enumerate(rows):
        top = 218 + k * 130
        say(ax, 0, top + 16, [(lab, 16.5, 700, INK), (f'  {n}건', 15, 500, MUTE)])
        y0, y1 = top + 30, top + 30 + 38
        full, w_ok = room * n / 121, room * ok / 121
        ax.add_patch(PathPatch(shape(0, y0, w_ok - 1, y1), facecolor=HONEY, lw=0))
        ax.add_patch(PathPatch(shape(w_ok + 1, y0, full, y1, tr=6, br=6), facecolor='#E6DBCD', lw=0))
        say(ax, w_ok / 2, (y0 + y1) / 2 + .36 * 15, [(f'{ok}', 15, 700, '#FFFFFF')], ha='center')
        if full - w_ok > 30:
            say(ax, (w_ok + full) / 2, (y0 + y1) / 2 + .36 * 15, [(f'{n - ok}', 15, 600, INK2)], ha='center')
        say(ax, full + 12, (y0 + y1) / 2 + .36 * 17, [(f'해결 {ok / n * 100:.1f}%', 17, 700, HONEY if k else INK)])
    return fig


def chart_causes_all():
    # 부록 A15 (466 × 606 px): 신청 사유 128건을 한 기둥에 — 진료상 과실 네 갈래(75%)와 그 외(25%), 조각 사이 2px 틈
    W, H = 466, 606
    fig, ax = canvas(W, H)
    parts = CAUSES + [('그 외', 25.0)]
    x0, x1, top, bottom, GAP = 150, 262, 8, 598, 2
    span = bottom - top - GAP * (len(parts) - 1)
    y = top
    for k, (lab, v) in enumerate(parts):
        h = span * v / 100
        col = HONEY if k == 0 else ('#EFD3B4' if k < 4 else '#E6DBCD')
        r = 8
        ax.add_patch(PathPatch(shape(x0, y, x1, y + h, tl=r if k == 0 else 0, tr=r if k == 0 else 0,
                                     bl=r if k == len(parts) - 1 else 0, br=r if k == len(parts) - 1 else 0), facecolor=col, lw=0))
        cy = y + h / 2
        say(ax, x1 + 16, cy + .36 * 17, [(lab, 17, 700 if k == 0 else 600, HONEY if k == 0 else INK), (f'  {v:.1f}%', 17, 700, HONEY if k == 0 else INK2)])
        y += h + GAP
    fault = span * .75 + GAP * 3   # bracket: the four kinds of clinical fault
    ax.plot([x0 - 14, x0 - 22, x0 - 22, x0 - 14], [top, top, top + fault, top + fault], color=LINE, lw=1.1 * PT * 1.4, zorder=1)
    say(ax, x0 - 34, top + fault / 2 - 4, [('진료상 과실', 16, 700, INK)], ha='right')
    say(ax, x0 - 34, top + fault / 2 + 20, [('75% · 96건', 16, 700, HONEY)], ha='right')
    return fig


def chart_pivc():
    # 부록 A16 (529 × 606 px): 수액 카테터 합병증 발생률 — 연구 3편, 카테터 기준. 발표에 쓴 영국 다기관 연구만 honey
    W, H = 529, 606
    fig, ax = canvas(W, H)
    studies = [('이탈리아 테라모 대학병원 · 2022', '개 76 · 고양이 40 · 6개월 전향 연구', 46.6, False, []),
               ('영국 19개 기관 다기관 연구 · 2024', '카테터 382개 · 개 325 · 고양이 57', 26.7, True, []),
               ('미국 CSU 대학병원 · 2023', '개 396마리 · 카테터 412개', 19.9, False, [('중환자실', 24.2), ('중간 병동', 13.1)])]
    room = W - advance('46.6%', 20, 800) - 14
    BAR, SUB = 36, 12
    heights = [58 + BAR + len(subs) * (SUB + 12) for *_, subs in studies]
    gap = (H - 6 - sum(heights)) / (len(studies) - 1)   # spread the studies over the card
    y = 4
    for (title, detail, v, main, subs), h in zip(studies, heights):
        say(ax, 0, y + 18, [(title, 17.5, 700, HONEY if main else INK)])
        say(ax, 0, y + 43, [(detail, 15, 500, MUTE)])
        y0 = y + 58
        w = room * v / 46.6
        ax.add_patch(PathPatch(shape(0, y0, w, y0 + BAR, tr=6, br=6), facecolor=HONEY if main else BAR_DIM, lw=0))
        say(ax, w + 12, y0 + BAR / 2 + .36 * 20, [(f'{v:.1f}%', 20, 800, HONEY if main else INK)])
        ys = y0 + BAR
        for lab, sv in subs:   # ward split, thinner bars under the study's bar
            ys += 12
            sw = room * sv / 46.6
            ax.add_patch(PathPatch(shape(0, ys, sw, ys + SUB, tr=4, br=4), facecolor='#E6DBCD', lw=0))
            say(ax, sw + 10, ys + SUB / 2 + .36 * 14.5, [(f'{lab} {sv:.1f}%', 14.5, 600, INK2)])
            ys += SUB
        y += h + gap
    return fig


def chart_signals():
    # 부록 A16 세 번째 카드(457 × 232 px): 기대 추세와의 차이(g), 모의 신호 20분 — 막힘은 덜 줄고, 빠짐은 당김이 튄 뒤 더 빨리 줆
    W, H = 457, 232
    fig, ax = canvas(W, H)
    rows = [('정상', 'normal', 11), ('막힘 · 꼬임', 'drop', 12), ('빠짐 · 줄 끊김', 'line', 13)]
    t0, t1, T = 1500, 2700, 1800
    lab_w, rh = 116, H / 3
    scale = rh * .5 / 45                        # the same g scale in every row: ±45 g fills a row
    xs = lambda t: lab_w + (t - t0) / (t1 - t0) * (W - lab_w - 2)
    for k, (lab, kind, seed) in enumerate(rows):
        raw, kw, exp, score = simulate(kind, seed)
        cy = rh * (k + .5)
        say(ax, 0, cy + .36 * 15.5, [(lab, 15.5, 700 if k else 600, INK if k else INK2)])
        rbox(ax, lab_w, cy - 5 * scale, W - lab_w - 2, 10 * scale, 2, color='#F2EBE2', lw=0)   # ±5 g: within normal
        ax.plot([lab_w, W - 2], [cy, cy], color=LINE, lw=.6, zorder=1)
        if k:
            ax.plot([xs(T), xs(T)], [cy - rh * .46, cy + rh * .46], color=LINE, lw=.9, ls=(0, (2, 2)), zorder=1)
        dev = np.convolve(raw - exp, np.ones(5) / 5, mode='same')   # 5-second moving average of the measured weight
        t = np.arange(t0, t1, 2)
        ax.plot(xs(t), cy - dev[t] * scale, color=HONEY if k else INK2, lw=2 * PT * 1.25, solid_joinstyle='round', zorder=2)
    say(ax, xs(T) + 5, H - 3, [('이상 시작', 12.5, 600, MUTE)])
    return fig


def chart_treat_cost():
    # 부록 A17 (529 × 632 px): 최근 2년 치료비(만 원) — KB 2023 · 2025 조사, 전체 가구 평균과 치료비를 쓴 가구 평균
    W, H = 529, 632
    fig, ax = canvas(W, H)
    for k, (lab, col) in enumerate((('2023 조사', BAR_DIM), ('2025 조사', HONEY))):  # legend
        x = k * 110
        rbox(ax, x, 4, 13, 13, 3, color=col, lw=0)
        say(ax, x + 20, 16, [(lab, 14.5, 500, INK2)])
    groups = [('전체 가구 평균', 57.7, 102.7), ('치료비를 쓴 가구 평균', 78.7, 146.3)]
    base, top, bar, inner = 560, 92, 76, 12
    ax.plot([0, W], [base, base], color=LINE, lw=PT, solid_capstyle='butt', zorder=3)
    for g, (lab, a, b) in enumerate(groups):
        xc = W * (g + .5) / 2
        for j, (v, col) in enumerate(((a, BAR_DIM), (b, HONEY))):
            x = xc - inner / 2 - bar if j == 0 else xc + inner / 2
            yt = base - (base - top) * v / 146.3
            ax.add_patch(PathPatch(shape(x, yt, x + bar, base, tl=6, tr=6), facecolor=col, lw=0, zorder=2))
            say(ax, x + bar / 2, yt - 10, [(f'{v:g}만', 18, 700, HONEY if j else INK2)], ha='center')
        say(ax, xc, base + 30, [(lab, 16, 600, INK2)], ha='center')
        say(ax, xc, base + 54, [(f'{b / a:.1f}배', 15, 700, HONEY)], ha='center')
    return fig


def chart_petcost():
    # 부록 A17 (468 × 112 px): 1마리 월 양육비 12.1만 원 — 병원비 3.7만 원(31%, 그중 사고 · 상해 · 질병 치료 1.4만 원)과 그 외 8.4만 원
    W, H, GAP = 468, 112, 2
    fig, ax = canvas(W, H)
    parts = [(1.4, HONEY, '치료 1.4만'), (2.3, '#EFD3B4', '그 외 병원비 2.3만'), (8.4, '#E6DBCD', '병원비 외 8.4만')]
    total, x, y0, y1 = 12.1, 0, 40, 76
    span = W - GAP * (len(parts) - 1)
    edges = []
    for k, (v, col, lab) in enumerate(parts):
        w = span * v / total
        l, r = (6 if k == 0 else 0), (6 if k == len(parts) - 1 else 0)
        ax.add_patch(PathPatch(shape(x, y0, x + w, y1, tl=l, bl=l, tr=r, br=r), facecolor=col, lw=0))
        edges.append((x, x + w))
        x += w + GAP
    say(ax, 0, 101, [(parts[0][2], 14.5, 700, HONEY)])
    # the treatment slice is narrow: its neighbour's label starts after the first label, not at the slice edge
    say(ax, max(edges[1][0], advance(parts[0][2], 14.5, 700) + 14), 101, [(parts[1][2], 14.5, 600, INK2)])
    say(ax, W, 101, [(parts[2][2], 14.5, 600, INK2)], ha='right')
    hx = edges[1][1]   # bracket over the hospital share
    ax.plot([0, 0, hx, hx], [y0 - 6, y0 - 12, y0 - 12, y0 - 6], color=HONEY, lw=1.2, zorder=1)
    say(ax, 0, y0 - 19, [('병원비 3.7만 원 · 31%', 15.5, 800, HONEY)])
    return fig


def chart_revenue():
    # 부록 A17 (457 × 206 px): 병원 1곳(입원장 5대) 연 매출 — 1년차 장비 125만 + 구독 720만, 2년차부터 구독 720만
    W, H = 457, 206
    fig, ax = canvas(W, H)
    for k, (lab, col) in enumerate((('구독(관리비 포함)', HONEY), ('장비', '#EFD3B4'))):  # legend
        x = 0 if k == 0 else 150
        rbox(ax, x, 2, 13, 13, 3, color=col, lw=0)
        say(ax, x + 20, 14, [(lab, 14.5, 500, INK2)])
    years = [('1년차', 720, 125), ('2년차', 720, 0), ('3년차', 720, 0)]
    base, top, bar = 176, 52, 84
    ax.plot([0, W], [base, base], color=LINE, lw=PT, solid_capstyle='butt', zorder=3)
    scale = (base - top) / 845
    for k, (lab, sub, equip) in enumerate(years):
        xc = W * (k + .5) / 3
        y_sub = base - sub * scale
        ax.add_patch(PathPatch(shape(xc - bar / 2, y_sub, xc + bar / 2, base, tl=0 if equip else 6, tr=0 if equip else 6), facecolor=HONEY, lw=0, zorder=2))
        if equip:
            y_eq = y_sub - 2 - equip * scale
            ax.add_patch(PathPatch(shape(xc - bar / 2, y_eq, xc + bar / 2, y_sub - 2, tl=6, tr=6), facecolor='#EFD3B4', lw=0, zorder=2))
        say(ax, xc, (y_eq if equip else y_sub) - 9, [(f'{sub + equip}만', 17, 700, INK)], ha='center')
        say(ax, xc, base + 22, [(lab, 15, 600, INK2)], ha='center')
    return fig


def chart_market():
    # 17장 시장 규모: TAM · SAM · SOM 상자를 계단처럼 겹치고 왼쪽에 위로 커지는 화살표 (덱의 자리 553 × 763 px)
    W, H = 553, 763
    fig, ax = canvas(W, H)
    top = H * .04
    arrow = [(15, 0), (30, 34), (20, 34), (20, 300), (10, 300), (10, 34), (0, 34)]
    ax.add_patch(Polygon([(8 + x / 30 * 52, top + y / 300 * (H - top)) for x, y in arrow], closed=True, color='#A9723F', lw=0, gid='arrow'))
    tiers = [  # left, top, height; label, value, money; box colour; text colours; pill background; shadow opacity
        (88, 0, 301, 'TAM · 전세계 · 동물용 인퓨전펌프(인접)', '3.15억 달러', '약 4,400억 원', '#F2EADF', (INK2, INK, HONEY), (173 / 255, 98 / 255, 41 / 255, .12), 0),
        (136, 284, 247, 'SAM · 국내 · 전국 동물병원(상한)', '5,312곳', '약 316억 원', '#EAD9C3', (INK2, INK, HONEY), (173 / 255, 98 / 255, 41 / 255, .12), .08),
        (184, 515, 248, 'SOM · 호남권 · 전남 · 전북(상한)', '약 300곳', '약 18억 원', '#B46A2F', ((1, 1, 1, .85), '#FFFFFF', '#FFFFFF'), (1, 1, 1, .2), .18)]
    for k, (x, y, h, lab, val, money, fill, (c_lab, c_val, c_money), bg, shadow) in enumerate(tiers):
        z = 2 + k * 3
        if shadow:  # box-shadow: 0 −.6em 1.6em — cast upward onto the tier behind
            rbox(ax, x, y - 12, W - x, h, 20, z=z - 1, gid=f'sh{k}', color='#5C3E24', alpha=shadow, lw=0)
        rbox(ax, x, y, W - x, h, 20, z=z, gid=f't{k}', facecolor=fill, edgecolor='#E6DBCD' if k == 0 else 'none', lw=PT if k == 0 else 0)
        cy, right = y + h / 2, W - 28
        say(ax, right, cy - 44, [(lab, 21, 600, c_lab)], ha='right', z=z + .2)
        say(ax, right, cy + 11, [(val, 50, 800, c_val, -.035)], ha='right', z=z + .2)
        pill(ax, right, cy + 43, money, 24, c_money, bg, z + .2)
        if k == 2:
            say(ax, right, cy + 92, [('구독 30% 시 약 9억 원', 18, 600, (1, 1, 1, .85))], ha='right', z=z + .2)
    return fig


def chart_visit():
    # only the two years the source gives: 2021 73.0% and 2025 95.1%
    return columns([73.0, 95.1], ['2021', '2025'], (460, 320), {1}, lambda v: f'{v:.1f}%', value_px=22, label_px=17, bar_px=84)


def chart_cagr():
    # four firms' forecasts as horizontal bars in one colour — firms are not a time axis, so no left-to-right "trend"
    rows = [(n, v, f'{v:g}%', '#E9BE8C', INK2, None) for n, v in
            [('Data Bridge', 12.3), ('Grand View', 7.4), ('GM Insights', 7.2), ('MRF', 6.55)]]
    return hbars(rows, (460, 300), label_w=118, value_px=20, label_px=17, bar_px=34)


RX = [257.6, 299.2, 323.6, 353.0]
def chart_rx(size, large=False):
    labs = ['2022', '2023', '2024', '2025']
    fmt = (lambda v: f'{v:g}') if large else (lambda v: f'{v:g}만')
    return columns(RX, labs, size, {3}, fmt, value_px=20 if large else 18, label_px=16.5 if large else 16,
                   bar_px=84 if large else 56)


def chart_epoch():
    # validation accuracy of the last six epochs, as dots on a 94–100% scale (not bars on a cut axis)
    acc = [95.66, 99.0, 95.24, 97.29, 97.41, 99.0]
    mean = sum(acc) / len(acc)
    fig, ax = plt.subplots(figsize=px(339, 104))
    x = np.arange(6)
    ax.plot([-.4, 5.3], [mean, mean], color=HONEY, lw=1.1, ls=(0, (3, 2.5)), zorder=1)
    ax.text(5.45, mean, f'평균 {mean:.1f}', ha='left', va='center', fontsize=11, fontweight='bold', color=HONEY)
    ax.plot(x, acc, color=BAR_DIM, lw=1.4, zorder=2)
    ax.scatter(x, acc, s=34, color=HONEY, zorder=3, linewidths=0)
    ax.set_xticks(x, [f'{e}' for e in range(62, 68)])
    ax.set_xlabel('학습 에폭 62~67(마지막 6회) · 내부 검증셋', fontsize=14 * .75, color=MUTE, labelpad=4)
    ax.set_yticks([95, 99]); ax.set_ylim(94, 100.2); ax.set_xlim(-.4, 6.6)
    ax.tick_params(axis='both', labelsize=11, labelcolor=MUTE, length=0, pad=3)
    for side in ('top', 'right', 'left', 'bottom'):
        ax.spines[side].set_visible(False)
    ax.grid(axis='y', color=GRID, lw=.8); ax.set_axisbelow(True)
    fig.subplots_adjust(left=.07, right=.8, top=.96, bottom=.2)
    return fig


def chart_cost_vs():
    plt.rcParams['hatch.color'] = '#FFFFFF'; plt.rcParams['hatch.linewidth'] = 2
    return hbars([('다중 센서 스마트 폴대 · 제작비', 100, '100만 원+', BAR_DIM, INK2, '//'),
                  ('INFU RETRO · 실질 판매원가', 8, '8만 원', HONEY, HONEY, None)], (787, 84), label_w=236,
                 value_px=17.5, label_px=16.5, bar_px=26)


def chart_cost_stack():
    # 원가 8만 원의 구성: 조각 사이는 2px 틈(카드 바탕), 바깥 두 끝만 둥글게
    W, H, GAP = 787, 48, 2
    fig, ax = canvas(W, H)
    parts = [('제조 3.5만', 35, HONEY, '#FFFFFF'), ('운영 2만', 20, '#EDBB85', INK), ('유통 2.5만', 25, '#EFE5D8', INK2)]
    total, x = sum(p[1] for p in parts), 0
    for k, (lab, w, col, tcol) in enumerate(parts):
        seg = (W - GAP * (len(parts) - 1)) * w / total
        l, r = (6 if k == 0 else 0), (6 if k == len(parts) - 1 else 0)
        ax.add_patch(PathPatch(shape(x, 0, x + seg, H, tl=l, bl=l, tr=r, br=r), facecolor=col, lw=0))
        say(ax, x + seg / 2, H / 2 + .36 * 16, [(lab, 16, 700, tcol)], ha='center')
        x += seg + GAP
    return fig


def chart_entry():
    # labels above the bars so both bars use the card's full width
    return hbars([('펌프 5대', 550, '550만', BAR_DIM, INK2, None),
                  ('INFU RETRO 5대', 125, '125만', HONEY, HONEY, None)], (331, 136), value_px=18, label_px=15.5, bar_px=28)


def chart_cnn_pattern():
    # 7장 썸네일: CNN이 보는 4×4 상태 패턴(최근 16초, 느림 −1 · 정상 0 · 빠름 +1) — 왼쪽 정상, 오른쪽 이상(유속 저하가 이어짐)
    W, H, C, G, SEP = 112, 84, 10, 2, 10
    fig, ax = canvas(W, H)
    normal = [0, 0, 1, 0, 0, -1, 0, 0, 0, 0, 0, 1, 0, 0, -1, 0]
    anomaly = [0, 1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]
    tone = {0: '#EFE7DC', 1: '#E9BE8C', -1: HONEY}
    side = 4 * C + 3 * G
    left = (W - 2 * side - SEP) / 2
    for x0, pat in ((left, normal), (left + side + SEP, anomaly)):
        for i, st in enumerate(pat):
            r, c = divmod(i, 4)
            rbox(ax, x0 + c * (C + G), (H - side) / 2 + r * (C + G), C, C, 2, color=tone[st], lw=0)
    return fig


def chart_grade():
    # 14장: 동물용 의료기기 등급 — 위험이 클수록 위(좁게). INFU RETRO 구조는 1등급(신고) (덱의 자리 447 px 폭)
    W, H, RH, GAP = 447, 312, 55, 9
    fig, ax = canvas(W, H)
    y = 4
    for k, (grade, kind, frac) in enumerate([('4등급', '허가', .50), ('3등급', '허가', .65), ('2등급', '허가', .80), ('1등급', '신고', .95)]):
        w, hit = W * frac, k == 3
        x = (W - w) / 2
        if hit:  # box-shadow: 0 .6em 1.4em rgba(173, 98, 41, .28)
            rbox(ax, x, y + 12.6, w, RH, 11.5, z=1, gid='hitsh', color=HONEY, alpha=.28, lw=0)
        rbox(ax, x, y, w, RH, 11.5, z=2, color=HONEY if hit else '#EFE5D8', lw=0)
        say(ax, x + 23, y + RH / 2 + .36 * 21, [(grade, 21, 800 if hit else 700, '#FFFFFF' if hit else INK2)])
        say(ax, x + w - 23, y + RH / 2 + .36 * 18.5, [(kind, 18.5, 800 if hit else 600, '#FFFFFF' if hit else MUTE)], ha='right')
        y += RH + GAP
    say(ax, W / 2, y - GAP + 7.6 + 16.8 * .95, [('INFU RETRO · 비접촉 무게 측정', 16.8, 800, HONEY)], ha='center')
    return fig


def chart_petins():
    # 부록 A19 (787 × 620 px): 펫보험 보유계약(손해보험업계 집계, 연말 기준) 2022 → 2025 — 3년 새 3.5배
    vals = [7.19, 10.91, 16.21, 25.18]   # 71,896 · 109,088 · 162,111 · 251,822건
    return columns(vals, ['2022', '2023', '2024', '2025'], (787, 620), {3}, lambda v: f'{v:.1f}만', value_px=20, label_px=16.5, bar_px=88)


def arrow(ax, x0, x1, y, col, lw=2.2, head=11, dash=False, z=2):
    """horizontal arrow from x0 to x1 (either way) with a solid head at x1"""
    d = 1 if x1 > x0 else -1
    ax.plot([x0, x1 - d * head * .6], [y, y], color=col, lw=lw * PT, solid_capstyle='butt', zorder=z,
            ls=(0, (4, 3)) if dash else '-')
    ax.add_patch(Polygon([(x1, y), (x1 - d * head, y - head * .5), (x1 - d * head, y + head * .5)], closed=True, color=col, lw=0, zorder=z))


def pill_c(ax, cx, cy, text, size, col, bg, z=4, weight=800):
    w = advance(text, size, weight)
    h = size * 1.2 + size * .5
    rbox(ax, cx - w / 2 - size * .8, cy - h / 2, w + size * 1.6, h, h / 2, z=z, color=bg, lw=0)
    say(ax, cx, cy + size * .37, [(text, size, weight, col)], ha='center', z=z + .1)


def thumb_sensors(media):
    # 7장 1단계 썸네일 (1200 × 840 px webp, 화면 약 300 × 210 — 글자 ≥ 14 px): 실제 사진 두 장 —
    # 기존 다중 센서 폴대 → INFU RETRO 하중센서 모듈
    from PIL import Image, ImageDraw, ImageFont
    W, H = 1200, 840
    im = Image.new('RGB', (W, H), '#FFFFFF')
    d = ImageDraw.Draw(im)
    pole = Image.open(os.path.join(media, 'pole-multi.webp')).convert('RGB')
    pole = pole.resize((int(pole.width * 610 / pole.height), 610), Image.LANCZOS)
    im.paste(pole, (270 - pole.width // 2, 30))
    mod = Image.open(os.path.join(media, 'module.webp')).convert('RGBA').crop((20, 40, 360, 800))
    mod = mod.resize((int(mod.width * 600 / mod.height), 600), Image.LANCZOS)
    im.paste(mod, (930 - mod.width // 2, 34), mod)
    otf = {os.path.basename(e.fname): e.fname for e in font_manager.fontManager.ttflist if e.fname.endswith('.otf')}
    f = ImageFont.truetype(otf['Pretendard-ExtraBold.otf'], 64)
    def pill(cx, cy, text, fg, bg):
        tw = d.textlength(text, font=f)
        h = 64 * 1.6
        d.rounded_rectangle((cx - tw / 2 - 48, cy - h / 2, cx + tw / 2 + 48, cy + h / 2), radius=h / 2, fill=bg)
        d.text((cx, cy), text, font=f, fill=fg, anchor='mm')
    pill(270, 740, '센서 여러 개', '#5B4B3F', '#EFE8DE')
    pill(930, 740, '하중센서 1개', '#FFFFFF', '#AD6229')
    ax0, ay = 545, 330
    d.line((ax0, ay, ax0 + 80, ay), fill='#AD6229', width=14)
    d.polygon([(ax0 + 120, ay), (ax0 + 74, ay - 32), (ax0 + 74, ay + 32)], fill='#AD6229')
    im.save(os.path.join(media, 'sv-sensors.webp'), quality=86, method=6)
    print('  media/sv-sensors.webp', im.size)


def chart_sv_ai():
    # 7장 3단계 썸네일 (300 × 210 px, 화면과 같은 크기 — 글자 ≥ 14 px): 흔들린 무게 신호 → 가상 자이로 AI → 보정된 무게, 개념 예시
    W, H = 300, 210
    fig, ax = canvas(W, H)
    rng = np.random.default_rng(7)
    x = np.linspace(18, 282, 160)
    t = np.linspace(0, 1, 160)
    sway = 15 * np.sin(2 * np.pi * 3.2 * t) * np.exp(-((t - .45) / .32) ** 2) + 5 * np.sin(2 * np.pi * 7.5 * t) * (t > .62) * (t < .9)
    say(ax, 18, 26, [('흔들린 무게', 15, 700, INK2)])
    pill_c(ax, 262, 21, '예시', 14, '#FFFFFF', INK2)
    ax.plot(x, 56 + sway + rng.normal(0, 1.4, x.size), color=HONEY, lw=2.2 * PT, zorder=2)
    rbox(ax, 62, 86, 176, 40, 20, z=3, color=HONEY, lw=0)
    say(ax, 150, 106 + .36 * 18, [('가상 자이로 AI', 18, 800, '#FFFFFF')], ha='center', z=4)
    for y0, y1 in ((76, 86), (126, 138)):
        ax.annotate('', xy=(150, y1), xytext=(150, y0), arrowprops=dict(arrowstyle='-|>', color=HONEY, lw=2 * PT, mutation_scale=12), zorder=3)
    ax.plot(x, 160 + rng.normal(0, .8, x.size), color=INK, lw=2.2 * PT, zorder=2)
    say(ax, 18, 196, [('보정된 무게', 15, 700, INK)])
    return fig


def chart_bm():
    # 18장 비즈니스 모델 흐름도 (덱 왼쪽 칸 약 1050 × 400 px): 생산 파트너 · WON SHOT · 유통 파트너 · 병원 고객 사이의
    # 제품(회색)과 돈(꿀색) 흐름만 — 가격 · 수익 숫자와 판매 대상은 슬라이드의 카드가 맡습니다
    W, H = 1050, 400
    fig, ax = canvas(W, H)
    CY = 215
    L, C, R = (92, 86), (440, 124), (958, 90)            # (cx, r)
    def edge(node, y, side):
        cx, r = node
        return cx + side * math.sqrt(r * r - (y - CY) ** 2)
    RIM = '#E6DBCD'

    lx = 4
    for lab, col in (('제품 · 서비스', INK2), ('돈', HONEY)):
        arrow(ax, lx, lx + 36, 22, col, lw=2.4, head=9)
        say(ax, lx + 46, 29, [(lab, 18, 700, col)])
        lx += 46 + advance(lab, 18, 700) + 34

    for k, (cx, r) in enumerate((L, R)):
        ax.add_patch(plt.Circle((cx, CY + 10), r, color='#5C3E24', alpha=.08, lw=0, zorder=1, gid=f'nsh{k}'))
        ax.add_patch(plt.Circle((cx, CY), r, facecolor='#FFFFFF', edgecolor=RIM, lw=PT, zorder=2))
    ax.add_patch(plt.Circle((C[0], CY + 13), C[1], color='#5C3E24', alpha=.2, lw=0, zorder=1, gid='cnsh'))
    ax.add_patch(plt.Circle((C[0], CY), C[1], color=HONEY, lw=0, zorder=2, gid='cnode'))
    say(ax, L[0], CY - 2, [('생산 파트너', 21, 800, INK)], ha='center')
    say(ax, L[0], CY + 26, [('PCB · 로드셀 · 조립', 19, 600, INK2)], ha='center')
    say(ax, C[0], CY - 44, [('INFU RETRO', 15, 700, '#F6E3CF', .14)], ha='center')
    say(ax, C[0], CY + 2, [('WON SHOT', 36, 800, '#FFFFFF', -.01)], ha='center')
    say(ax, C[0], CY + 34, [('모듈 + A/S · 운영 관리', 17, 600, '#FFFFFF')], ha='center')
    say(ax, R[0], CY - 2, [('병원 고객', 21, 800, INK)], ha='center')
    say(ax, R[0], CY + 26, [('폴대마다 1대', 19, 600, INK2)], ha='center')

    # 생산 파트너 ⇄ WON SHOT
    y1, y2 = CY - 30, CY + 30
    a, b = edge(L, y1, 1) + 10, edge(C, y1, -1) - 10
    arrow(ax, a, b, y1, INK2)
    say(ax, (a + b) / 2, y1 - 14, [('부품 · 생산', 20, 700, INK2)], ha='center')
    a, b = edge(L, y2, 1) + 10, edge(C, y2, -1) - 10
    arrow(ax, b, a, y2, HONEY)
    say(ax, (a + b) / 2, y2 + 28, [('제조비', 20, 800, HONEY)], ha='center')

    # WON SHOT → 병원: 직접 판매(위) · 유통 파트너 경유(가운데) · 돈(아래)
    y1, y2, y3 = CY - 78, CY, CY + 118
    a, b = edge(C, y1, 1) + 10, edge(R, y1, -1) - 10
    arrow(ax, a, b, y1, INK2)
    say(ax, (a + b) / 2, y1 - 14, [('직접 판매', 21, 800, INK)], ha='center')
    bx, bw, bh = 712, 236, 70
    rbox(ax, bx - bw / 2, y2 - bh / 2, bw, bh, 14, z=3, facecolor='#FFFFFF', edgecolor=LINE, lw=1.2 * PT)
    say(ax, bx, y2 - 4, [('유통 파트너', 18, 800, INK)], ha='center', z=4)
    say(ax, bx, y2 + 20, [('씨엔 · 에스케이엠엔엠', 18, 600, MUTE)], ha='center', z=4)
    a = edge(C, y2, 1) + 10
    arrow(ax, a, bx - bw / 2 - 6, y2, INK2)
    b = edge(R, y2, -1) - 10
    arrow(ax, bx + bw / 2 + 6, b, y2, INK2)
    yd = CY + 58
    ax.plot([bx, bx], [y2 + bh / 2, yd], color=HONEY, lw=2.4, solid_capstyle='butt', zorder=2)
    arrow(ax, bx, edge(C, yd, 1) + 10, yd, HONEY)
    say(ax, (bx + edge(C, yd, 1)) / 2 + 6, yd + 26, [('유통: 공급가 17만 원', 20, 800, HONEY)], ha='center')
    a, b = edge(C, min(y3, CY + C[1] - 8), 1) + 10, edge(R, min(y3, CY + R[1] - 4), -1) - 10
    arrow(ax, b, a, y3, HONEY)
    say(ax, (a + b) / 2, y3 + 30, [('직판: 35만 원 + 선택 구독 월 7만 원', 21, 800, HONEY)], ha='center')
    return fig


# ---- technical appendix: system, signal pipeline, CNN (facts from the deck and the paper's figures · formulas) ----
CARD, RIM, HI_BG, HI_RIM = '#FFFFFF', '#E6DBCD', '#FFF6EA', '#EED1AE'
ST = {1: '#E9BE8C', 0: '#E8DFD3', -1: HONEY}   # +1 빠름 · 0 정상 · −1 느림, as in the paper's figures


def card(ax, x, y, w, h, gid=None, hi=False, r=16):
    """deck .card: white (or .card.hi honey tint) with a hairline border and a soft shadow"""
    if gid:
        rbox(ax, x, y + 10, w, h, r, z=.4, gid=gid, color='#5C3E24', alpha=.07, lw=0)
    rbox(ax, x, y, w, h, r, z=.5, facecolor=HI_BG if hi else CARD, edgecolor=HI_RIM if hi else RIM, lw=PT)


def sub_say(ax, x, y, parts, size, col=INK, weight=600, ha='left', z=3):
    """a formula line: parts are (text, is_subscript); subscripts set smaller and lower, like the paper"""
    def w(t, sub):
        return advance(t, size * (.62 if sub else 1), weight)
    total = sum(w(t, sb) for t, sb in parts)
    x0 = x - total if ha == 'right' else x - total / 2 if ha == 'center' else x
    for t, sb in parts:
        sz = size * (.62 if sb else 1)
        ax.text(x0, y + (size * .2 if sb else 0), t, fontsize=sz * PT, fontweight=WEIGHT[weight], color=col, ha='left', va='baseline', zorder=z)
        x0 += w(t, sb)
    return total


def varrow(ax, x, y0, y1, col, lw=2, head=9, z=2):
    d = 1 if y1 > y0 else -1
    ax.plot([x, x], [y0, y1 - d * head * .6], color=col, lw=lw * PT, solid_capstyle='butt', zorder=z)
    ax.add_patch(Polygon([(x, y1), (x - head * .5, y1 - d * head), (x + head * .5, y1 - d * head)], closed=True, color=col, lw=0, zorder=z))


def chart_t_arch():
    # 부록 · 시스템 구성 (덱 본문 1680 × 763 px): 로드셀 → ADS1232 → ESP32(칼만 · 유속 · 부호화 · CNN) → MQTT 이벤트 → 서버 · 대시보드 · 휴대폰
    W, H = 1680, 763
    fig, ax = canvas(W, H)
    top, bot, ay = 58, 556, 300
    zones = [(0, 300, '① 측정', 'SENSE'), (356, 1004, '② 판정', 'EDGE · 기기 안'), (1060, 1264, '③ 전송', 'NETWORK'), (1320, 1680, '④ 기록 · 알림', 'APP')]
    for k, (x0, x1, ko, en) in enumerate(zones):
        say(ax, x0 + 4, 30, [(ko, 19, 800, INK), (en, 13, 700, MUTE, .12, .7)])
        card(ax, x0, top, x1 - x0, bot - top, gid=f'ash{k}', hi=k == 1)
    # ① load cell + IV bag
    cx = 150
    rbox(ax, cx - 62, 104, 124, 26, 6, z=2, color=INK2, lw=0)
    for i in range(4):  # strain-gauge marks
        ax.plot([cx - 30 + i * 20, cx - 30 + i * 20], [109, 125], color='#CDBFAF', lw=1.4 * PT, zorder=3)
    ax.plot([cx, cx], [130, 152], color=INK2, lw=2.2 * PT, zorder=2)
    rbox(ax, cx - 52, 152, 104, 150, 18, z=2, facecolor='#FBF6F0', edgecolor=LINE, lw=1.2 * PT)
    rbox(ax, cx - 52, 206, 104, 96, 18, z=2.1, color='#F1DCC2', lw=0)
    ax.plot([cx, cx], [302, 352], color=LINE, lw=2 * PT, zorder=2)
    say(ax, cx, 404, [('로드셀 1개', 22, 800, INK)], ha='center')
    say(ax, cx, 434, [('수액백 무게 · 1초마다', 16, 500, INK2)], ha='center')
    pill_c(ax, cx, 492, '제품 센서는 이것 하나', 14.5, HONEY, '#F6E7D6')
    arrow(ax, 306, 350, ay, INK2)
    say(ax, 328, ay - 14, [('신호', 14, 600, MUTE)], ha='center')
    # ② module: ADS1232 → ESP32 pipeline
    say(ax, 380, top + 40, [('INFU RETRO 모듈', 21, 800, INK), ('자체 PCB 60 × 35 mm', 15.5, 600, MUTE, 0, .5)])
    rbox(ax, 382, 128, 150, 330, 14, z=2, facecolor=CARD, edgecolor=LINE, lw=PT)
    say(ax, 457, 262, [('ADS1232', 19, 800, INK)], ha='center')
    say(ax, 457, 290, [('24-bit ADC', 15, 600, MUTE)], ha='center')
    say(ax, 457, 334, [('신호 증폭', 14.5, 500, INK2)], ha='center')
    say(ax, 457, 356, [('디지털 변환', 14.5, 500, INK2)], ha='center')
    arrow(ax, 538, 572, ay, INK2)
    rbox(ax, 578, 128, 400, 330, 14, z=2, facecolor=CARD, edgecolor=HONEY, lw=1.4 * PT)
    say(ax, 602, 166, [('ESP32', 21, 800, INK)])
    pill(ax, 956, 159, 'TFLite Micro ≈ 10KB', 13.5, HONEY, '#F6E7D6', 3)
    steps = ['칼만필터 — 흔들림 보정', '기준 유속 vₙ · 잔량 · 종료 예측', '상태 부호화 → 4 × 4 패턴', '경량 CNN 판정 · 파라미터 ≈ 660']
    for i, t in enumerate(steps):
        y = 190 + i * 64
        rbox(ax, 600, y, 356, 52, 10, z=3, color='#FBF6F0', lw=0)
        ax.add_patch(plt.Circle((626, y + 26), 13, color=HONEY if i == 3 else INK2, lw=0, zorder=4))
        say(ax, 626, y + 26 + .36 * 14, [(str(i + 1), 14, 800, '#FFFFFF')], ha='center', z=5)
        say(ax, 650, y + 26 + .36 * 16.5, [(t, 16.5, 700 if i == 3 else 600, INK if i == 3 else INK2)], z=5)
    for k, t in enumerate(['USB-C 전원', '로드셀 4핀', 'BLE · Wi-Fi']):
        pill_c(ax, 470 + k * 175, 500, t, 14, INK2, '#F1EBE3')
    arrow(ax, 1010, 1054, ay, INK2)
    say(ax, 1032, ay - 14, [('MQTT', 13, 700, MUTE)], ha='center')
    # ③ network: event messages
    c3 = 1162
    for dx, dy, r in ((-26, 8, 26), (0, -8, 32), (28, 6, 24), (0, 14, 26)):
        ax.add_patch(plt.Circle((c3 + dx, 172 + dy), r, color='#EFE5D8', lw=0, zorder=2))
    say(ax, c3, 270, [('Wi-Fi · MQTT', 19, 800, INK)], ha='center')
    say(ax, c3, 300, [('이벤트 전송', 16, 500, INK2)], ha='center')
    say(ax, c3, 404, [('−80', 50, 800, HONEY, -.03), ('%', 22, 700, HONEY, 0, .04)], ha='center')
    say(ax, c3, 440, [('전송 트래픽', 15.5, 600, INK2)], ha='center')
    say(ax, c3, 464, [('80% 이상 감소', 14, 500, MUTE)], ha='center')
    arrow(ax, 1270, 1314, ay, INK2)
    # ④ server · dashboard · phone
    x4 = 1346
    for i, yy in enumerate((104, 118, 132)):   # database
        ax.add_patch(Ellipse((x4 + 30, yy), 52, 16, facecolor='#EFE5D8' if i < 2 else '#F6EEE5', edgecolor=LINE, lw=PT, zorder=3 - i * .1))
    rbox(ax, x4 + 4, 104, 52, 28, 0, z=2, color='#EFE5D8', lw=0)
    say(ax, x4 + 72, 116, [('서버', 18, 800, INK)])
    say(ax, x4 + 72, 140, [('투약 기록 24시간 자동 저장', 14.5, 500, INK2)])
    ax.plot([x4, 1656], [176, 176], color=GRID, lw=PT, zorder=2)
    rbox(ax, x4, 204, 92, 60, 6, z=3, facecolor='#2A1F18', edgecolor='none')            # monitor
    for k, h in enumerate((22, 34, 16, 28)):
        rbox(ax, x4 + 12 + k * 18, 252 - h, 10, h, 2, z=4, color=HONEY if k == 1 else '#8C7A6B', lw=0)
    ax.plot([x4 + 46, x4 + 46], [264, 278], color=INK2, lw=3 * PT, zorder=3)
    ax.plot([x4 + 30, x4 + 62], [279, 279], color=INK2, lw=3 * PT, zorder=3, solid_capstyle='round')
    say(ax, x4 + 112, 230, [('대시보드', 18, 800, INK)])
    say(ax, x4 + 112, 256, [('입원장별 잔량 · 종료 시각', 14.5, 500, INK2)])
    rbox(ax, x4 + 22, 316, 48, 88, 10, z=3, facecolor='#2A1F18', edgecolor='none')     # phone
    rbox(ax, x4 + 27, 330, 38, 22, 4, z=4, color=ALERT, lw=0)
    say(ax, x4 + 46, 346, [('!', 15, 800, '#FFFFFF')], ha='center', z=5)
    say(ax, x4 + 112, 346, [('휴대폰 알림', 18, 800, INK)])
    for k, t in enumerate(('과다', '느림', '정지')):
        pill_c(ax, x4 + 136 + k * 66, 380, t, 14, ALERT, '#F8E2DA')
    pill_c(ax, 1500, 492, '구독 · 관리비 포함', 14, INK2, '#F1EBE3')
    # timeline
    ty = 650
    ax.plot([0, W], [ty, ty], color=LINE, lw=1.2 * PT, zorder=1)
    for k in range(8):
        ax.add_patch(plt.Circle((24 + k * 36, ty), 6, color=INK2 if k < 7 else HONEY, lw=0, zorder=2))
    say(ax, 4, ty - 26, [('0초', 15, 800, INK), ('무게 측정 · 1초 간격', 15, 500, INK2, 0, .5)])
    rbox(ax, 356, ty - 9, 648, 18, 9, z=2, color='#F1DCC2', lw=0)
    say(ax, 680, ty - 26, [('판정은 기기 안에서 — 서버 응답을 기다리지 않음', 15, 600, INK2)], ha='center')
    ax.add_patch(plt.Circle((1490, ty), 13, color=HONEY, lw=0, zorder=3))
    say(ax, 1672, ty - 26, [('이상 알림', 15, 600, INK2), ('≤ 5초', 26, 800, HONEY, 0, .4)], ha='right')
    say(ax, 1672, ty + 40, [('시험 1,000회 · 흔들림 · 당겨짐 보정 포함 최대 검측 시간', 14, 500, MUTE)], ha='right')
    return fig


PAPER_NORMAL = [0, 1, 0, -1, 1, 0, 0, 0, 0, -1, 1, 0, -1, 0, 0, 1]        # 논문 그림 2(a) 정상 상태 패턴
PAPER_ANOMALY = [0, 0, -1, -1, 0, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]  # 논문 그림 2(b) 이상 상태 패턴


def grid44(ax, x0, y0, pat, cell, gap, txt=True, z=3):
    for i, st in enumerate(pat):
        r, c = divmod(i, 4)
        x, y = x0 + c * (cell + gap), y0 + r * (cell + gap)
        rbox(ax, x, y, cell, cell, 5, z=z, color=ST[st], lw=0)
        if txt:
            lab = {1: '+1', 0: '0', -1: '−1'}[st]
            say(ax, x + cell / 2, y + cell / 2 + .36 * 14, [(lab, 14, 700, '#FFFFFF' if st == -1 else INK2)], ha='center', z=z + .1)


def chart_t_signal():
    # 부록 · 판별 파이프라인 ① (1680 × 763 px): 기준 유속 자가측정 → 칼만필터 → 상태 부호화 → 4×4 패턴 — 논문 식 (1) · (2) · 그림 2
    W, H = 1680, 763
    fig, ax = canvas(W, H)
    cw, gap, y0, y1 = 386, 45, 8, 752
    titles = ['기준 유속 자가측정', '흔들림 보정', '상태 부호화', '4 × 4 패턴 이미지']
    for k, t in enumerate(titles):
        x = k * (cw + gap)
        card(ax, x, y0, cw, y1 - y0, gid=f'ssh{k}', hi=k == 3)
        ax.add_patch(plt.Circle((x + 40, y0 + 44), 17, color=HONEY, lw=0, zorder=3))
        say(ax, x + 40, y0 + 44 + .36 * 16, [(str(k + 1), 16, 800, '#FFFFFF')], ha='center')
        say(ax, x + 68, y0 + 44 + .36 * 21, [(t, 21, 800, INK)])
        if k < 3:
            arrow(ax, x + cw + 6, x + cw + gap - 6, 300, LINE, lw=2.4, head=12)
    px0, px1, py0, py1 = 28, cw - 28, 110, 440      # chart box inside each card
    # ① weight falls steadily; the first T seconds give vₙ
    x = 0
    t = np.linspace(0, 1, 60)
    wv = 1 - .55 * t
    X = x + px0 + (px1 - px0) * t
    Y = py0 + 46 + (py1 - py0 - 86) * (1 - wv) / .55 * .9
    ax.plot([x + px0, x + px0], [py0, py1], color=LINE, lw=PT, zorder=2)
    ax.plot([x + px0, x + px1], [py1, py1], color=LINE, lw=PT, zorder=2)
    ax.plot(X, Y, color=BAR_DIM, lw=3 * PT, zorder=3, solid_capstyle='round')
    n = 22
    ax.plot(X[:n], Y[:n], color=HONEY, lw=5 * PT, zorder=4, solid_capstyle='round')
    for i, lab in ((0, 'I'), (n - 1, 'f')):
        ax.add_patch(plt.Circle((X[i], Y[i]), 7, color=HONEY, lw=0, zorder=5))
        sub_say(ax, X[i] + 14, Y[i] - 12, [('W', False), (lab, True)], 18, col=HONEY, weight=800)
    ax.plot([X[0], X[n - 1]], [py1 - 28, py1 - 28], color=INK2, lw=1.4 * PT, zorder=3)
    for xx in (X[0], X[n - 1]):
        ax.plot([xx, xx], [py1 - 34, py1 - 22], color=INK2, lw=1.4 * PT, zorder=3)
    say(ax, (X[0] + X[n - 1]) / 2, py1 - 38, [('T', 17, 800, INK2)], ha='center')
    say(ax, x + px1, py1 + 26, [('시간 →', 13.5, 600, MUTE)], ha='right')
    say(ax, x + px0 + 8, py0 + 4, [('무게 ↑', 13.5, 600, MUTE)])
    # ② raw vs Kalman (모의 신호)
    x = cw + gap
    raw, kw, *_ = simulate('shake', 23)
    tt = np.arange(660, 1380)
    lo, hi = min(raw[tt].min(), kw[tt].min()), max(raw[tt].max(), kw[tt].max())
    mx = lambda v: x + px0 + (px1 - px0) * (v - tt[0]) / (tt[-1] - tt[0])
    my = lambda v: py1 - 10 - (py1 - py0 - 30) * (v - lo) / (hi - lo)
    ax.scatter([mx(v) for v in tt[::5]], [my(v) for v in raw[tt][::5]], s=5, color=RAW, alpha=.75, linewidths=0, zorder=3)
    ax.plot([mx(v) for v in tt[::3]], [my(v) for v in kw[tt][::3]], color=HONEY, lw=3 * PT, zorder=4)
    ax.add_patch(plt.Circle((x + px0 + 8, py0 + 2), 5, color=RAW, lw=0, zorder=5))
    say(ax, x + px0 + 20, py0 + 7, [('원신호', 14, 600, INK2)])
    ax.plot([x + px0 + 100, x + px0 + 124], [py0 + 2, py0 + 2], color=HONEY, lw=3.5 * PT, zorder=5)
    say(ax, x + px0 + 132, py0 + 7, [('칼만필터', 14, 700, HONEY)])
    say(ax, x + px1, py1 + 26, [('모의 신호 · 흔들림 구간', 13.5, 600, MUTE)], ha='right')
    # ③ r(t) bars against ±τ → −1 · 0 · +1 (그림 2(a)의 정상 패턴과 같은 순서)
    x = 2 * (cw + gap)
    rv = {1: [.19, .17, .21, .18, .2], 0: [.03, -.04, .02, -.02, .04, -.03, .01, .02], -1: [-.18, -.21, -.17, -.2]}
    idx = {1: 0, 0: 0, -1: 0}
    mid, sc, tau = (py0 + py1) / 2 - 10, 520, .1
    band = sc * tau
    rbox(ax, x + px0, mid - band, px1 - px0, 2 * band, 0, z=1.5, color='#F4EEE6', lw=0)
    for sgn in (1, -1):
        ax.plot([x + px0, x + px1], [mid - sgn * band] * 2, color=LINE, lw=1.2 * PT, ls=(0, (4, 3)), zorder=2)
        say(ax, x + px1, mid - sgn * band + (-6 if sgn > 0 else 18), [(('+' if sgn > 0 else '−') + 'τ', 15, 700, MUTE)], ha='right')
    ax.plot([x + px0, x + px1], [mid, mid], color=LINE, lw=PT, zorder=2)
    bw = (px1 - px0 - 30) / 16
    for i, st in enumerate(PAPER_NORMAL):
        v = rv[st][idx[st] % len(rv[st])]; idx[st] += 1
        bx = x + px0 + 15 + i * bw
        top_, botm = (mid - v * sc, mid) if v > 0 else (mid, mid - v * sc)
        ax.add_patch(PathPatch(shape(bx + 2, top_, bx + bw - 2, botm, tl=3 if v > 0 else 0, tr=3 if v > 0 else 0, bl=3 if v < 0 else 0, br=3 if v < 0 else 0), facecolor=ST[st], lw=0, zorder=3))
        say(ax, bx + bw / 2, py1 + 4, [({1: '+1', 0: '0', -1: '−1'}[st], 12.5, 700, HONEY if st == -1 else INK2)], ha='center')
    say(ax, x + px0, py0 + 4, [('r(t)', 14, 700, MUTE)])
    # ④ two 4×4 patterns
    x = 3 * (cw + gap)
    cell, g = 34, 5
    side = 4 * cell + 3 * g
    gx = x + (cw - 2 * side - 30) / 2
    for j, (pat, lab, col) in enumerate(((PAPER_NORMAL, '정상', INK2), (PAPER_ANOMALY, '이상', HONEY))):
        xx = gx + j * (side + 30)
        say(ax, xx + side / 2, py0 + 30, [(lab, 18, 800, col)], ha='center')
        grid44(ax, xx, py0 + 50, pat, cell, g)
    say(ax, x + cw / 2, py0 + 50 + side + 40, [('흩어진 변화', 14.5, 600, INK2), ('  vs  ', 14.5, 500, MUTE), ('이어지는 느림', 14.5, 700, HONEY)], ha='center')
    for k, (lab, c) in enumerate(((' +1 빠름', ST[1]), (' 0 정상', ST[0]), (' −1 느림', ST[-1]))):
        xx = x + 52 + k * 104
        rbox(ax, xx, py1 - 10, 14, 14, 3, z=3, color=c, lw=0)
        say(ax, xx + 16, py1 + 2, [(lab, 13.5, 600, INK2)])
    # formula + one line under each chart
    fy, cy = 540, 600
    sub_say(ax, 0 * (cw + gap) + cw / 2, fy, [('v', False), ('n', True), (' = (W', False), ('I', True), (' − W', False), ('f', True), (') / T', False)], 24, col=INK, weight=700, ha='center')
    say(ax, 1 * (cw + gap) + cw / 2, fy, [('칼만필터', 24, 700, INK)], ha='center')
    sub_say(ax, 2 * (cw + gap) + cw / 2, fy, [('r(t) = (v(t) − v', False), ('n', True), (') / v', False), ('n', True)], 24, col=INK, weight=700, ha='center')
    say(ax, 3 * (cw + gap) + cw / 2, fy, [('연속 16개 → 4 × 4', 24, 700, INK)], ha='center')
    lines = [('거치 직후 T 동안 스스로 측정', '사용자 입력 0개 · 비정상 값이면 재측정'),
             ('동물 움직임 · 폴대 흔들림', '순간 노이즈만 걸러 냄'),
             ('|r| ≤ τ 이면 0', '넘으면 +1 · 못 미치면 −1'),
             ('한 시점이 아니라', '시간 흐름의 모양을 봄')]
    for k, (a, b) in enumerate(lines):
        cxk = k * (cw + gap) + cw / 2
        say(ax, cxk, cy, [(a, 16, 600, INK2)], ha='center')
        say(ax, cxk, cy + 28, [(b, 16, 500, MUTE)], ha='center')
    say(ax, 3 * (cw + gap) + cw / 2, 700, [('→ 다음 장 CNN', 15, 800, HONEY)], ha='center')
    return fig


def chart_t_cnn():
    # 부록 · 판별 파이프라인 ② (1680 × 763 px): 경량 CNN — 논문 구조 Conv2D(8, 3×3) → MaxPool(2×2) → Dense(16) → Dense(3) → Softmax
    # 파라미터는 층마다 계산: 8 × (3·3 + 1) = 80 · 0 · 32 × 16 + 16 = 528 · 16 × 3 + 3 = 51 → 659 (논문 '약 660개')
    W, H = 1680, 763
    fig, ax = canvas(W, H)
    card(ax, 0, 8, W, 430, gid='csh0')
    cy = 218
    cols = [118, 330, 545, 735, 930, 1130, 1330, 1540]
    heads = [('입력', '4 × 4 × 1'), ('Conv2D', '8 필터 · 3 × 3'), ('MaxPool', '2 × 2'), ('Flatten', '32'), ('Dense', '16'), ('Dense', '3'), ('Softmax', '확률 3개'), ('판정', '기기 안에서')]
    params = ['', '80', '0', '0', '528', '51', '', '']
    shapes = ['4×4×1', '4×4×8', '2×2×8', '32', '16', '3', '3', '']
    for k, (h1, h2) in enumerate(heads):
        say(ax, cols[k], 70, [(h1, 19, 800, HONEY if k in (1, 4, 5) else INK)], ha='center')
        say(ax, cols[k], 96, [(h2, 14.5, 600, MUTE)], ha='center')
        if shapes[k]:
            say(ax, cols[k], 342, [(shapes[k], 15, 700, INK2)], ha='center')
        if params[k]:
            pill_c(ax, cols[k], 378, f'파라미터 {params[k]}', 13.5, HONEY if params[k] != '0' else MUTE, '#F6E7D6' if params[k] != '0' else '#F1EBE3')
    grid44(ax, cols[0] - 44, cy - 44, PAPER_ANOMALY, 19, 4, txt=False)
    for i in range(8):                                # 8 feature maps 4×4
        o = i * 7
        rbox(ax, cols[1] - 50 + o, cy - 60 + o, 62, 62, 4, z=2 + i * .01, facecolor='#F6EEE5' if i < 7 else '#F1DCC2', edgecolor='#D9C3A8', lw=PT)
    for i in range(8):                                # 8 maps 2×2
        o = i * 6
        rbox(ax, cols[2] - 34 + o, cy - 38 + o, 30, 30, 3, z=2 + i * .01, facecolor='#F6EEE5' if i < 7 else '#F1DCC2', edgecolor='#D9C3A8', lw=PT)
    for i in range(32):                               # flatten 32
        rbox(ax, cols[3] - 9, cy - 96 + i * 6, 18, 4.2, 1.2, z=3, color='#E3D3BF' if i % 8 else '#D2B590', lw=0)
    for i in range(16):                               # dense 16
        ax.add_patch(plt.Circle((cols[4], cy - 90 + i * 12), 4.8, color='#E3D3BF', lw=0, zorder=3))
    for i in range(3):                                # dense 3
        ax.add_patch(plt.Circle((cols[5], cy - 34 + i * 34), 11, color=HONEY, lw=0, zorder=3))
    for i, (pv, c) in enumerate(((.04, BAR_OFF), (.91, HONEY), (.05, BAR_OFF))):   # softmax (예시)
        rbox(ax, cols[6] - 34 + i * 24, cy + 44 - 88 * pv - 4, 18, 88 * pv + 4, 3, z=3, color=c, lw=0)
    ax.plot([cols[6] - 40, cols[6] + 40], [cy + 44, cy + 44], color=LINE, lw=PT, zorder=2)
    ax.add_patch(plt.Circle((cols[7], cy), 34, color=HONEY, lw=0, zorder=3))
    say(ax, cols[7], cy + .36 * 16, [('알림', 16, 800, '#FFFFFF')], ha='center', z=4)
    for a, b in zip(cols[:-1], cols[1:]):
        arrow(ax, a + 62, b - 62, cy, LINE, lw=2, head=10)
    # total and footprint
    say(ax, 40, 424, [('합계', 15, 600, MUTE), ('659', 22, 800, INK, 0, .4), ('≈ 660개', 15, 700, INK2, 0, .3), ('·', 15, 500, MUTE, 0, .5), ('TFLite Micro ≈ 10KB', 15, 700, INK2, 0, .5), ('· ESP32에서 BLE · Wi-Fi와 함께 동작', 15, 500, MUTE, 0, .4)])
    # comparison: 선행 Dual-Track → 제안 CNN
    ry0 = 486
    say(ax, 300, ry0, [('선행 Dual-Track', 17, 700, MUTE)], ha='center')
    say(ax, 640, ry0, [('제안 CNN', 17, 800, HONEY)], ha='center')
    rows = [('사용자 입력', '2개', '0개'), ('점적 계수 의존', '있음', '없음'), ('판정에 쓰는 샘플', '1개 · 현재 시점', '16개 · 시간 패턴'), ('판정 표현', '임계값', '2D 패턴 이미지')]
    for i, (lab, a, b) in enumerate(rows):
        y = ry0 + 46 + i * 58
        say(ax, 40, y + .36 * 16, [(lab, 16, 600, INK2)])
        pill_c(ax, 300, y, a, 16, INK2, '#EFE7DC', weight=700)
        arrow(ax, 400, 520, y, LINE, lw=2, head=10)
        pill_c(ax, 640, y, b, 16, '#FFFFFF', HONEY, weight=800)
    # right: results that the structure delivers
    kx = 900
    card(ax, kx, 470, W - kx, 290, gid='csh1', hi=True)
    for k, (num, unit, lab, note) in enumerate((('97.3', '%', '검증 정확도', '최근 6 epoch 평균 · 95.2 ~ 99.0%'), ('5', '초 이내', '이상 감지', '시험 1,000회 · 보정 포함 최대'), ('0', '개', '사용자 입력', '점적 계수 · 게인 설정 없음'))):
        xx = kx + 36 + k * 260
        say(ax, xx, 560, [(lab, 16, 700, HONEY)])
        say(ax, xx, 640, [(num, 62, 800, INK, -.04), (unit, 20, 700, INK, 0, .08)])
        say(ax, xx, 690, [(note, 13.5, 500, MUTE)])
    return fig


def badge(ax, x, y, n, col=HONEY, r=13, size=14, z=4):
    ax.add_patch(plt.Circle((x, y), r, color=col, lw=0, zorder=z))
    say(ax, x, y + .36 * size, [(str(n), size, 800, '#FFFFFF')], ha='center', z=z + .1)


def chart_t_chain():
    # 부록 · 하드웨어 (오른쪽 카드 749 × 700 px): 로드셀 → 입력 RC 필터 → ADS1232(PGA · 24-bit ΔΣ · 디지털 필터) → ESP32, 아래는 전원 · 접지
    # 번호 ①~⑥은 왼쪽 PCB 레이아웃 사진의 표시와 같다. ADS1232의 기능은 데이터시트 사양(PGA 1 · 2 · 64 · 128배, 10 SPS에서 50 · 60 Hz 동시 제거)
    W, H = 749, 700
    fig, ax = canvas(W, H)
    def node(y, h, n, title, sub, hi=False, tag=None):
        rbox(ax, 0, y, W, h, 14, z=1, facecolor=HI_BG if hi else '#FBF6F0', edgecolor=HONEY if hi else RIM, lw=(1.3 if hi else 1) * PT)
        badge(ax, 30, y + 34, n)
        say(ax, 56, y + 34 + .36 * 19, [(title, 19, 800, INK)])
        if sub:
            say(ax, 56, y + 64, [(sub, 15, 500, INK2)])
        if tag:
            pill(ax, W - 18, y + 34, tag, 13.5, HONEY if hi else INK2, '#F6E7D6' if hi else '#EFE7DC', 3)
    def down(y0, y1, lab=None):
        varrow(ax, 70, y0 + 4, y1 - 4, INK2)
        if lab:
            say(ax, 88, (y0 + y1) / 2 + 5, [(lab, 13.5, 600, MUTE)])
    node(0, 84, 1, '로드셀', '수액 무게 → mV 단위 차동 신호', tag='E+ · E− · A+ · A−')
    down(84, 122, 'A+ / A− 차동 입력')
    node(122, 84, 2, '입력 RC 필터', 'R17 · R18 · C18 — 고주파 잡음 차단')
    down(206, 244)
    node(244, 196, 3, 'ADS1232', '', hi=True, tag='내장 앰프 + ADC')
    for k, (t1, t2, t3) in enumerate((('PGA', '저잡음 증폭', '× 1 · 2 · 64 · 128'), ('ΔΣ ADC', '24-bit 변환', '내부 오실레이터'), ('디지털 필터', '50 · 60 Hz 동시 제거', '10 SPS 모드'))):
        x = 24 + k * 238
        rbox(ax, x, 300, 222, 118, 12, z=2, facecolor=CARD, edgecolor=HI_RIM, lw=PT)
        say(ax, x + 18, 334, [(t1, 18, 800, HONEY)])
        say(ax, x + 18, 366, [(t2, 15.5, 700, INK)])
        say(ax, x + 18, 394, [(t3, 14, 500, MUTE)])
        if k < 2:
            arrow(ax, x + 224, x + 236, 359, HONEY, lw=2, head=8, z=3)
    down(440, 478, 'DOUT · SCLK 직렬')
    node(478, 84, 6, 'ESP32', '칼만필터 · 유속 · CNN 판정 · Wi-Fi · BLE', tag='뒷면 · 디지털부')
    # power & ground band
    ax.plot([0, W], [590, 590], color=GRID, lw=PT, zorder=1)
    say(ax, 0, 618, [('전원', 15, 800, INK2)])
    x = 52
    for k, (t, n) in enumerate((('USB-C 5 V', None), ('3.3 V', None), ('LC 필터', 4), ('AVDD = E+', None))):
        w = advance(t, 14.5, 700) + 28 + (26 if n else 0)
        rbox(ax, x, 600, w, 30, 15, z=2, facecolor=HI_BG if n else '#EFE7DC', edgecolor=HI_RIM if n else 'none', lw=PT)
        if n:
            badge(ax, x + 17, 615, n, r=10, size=12)
        say(ax, x + 14 + (26 if n else 0), 615 + .36 * 14.5, [(t, 14.5, 700, HONEY if n else INK2)])
        x += w
        if k < 3:
            arrow(ax, x + 6, x + 26, 615, LINE, lw=1.8, head=8)
            x += 32
    say(ax, 0, 668, [('접지', 15, 800, INK2)])
    badge(ax, 66, 662, 5, r=10, size=12)
    say(ax, 84, 668, [('GND 동박 전면 채움 · 아날로그부(앞면) ↔ 디지털부(뒷면 ESP32) 분리', 14.5, 600, INK2)])
    return fig


def chart_t_gyroflow():
    # 부록 · 센서 절감 학습 (1680 × 200 px): 동시 수집 → 상관 분석 → 보정 튜닝 → 제품 적용 (수치는 학습 장비 모의 신호 기준)
    t, gyro, dev, _, r, rms0, rms1 = gyro_signals()
    W, H, gap = 1680, 200, 46
    fig, ax = canvas(W, H)
    cw = (W - 3 * gap) / 4
    # ③ is the gyro-input correction (simulated); ④ is the product, which learns to reproduce it from the load signal alone
    steps = [('동시 수집', '학습 장비: 로드셀 + 자이로 · 20 Hz', None),
             ('상관 분석', '자이로 각속도 ↔ 무게 편차 · 모의 신호', f'r = {r:.2f}'),
             ('보정 튜닝', '자이로 입력으로 편차 보정 · 모의 신호', f'{rms0:.1f} g → {rms1:.1f} g'),
             ('제품 적용', '자이로 없이 하중센서 1개 · 실측 검증 중', '하중 신호만으로 보정')]
    for k, (t1, t2, big) in enumerate(steps):
        x = k * (cw + gap)
        card(ax, x, 6, cw, H - 22, gid=f'gsh{k}', hi=k == 3)
        badge(ax, x + 38, 50, k + 1, r=16, size=15)
        say(ax, x + 64, 50 + .36 * 21, [(t1, 21, 800, INK)])
        say(ax, x + 26, 104, [(t2, 15.5, 500, INK2)])
        if big:
            say(ax, x + 26, 150, [(big, 26, 800, HONEY, -.01)])
        else:  # a small trace instead of a number: both sensors (1)
            sl = slice(20, 220)
            sx = lambda i: x + 26 + (cw - 52) * (i - sl.start) / (sl.stop - sl.start)
            for y_, col, lw in ((gyro / 46, SAGE, 1.6), (dev / 9, HONEY, 1.8)):
                ii = np.arange(sl.start, sl.stop)
                ax.plot([sx(i) for i in ii], [140 - 22 * y_[i] for i in ii], color=col, lw=lw * PT, zorder=3)
            say(ax, x + cw - 26, 176, [('자이로', 14.5, 700, SAGE), ('무게 편차', 14.5, 700, HONEY, 0, .8)], ha='right')
        if k < 3:
            arrow(ax, x + cw + 8, x + cw + gap - 8, 84, LINE, lw=2.4, head=12)
    return fig


def chart_t_gyroscatter():
    # 부록 · 센서 절감 학습 (630 × 420 px): 같은 시각의 자이로 각속도(지연 보정) ↔ 무게 편차 — 학습 장비 모의 신호, 12초 · 20 Hz
    t, gyro, dev, res, r, rms0, rms1 = gyro_signals()
    x, y = np.roll(gyro, 2)[4:], dev[4:]
    W, H = 630, 420
    fig, ax = canvas(W, H)
    x0, x1, y0, y1 = 64, W - 12, 24, H - 58
    gx = lambda v: x0 + (x1 - x0) * (v + 46) / 92
    gy = lambda v: y1 - (y1 - y0) * (v + 11) / 22
    for v in (-40, -20, 0, 20, 40):
        ax.plot([gx(v), gx(v)], [y0, y1], color=GRID, lw=PT, zorder=1)
        say(ax, gx(v), y1 + 24, [(f'{v:+d}' if v else '0', 15, 500, MUTE)], ha='center')
    for v in (-10, -5, 0, 5, 10):
        ax.plot([x0, x1], [gy(v), gy(v)], color=GRID, lw=PT, zorder=1)
        say(ax, x0 - 10, gy(v) + 5, [(f'{v:+d}' if v else '0', 15, 500, MUTE)], ha='right')
    ax.plot([gx(0), gx(0)], [y0, y1], color=LINE, lw=PT, zorder=1.5)
    ax.plot([x0, x1], [gy(0), gy(0)], color=LINE, lw=PT, zorder=1.5)
    ax.scatter([gx(v) for v in x], [gy(v) for v in y], s=26, color=HONEY, alpha=.45, linewidths=0, zorder=3)
    k, b = np.polyfit(x, y, 1)
    ax.plot([gx(-44), gx(44)], [gy(k * -44 + b), gy(k * 44 + b)], color=INK, lw=2 * PT, zorder=4)
    say(ax, x0 + 14, y0 + 36, [(f'r = {r:.2f}', 30, 800, HONEY, -.01)])
    say(ax, x0 + 14, y0 + 62, [(f'샘플 {x.size}개 · 12초 · 20 Hz', 15, 500, MUTE)])
    say(ax, (x0 + x1) / 2, H - 6, [('자이로 각속도 (°/s)', 15, 600, INK2)], ha='center')
    ax.text(14, (y0 + y1) / 2, '무게 편차 (g)', rotation=90, fontsize=15 * PT, fontweight=WEIGHT[600], color=INK2, ha='center', va='center')
    return fig


def chart_t_data():
    # 부록 · 데이터 구축 · 학습 (1680 × 763 px): 실측 + 의료 데이터 → 의료 데이터 사전학습(전이학습) → 실측 파인튜닝 → 실측 교차 검증 → ESP32 배포
    # 아래: 검증 정확도 최근 6 epoch (학습 로그, 부록 알고리즘 장과 같은 값)
    W, H = 1680, 763
    fig, ax = canvas(W, H)
    cw, gap, top, h = 300, 45, 8, 456
    titles = ['데이터 구축', '전이학습', '파인튜닝', '실측 교차 검증', '기기 배포']
    for k, t in enumerate(titles):
        x = k * (cw + gap)
        card(ax, x, top, cw, h, gid=f'dsh{k}', hi=k == 4)
        badge(ax, x + 36, top + 40, k + 1, r=16, size=15)
        say(ax, x + 62, top + 40 + .36 * 20, [(t, 20, 800, INK)])
        if k < 4:
            arrow(ax, x + cw + 7, x + cw + gap - 7, top + 230, LINE, lw=2.4, head=12)
    def db(cx, cy, col, w=56):
        for i in (2, 1, 0):
            ax.add_patch(Ellipse((cx, cy + i * 14), w, 16, facecolor=col, edgecolor='#FFFFFF', lw=1.2 * PT, zorder=3 - i * .1))
        rbox(ax, cx - w / 2, cy, w, 28, 0, z=2.5, color=col, lw=0)
    # ① two sources
    x = 0
    for j, (lab, l2, l3, col) in enumerate((('실측 데이터', '모의 병실 · 원광대 간호학과', '수액 10종 점도별 감소 패턴', HONEY), ('의료 데이터', '사전학습용', '', '#C9B49C'))):
        yy = top + 112 + j * 170
        db(x + 58, yy, col)
        say(ax, x + 100, yy + 6, [(lab, 18, 800, INK)])
        say(ax, x + 100, yy + 32, [(l2, 14, 500, INK2)])
        if l3:
            say(ax, x + 100, yy + 54, [(l3, 14, 500, INK2)])
    # ② transfer: pretrained layers carried over
    x = cw + gap
    for i in range(4):
        yy = top + 110 + i * 52
        frozen = i < 2
        rbox(ax, x + 40, yy, 220, 38, 9, z=2, facecolor='#EFE7DC' if frozen else HI_BG, edgecolor=LINE if frozen else HI_RIM, lw=PT)
        say(ax, x + 58, yy + 19 + .36 * 14.5, [('사전학습 층' if frozen else '새로 맞출 층', 14.5, 700, INK2 if frozen else HONEY)])
        if frozen:
            rbox(ax, x + 228, yy + 13, 14, 12, 2, z=3, color=INK2, lw=0)
            ax.add_patch(PathPatch(Path([(x + 231, yy + 13), (x + 231, yy + 7), (x + 239, yy + 7), (x + 239, yy + 13)], [Path.MOVETO, Path.LINETO, Path.LINETO, Path.LINETO]), fill=False, edgecolor=INK2, lw=1.6 * PT, zorder=3))
    say(ax, x + cw / 2, top + 356, [('의료 데이터로 익힌 가중치를', 15, 600, INK2)], ha='center')
    say(ax, x + cw / 2, top + 382, [('그대로 옮겨 시작', 15, 600, INK2)], ha='center')
    # ③ fine-tune: sliders
    x = 2 * (cw + gap)
    for i, (lab, pos) in enumerate((('수액 10종 점도', .72), ('흔들림 · 당겨짐', .45), ('폴대 · 거치 조건', .6))):
        yy = top + 128 + i * 74
        say(ax, x + 30, yy - 12, [(lab, 14.5, 600, INK2)])
        rbox(ax, x + 30, yy, 240, 8, 4, z=2, color='#EFE7DC', lw=0)
        rbox(ax, x + 30, yy, 240 * pos, 8, 4, z=2.1, color=HONEY, lw=0)
        ax.add_patch(plt.Circle((x + 30 + 240 * pos, yy + 4), 11, facecolor='#FFFFFF', edgecolor=HONEY, lw=2 * PT, zorder=3))
    say(ax, x + cw / 2, top + 382, [('실측 데이터로 미세 조정', 15, 600, INK2)], ha='center')
    # ④ k-fold
    x = 3 * (cw + gap)
    cols_, rows_ = 5, 4
    bw, bh, gx = 40, 26, 6
    gx0 = x + (cw - (cols_ * bw + (cols_ - 1) * gx)) / 2
    for i in range(rows_):
        for j in range(cols_):
            last = j == cols_ - 1
            val = (j == i) if i < 3 else last
            yy = top + 112 + i * 44
            rbox(ax, gx0 + j * (bw + gx), yy, bw, bh, 5, z=2, color=HONEY if val else '#E8DFD3', lw=0)
        say(ax, gx0 - 12, top + 112 + i * 44 + bh / 2 + 5, [(('1', '2', '3', 'k')[i], 14, 700, MUTE)], ha='right')
    for d in range(3):  # rows 3 … k
        ax.add_patch(plt.Circle((gx0 - 18, top + 112 + 2 * 44 + bh + 6 + d * 5), 1.6, color=MUTE, lw=0, zorder=2))
    lx = x + 52
    rbox(ax, lx, top + 312, 14, 14, 3, z=2, color='#E8DFD3', lw=0); say(ax, lx + 20, top + 324, [('학습', 14, 600, INK2)])
    rbox(ax, lx + 90, top + 312, 14, 14, 3, z=2, color=HONEY, lw=0); say(ax, lx + 110, top + 324, [('검증', 14, 700, HONEY)])
    say(ax, x + cw / 2, top + 382, [('실측 데이터를 나눠 번갈아 검증', 15, 600, INK2)], ha='center')
    # ⑤ deploy
    x = 4 * (cw + gap)
    rbox(ax, x + 70, top + 110, 160, 110, 12, z=2, facecolor='#2A1F18', edgecolor='none')
    for i in range(7):
        ax.plot([x + 82 + i * 22, x + 82 + i * 22], [top + 100, top + 110], color=INK2, lw=3 * PT, zorder=1.9)
        ax.plot([x + 82 + i * 22, x + 82 + i * 22], [top + 220, top + 230], color=INK2, lw=3 * PT, zorder=1.9)
    say(ax, x + 150, top + 158, [('ESP32', 20, 800, '#F3ECE2')], ha='center', z=3)
    say(ax, x + 150, top + 186, [('CNN ≈ 10KB', 14.5, 700, '#E3BC8C')], ha='center', z=3)
    say(ax, x + cw / 2, top + 284, [('TFLite Micro 변환', 17, 800, HONEY)], ha='center')
    say(ax, x + cw / 2, top + 312, [('파라미터 ≈ 660개', 15, 600, INK2)], ha='center')
    say(ax, x + cw / 2, top + 382, [('기기 안에서 실시간 판정', 15, 600, INK2)], ha='center')
    # bottom: validation accuracy, last 6 epochs
    by = 500
    card(ax, 0, by, W, H - by - 4, gid='dsh5')
    say(ax, 36, by + 46, [('검증 정확도', 18, 800, INK), ('최근 6 epoch · 학습 80 epoch', 14.5, 500, MUTE, 0, .6)])
    say(ax, 36, by + 150, [('97.3', 66, 800, HONEY, -.04), ('%', 24, 700, HONEY, 0, .06)])
    say(ax, 36, by + 196, [('평균 · 범위 95.2 ~ 99.0%', 15, 600, INK2)])
    # dots on an axis that starts at 94% — the gridlines say so, no bar pretends to start at zero
    eps = [(62, 95.66), (63, 99.00), (64, 95.24), (65, 97.29), (66, 97.41), (67, 99.00)]
    bx0, bx1, lo_, hi_ = 470, 1640, by + 214, by + 74
    sc = lambda v: lo_ - (lo_ - hi_) * (v - 94) / 6
    for g in (95, 97, 99):
        ax.plot([bx0, bx1], [sc(g)] * 2, color=GRID, lw=PT, zorder=1.5)
        say(ax, bx0 - 12, sc(g) + 5, [(f'{g}%', 13.5, 500, MUTE)], ha='right')
    ax.plot([bx0, bx1], [sc(97.27)] * 2, color=HONEY, lw=1.4 * PT, ls=(0, (5, 4)), zorder=2)
    say(ax, bx0 - 12, sc(97.27) - 14, [('평균', 13.5, 700, HONEY)], ha='right')
    band = (bx1 - bx0) / 6
    pts = [(bx0 + band * (i + .5), sc(v)) for i, (e, v) in enumerate(eps)]
    ax.plot([p_[0] for p_ in pts], [p_[1] for p_ in pts], color='#D9C3A8', lw=1.6 * PT, zorder=2.5)
    for (cx, cyv), (e, v) in zip(pts, eps):
        ax.add_patch(plt.Circle((cx, cyv), 9, color=HONEY if v >= 99 else '#C9A783', lw=0, zorder=3))
        say(ax, cx, cyv - 18, [(f'{v:.2f}', 15, 700, HONEY if v >= 99 else INK2)], ha='center')
        say(ax, cx, lo_ + 30, [(f'epoch {e}', 13.5, 500, MUTE)], ha='center')
    return fig


def chart_v_kaha():
    # 부록 · 현장의 목소리 (카드 안 480 × 200 px): 진료수의사가 꼽은 근무 어려움 상위 3개 — 한국동물병원협회 설문(FASAVA 2025, 중복응답)
    return hbars([('야간 · 휴일 근무로 인한 피로 · 번아웃', 53.4, '53.4%', HONEY, HONEY, None),
                  ('인력 부족으로 인한 업무 과중', 39.4, '39.4%', BAR_DIM, INK2, None),
                  ('보호자 응대 · 민원 대응 부담', 32.1, '32.1%', BAR_DIM, INK2, None)], (480, 200), value_px=18, label_px=15.5, bar_px=20)


def chart_v_rank():
    # 부록 · 현장의 목소리 (480 × 90 px): 동물병원 서비스 — 소비자시장평가지표 40개 시장 중 37위(한국소비자원, 2024 지표)
    W, H = 480, 90
    fig, ax = canvas(W, H)
    n, hit, gap = 40, 37, 3
    w = (W - gap * (n - 1)) / n
    for i in range(n):
        x = i * (w + gap)
        on = i + 1 == hit
        ax.add_patch(PathPatch(shape(x, 30 if not on else 12, x + w, 62, tl=2, tr=2, bl=2, br=2), facecolor=HONEY if on else ('#E8DFD3' if i < 36 else '#D9CBBA'), lw=0, zorder=2))
    xh = (hit - 1) * (w + gap) + w / 2
    say(ax, xh, 6 + .36 * 13, [('37위', 13, 800, HONEY)], ha='center')
    say(ax, 0, 84, [('1위', 13, 600, MUTE)])
    say(ax, W, 84, [('40위', 13, 600, MUTE)], ha='right')
    return fig


def chart_filter():
    raw, kw, *_ = simulate('shake', 23)
    t = np.arange(660, 1380)
    fig = plt.figure(figsize=(2.8, 2.1))
    ax = fig.add_axes([.02, .04, .96, .92])
    ax.scatter(t[::6], raw[t][::6], s=2.2, color=RAW, alpha=.8, linewidths=0)
    ax.plot(t[::3], kw[t][::3], color=HONEY, lw=2)
    ax.set_xlim(t[0], t[-1]); ax.axis('off')
    return fig


def chart_ir_raw(size=(640, 450)):
    # IR 방향성 ② (640 × 450 px): 로드셀 단일 측정 — 흔들림 · 기울기가 무게 신호에 남기는 편차 (모의 신호)
    t, gyro, dev, res, r, rms0, rms1 = gyro_signals()
    fig, ax = plt.subplots(figsize=px(*size))
    ax.axvspan(1.6, 4.4, color='#F6E2D8', lw=0, zorder=0)
    ax.axvspan(7.1, 9.3, color='#F6E2D8', lw=0, zorder=0)
    ax.plot(t, dev, color=ALERT, lw=1.7, solid_joinstyle='round', zorder=2)
    ax.axhline(0, color=INK2, lw=1.1, ls=(0, (4, 3)), zorder=1)
    lim = float(abs(dev).max() * 1.25)
    ax.set_ylim(-lim, lim * 1.35); ax.set_yticks([-5, 0, 5])
    ax.set_xlim(0, 12); ax.set_xticks(range(0, 13, 2))
    ax.set_xlabel('시간 (s) · 20 Hz', fontsize=19, color=INK2, labelpad=3)
    ax.set_title('로드셀 단일 측정의 무게 편차 (g)', loc='left', fontsize=20, fontweight='semibold', color=INK2, pad=6)
    ax.set_title('모의 신호 예시', loc='right', fontsize=18, fontweight='semibold', color=MUTE, pad=6)
    for x0 in (3.0, 8.2):
        ax.text(x0, lim * 1.12, '흔들림 · 기울기', ha='center', va='center', fontsize=19, fontweight='bold', color=ALERT)
    ax.grid(axis='y', color=GRID, lw=.8); ax.set_axisbelow(True)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.tick_params(labelsize=19)
    fig.subplots_adjust(left=.09, right=.98, top=.88, bottom=.16)
    return fig


def chart_ir_pair():
    # IR 4장 카드 ① (약 400 × 270 px): 같은 흔들림을 자이로와 로드셀이 동시에 기록 — 모의 신호
    t, gyro, dev, res, r, rms0, rms1 = gyro_signals()
    fig, axs = plt.subplots(2, 1, sharex=True, figsize=px(400, 270), gridspec_kw=dict(hspace=.55))
    for ax, y, col, lab in ((axs[0], gyro, SAGE, '자이로 각속도'), (axs[1], dev, HONEY, '로드셀 무게 편차')):
        ax.plot(t, y, color=col, lw=1.5, solid_joinstyle='round')
        ax.set_title(lab, loc='left', fontsize=14, fontweight='bold', color=col, pad=4)
        ax.set_yticks([]); ax.grid(False)
        for side in ('top', 'right', 'left'):
            ax.spines[side].set_visible(False)
        ax.tick_params(labelsize=14)
    axs[1].set_xlim(0, 12); axs[1].set_xticks([0, 4, 8, 12])
    axs[1].set_xlabel('시간 (s)', fontsize=14, color=INK2, labelpad=2)
    fig.subplots_adjust(left=.03, right=.97, top=.9, bottom=.2)
    return fig


def chart_ir_nn():
    # IR 4장 카드 ③ (480 × 290 px): 개념도 — 로드셀 신호 → 신경망 → 가상 자이로 3축 → 보정 무게
    W, H = 480, 290
    fig, ax = canvas(W, H)
    pill_c(ax, 436, 18, '개념도', 15, '#FFFFFF', INK2)
    layers = [(70, 3), (170, 5), (250, 5), (340, 3)]
    pts = []
    for x, n in layers:
        ys = [145 + (k - (n - 1) / 2) * 44 for k in range(n)]
        pts.append([(x, y) for y in ys])
    for a, b in zip(pts, pts[1:]):
        for (x0, y0) in a:
            for (x1, y1) in b:
                ax.plot([x0, x1], [y0, y1], color='#E6D6C3', lw=.9, zorder=1)
    for k, layer in enumerate(pts):
        for (x, y) in layer:
            col = HONEY if k in (1, 2) else ('#EFE5D8' if k == 0 else SAGE)
            ax.add_patch(plt.Circle((x, y), 12.5, color=col, lw=0, zorder=2))
    say(ax, 70, 268, [('로드셀 신호', 15.5, 700, INK2)], ha='center')
    say(ax, 210, 268, [('AI 신경망', 15.5, 800, HONEY)], ha='center')
    for (x, y), lab in zip(pts[3], ('x', 'y', 'z')):
        say(ax, x, y + .36 * 13, [(lab, 15, 800, '#FFFFFF')], ha='center', z=3)
    say(ax, 340, 268, [('가상 자이로', 15.5, 800, SAGE)], ha='center')
    arrow(ax, 368, 400, 145, HONEY, lw=2.2, head=10)
    rbox(ax, 404, 120, 70, 50, 12, z=2, color=INK, lw=0)
    say(ax, 439, 141 + .36 * 14, [('보정', 15.5, 800, '#FFFFFF')], ha='center', z=3)
    say(ax, 439, 160 + .36 * 14, [('무게', 15.5, 800, '#FFFFFF')], ha='center', z=3)
    return fig


def chart_ir_scatter():
    # IR 4장 카드 ② (460 × 330 px, 화면 크기 그대로 — 글자 ≥ 14 px): 자이로 각속도 ↔ 무게 편차, 학습 장비 모의 신호
    t, gyro, dev, res, r, rms0, rms1 = gyro_signals()
    x, y = np.roll(gyro, 2)[4:], dev[4:]
    W, H = 460, 330
    fig, ax = canvas(W, H)
    x0, x1, y0, y1 = 52, W - 8, 12, H - 60
    gx = lambda v: x0 + (x1 - x0) * (v + 46) / 92
    gy = lambda v: y1 - (y1 - y0) * (v + 11) / 22
    for v in (-40, 0, 40):
        ax.plot([gx(v), gx(v)], [y0, y1], color=GRID, lw=PT, zorder=1)
        say(ax, gx(v), y1 + 24, [(f'{v:+d}' if v else '0', 19, 500, MUTE)], ha='center')
    for v in (-10, 0, 10):
        ax.plot([x0, x1], [gy(v), gy(v)], color=GRID, lw=PT, zorder=1)
        say(ax, x0 - 8, gy(v) + 7, [(f'{v:+d}' if v else '0', 19, 500, MUTE)], ha='right')
    ax.scatter([gx(v) for v in x], [gy(v) for v in y], s=22, color=HONEY, alpha=.45, linewidths=0, zorder=3)
    k, b = np.polyfit(x, y, 1)
    ax.plot([gx(-44), gx(44)], [gy(k * -44 + b), gy(k * 44 + b)], color=INK, lw=2 * PT, zorder=4)
    say(ax, x0 + 10, y0 + 24, [('모의 신호 예시', 19, 600, MUTE)])
    say(ax, (x0 + x1) / 2, H - 4, [('자이로 각속도 (°/s) ↔ 무게 편차 (g)', 18, 600, INK2)], ha='center')
    return fig


def chart_ir_epoch():
    # IR 6장 (520 × 250 px, 화면 크기 그대로): CNN 검증 정확도 최근 6 epoch — 실제 학습 로그
    acc = [95.66, 99.0, 95.24, 97.29, 97.41, 99.0]
    mean = sum(acc) / len(acc)
    fig, ax = plt.subplots(figsize=px(520, 250))
    x = np.arange(6)
    ax.plot(x, acc, color=BAR_DIM, lw=1.8, zorder=2)
    ax.scatter(x, acc, s=70, color=HONEY, zorder=3, linewidths=0)
    for xi, a in zip(x, acc):
        ax.text(xi, a + .45, f'{a:.1f}', ha='center', va='bottom', fontsize=14 * .75, color=INK2, fontweight='bold')
    ax.set_xticks(x, [f'{e}' for e in range(62, 68)])
    ax.set_xlabel('학습 마지막 6회 · 내부 검증셋', fontsize=14 * .75, color=MUTE, labelpad=4)
    ax.set_yticks([90, 95, 100], ['90%', '95%', '100%']); ax.set_ylim(88, 101.5); ax.set_xlim(-.5, 5.5)
    ax.tick_params(axis='both', labelsize=14 * .75, labelcolor=MUTE, length=0, pad=4)
    for side in ('top', 'right', 'left', 'bottom'):
        ax.spines[side].set_visible(False)
    ax.grid(axis='y', color=GRID, lw=.8); ax.set_axisbelow(True)
    fig.subplots_adjust(left=.1, right=.97, top=.95, bottom=.2)
    return fig


def chart_ir_visit():
    # IR 9장 (360 × 240 px): 반려동물 양육가구의 최근 1년 동물병원 이용률 — 2021 73.0% → 2025 95.1%
    # same canvas and type sizes as ir-rx so the two baselines line up side by side
    return columns([73.0, 95.1], ['2021', '2025'], (400, 250), {1}, lambda v: f'{v:.1f}%', value_px=17, label_px=15, bar_px=70)


def chart_ir_petins():
    # IR 동향 (400 × 250 px): 펫보험 보유계약 2024년 말 162,111 → 2025년 말 251,822건 (13개 보험사 합산)
    return columns([16.21, 25.18], ['2024년 말', '2025년 말'], (400, 250), {1}, lambda v: f'{v:.1f}만 건', value_px=19, label_px=16, bar_px=80)


def chart_ir_rx():
    # IR 동향 (400 × 250 px): 동물병원 의료용 마약류 처방량 2022 → 2025 (만 개, NIMS)
    return columns(RX, ['2022', '2023', '2024', '2025'], (400, 250), {3}, lambda v: f'{v:g}만 개', value_px=17, label_px=15, bar_px=50)


def chart_ir_care():
    # IR 수요 (400 × 250 px): 최근 2년 반려동물 치료비(만 원, 전체 가구 평균) — KB 2023 · 2025 보고서
    return columns([57.7, 102.7], ['2023 보고서', '2025 보고서'], (400, 250), {1}, lambda v: f'{v:g}만 원', value_px=18, label_px=15, bar_px=70)


def chart_ir_curve():
    # IR 방향성 ① (640 × 450 px): 수액 무게가 줄어드는 모양으로 상황을 구분 — 개념도
    fig, ax = plt.subplots(figsize=px(640, 450))
    t = np.linspace(0, 66, 330)
    normal = 500 - 6.2 * t
    clog = np.where(t < 24, 500 - 6.2 * t, 500 - 6.2 * 24 - 0.25 * (t - 24))
    fast = np.where(t < 24, 500 - 6.2 * t, 500 - 6.2 * 24 - 16 * (t - 24))
    fast = np.maximum(fast, 0)
    ax.plot(t, normal, color='#B8A797', lw=3, label='정상')
    ax.plot(t, clog, color=HONEY, lw=3.4)
    m = fast > 0
    ax.plot(t[m], fast[m], color=ALERT, lw=3.4)
    ax.axvline(24, color=LINE, lw=1.2, ls=(0, (3, 3)))
    ax.text(24.8, 470, '이상 시작', fontsize=22 * .75, color=MUTE, fontweight='bold')
    ax.text(66.8, normal[-1] + 22, '정상', fontsize=26 * .75, color=INK2, fontweight='bold', va='center')
    ax.text(66.8, clog[-1], '막힘 · 꼬임\n줄지 않음', fontsize=26 * .75, color=HONEY, fontweight='bold', va='center', linespacing=1.15)
    ax.text(2, 120, '줄 분리 · 과다 주입\n둘 다 빨리 줄어듦', fontsize=26 * .75, color=ALERT, fontweight='bold', va='center', linespacing=1.15)
    ax.set_xlim(0, 92); ax.set_ylim(0, 540)
    ax.set_xticks([0, 20, 40, 60]); ax.set_yticks([0, 250, 500])
    ax.set_xlabel('시간 (분)', fontsize=22 * .75, color=INK2, labelpad=2)
    ax.set_ylabel('수액 무게 (g)', fontsize=22 * .75, color=INK2, labelpad=4)
    ax.tick_params(labelsize=22 * .75, colors=MUTE, length=0)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    ax.grid(axis='y', color=GRID, lw=.8); ax.set_axisbelow(True)
    fig.subplots_adjust(left=.14, right=.98, top=.96, bottom=.16)
    return fig


def chart_ir_glob_pump():
    # IR 시장 (300 × 250 px): 세계 동물용 인퓨전펌프 2025 → 2032 (Global Industry Analysts)
    return columns([3.15, 4.67], ['2025', '2032'], (300, 250), {1}, lambda v: f'{v:g}억 달러', value_px=17, label_px=15, bar_px=64)


def chart_ir_glob_iv():
    # IR 시장 (300 × 250 px): 세계 수액 모니터링 장비 2024 → 2030 (Global Industry Analysts)
    return columns([50, 71], ['2024', '2030'], (300, 250), {1}, lambda v: f'{v:g}억 달러', value_px=17, label_px=15, bar_px=64)


def chart_ir_cagr():
    # IR 수요 · 법령 장 (460 × 260 px): 동물용 인퓨전펌프 글로벌 CAGR 전망 4곳 — 조사기관은 시간축이 아니므로 가로 막대 한 색
    rows = [(n, v, f'{v:g}%', '#E9BE8C', INK2, None) for n, v in
            [('Data Bridge', 12.3), ('Grand View', 7.4), ('GM Insights', 7.2), ('MRF', 6.55), ('GIA', 5.8)]]
    return hbars(rows, (460, 270), label_w=128, value_px=19, label_px=16, bar_px=26)


def chart_ir_rev2():
    # IR 목표 매출 (480 × 320 px): 1년차 = 공급 약정 0.51억 + 구매의향 협약 0.5억(빗금) = 10,100만 원 규모,
    # 2 · 3년차 = 직판 신규 장비(35만 원) + 구독 연환산(월 7만 원) 쌓은 막대
    W, H = 480, 320
    fig, ax = canvas(W, H)
    base, top_room, bar = H - 50, 40, 58
    vmax = 2.7
    room = base - top_room
    ax.plot([0, W], [base, base], color=LINE, lw=PT, solid_capstyle='butt', zorder=3)
    def y(v): return base - room * v / vmax
    for xc, v, lab, solid in ((W * .09, .51, '약정 0.51', True), (W * .24, .5, '협약 0.5', False)):
        if solid:
            ax.add_patch(PathPatch(shape(xc - bar / 2, y(v), xc + bar / 2, base, tl=6, tr=6), facecolor=INK2, lw=0, zorder=2))
        else:
            ax.add_patch(PathPatch(shape(xc - bar / 2, y(v), xc + bar / 2, base, tl=6, tr=6), facecolor='#FFFFFF', edgecolor=INK2, hatch='////', lw=1.2, zorder=2))
        say(ax, xc, y(v) - 10, [(lab, 15, 700, INK2 if solid else MUTE)], ha='center')
    rbox(ax, W * .24 - 26, y(.5) + 8, 52, 20, 6, z=3.5, facecolor='#FFFFFF', lw=0)
    say(ax, W * .24, y(.5) + 23, [('비구속', 13, 800, INK2)], ha='center', z=4)
    say(ax, W * .165, y(.51) - 40, [('10,100만 원 규모', 17, 800, INK)], ha='center')
    say(ax, W * .165, base + 24, [('1년차(KC 후 · 2027 하~)', 15, 400, MUTE)], ha='center')
    say(ax, W * .165, base + 44, [('유통 공급가 · 확정 0.51', 13, 400, MUTE)], ha='center')
    ax.plot([W * .355, W * .355], [top_room - 10, base + 50], color=LINE, lw=1, ls=(0, (3, 3)), zorder=1)
    for xc, w, eq, sub, lab, sub2, big in ((W * .52, 40, .35, .84, '2년차(2028)', '직판만 · 100대 · 연환산', False),
                                         (W * .82, 46, .525, 2.1, '3년차 말(2029)', '직판만 · 누적 250대', True)):
        ax.add_patch(PathPatch(shape(xc - w, y(eq), xc + w, base), facecolor='#EFD3B4', lw=0, zorder=2))
        ax.add_patch(PathPatch(shape(xc - w, y(eq + sub), xc + w, y(eq) - 2, tl=6, tr=6), facecolor=HONEY if big else '#D9955A', lw=0, zorder=2))
        tot = eq + sub
        say(ax, xc, (y(eq) + base) / 2 + 5, [(f'장비 {eq:.2f}'.rstrip('0').rstrip('.'), 13, 700, INK2)], ha='center', z=4)
        yb = y(eq + sub * .3)
        if not big:
            ax.plot([xc - w, xc + w], [yb, yb], color='#FFFFFF', lw=1.4, ls=(0, (4, 3)), zorder=4)
        if big:
            ax.plot([xc - w, xc + w], [yb, yb], color='#FFFFFF', lw=1.6, ls=(0, (4, 3)), zorder=4)
            say(ax, xc, (y(eq + sub) + yb) / 2 + 5, [(f'구독 {sub:g}', 15, 800, '#FFFFFF')], ha='center', z=4)
            say(ax, xc, yb + 17, [('기준 1.2억', 13, 800, '#FFFFFF')], ha='center', z=4)
            say(ax, xc, yb + 33, [('구독 30% 가정', 11, 600, '#FFFFFF')], ha='center', z=4)
        else:
            say(ax, xc, (y(eq + sub) + yb) / 2 + 5, [(f'구독 {sub:g}', 12, 800, '#FFFFFF')], ha='center', z=4)
            say(ax, xc, yb + 13, [('기준 0.6억', 11, 800, '#FFFFFF')], ha='center', z=4)
        say(ax, xc, y(tot) - 30, [(('기준 1.2억 원 / 년' if big else '기준 0.6억 원'), 19 if big else 16, 800, HONEY)], ha='center')
        say(ax, xc, y(tot) - 9, [(('상한 2.6억 · 구독 100%' if big else '상한 1.19억 · 구독 100%'), 12, 600, MUTE)], ha='center')
        say(ax, xc, base + 24, [(lab, 16, 400, MUTE)], ha='center')
        say(ax, xc, base + 44, [(sub2, 13, 400, MUTE)], ha='center')
    return fig


def chart_ir_test():
    # IR 부록 A1 (520 × 300 px): 모의 병실 1,000회 내부 테스트 시나리오 구성(회)
    rows = [(n, v, f'{v}회', HONEY if hi else '#E9BE8C', HONEY if hi else INK2, None) for n, v, hi in
            [('정상 투여', 300, False), ('흔들림 · 이동', 250, False), ('당겨짐', 200, False), ('수액줄 분리', 150, True), ('소진', 100, True)]]
    return hbars(rows, (520, 300), label_w=150, value_px=19, label_px=17, bar_px=28)


CMP = [  # 잔량 오차(%) — 정지 · 흔들림 · 당겨짐, 같은 연출 각 100회(학습 장비 비교 측정 · 예비)
    ('로드셀 단일', '#D9CCBD', MUTE, [0.8, 9.6, 14.2]),
    ('로드셀 + 자이로 + 가속도 + 광학', INK2, INK2, [0.6, 1.8, 2.4]),
    ('로드셀 + 가상 AI 자이로', HONEY, HONEY, [0.7, 2.1, 2.9])]
def chart_ir_compare():
    # IR 8-2장 (640 × 420 px): 세 센서 구성의 잔량 오차를 상황별 묶음 막대로
    W, H = 640, 470
    fig, ax = canvas(W, H)
    base, top = H - 46, 80
    vmax = 15
    ax.plot([0, W], [base, base], color=LINE, lw=PT, solid_capstyle='butt', zorder=3)
    say(ax, 44, base + 6, [('0%', 16, 500, MUTE)], ha='right')
    for v in (5, 10, 15):
        yv = base - (base - top) * v / vmax
        ax.plot([52, W], [yv, yv], color=GRID, lw=PT, zorder=1)
        say(ax, 44, yv + 6, [(f'{v}%', 16, 500, MUTE)], ha='right')
    groups = ['정지', '흔들림', '당겨짐']
    band = (W - 56) / 3
    bw = 46
    for g, name in enumerate(groups):
        xc = 56 + band * (g + .5)
        say(ax, xc, base + 30, [(name, 19, 600, INK2)], ha='center')
        for k, (lab, col, tcol, vals) in enumerate(CMP):
            x = xc + (k - 1) * (bw + 10)
            v = vals[g]
            yv = base - (base - top) * v / vmax
            ax.add_patch(PathPatch(shape(x - bw / 2, yv, x + bw / 2, base, tl=6, tr=6), facecolor=col, lw=0, zorder=2))
            say(ax, x, yv - 9, [(f'{v:g}', 17 if k == 2 else 15, 800 if k == 2 else 600, tcol)], ha='center')
    lx = 40
    for lab, col, tcol, _ in CMP:
        rbox(ax, lx, 18, 18, 18, 4, z=3, facecolor=col, lw=0)
        say(ax, lx + 26, 34, [(lab, 17, 700 if col == HONEY else 600, tcol if col == HONEY else INK2)])
        lx += 26 + advance(lab, 17, 600) + 30
    return fig


def chart_ir_curve2():
    # IR 3장 ① (화면 크기 그대로 810 × 540 px): 무게가 줄어드는 모양 = 수액 상태 — 개념도, 축은 최소(0 · 500 g, 시간 →)
    W, H = 810, 540
    fig, ax = plt.subplots(figsize=px(W, H))
    t = np.linspace(0, 66, 330)
    normal = 500 - 6.2 * t
    clog = np.where(t < 24, 500 - 6.2 * t, 500 - 6.2 * 24 - 0.25 * (t - 24))
    fast = np.maximum(np.where(t < 24, 500 - 6.2 * t, 500 - 6.2 * 24 - 16 * (t - 24)), 0)
    ax.plot(t, normal, color='#B8A797', lw=4.5, solid_capstyle='round')
    ax.plot(t, clog, color=HONEY, lw=5, solid_capstyle='round')
    m = fast > 0
    ax.plot(t[m], fast[m], color=ALERT, lw=5, solid_capstyle='round')
    ax.axvline(24, color=LINE, lw=1.4, ls=(0, (4, 4)))
    ax.text(25, 505, '이상 시작', fontsize=22 * .75, color=MUTE, fontweight='bold', va='bottom')
    ax.text(67.5, normal[-1] + 42, '정상', fontsize=30 * .75, color=INK2, fontweight='bold', va='center')
    ax.text(67.5, clog[-1] + 10, '막힘 · 꼬임\n줄지 않음', fontsize=30 * .75, color=HONEY, fontweight='bold', va='center', linespacing=1.15)
    ax.text(50, 36, '줄 분리 · 과다 주입\n빨리 줄어듦', fontsize=30 * .75, color=ALERT, fontweight='bold', va='center', linespacing=1.15)
    ax.set_xlim(0, 96); ax.set_ylim(0, 560)
    ax.set_xticks([]); ax.set_yticks([0, 500], ['0', '500 g'])
    ax.tick_params(axis='y', labelsize=22 * .75, colors=MUTE, length=0, pad=6)
    ax.set_xlabel('시간 →', fontsize=22 * .75, color=MUTE, loc='right', labelpad=6)
    for side in ('top', 'right'):
        ax.spines[side].set_visible(False)
    for side in ('left', 'bottom'):
        ax.spines[side].set_color(LINE)
    fig.subplots_adjust(left=.085, right=.995, top=.97, bottom=.08)
    return fig


def chart_ir_raw_strip():
    # IR 3장 ② (810 × 110 px): 로드셀 단일 무게 편차 모의 신호 — 흔들림 구간만 붉게, 축 최소
    t, gyro, dev, res, r, rms0, rms1 = gyro_signals()
    W, H = 810, 110
    fig, ax = plt.subplots(figsize=px(W, H))
    ax.axvspan(1.6, 4.4, color='#F6DDD3', lw=0, zorder=0)
    ax.axvspan(7.1, 9.3, color='#F6DDD3', lw=0, zorder=0)
    ax.plot(t, dev, color=ALERT, lw=2.2, solid_joinstyle='round', zorder=2)
    ax.axhline(0, color=INK2, lw=1, ls=(0, (4, 3)), zorder=1)
    lim = float(abs(dev).max() * 1.1)
    ax.set_ylim(-lim, lim); ax.set_xlim(0, 12)
    ax.set_xticks([]); ax.set_yticks([-5, 5], ['−5 g', '+5 g'])
    ax.tick_params(axis='y', labelsize=22 * .75, colors=MUTE, length=0, pad=4)
    for side in ('top', 'right', 'bottom', 'left'):
        ax.spines[side].set_visible(False)
    fig.subplots_adjust(left=.075, right=.995, top=.98, bottom=.04)
    return fig


def mini_cols(values, labels, hl, fmt, size=(250, 120)):
    return columns(values, labels, size, hl, fmt, value_px=17, label_px=15, bar_px=34)


def chart_ir_visit_s():
    return columns([73.0, 95.1], ['2021', '2025'], (250, 120), {1}, lambda v: f'{v:.1f}%', value_px=18, label_px=17, bar_px=34)


def chart_ir_resolve_s():
    return columns([30.0, 19.5], ['기록 있음', '기록 없음'], (250, 120), {0}, lambda v: f'{v:g}%', value_px=18, label_px=17, bar_px=40)


def chart_ir_rx_s():
    return columns(RX, ['2022', '', '', '2025'], (250, 120), {3}, lambda v: {257.6: '257.6만', 353.0: '353만'}.get(v, ''), value_px=18, label_px=17, bar_px=28)


def chart_ir_cagr_s():
    # 5곳 전망을 한 줄 점 범위로: 5.8 ~ 12.3% (점은 작게, 양 끝만 라벨)
    W, H = 250, 120
    fig, ax = canvas(W, H)
    vals = [5.8, 6.55, 7.2, 7.4, 12.3]
    x0, x1, cy = 24, W - 24, 58
    gx = lambda v: x0 + (x1 - x0) * (v - 5.5) / 7.2
    ax.plot([gx(5.8), gx(12.3)], [cy, cy], color='#F0D7BB', lw=5, solid_capstyle='round', zorder=1)
    for v in vals:
        ax.add_patch(plt.Circle((gx(v), cy), 4.6, color=HONEY, zorder=3))
    say(ax, gx(5.8), cy + 34, [('5.8%', 18, 700, INK2)], ha='center')
    say(ax, gx(12.3), cy + 34, [('12.3%', 18, 700, HONEY)], ha='center')
    say(ax, W / 2, cy - 20, [('조사기관 5곳', 17, 600, MUTE)], ha='center')
    return fig


def chart_ir_rev():
    # IR 목표 매출 (420 × 300 px): 1년차 계약 기반 1억 100만 원 → 3년차 목표 4.2억 원(50곳 · 250대)
    return columns([1.01, 4.2], ['1년차 · 계약', '3년차 · 목표'], (420, 300), {1}, lambda v: f'{v:g}억 원', value_px=21, label_px=16, bar_px=86)


if __name__ == '__main__':
    use_font()
    os.makedirs(OUT, exist_ok=True)
    save(chart_resolve(), 'resolve.svg')
    save(chart_market(), 'market.svg',
         fills={'arrow': (0, 1, 0, 0, [(0, '#A9723F', .25), (1, '#E3BC8C', 1)]),       # CSS: from the foot, faint → honey
                't2': (.25, .067, .75, .933, [(0, '#C97F40', 1), (1, '#A35A22', 1)])},  # CSS: linear-gradient(150deg)
         blurs={'sh1': 16, 'sh2': 16})                                                  # CSS: 1.6em blur → σ 16 px
    save(chart_bm(), 'bm.svg', fills={'cnode': (.25, .067, .75, .933, [(0, '#C97F40', 1), (1, '#A35A22', 1)])},
         blurs={'cnsh': 18, 'nsh0': 16, 'nsh1': 16})
    save(chart_ir_raw(), 'ir-raw.svg')
    save(chart_ir_pair(), 'ir-pair.svg')
    save(chart_ir_nn(), 'ir-nn.svg')
    save(chart_ir_scatter(), 'ir-scatter.svg')
    save(chart_ir_epoch(), 'ir-epoch.svg')
    save(chart_ir_visit(), 'ir-visit.svg')
    save(chart_ir_petins(), 'ir-petins.svg')
    save(chart_ir_rx(), 'ir-rx.svg')
    save(chart_ir_care(), 'ir-care.svg')
    save(chart_ir_curve(), 'ir-curve.svg')
    save(chart_ir_rev(), 'ir-rev.svg')
    save(chart_ir_rev2(), 'ir-rev2.svg')
    save(chart_ir_test(), 'ir-test.svg')
    save(chart_ir_compare(), 'ir-compare.svg')
    save(chart_ir_curve2(), 'ir-curve2.svg')
    save(chart_ir_raw_strip(), 'ir-raw-strip.svg')
    save(chart_ir_visit_s(), 'ir-visit-s.svg')
    save(chart_ir_resolve_s(), 'ir-resolve-s.svg')
    save(chart_ir_rx_s(), 'ir-rx-s.svg')
    save(chart_ir_cagr_s(), 'ir-cagr-s.svg')
    save(chart_ir_cagr(), 'ir-cagr.svg')
    save(chart_ir_glob_pump(), 'ir-glob-pump.svg')
    save(chart_ir_glob_iv(), 'ir-glob-iv.svg')
    save(chart_grade(), 'grade.svg', blurs={'hitsh': 14.7})
