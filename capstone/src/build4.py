# Stage 4 (2026-11-18): white, document-like theme — no purple gradients, glows or neon; one navy accent,
# neutral grays, lighter weights, larger small text. Remaps the template palette everywhere (CSS + inline SVG).
import re
DST = '/home/user/pet_test/capstone/index.html'
s = open(DST, encoding='utf-8').read()
MAP = {  # indigo/lavender family -> navy/neutral
 '#4B48E0': '#1E3A8A', '#4E4AE3': '#1E3A8A', '#5F5BEA': '#1E3A8A', '#8783F5': '#3B5BA9', '#7471F0': '#3B5BA9', '#6E6BF2': '#2B4A9C',
 '#8C89F5': '#5B74B0', '#AEB2FB': '#B7C3DB', '#A7ACFA': '#FFFFFF', '#C2C5FC': '#FFFFFF', '#E6E6FE': '#FFFFFF',
 '#ECEBFE': '#F2F4F7', '#EEEDFE': '#F2F4F7', '#DCDBFB': '#E3E7EE', '#C9C8F8': '#CDD4E0', '#B9B7F7': '#CDD4E0', '#E5E4FF': '#D7DEEA',
 '#DCDAFD': '#FFFFFF', '#F4F4FF': '#FFFFFF', '#C9C7FF': '#6B7280', '#A9A6FF': '#1E3A8A', '#EDEBFF': '#4B5563',
 '#1D1C2B': '#111418', '#4A4A5C': '#3F4651', '#8B8B9C': '#6B7280', '#5E5E72': '#4B5563', '#9C9CAC': '#7B828C', '#2B2950': '#3F4651', '#17162A': '#111418',
 '#DCDCE6': '#E5E7EB', '#E2E2EC': '#E5E7EB', '#E4E4EC': '#E5E7EB', '#EFEFF4': '#F3F4F6', '#F4F4F8': '#F6F7F9',
 '#F0506E': '#C0392B', '#FFF0F3': '#FBEDEB', '#FFD84D': '#DDE4F0', '#2E9E6A': '#1E7F55', '#E07B2E': '#B4641C', '#FFF4EA': '#FAF2E9', '#FBE3CC': '#F4EADC', '#A04E10': '#7A4310',
}
for a, b in MAP.items():
    s = re.sub(re.escape(a), b, s, flags=re.I)
s = s.replace('rgba(60, 50, 160,', 'rgba(17, 20, 24,').replace('rgba(50, 40, 150,', 'rgba(17, 20, 24,').replace('rgba(20, 16, 90,', 'rgba(17, 20, 24,')
THEME = '''
/* ===== white theme ===== */
.slide.rf, .slide.rf.r-reveal, .slide.rf.r-band, .slide.rf.r-solid, .slide.rf.r-cover { background: #FFFFFF !important; color: #111418; }
.slide.rf { --ri: #1E3A8A; --ri2: #3B5BA9; --rp: #B7C3DB; --rl: #F2F4F7; --rk: #111418; --rk2: #3F4651; --rm: #6B7280; --rline: #E5E7EB; --ry: #1E3A8A; --rr: #C0392B; --rg: #F3F4F6; }
.slide.rf *, .slide.rf *::before, .slide.rf *::after { box-shadow: none !important; text-shadow: none !important; }
.slide.rf .frame::before { color: #9AA0A8 !important; font-weight: 700 !important; letter-spacing: .12em !important; }
.slide.rf .frame::after { color: #9AA0A8 !important; }
/* typography */
.rf .r-t { font-weight: 700; letter-spacing: -.03em; line-height: 1.3; }
.rf .r-t em { font-style: normal; color: var(--ri); }
.rf .r-kick { padding-bottom: 0; border-bottom: 0; font-size: 1.15em; font-weight: 700; letter-spacing: .02em; color: var(--ri); }
.rf .r-kick::before { content: ""; display: inline-block; width: 1.6em; height: .14em; margin-right: .6em; vertical-align: .3em; background: var(--ri); }
.rf .r-hd { margin-bottom: 1.7em; }
.rf .r-src { font-size: .95em; font-weight: 500; color: #7B828C; }
.rf .r-ct { font-size: 1.2em; font-weight: 700; color: #3F4651; }
.rf .r-cap { font-weight: 700; }
.rf .r-foot { font-weight: 600; color: #3F4651; }
/* surfaces */
.rf .r-card { border: 1px solid #E5E7EB; border-radius: .7em; }
#s-background .r-foot, #s-onevet .r-foot, .rf .r-foot { background: none !important; padding: 0 !important; border-radius: 0 !important; }
.rf .r-pie { background: conic-gradient(#1E3A8A 0, #1E3A8A calc(var(--p) * 1%), #EEF0F3 calc(var(--p) * 1%)) !important; }
.rf .r-pie span { background: #C0392B; font-weight: 700; }
/* cover — white with the product photo fading in from the right */
.r-cover .frame::before { color: #9AA0A8 !important; }
.rf .r-cv-bg { width: 58%; -webkit-mask-image: linear-gradient(90deg, transparent 0%, rgba(0, 0, 0, .35) 18%, #000 42%) !important; mask-image: linear-gradient(90deg, transparent 0%, rgba(0, 0, 0, .35) 18%, #000 42%) !important; }
.r-cover .r-cv-k { color: #3F4651 !important; font-weight: 600; }
.r-cover .r-cv-w { color: #111418 !important; font-weight: 800; }
.r-cover .r-cv-w .tri path { fill: #1E3A8A; }
.r-cover .r-cv-s { color: #3F4651 !important; font-weight: 600; }
.r-cover .r-cv-s b { color: #1E3A8A !important; }
.r-cover .r-cv-bd li, #s-opening .r-cv-bd li { background: #FFFFFF !important; border: 1px solid #E5E7EB !important; border-radius: .5em; -webkit-backdrop-filter: none; backdrop-filter: none; }
.r-cover .r-cv-bd b { color: #111418 !important; }
.r-cover .r-cv-bd span { color: #6B7280 !important; }
.rf .r-cv-cap { background: #FFFFFF; color: #1E3A8A; border: 1.5px solid #1E3A8A; border-radius: .35em; font-weight: 700; letter-spacing: .04em; }
/* hook / closing — white */
.rf .r-st-k { color: #6B7280; font-weight: 600; } .rf .r-st-k b { color: #111418; }
.rf .r-st-t { color: #111418; font-weight: 700; }
.rf .r-st-t u { color: #1E3A8A; background: linear-gradient(#1E3A8A, #1E3A8A) 0 100% / 100% .06em no-repeat; }
.rf .r-st-c li { background: #FFFFFF; border: 1px solid #D1D5DB; border-radius: .5em; color: #111418; font-weight: 600; }
.rf .r-st-c i { background: #1E3A8A; color: #FFFFFF; font-weight: 700; }
.rf .r-st-s { color: #7B828C; }
/* test band — white with a thin rule */
.rf .r-bd { color: #111418; padding-bottom: 1.2em; border-bottom: 1px solid #E5E7EB; }
.rf .r-bd-t { font-weight: 700; } .rf .r-bd-t span { color: #6B7280; opacity: 1; }
.rf .r-bub li { background: #F6F7F9; border: 1px solid #E5E7EB; border-radius: .5em; color: #111418; font-weight: 600; }
.rf .r-bub li::after { display: none; }
/* reveal */
.rf .r-rv2-ph { border-radius: .8em; }
.rf .r-rv2-t { font-weight: 750; }
.rf .r-rv2-l i { color: #1E3A8A; font-weight: 700; }
.rf .r-rv2-l b { font-weight: 700; }
.rf .r-rv2-p { border-radius: .4em; font-weight: 600; } .rf .r-rv2-p b { color: #FFFFFF; }
.rf .r-rv2-v li { border: 1px solid #E5E7EB; border-radius: .5em; }
/* new slides */
.rf .cp-tasks li, .rf .cp-why li, .rf .cp-hw > li, .rf .cp-res p { border-radius: .6em; }
.rf .cp-why li.pp { background: #1E3A8A; } .rf .cp-why li.pp i { background: #FFFFFF; color: #1E3A8A; }
.rf .cp-why i { font-weight: 700; } .rf .cp-why b, .rf .cp-hw > li > b, .rf .cp-tasks b { font-weight: 700; }
.rf .cp-tasks li.iv { background: #FBEDEB; box-shadow: none; outline: 1.5px solid #C0392B; outline-offset: -1.5px; }
/* highlights that used to be yellow on navy */
.rf .r-hyp p b, .rf .r-iv blockquote b, .rf .r-st-a b, .rf .r-rv2-p b { color: #FFFFFF; text-decoration: underline; text-decoration-thickness: .08em; text-underline-offset: .2em; }
.rf .r-src { line-height: 1.45; }
'''
s = s.replace('</head>', f'<style id="cap-theme">{THEME}</style>\n</head>', 1)
open(DST, 'w', encoding='utf-8').write(s); print('theme ok')
