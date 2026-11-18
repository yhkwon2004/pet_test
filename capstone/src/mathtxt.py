
import re
def M(s, fs):
    """'x_{k-1}^{-}' style -> SVG tspans (sub/superscript at 72%)"""
    out=[]; i=0; small=round(fs*0.72)
    pat=re.compile(r'([_^])\{([^}]*)\}|([_^])(.)')
    pos=0
    for m in pat.finditer(s):
        out.append(esc(s[pos:m.start()]))
        kind=m.group(1) or m.group(3); body=m.group(2) if m.group(2) is not None else m.group(4)
        sh='sub' if kind=='_' else 'super'
        out.append(f'<tspan font-size="{small}" baseline-shift="{sh}">{esc(body)}</tspan>')
        pos=m.end()
    out.append(esc(s[pos:]))
    return ''.join(out)
def esc(t): return t.replace('&','&amp;').replace('<','&lt;').replace('>','&gt;')
