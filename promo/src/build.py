# Builds the promo video and the edit package from the rendered graphics (run after `node render.cjs`).
#   edit/media/scene_s1..s9.mp4   every scene as one finished clip (s3, s5 = footage + graphics composited)
#   edit/media/bg_s3.mp4, bg_s5.mp4 · gfx_s3.mov, gfx_s5.mov   the same two scenes as separate layers
#   edit/media/music.wav · ding_alert.wav · ding_total.wav
#   edit/captions.srt · edit/INFU-RETRO_promo_timeline.xml (Premiere Pro / DaVinci Resolve, FCP 7 XML)
#   export/INFU-RETRO_홍보영상.mp4   final 1920×1080 · 30 fps
# All times below are relative to a scene's start (scenes.json from render.cjs), so changing scene
# lengths in scenes.html keeps captions and sounds on their scenes.
import json, os, subprocess, wave
from urllib.parse import quote
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC_MEDIA, EDIT, EXPORT = os.path.join(ROOT, 'media'), os.path.join(ROOT, 'edit'), os.path.join(ROOT, 'export')
MED = os.path.join(EDIT, 'media')
os.makedirs(EXPORT, exist_ok=True)
FPS, SR = 30, 48000
SC = json.load(open(os.path.join(MED, 'scenes.json')))
S = {s['id']: s for s in SC}
TOTAL = max(s['t1'] for s in SC)
OVER = ('reveal', 'demo')
ff = lambda *a: subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
dur = lambda i: S[i]['t1'] - S[i]['t0']
X264 = ['-c:v', 'libx264', '-crf', '15', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS)]

# ── 1. footage layers ────────────────────────────────────────────────────────────────
# s3: housing assembly render (600×600). Exploded → assembled 3/4 view (first 4.4 s), slowed 2× with
# motion interpolation, then a slow push-in hold on that view; right half of the frame.
d3 = dur('reveal')
ff('-i', os.path.join(SRC_MEDIA, 'hanger.mp4'), '-f', 'lavfi', '-i', f'color=c=0xF6F9FD:s=1920x1080:r={FPS}:d={d3}',
   '-filter_complex',
   f"[0:v]trim=0:4.4,setpts=2*(PTS-STARTPTS),minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
   f"scale=840:840:flags=lanczos,tpad=stop_mode=clone:stop_duration={d3},"
   f"zoompan=z='if(lte(on,{int(8.8*FPS)}),1,1+0.0015*(on-{int(8.8*FPS)}))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=840x840:fps={FPS},"
   f"null[v];[1:v][v]overlay=960:120,trim=duration={d3}[o]",
   '-map', '[o]', '-an', *X264, os.path.join(MED, 'bg_reveal.mp4'))
# s5: live demo at normal speed, recut with hard cuts (no source dissolves); each alert screen held briefly.
#   (source in, source out, hold seconds after)
CUTS = [(1.0, 4.6, 0), (6.3, 8.6, 0), (9.6, 11.6, 0), (13.1, 16.7, .8), (17.6, 20.6, .8), (21.6, 24.7, .8)]
fc, labels = [], []
for k, (a, b, hold) in enumerate(CUTS):
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS},scale=1920:1080:flags=lanczos" + (f",tpad=stop_mode=clone:stop_duration={hold}" if hold else '') + f"[c{k}]")
    labels.append(f'[c{k}]')
d5 = dur('demo')
fc.append(''.join(labels) + f"concat=n={len(CUTS)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={d5},trim=duration={d5}[o]")
ff('-i', os.path.join(SRC_MEDIA, 'demo-full.mp4'), '-filter_complex', ';'.join(fc), '-map', '[o]', '-an', *X264, os.path.join(MED, 'bg_demo.mp4'))
# where each alert appears in the recut (scene-relative): segment start + time until the phone turns red
seg_start = np.cumsum([0] + [b - a + h for a, b, h in CUTS])
ALERTS = [('demo', seg_start[3] + 2.4), ('demo', seg_start[4] + 1.9), ('demo', seg_start[5] + 1.9)]
TOTAL_DING = ('deal', 13.3)                    # the agreement total lands

# composite the two footage scenes into finished clips
for i in OVER:
    ff('-i', os.path.join(MED, f'bg_{i}.mp4'), '-i', os.path.join(MED, f'gfx_{i}.mov'),
       '-filter_complex', '[0:v][1:v]overlay=0:0:format=auto,format=yuv420p[o]', '-map', '[o]', *X264, os.path.join(MED, f'scene_{i}.mp4'))

# ── 2. audio ─────────────────────────────────────────────────────────────────────────
N = int(TOTAL * SR); t = np.arange(N) / SR
note = lambda m: 440 * 2 ** ((m - 69) / 12)
def env(n, a, r):
    e = np.ones(n); a = min(a, n // 2); r = min(r, n - a)
    e[:a] = np.linspace(0, 1, a); e[n - r:] = np.linspace(1, 0, r) ** 2; return e
BEAT = 60 / 72; BAR = 4 * BEAT
CHORDS = [[53, 57, 60, 64], [55, 59, 62, 67], [52, 55, 59, 62], [57, 60, 64, 67]]   # Fmaj7 · G · Em7 · Am7 — light, clinical
mus = np.zeros(N)
def add(sig, start):
    i = int(start * SR); j = min(N, i + len(sig))
    if 0 <= i < N: mus[i:j] += sig[:j - i]
reveal = S['reveal']['t0']
for k in range(int(np.ceil(TOTAL / BAR))):
    st = k * BAR; ch = CHORDS[k % 4]; n = int((BAR + 1.2) * SR); tt = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * note(m) * tt) + .5 * np.sin(2 * np.pi * note(m) * 1.003 * tt) + .12 * np.sin(4 * np.pi * note(m) * tt) for m in ch)
    add(.05 * pad * env(n, int(.9 * SR), int(1.4 * SR)), st)
    if st >= S['market']['t0']:
        for b in (0, 2):
            nn = int(BEAT * 1.8 * SR); tb = np.arange(nn) / SR
            add(.12 * np.sin(2 * np.pi * note(ch[0] - 12) * tb) * np.exp(-tb * 2.2) * env(nn, 400, 4000), st + b * BEAT)
    if reveal <= st < TOTAL - 4:
        for e8 in range(0, 8, 2):
            m = ch[[0, 1, 2, 3, 2, 1, 2, 3][e8]] + 12; nn = int(.6 * SR); tp = np.arange(nn) / SR
            add(.045 * (np.sin(2 * np.pi * note(m) * tp) + .3 * np.sin(4 * np.pi * note(m) * tp)) * np.exp(-tp * 6) * env(nn, 60, 2000), st + e8 * BEAT / 2)
rng = np.random.default_rng(1)
def impact(at, g=1.0):                   # low cinematic hit at a chapter opening
    nn = int(2.2 * SR); tk = np.arange(nn) / SR; f = 34 + 26 * np.exp(-tk * 6)
    sig = .34 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk * 2.4) + .05 * rng.standard_normal(nn) * np.exp(-tk * 9)
    add(g * sig * env(nn, 60, int(.8 * SR)), at)
def riser(end, dur=2.2):                 # filtered noise + rising tone into a reveal
    nn = int(dur * SR); tk = np.arange(nn) / SR; ramp = (tk / dur) ** 2.2
    sig = .05 * rng.standard_normal(nn) * ramp + .05 * np.sin(2 * np.pi * np.cumsum(220 + 660 * ramp) / SR) * ramp
    add(sig, end - dur)
for sid in ('hook', 'market', 'law', 'problem', 'field', 'reveal', 'kalman', 'verify', 'deal', 'close'):
    impact(S[sid]['t0'], .8 if sid in ('reveal', 'close') else .5)
riser(S['reveal']['t0']); riser(S['close']['t0'], 2.6)
y = np.zeros_like(mus); a = np.exp(-2 * np.pi * 5200 / SR)
for i in range(1, N): y[i] = (1 - a) * mus[i] + a * y[i - 1]
mus = y * np.clip(t / 1.5, 0, 1) * np.clip((TOTAL - t) / 3.0, 0, 1)
mus *= .5 / np.max(np.abs(mus))
def ding(hi=False):
    nn = int(.95 * SR); out = np.zeros(nn)
    for k, f in enumerate((1318.5, 1760.0) if not hi else (1568.0, 2093.0)):
        i = int(k * .11 * SR); m = nn - i; tt = np.arange(m) / SR
        out[i:] += .22 * np.sin(2 * np.pi * f * tt) * np.exp(-tt * 7) * env(m, 80, 4000)
    return out
def wav(path, x):
    x = np.clip(x, -1, 1); st = (np.stack([x, x], 1) * 32767).astype('<i2')
    with wave.open(path, 'wb') as w: w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR); w.writeframes(st.tobytes())
wav(os.path.join(MED, 'music.wav'), mus)
DA, DT = ding(), ding(True)
wav(os.path.join(MED, 'ding_alert.wav'), DA); wav(os.path.join(MED, 'ding_total.wav'), DT)
DINGS = [(S[i]['t0'] + r, 'ding_alert.wav', DA) for i, r in ALERTS] + [(S[TOTAL_DING[0]]['t0'] + TOTAL_DING[1], 'ding_total.wav', DT)]
mix = mus.copy()
for at, _, d in DINGS:
    i = int(at * SR); j = min(N, i + len(d)); mix[i:j] += d[:j - i]

# ── 3. final export ──────────────────────────────────────────────────────────────────
TMP = os.path.join(EDIT, '.tmp'); os.makedirs(TMP, exist_ok=True)
lst = os.path.join(TMP, 'list.txt')
open(lst, 'w').write(''.join(f"file '{os.path.join(MED, 'scene_' + s['id'] + '.mp4')}'\n" for s in SC))
ff('-f', 'concat', '-safe', '0', '-i', lst, '-c', 'copy', os.path.join(TMP, 'video.mp4'))
wav(os.path.join(TMP, 'mix.wav'), mix)
final = os.path.join(EXPORT, 'INFU-RETRO_홍보영상.mp4')
ff('-i', os.path.join(TMP, 'video.mp4'), '-i', os.path.join(TMP, 'mix.wav'), '-map', '0:v', '-map', '1:a',
   '-c:v', 'libx264', '-crf', '18', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-c:a', 'aac', '-b:a', '192k', '-movflags', '+faststart',
   '-metadata', 'title=INFU RETRO 홍보 영상', final)
for f in os.listdir(TMP): os.remove(os.path.join(TMP, f))
os.rmdir(TMP)

# ── 4. subtitles: (scene, start, end, text) — scene-relative, '\n' = line break ──────
SUBS = [('cover', .6, 4.8, 'INFU RETRO — 가상의 자이로 AI 모델을 활용한 동물용 약물이상감지 시스템'),
        ('hook', .4, 5.8, '진료가 끝난 밤, 수액은 지금도 들어가고 있지만\n지켜보는 사람은 없습니다.'),
        ('market', .4, 10.8, '반려동물 양육가구 29.2% · 병원 이용률 95.1%\n동물병원 피해구제 접수는 4년 새 3배 이상 늘었습니다.'),
        ('law', .4, 10.8, '진료기록 열람 · 사본 발급 법안 농해수위 의결(2026.9.2)\n감시에 기록까지, 1인 수의사 혼자 해야 합니다.'),
        ('problem', .4, 8.8, '입원 동물 수액 카테터 4개 중 1개에서 합병증(정맥염 포함)\n동물병원 10곳 중 7곳은 수의사 1명입니다.'),
        ('field', .4, 7.8, '현장 26곳 직접 방문 · 간호사 75명 인터뷰\n70%가 이상 상황 자동 전송을 원했습니다.'),
        ('reveal', .5, 9.6, 'INFU RETRO — 쓰던 폴대에 끼우기만 하면,\n수액 이상을 먼저 알립니다.'),
        ('real', .3, 4.8, 'MVP 구현 — 로드셀 4개 모듈과\nADS1232 & ESP32 프로세서 일체 PCB(4×4 이미지 처리 · 연산 가속)'),
        ('demo', .3, 7.6, '실제 시연 — 폴대에 끼우고 수액백을 걸면\n무게를 실시간으로 측정합니다.'),
        ('demo', 8.0, 12.0, '유속 빠름 → 알림 · 줄 빠짐 · 조절기 풀림 의심'),
        ('demo', 12.4, 15.8, '유속 느림 → 알림 · 줄 꺾임 · 혈액 역류 위험'),
        ('demo', 16.2, 19.7, '유속 정지 → 알림 · 수액 소진 · 공기 색전 위험'),
        ('kalman', .4, 12.6, '로드셀 측정값 z = w + n 의 잡음을\n칼만 필터(예측 → 이득 → 갱신)로 걸러 냅니다.'),
        ('pid', .4, 15.6, '가상 AI 자이로가 기울기를 추정하고, LLM(LoRA)과 유전 알고리즘이\n찾은 PID 게인으로 흔들림 오차를 상쇄합니다.'),
        ('grid', .4, 11.6, '유속 편차를 −1 · 0 · +1로 부호화해\n16개씩 모아 4×4 그림으로 만듭니다.'),
        ('rcnn', .4, 12.6, 'RCNN — CNN은 4×4 그림의 모양을, RNN은 유속의 흐름을 보고\n두 특징을 결합해 5가지 상태로 판정합니다.'),
        ('verify', .3, 9.6, '잔량 최대 오차 2.9% · 줄 분리 · 소진 250/250 (내부 모의시험)\n산업통상부장관상 · 우수논문상 2편'),
        ('deal', .4, 6.2, '㈜씨엔 물품공급 약정 5,100만 원 (KC 인증 후 효력)'),
        ('deal', 6.6, 11.2, '㈜에스케이엠엔엠 구매의향 · 사업협력 협약 5,000만 원 (비구속)'),
        ('deal', 11.6, 15.8, '약정 · 협약 합계 1억 100만 원 · 확정 매출 아님'),
        ('close', .4, 6.8, '폴대는 그대로, 수액은 놓치지 않게 — INFU RETRO')]
ts = lambda x: '%02d:%02d:%02d,%03d' % (x // 3600, x % 3600 // 60, int(x % 60), round(x % 1 * 1000) % 1000)
open(os.path.join(EDIT, 'captions.srt'), 'w', encoding='utf-8').write(
    ''.join(f"{k}\n{ts(S[i]['t0'] + a)} --> {ts(S[i]['t0'] + b)}\n{txt}\n\n" for k, (i, a, b, txt) in enumerate(SUBS, 1)))

# ── 5. Premiere Pro / DaVinci Resolve timeline (FCP 7 XML) ───────────────────────────
fr = lambda x: int(round(x * FPS))
RATE = f'<rate><timebase>{FPS}</timebase><ntsc>FALSE</ntsc></rate>'
url = lambda name: 'file://localhost' + quote(os.path.join(MED, name).replace(os.sep, '/'))
VCHAR = f'<samplecharacteristics>{RATE}<width>1920</width><height>1080</height><anamorphic>FALSE</anamorphic><pixelaspectratio>square</pixelaspectratio><fielddominance>none</fielddominance></samplecharacteristics>'
ACHAR = f'<samplecharacteristics><depth>16</depth><samplerate>{SR}</samplerate></samplecharacteristics>'
cid = 0
def clip(name, fname, start, length, kind='video', alpha=False):
    global cid; cid += 1
    d = fr(length)
    media = (f'<media><video>{VCHAR}</video></media>' if kind == 'video'
             else f'<media><audio>{ACHAR}<channelcount>2</channelcount></audio></media>')
    tail = '<sourcetrack><mediatype>audio</mediatype><trackindex>1</trackindex></sourcetrack>' if kind == 'audio' else ''
    return (f'<clipitem id="clip-{cid}"><name>{name}</name><enabled>TRUE</enabled><duration>{d}</duration>{RATE}'
            f'<start>{fr(start)}</start><end>{fr(start) + d}</end><in>0</in><out>{d}</out>'
            f'<file id="file-{cid}"><name>{fname}</name><pathurl>{url(fname)}</pathurl>{RATE}<duration>{d}</duration>{media}</file>'
            + ('<alphatype>straight</alphatype>' if alpha else '') + tail + '</clipitem>')
NAMES = {'cover': '표지', 'hook': '도입', 'market': '01 시장 변화', 'law': '02 제도 변화', 'problem': '03 현장 문제', 'field': '04 현장 인터뷰', 'reveal': '05 제품 공개', 'real': '05 MVP 구현', 'demo': '06 실제 시연', 'kalman': '07 칼만 필터', 'pid': '07 가상 자이로 · PID', 'grid': '07 4×4 패턴', 'rcnn': '07 RCNN', 'verify': '08 검증', 'deal': '09 구매 협약', 'close': '마무리'}
v1 = ''.join(clip(NAMES[s['id']], f"scene_{s['id']}.mp4", s['t0'], dur(s['id'])) for s in SC)
v2 = ''.join(clip(NAMES[i] + ' · 배경 영상', f'bg_{i}.mp4', S[i]['t0'], dur(i)) for i in OVER)
v3 = ''.join(clip(NAMES[i] + ' · 그래픽(투명)', f'gfx_{i}.mov', S[i]['t0'], dur(i), alpha=True) for i in OVER)
a1 = clip('음악', 'music.wav', 0, TOTAL, 'audio')
a2 = ''.join(clip('알림음', fn, at, len(d) / SR, 'audio') for at, fn, d in DINGS)
xml = f'''<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE xmeml>
<xmeml version="5"><sequence id="seq-1"><name>INFU RETRO 홍보 영상</name><duration>{fr(TOTAL)}</duration>{RATE}
<timecode>{RATE}<string>00:00:00:00</string><frame>0</frame><displayformat>NDF</displayformat></timecode>
<media><video><format>{VCHAR}</format>
<track>{v1}<enabled>TRUE</enabled><locked>FALSE</locked></track>
<track>{v2}<enabled>FALSE</enabled><locked>FALSE</locked></track>
<track>{v3}<enabled>FALSE</enabled><locked>FALSE</locked></track></video>
<audio><numOutputChannels>2</numOutputChannels><format>{ACHAR}</format>
<outputs><group><index>1</index><numchannels>2</numchannels><downmix>0</downmix><channel><index>1</index></channel><channel><index>2</index></channel></group></outputs>
<track>{a1}<enabled>TRUE</enabled><locked>FALSE</locked><outputchannelindex>1</outputchannelindex></track>
<track>{a2}<enabled>TRUE</enabled><locked>FALSE</locked><outputchannelindex>1</outputchannelindex></track></audio></media></sequence></xmeml>
'''
open(os.path.join(EDIT, 'INFU-RETRO_promo_timeline.xml'), 'w', encoding='utf-8').write(xml)
print('done', final, round(os.path.getsize(final) / 1e6, 1), 'MB · alerts at', [round(S[i]['t0'] + r, 2) for i, r in ALERTS])
