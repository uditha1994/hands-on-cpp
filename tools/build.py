#!/usr/bin/env python3
"""Build the Hands-On C++ handbook (web and PDF) from content/*.md.

Usage: python3 tools/build.py web|pdf|verify
"""
import re, sys, os, html, json, hashlib, base64, random, subprocess, glob

ROOT = os.path.dirname(os.path.abspath(__file__))          # tools/
REPO = os.path.dirname(ROOT)                               # repository root
SRC = os.path.join(REPO, 'content')
CAPSTONE = os.path.join(REPO, 'capstone')
BUILD = os.path.join(REPO, 'build')
CACHE = os.path.join(REPO, '.cache')
os.makedirs(BUILD, exist_ok=True); os.makedirs(CACHE, exist_ok=True)
import markdown as MD

AUTHOR = 'Uditha Landekumbura'
BOOK = 'Head Start C++'
SUB = 'A brain-friendly guide to programming in C++, from your first line of code to real projects'
LOGO = os.path.join(REPO, 'assets', 'logo.png')

def b64(path):
    with open(path, 'rb') as f: return base64.b64encode(f.read()).decode()

# ------------------------------------------------------------------ highlighter
KW = set('''alignas alignof and asm auto break case catch class const constexpr const_cast continue
decltype default delete do dynamic_cast else enum explicit export extern false for friend goto if inline
mutable namespace new noexcept not nullptr operator or private protected public register reinterpret_cast
return sizeof static static_assert static_cast struct switch template this throw true try typedef typeid
typename union using virtual volatile while xor'''.split())
TY = set('''int double float char bool void long short unsigned signed string size_t vector ifstream ofstream
fstream istream ostream array stringstream istringstream'''.split())
LIB = set('cout cin endl cerr getline main std'.split())

TOK = re.compile(r'''(?P<com>//[^\n]*|/\*.*?\*/)|(?P<pre>^\s*\#\s*\w+[^\n]*)|(?P<str>"(?:\\.|[^"\\])*")|(?P<chr>'(?:\\.|[^'\\])')|(?P<num>\b\d+(?:\.\d+)?(?:[eE][+-]?\d+)?[fFlLuU]*\b)|(?P<id>[A-Za-z_]\w*)|(?P<other>.)''', re.S | re.M)

def hl_cpp(code):
    out = []
    for m in TOK.finditer(code):
        k = m.lastgroup; t = html.escape(m.group())
        if k == 'com': out.append(f'<span class="c-com">{t}</span>')
        elif k == 'pre':
            # highlight <header> inside
            out.append(f'<span class="c-pre">{t}</span>')
        elif k in ('str', 'chr'): out.append(f'<span class="c-str">{t}</span>')
        elif k == 'num': out.append(f'<span class="c-num">{t}</span>')
        elif k == 'id':
            w = m.group()
            if w in KW: out.append(f'<span class="c-kw">{t}</span>')
            elif w in TY: out.append(f'<span class="c-ty">{t}</span>')
            elif w in LIB: out.append(f'<span class="c-lib">{t}</span>')
            else: out.append(t)
        else: out.append(t)
    return ''.join(out)

def hl_pseudo(code):
    t = html.escape(code)
    t = re.sub(r'\b(START|END|STOP|BEGIN|IF|THEN|ELSE|ELSE IF|END IF|ENDIF|WHILE|END WHILE|ENDWHILE|FOR|TO|STEP|END FOR|ENDFOR|DO|REPEAT|UNTIL|READ|INPUT|DISPLAY|PRINT|OUTPUT|SET|RETURN|FUNCTION|END FUNCTION|CALL|AND|OR|NOT)\b',
               r'<span class="c-kw">\1</span>', t)
    return t

# ------------------------------------------------------------------ context
class Ctx:
    def __init__(self, mode):
        self.mode = mode
        self.chapter = None
        self.sec = 0
        self.ex = 0
        self.solutions = []     # (chapter, label, title, html)
        self.code = []          # dicts for verification
        self.toc = []           # (chnum, title, tagline, [(id,title)])
        self.blk = {}
        self.uid = 0
        self.files = {}
    def key(self, h):
        self.uid += 1
        k = f'XBLKX{self.uid}XBLKX'
        self.blk[k] = h
        return k
    def next_id(self, p):
        self.uid += 1
        return f'{p}{self.uid}'

ICONS = {
 'brain': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 18h6M10 21h4M12 3a6 6 0 0 0-3.6 10.8c.6.5 1 1.2 1.1 2h5c.1-.8.5-1.5 1.1-2A6 6 0 0 0 12 3z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>',
 'pencil': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 20l1-5L16 4l4 4L9 19l-5 1zM14 6l4 4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 'warn': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 3l10 18H2L12 3zM12 10v5M12 18v.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round" stroke-linecap="round"/></svg>',
 'q': '<svg viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M9.5 9.5a2.5 2.5 0 1 1 3.5 2.3c-.6.3-1 .9-1 1.6v.6M12 17v.5" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 'chip': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="6" y="6" width="12" height="12" rx="2" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M9 2v4M15 2v4M9 18v4M15 18v4M2 9h4M2 15h4M18 9h4M18 15h4" stroke="currentColor" stroke-width="1.8"/></svg>',
 'coffee': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M4 9h13v5a5 5 0 0 1-5 5H9a5 5 0 0 1-5-5V9zM17 10h1.5a2.5 2.5 0 0 1 0 5H17M8 3v3M12 3v3" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/></svg>',
 'magnet': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6 3v8a6 6 0 0 0 12 0V3h-4v8a2 2 0 0 1-4 0V3H6zM6 7h4M14 7h4" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 'bug': '<svg viewBox="0 0 24 24" aria-hidden="true"><rect x="7" y="7" width="10" height="13" rx="5" fill="none" stroke="currentColor" stroke-width="1.8"/><path d="M12 7v13M9 4l1.5 2M15 4l-1.5 2M3 12h4M17 12h4M4 7l3 2M20 7l-3 2M4 18l3-2M20 18l-3-2" stroke="currentColor" stroke-width="1.6" stroke-linecap="round"/></svg>',
 'flask': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 3h6M10 3v6L4.5 19a1.5 1.5 0 0 0 1.3 2h12.4a1.5 1.5 0 0 0 1.3-2L14 9V3M7 15h10" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 'list': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M9 6h11M9 12h11M9 18h11M4 6h.5M4 12h.5M4 18h.5" stroke="currentColor" stroke-width="2.2" stroke-linecap="round"/></svg>',
 'fire': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 21c-4 0-7-2.7-7-6.5 0-3 2-5 3.5-6.5.3 2 1.5 3 2.5 3.5C11 8 12 5 14 3c.5 3 5 5.5 5 11 0 4-3 7-7 7z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
 'build': '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M14.7 6.3a4 4 0 0 0-5.4 5.4L3 18l3 3 6.3-6.3a4 4 0 0 0 5.4-5.4l-2.6 2.6-2.4-.6-.6-2.4 2.6-2.6z" fill="none" stroke="currentColor" stroke-width="1.8" stroke-linejoin="round"/></svg>',
}

BOXES = {
 'brain':   ('brain',  'Brain Power'),
 'sharpen': ('pencil', 'Sharpen your pencil'),
 'watch':   ('warn',   'Watch it!'),
 'nodumb':  ('q',      'There are no Dumb Questions'),
 'industry':('chip',   'From the real world'),
 'relax':   ('coffee', 'Relax'),
 'magnets': ('magnet', 'Code Magnets'),
 'compiler':('bug',    'Be the Compiler'),
 'lab':     ('flask',  'Lab'),
 'bullets': ('list',   'Bullet Points'),
 'fireside':('fire',   'Fireside Chat'),
 'quiz':    ('q',      'Quick Check'),
 'project': ('build',  'Project Time'),
 'deep':    ('chip',   'Under the hood'),
}

# ------------------------------------------------------------------ code blocks
def render_code(lang, info, code, ctx):
    lang = lang or 'text'
    flags = info.split()
    if lang == 'flow':
        return render_flow(code)
    if lang == 'output':
        # [[typed input]] -> highlighted
        esc = html.escape(code)
        esc = re.sub(r'\[\[(.*?)\]\]', r'<span class="typed">\1</span>', esc)
        if 'shell' not in flags:
            pend = [c for c in ctx.code if c.get('run') and c.get('want') is None and 'random' not in c['flags']]
            if pend:
                pend[0]['want'] = code
        label = 'Output' if 'noterm' in flags else 'Terminal'
        return f'<figure class="term"><div class="term-bar"><span></span><span></span><span></span><b>{label}</b></div><pre>{esc}</pre></figure>'
    if lang == 'file':
        name = flags[0] if flags else 'file.txt'
        if 'seed' in flags:
            ctx.files[name] = code + '\n'
        if 'result' in flags:
            for c in reversed(ctx.code):
                if ('expectfile=' + name) in c['flags']:
                    c.setdefault('wantfiles', {})[name] = code
                    break
        return f'<figure class="txtfile"><figcaption>{html.escape(name)}</figcaption><pre>{html.escape(code)}</pre></figure>'
    # code with optional annotations  //@ note
    lines = code.split('\n')
    rows = []; anns = False
    for ln in lines:
        note = ''
        m = re.search(r'\s*//@\s?(.*)$', ln)
        if m:
            note = m.group(1); ln = ln[:m.start()]; anns = True
        rows.append((ln, note))
    if lang == 'cpp':
        plain = '\n'.join(r[0] for r in rows)
        rec = {'chapter': ctx.chapter, 'code': plain, 'flags': flags, 'run': 'run' in flags, 'want': None, 'files': dict(ctx.files)}
        ctx.code.append(rec)
        hl = hl_cpp(plain).split('\n')
    elif lang == 'pseudo':
        hl = hl_pseudo('\n'.join(r[0] for r in rows)).split('\n')
    else:
        hl = [html.escape(r[0]) for r in rows]
    # multi-line comments can break per-line spans; close/reopen spans per line
    hl = fix_spans(hl)
    title = ''
    for f in flags:
        if f.startswith('title='): title = f[6:]
    tag = {'cpp': 'C++', 'pseudo': 'Pseudocode', 'text': ''}.get(lang, lang)
    if 'error' in flags: tag = 'C++ (has a bug)'
    head = ''
    if title or tag:
        head = f'<div class="code-head"><span>{html.escape(title)}</span><em>{tag}</em></div>'
    body = []
    for (raw, note), h in zip(rows, hl):
        n = f'<span class="ann">{md_inline(note)}</span>' if note else '<span class="ann"></span>'
        body.append(f'<span class="cl"><code>{h if h else " "}</code>{n if anns else ""}</span>')
    cls = 'code' + (' annotated' if anns else '') + (' buggy' if 'error' in flags else '')
    return f'<figure class="{cls}">{head}<pre class="lang-{lang}">' + ''.join(body) + '</pre></figure>'

def fix_spans(lines):
    out = []; carry = ''
    for l in lines:
        l2 = carry + l
        opens = len(re.findall(r'<span[^>]*>', l2)); closes = l2.count('</span>')
        carry = ''
        if opens > closes:
            m = re.findall(r'<span[^>]*>', l2)
            carry = m[-1]
            l2 += '</span>'
        out.append(l2)
    return out

def render_flow(code):
    if os.environ.get('HB_NO_FLOW'):          # verification runs do not need diagrams
        return '<figure class="flow"></figure>'
    h = hashlib.md5(code.encode()).hexdigest()[:12]
    svgp = os.path.join(CACHE, h + '.svg')
    if not os.path.exists(svgp):
        mp = os.path.join(CACHE, h + '.mmd')
        open(mp, 'w').write(code)
        cfg = os.path.join(CACHE, 'mcfg.json')
        json.dump({"theme": "base", "flowchart": {"htmlLabels": False, "curve": "basis"},
                   "themeVariables": {"primaryColor": "#FFF4E5", "primaryBorderColor": "#111111",
                                      "primaryTextColor": "#111111", "lineColor": "#333333",
                                      "fontFamily": "Helvetica, Arial, sans-serif", "fontSize": "15px"}},
                  open(cfg, 'w'))
        subprocess.run(['mmdc', '-i', mp, '-o', svgp, '-c', cfg, '-b', 'white'], check=True,
                       stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=120)
    svg = open(svgp).read()
    svg = re.sub(r'<\?xml[^>]*>', '', svg)
    # make responsive
    svg = re.sub(r'(<svg[^>]*?)\sstyle="max-width:\s*([\d.]+)px;?"', r'\1 style="max-width:min(100%,\2px)"', svg, count=1)
    return f'<figure class="flow">{svg}</figure>'

def md_inline(s):
    h = MD.markdown(s)
    return re.sub(r'^<p>(.*)</p>$', r'\1', h.strip(), flags=re.S)

# ------------------------------------------------------------------ containers
def render_container(kind, arg, body, ctx):
    icon, label = BOXES.get(kind, ('q', kind.title()))
    title = arg.strip()
    sol_html = None; sol = None
    if '\n---solution\n' in '\n' + body + '\n':
        parts = re.split(r'^---solution\s*$', body, flags=re.M)
        body, sol = parts[0], parts[1]
    if kind == 'story':
        return render_story(body, ctx)
    if kind == 'quiz':
        inner = render_quiz(body, ctx)
    elif kind == 'magnets':
        inner = render_magnets(body, ctx, title)
    elif kind == 'nodumb':
        inner = render_nodumb(body, ctx)
    elif kind == 'fireside':
        inner = render_fireside(body, ctx, title)
    else:
        inner = render(body, ctx)
    if sol is not None:
        sol_html = render(sol, ctx)
    sol_part = ''
    if sol_html is not None:
        ctx.ex += 1
        lab = f'{ctx.chapter}.{ctx.ex}'
        if ctx.mode == 'web':
            sol_part = f'<details class="sol"><summary>Show the solution</summary><div class="sol-body">{sol_html}</div></details>'
        else:
            ctx.solutions.append((ctx.chapter, lab, f'{label}{": " + title if title and kind not in ("fireside",) else ""}', sol_html))
            sol_part = f'<p class="sol-ref">Solution: see Solutions at the back, exercise {lab}</p>'
        num = f'<span class="exnum">Exercise {lab}</span>'
    else:
        num = ''
    shown_title = '' if kind == 'fireside' else (f'<h4 class="box-title">{md_inline(title)}</h4>' if title else '')
    return (f'<aside class="box box-{kind}"><div class="box-label">{ICONS[icon]}<span>{label}</span>{num}</div>'
            f'{shown_title}<div class="box-body">{inner}</div>{sol_part}</aside>')

CAST = {
 'amaya': ('Amaya', 'A'), 'nuwan': ('Nuwan', 'N'), 'ruwan': ('Uncle Ruwan', 'R'),
 'you': ('You', 'Y'), 'compiler': ('The Compiler', 'g++'), 'dilshan': ('Dilshan', 'D'),
}
def render_story(body, ctx):
    out = []
    for para in re.split(r'\n\s*\n', body.strip()):
        m = re.match(r'^(\w+):\s*(.*)$', para.strip(), re.S)
        if m and m.group(1).lower() in CAST:
            k = m.group(1).lower(); name, ini = CAST[k]
            out.append(f'<div class="say say-{k}"><span class="avatar" aria-hidden="true">{ini}</span>'
                       f'<div class="bubble"><b>{name}</b>{md_inline(m.group(2).strip())}</div></div>')
        else:
            out.append(f'<p class="scene">{md_inline(para.strip())}</p>')
    return '<div class="story">' + ''.join(out) + '</div>'

def render_nodumb(body, ctx):
    out = []
    for qa in re.split(r'^Q:\s*', body.strip(), flags=re.M):
        if not qa.strip(): continue
        q, _, a = qa.partition('\nA:')
        out.append(f'<div class="qa"><p class="q"><b>Q:</b> {md_inline(q.strip())}</p><div class="a"><b>A:</b> {render(a.strip(), ctx)}</div></div>')
    return ''.join(out)

def render_fireside(body, ctx, title):
    # title: "while loop|do-while loop"
    names = [t.strip() for t in title.split('|')]
    out = [f'<p class="fs-topic">Tonight\'s talk: <b>{html.escape(names[0])}</b> and <b>{html.escape(names[1])}</b> settle an argument.</p><div class="fs">']
    for para in re.split(r'\n\s*\n', body.strip()):
        m = re.match(r'^([12]):\s*(.*)$', para.strip(), re.S)
        if not m: continue
        i = int(m.group(1)) - 1
        out.append(f'<div class="fs-line fs-{i+1}"><b>{html.escape(names[i])}:</b> {md_inline(m.group(2).strip())}</div>')
    out.append('</div>')
    return ''.join(out)

def render_quiz(body, ctx):
    qs = [q for q in re.split(r'^\?\s*', body.strip(), flags=re.M) if q.strip()]
    out = []
    answers = []
    for qi, q in enumerate(qs, 1):
        lines = q.strip().split('\n')
        stem = []; opts = []; expl = []
        for l in lines:
            if re.match(r'^[-*]\s', l): opts.append((l[0] == '*', l[2:].strip()))
            elif l.startswith('>'): expl.append(l[1:].strip())
            elif not opts: stem.append(l)
        stem_html = render('\n'.join(stem), ctx)
        ex = md_inline(' '.join(expl))
        qid = ctx.next_id('q')
        if ctx.mode == 'web':
            btns = ''.join(f'<button type="button" class="opt" data-ok="{1 if ok else 0}">{md_inline(t)}</button>' for ok, t in opts)
            out.append(f'<div class="qz" id="{qid}"><div class="qz-stem"><span class="qn">{qi}</span>{stem_html}</div><div class="opts">{btns}</div><p class="qz-ex" hidden>{ex}</p></div>')
        else:
            items = ''.join(f'<li>{md_inline(t)}</li>' for ok, t in opts)
            out.append(f'<div class="qz"><div class="qz-stem"><span class="qn">{qi}</span>{stem_html}</div><ol class="opts-p" type="a">{items}</ol></div>')
            ok = [i for i, (o, _) in enumerate(opts) if o][0]
            answers.append(f'<p><b>{qi}. ({"abcdef"[ok]})</b> {md_inline(opts[ok][1])}. {ex}</p>')
    if ctx.mode == 'pdf':
        ctx.ex += 1
        lab = f'{ctx.chapter}.{ctx.ex}'
        ctx.solutions.append((ctx.chapter, lab, 'Quick Check answers', ''.join(answers)))
        out.append(f'<p class="sol-ref">Answers: see Solutions at the back, exercise {lab}</p>')
    return ''.join(out)

def render_magnets(body, ctx, title):
    # body: optional intro text, then a ```magnets fence-like list after line "~~~"
    intro, _, code = body.partition('~~~\n')
    code = code.rsplit('~~~', 1)[0]
    lines = [l for l in code.split('\n') if l.strip()]
    rnd = random.Random(hashlib.md5(code.encode()).hexdigest())
    order = list(range(len(lines)))
    while True:
        rnd.shuffle(order)
        if order != sorted(order) or len(order) < 2: break
    intro_html = render(intro, ctx)
    if ctx.mode == 'web':
        mags = ''.join(f'<button type="button" class="mag" data-i="{i}"><code>{hl_cpp(lines[i].strip())}</code></button>' for i in order)
        sol = '<pre class="mag-sol" hidden>' + '\n'.join(html.escape(l) for l in lines) + '</pre>'
        return (f'{intro_html}<div class="magnets" data-n="{len(lines)}"><div class="mag-pool">{mags}</div>'
                f'<div class="mag-board" aria-live="polite"><p class="mag-hint">Click the magnets in the right order to build the program here.</p></div>'
                f'<div class="mag-ctl"><button type="button" class="btn mag-check">Check my order</button><button type="button" class="btn ghost mag-reset">Start again</button><button type="button" class="btn ghost mag-show">Show answer</button></div><p class="mag-msg" role="status"></p>{sol}</div>')
    mags = ''.join(f'<span class="mag"><code>{hl_cpp(lines[i].strip())}</code></span>' for i in order)
    ctx.ex += 1
    lab = f'{ctx.chapter}.{ctx.ex}'
    solh = render_code('cpp', 'nocheck', '\n'.join(lines), ctx)
    ctx.code.pop()  # avoid double verification; verified via src run elsewhere
    ctx.solutions.append((ctx.chapter, lab, 'Code Magnets', solh))
    return f'{intro_html}<div class="magnets-p">{mags}</div><p class="sol-ref">Solution: see Solutions at the back, exercise {lab}</p>'

# ------------------------------------------------------------------ main renderer
def render(text, ctx):
    lines = text.split('\n')
    out = []; i = 0
    while i < len(lines):
        l = lines[i]
        m = re.match(r'^```(\w*)\s*(.*)$', l)
        if m:
            lang, info = m.group(1), m.group(2)
            j = i + 1; buf = []
            while j < len(lines) and not lines[j].startswith('```'):
                buf.append(lines[j]); j += 1
            out.append('\n' + ctx.key(render_code(lang, info, '\n'.join(buf), ctx)) + '\n')
            i = j + 1; continue
        m = re.match(r'^:::(\w+)\s*(.*)$', l)
        if m:
            kind, arg = m.group(1), m.group(2)
            j = i + 1; buf = []; infence = False
            while j < len(lines):
                if lines[j].startswith('```'): infence = not infence
                if not infence and lines[j].strip() == ':::': break
                buf.append(lines[j]); j += 1
            out.append('\n' + ctx.key(render_container(kind, arg, '\n'.join(buf), ctx)) + '\n')
            i = j + 1; continue
        m = re.match(r'^(#{2,4})\s+(.*)$', l)
        if m and ctx.chapter is not None:
            lvl = len(m.group(1)); t = m.group(2)
            if lvl == 2:
                ctx.sec += 1
                hid = f'ch{ctx.chapter}-{ctx.sec}'
                ctx.toc[-1][3].append((hid, t))
                sn = f'<span class="secnum">{ctx.chapter}.{ctx.sec}</span>' if ctx.chapter else ''
                out.append('\n' + ctx.key(f'<h2 id="{hid}">{sn}{md_inline(t)}</h2>') + '\n')
            else:
                out.append('\n' + ctx.key(f'<h{lvl}>{md_inline(t)}</h{lvl}>') + '\n')
            i += 1; continue
        out.append(l); i += 1
    h = MD.markdown('\n'.join(out), extensions=['tables', 'sane_lists'])
    h = h.replace('<table>', '<div class="tablewrap"><table>').replace('</table>', '</table></div>')
    # substitute placeholders (possibly nested)
    for _ in range(4):
        h = re.sub(r'<p>(XBLKX\d+XBLKX)</p>', lambda mm: ctx.blk[mm.group(1)], h)
        h = re.sub(r'XBLKX\d+XBLKX', lambda mm: ctx.blk[mm.group(0)], h)
    return h

def parse_front(txt):
    m = re.match(r'^---\n(.*?)\n---\n', txt, re.S)
    meta = {}
    for l in m.group(1).split('\n'):
        k, _, v = l.partition(':'); meta[k.strip()] = v.strip()
    return meta, txt[m.end():]

def chapter_opener(num, meta, ctx):
    learn = meta.get('learn', '')
    items = ''.join(f'<li>{md_inline(x.strip())}</li>' for x in learn.split(';') if x.strip())
    kind = meta.get('kind', 'chapter')
    label = {'chapter': 'Chapter', 'appendix': 'Appendix'}.get(kind, '')
    numhtml = f'<div class="op-num"><span>{label}</span><b>{num}</b></div>' if num else ''
    mk = f'<span class="marker">@@MARK{ctx.cur_id}@@</span>' if ctx.mode == 'pdf' else ''
    return (f'<header class="opener">{mk}{numhtml}'
            f'<h1>{md_inline(meta["title"])}</h1><p class="tagline">{md_inline(meta.get("tagline", ""))}</p>'
            + (f'<div class="op-learn"><h4>In this chapter you will</h4><ul>{items}</ul></div>' if items else '')
            + '<svg class="op-circuit" viewBox="0 0 600 70" aria-hidden="true"><path d="M0 35H180l20-20h120l20 20h260" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="200" cy="15" r="7" fill="var(--bg)" stroke="currentColor" stroke-width="3"/><circle cx="320" cy="15" r="7" fill="var(--bg)" stroke="currentColor" stroke-width="3"/><path d="M380 35v22h80" fill="none" stroke="currentColor" stroke-width="3"/><circle cx="470" cy="57" r="7" fill="var(--bg)" stroke="currentColor" stroke-width="3"/><rect x="560" y="22" width="40" height="26" fill="var(--accent)"/></svg>'
            + '</header>')

def build(mode):
    ctx = Ctx(mode)
    files = sorted(glob.glob(os.path.join(SRC, '*.md')) + glob.glob(os.path.join(SRC, '*.md.in')))
    chapters = []
    for f in files:
        text = open(f).read()
        if f.endswith('.md.in'):               # {{FILE:name}} pulls in a capstone source file
            text = re.sub(r'\{\{FILE:([\w.]+)\}\}',
                          lambda m: open(os.path.join(CAPSTONE, m.group(1))).read().rstrip('\n'), text)
        meta, body = parse_front(text)
        num = meta.get('num', '')
        ctx.cur_id = len(chapters)
        ctx.chapter = num; ctx.sec = 0; ctx.ex = 0; ctx.files = {}
        ctx.toc.append((num, meta['title'], meta.get('tagline', ''), [], meta.get('kind', 'chapter'), meta))
        h = render(body, ctx)
        chapters.append((num, meta, chapter_opener(num, meta, ctx) + h))
    return ctx, chapters

if __name__ == '__main__':
    mode = sys.argv[1] if len(sys.argv) > 1 else 'web'
    import assemble
    ctx, chapters = build('pdf' if mode == 'pdf' else 'web')
    if mode == 'verify':
        json.dump(ctx.code, open(os.path.join(BUILD, 'code.json'), 'w'), indent=1)
        print(len(ctx.code), 'code blocks')
    else:
        assemble.write(mode, ctx, chapters)
