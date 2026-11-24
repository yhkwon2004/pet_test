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
OVER = ('s3', 's5')
ff = lambda *a: subprocess.run(['ffmpeg', '-v', 'error', '-y', *a], check=True)
dur = lambda i: S[i]['t1'] - S[i]['t0']
X264 = ['-c:v', 'libx264', '-crf', '15', '-preset', 'slow', '-pix_fmt', 'yuv420p', '-r', str(FPS)]

# ── 1. footage layers ────────────────────────────────────────────────────────────────
# s3: housing assembly render (600×600). Exploded → assembled 3/4 view (first 4.4 s), slowed 2× with
# motion interpolation, then a slow push-in hold on that view; right half of the frame.
d3 = dur('s3')
ff('-i', os.path.join(SRC_MEDIA, 'hanger.mp4'), '-f', 'lavfi', '-i', f'color=c=0x7f7f7f:s=1920x1080:r={FPS}:d={d3}',
   '-filter_complex',
   f"[0:v]trim=0:4.4,setpts=2*(PTS-STARTPTS),minterpolate=fps={FPS}:mi_mode=mci:mc_mode=aobmc:vsbmc=1,"
   f"scale=1080:1080:flags=lanczos,tpad=stop_mode=clone:stop_duration={d3},"
   f"zoompan=z='if(lte(on,{int(8.8*FPS)}),1,1+0.0015*(on-{int(8.8*FPS)}))':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d=1:s=1080x1080:fps={FPS},"
   f"crop=960:1080[v];[1:v][v]overlay=960:0,trim=duration={d3}[o]",
   '-map', '[o]', '-an', *X264, os.path.join(MED, 'bg_s3.mp4'))
# s5: live demo at normal speed, recut with hard cuts (no source dissolves); each alert screen held briefly.
#   (source in, source out, hold seconds after)
CUTS = [(1.0, 4.6, 0), (6.3, 8.6, 0), (9.6, 11.6, 0), (13.1, 16.7, .8), (17.6, 20.6, .8), (21.6, 24.7, .8)]
fc, labels = [], []
for k, (a, b, hold) in enumerate(CUTS):
    fc.append(f"[0:v]trim={a}:{b},setpts=PTS-STARTPTS,fps={FPS},scale=1920:1080:flags=lanczos" + (f",tpad=stop_mode=clone:stop_duration={hold}" if hold else '') + f"[c{k}]")
    labels.append(f'[c{k}]')
d5 = dur('s5')
fc.append(''.join(labels) + f"concat=n={len(CUTS)}:v=1:a=0,tpad=stop_mode=clone:stop_duration={d5},trim=duration={d5}[o]")
ff('-i', os.path.join(SRC_MEDIA, 'demo-full.mp4'), '-filter_complex', ';'.join(fc), '-map', '[o]', '-an', *X264, os.path.join(MED, 'bg_s5.mp4'))
# where each alert appears in the recut (scene-relative): segment start + time until the phone turns red
seg_start = np.cumsum([0] + [b - a + h for a, b, h in CUTS])
ALERTS = [('s5', seg_start[3] + 2.4), ('s5', seg_start[4] + 1.9), ('s5', seg_start[5] + 1.9)]
TOTAL_DING = ('s8', 6.8)                    # the agreement total lands

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
BEAT = 60 / 96; BAR = 4 * BEAT
CHORDS = [[53, 57, 60, 64], [55, 59, 62, 67], [52, 55, 59, 62], [57, 60, 64, 67]]   # Fmaj7 · G · Em7 · Am7
mus = np.zeros(N)
def add(sig, start):
    i = int(start * SR); j = min(N, i + len(sig))
    if 0 <= i < N: mus[i:j] += sig[:j - i]
reveal = S['s3']['t0']
for k in range(int(np.ceil(TOTAL / BAR))):
    st = k * BAR; ch = CHORDS[k % 4]; n = int((BAR + 1.2) * SR); tt = np.arange(n) / SR
    pad = sum(np.sin(2 * np.pi * note(m) * tt) + .5 * np.sin(2 * np.pi * note(m) * 1.003 * tt) + .12 * np.sin(4 * np.pi * note(m) * tt) for m in ch)
    add(.05 * pad * env(n, int(.9 * SR), int(1.4 * SR)), st)
    if st >= S['s2']['t0']:
        for b in (0, 2):
            nn = int(BEAT * 1.8 * SR); tb = np.arange(nn) / SR
            add(.12 * np.sin(2 * np.pi * note(ch[0] - 12) * tb) * np.exp(-tb * 2.2) * env(nn, 400, 4000), st + b * BEAT)
    if reveal <= st < TOTAL - 4:
        for e8 in range(8):
            m = ch[[0, 1, 2, 3, 2, 1, 2, 3][e8]] + 12; nn = int(.6 * SR); tp = np.arange(nn) / SR
            add(.045 * (np.sin(2 * np.pi * note(m) * tp) + .3 * np.sin(4 * np.pi * note(m) * tp)) * np.exp(-tp * 6) * env(nn, 60, 2000), st + e8 * BEAT / 2)
    if reveal <= st < TOTAL - 7:
        for b in range(4):
            nn = int(.18 * SR); tk = np.arange(nn) / SR; f = 50 + 70 * np.exp(-tk * 30)
            add(.16 * np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tk * 22), st + b * BEAT)
sw = (t > reveal - 1.7) & (t < reveal); mus[sw] += .06 * np.random.default_rng(1).standard_normal(sw.sum()) * np.linspace(0, 1, sw.sum()) ** 2
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
SUBS = [('s1', .5, 6.6, '진료가 끝난 밤, 수액은 지금도 들어가고 있지만\n지켜보는 사람은 없습니다.'),
        ('s2', .4, 5.2, '입원 동물 수액 카테터 4개 중 1개에서 합병증(정맥염 포함)\n사고는 순회와 순회 사이에서 납니다.'),
        ('s2', 5.4, 9.6, '동물병원 10곳 중 7곳은 수의사 1명.\n이상이 생긴 순간 먼저 알려 줘야 합니다.'),
        ('s3', .5, 9.6, 'INFU RETRO — 쓰던 폴대에 끼우기만 하면,\n수액 이상을 먼저 알립니다.'),
        ('s4', .3, 5.6, '시제품 · 모듈 · PCB를 실물로 만들었습니다.'),
        ('s5', .3, 7.6, '실제 시연 — 폴대에 끼우고 수액백을 걸면\n무게를 실시간으로 측정합니다.'),
        ('s5', 8.0, 19.7, '유속이 빠르거나 느리거나 멈추면\n대시보드와 휴대폰으로 알립니다.'),
        ('s6', .4, 7.2, '로드셀 → 칼만 필터 → 가상 AI 자이로 + PID\n→ 4×4 패턴 CNN · RNN → 5가지 상태 판정'),
        ('s6', 7.4, 15.6, '잔량 최대 오차 2.9% · 줄 분리 · 소진 250/250 감지 · 센서 비용 1/36\n(내부 모의시험 기준)'),
        ('s7', .3, 7.6, '모의 병실 1,000회 내부 시험\n창의적종합설계경진대회 산업통상부장관상 · 우수논문상 2편'),
        ('s8', .4, 11.6, '㈜씨엔 공급 약정 5,100만 원(KC 인증 후 효력) · ㈜에스케이엠엔엠 구매의향 협약 5,000만 원(비구속)\n합계 1억 100만 원 · 확정 매출 아님'),
        ('s9', .4, 6.8, '폴대는 그대로, 수액은 놓치지 않게 — INFU RETRO')]
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
NAMES = {'s1': '도입', 's2': '01 문제', 's3': '02 제품 공개', 's4': '02 실물', 's5': '03 실제 시연', 's6': '04 기술', 's7': '05 검증', 's8': '06 구매 협약', 's9': '마무리'}
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
