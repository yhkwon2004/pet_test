import re
def esc(t): return t.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
def M(s, fs):
    """Tiny math markup -> SVG tspans.  _{..} subscript, ^{..} superscript, *..* italic (may nest)."""
    small = round(fs * 0.7)
    out, i = [], 0
    while i < len(s):
        c = s[i]
        if c in '_^' and i + 1 < len(s) and s[i + 1] == '{':
            depth, j = 1, i + 2
            while depth:
                depth += {'{': 1, '}': -1}.get(s[j], 0); j += 1
            inner = s[i + 2:j - 1]
            out.append(f'<tspan font-size="{small}" baseline-shift="{"sub" if c == "_" else "super"}">{M(inner, small)}</tspan>')
            i = j; continue
        if c == '*':
            j = s.index('*', i + 1)
            out.append(f'<tspan font-style="italic">{M(s[i + 1:j], fs)}</tspan>')
            i = j + 1; continue
        out.append(esc(c)); i += 1
    return ''.join(out)
