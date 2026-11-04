# 5-minute speaker script (main slides) + a spoken-length estimate in Korean syllables
import re, html

DECK = __import__('os').path.join(__import__('os').path.dirname(__import__('os').path.dirname(__import__('os').path.abspath(__file__))), 'index.html')
def load_notes():
    """speaker notes of the main slides, read from the deck itself (slides with data-time)"""
    src = open(DECK, encoding='utf-8').read(); out = {}
    for m in re.finditer(r'<section ([^>]*)>(.*?)</section>', src, re.S):
        if 'data-time=' not in m.group(1): continue
        sid = re.search(r'id="([^"]+)"', m.group(1)).group(1)
        n = re.search(r'<div class="note" hidden>(.*?)</div>', m.group(2), re.S).group(1)
        out[sid] = [html.unescape(re.sub(r'\s+', ' ', re.sub(r'<[^>]+>', ' ', p))).strip() for p in re.findall(r'<p>(.*?)</p>', n, re.S)]
    return out
NOTES = load_notes()
DEMO_VIDEO = 10  # the demo video plays at 2.5x: 0:10 (last chapter 0:08)

DIG = '영일이삼사오육칠팔구'
def read_int(n):
    """sino-Korean reading of an integer, e.g. 5312 -> 오천삼백십이"""
    if n == 0: return '영'
    out = ''
    for unit, word in ((10**8, '억'), (10**4, '만')):
        if n >= unit:
            out += read_int(n // unit) + word; n %= unit
    for unit, word in ((1000, '천'), (100, '백'), (10, '십')):
        d = n // unit
        if d: out += ('' if d == 1 else DIG[d]) + word
        n %= unit
    return out + (DIG[n] if n else '')
WORDS = {'WON SHOT': '원샷', 'INFUTECH': '인퓨테크', 'INFU RETRO': '인퓨레트로', 'CNN': '씨엔엔', 'AI': '에이아이', 'SKM&M': '에스케이엠앤엠', 'MOU': '엠오유', '㈜': ''}
def spoken(text):
    t = text
    for k, v in WORDS.items(): t = t.replace(k, v)
    t = t.replace('4×4', '사바이사').replace('%', '퍼센트')
    t = re.sub(r'(\d[\d,]*)\.(\d+)', lambda m: read_int(int(m.group(1).replace(',', ''))) + '점' + ''.join(DIG[int(c)] for c in m.group(2)), t)
    t = re.sub(r'\d[\d,]*', lambda m: read_int(int(m.group(0).replace(',', ''))), t)
    return len(re.findall(r'[가-힣]', t)) + len(re.findall(r'[A-Za-z]', t))

TOTAL = 600  # 10분
def plan():
    """spoken length at about 5 syllables a second, then scaled so the slides add up to TOTAL (the slack is pauses)"""
    syl = {k: sum(spoken(p) for p in v) for k, v in NOTES.items()}
    n = sum(syl.values())
    raw = {k: max(4, v * TOTAL / n) for k, v in syl.items()}
    secs = {k: int(x) for k, x in raw.items()}
    for k in sorted(raw, key=lambda k: raw[k] - secs[k], reverse=True)[:TOTAL - sum(secs.values())]:
        secs[k] += 1
    return syl, secs

if __name__ == '__main__':
    syl, secs = plan()
    for k in NOTES: print(f'{k:9s} {syl[k]:4d}음절 {secs[k]:3d}s')
    print('total', sum(syl.values()), '음절,', sum(secs.values()), 's ·', round(sum(syl.values()) / TOTAL, 2), '음절/초')
