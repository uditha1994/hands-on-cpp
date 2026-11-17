import os, re, html, base64, json, subprocess
from build import ROOT, REPO, BUILD, AUTHOR, BOOK, SUB, LOGO, b64, md_inline, hl_cpp

FONTDIR = os.path.join(REPO, 'node_modules', '@fontsource')
FONTS = [
 ('Lexend', 'lexend/files/lexend-latin-{w}-normal.woff2', [400, 500, 600, 700, 800, 900], 'normal'),
 ('Source Sans 3', 'source-sans-3/files/source-sans-3-latin-{w}-normal.woff2', [400, 600, 700], 'normal'),
 ('Source Sans 3', 'source-sans-3/files/source-sans-3-latin-{w}-italic.woff2', [400], 'italic'),
 ('Caveat', 'caveat/files/caveat-latin-{w}-normal.woff2', [400, 600, 700], 'normal'),
 ('JetBrains Mono', 'jetbrains-mono/files/jetbrains-mono-latin-{w}-normal.woff2', [400, 600], 'normal'),
]
def fontface():
    out = []
    for fam, pat, ws, style in FONTS:
        for w in ws:
            p = os.path.join(FONTDIR, pat.format(w=w))
            out.append(f"@font-face{{font-family:'{fam}';font-style:{style};font-weight:{w};font-display:swap;"
                       f"src:url(data:font/woff2;base64,{b64(p)}) format('woff2')}}")
    return '\n'.join(out)

def logo_small():
    p = os.path.join(BUILD, 'logo_small.png')
    if not os.path.exists(p):
        from PIL import Image
        im = Image.open(LOGO); im.thumbnail((300, 300)); im.save(p, optimize=True)
    return b64(p)

def slug(num, meta, i):
    k = meta.get('kind', 'chapter')
    if k == 'chapter': return f'ch{num}'
    if k == 'appendix': return f'app{num}'
    return meta.get('slug', f'part{i}')

COVER_CODE = '''#include <iostream>
#include <string>
using namespace std;

int main() {
    string name;
    cout << "What's your name? ";
    getline(cin, name);
    cout << "Hello, " << name << "! Let's learn C++.";
    return 0;
}'''

JS = r'''
(function(){
const $=(s,r=document)=>r.querySelector(s), $$=(s,r=document)=>Array.from(r.querySelectorAll(s));
const store={get(k,d){try{const v=localStorage.getItem(k);return v===null?d:JSON.parse(v)}catch(e){return d}},
             set(k,v){try{localStorage.setItem(k,JSON.stringify(v))}catch(e){}}};
// theme
const root=document.documentElement;
const th=store.get('hb-theme',null); if(th) root.setAttribute('data-theme',th);
const tbtn=$('#themeBtn');
function themeLabel(){const t=root.getAttribute('data-theme'); const dark=t? t==='dark' : matchMedia('(prefers-color-scheme: dark)').matches; tbtn.textContent=dark?'Light':'Dark';}
tbtn.addEventListener('click',()=>{const t=root.getAttribute('data-theme'); const dark=t? t==='dark' : matchMedia('(prefers-color-scheme: dark)').matches; const n=dark?'light':'dark'; root.setAttribute('data-theme',n); store.set('hb-theme',n); themeLabel();});
themeLabel();
// sidebar
const side=$('#side'); let scrim=null;
function closeSide(){side.classList.remove('open'); if(scrim){scrim.remove(); scrim=null;}}
$('#menuBtn').addEventListener('click',()=>{side.classList.add('open'); scrim=document.createElement('div'); scrim.className='scrim'; scrim.addEventListener('click',closeSide); document.body.appendChild(scrim);});
// routing
const arts=$$('article.chapter'); const cover=$('#cover');
function show(h){
  let art=arts.find(a=>a.dataset.slug===h), target=null;
  if(!art && h){ target=document.getElementById(h); if(target) art=target.closest('article.chapter'); }
  const start=!art;
  if(start) art=arts[0];
  arts.forEach(a=>a.hidden=(a!==art));
  cover.hidden=!start;
  $$('.toc a').forEach(a=>a.classList.toggle('on',a.dataset.slug===art.dataset.slug));
  closeSide();
  if(target) target.scrollIntoView(); else if(!start) window.scrollTo(0,0);
}
window.addEventListener('hashchange',()=>show(location.hash.slice(1)));
show(location.hash.slice(1));
// progress
const total=arts.filter(a=>a.dataset.track==='1').length;
function prog(){const d=store.get('hb-done',[]); $$('.toc a').forEach(a=>a.classList.toggle('done',d.includes(a.dataset.slug)));
  const n=arts.filter(a=>a.dataset.track==='1'&&d.includes(a.dataset.slug)).length;
  $('#progBar').style.width=(100*n/total)+'%'; $('#progTxt').textContent=n+' of '+total+' chapters done';
  $$('.done-btn').forEach(b=>{const on=d.includes(b.dataset.slug); b.classList.toggle('isdone',on); b.textContent=on?'Done! (click to undo)':'Mark this chapter as done';});}
$$('.done-btn').forEach(b=>b.addEventListener('click',()=>{let d=store.get('hb-done',[]); const s=b.dataset.slug; d=d.includes(s)?d.filter(x=>x!==s):d.concat([s]); store.set('hb-done',d); prog();}));
prog();
// quizzes
$$('.qz').forEach(q=>{ $$('.opt',q).forEach(o=>o.addEventListener('click',()=>{
   $$('.opt',q).forEach(x=>{x.disabled=true; if(x.dataset.ok==='1') x.classList.add('right');});
   if(o.dataset.ok!=='1') o.classList.add('wrong');
   const ex=$('.qz-ex',q); if(ex){ ex.hidden=false; ex.insertAdjacentHTML('afterbegin', o.dataset.ok==='1'?'<b>Correct. </b>':'<b>Not quite. </b>'); }
   const box=q.closest('.box'); if(box){ const all=$$('.qz',box); const doneQ=all.filter(z=>$('.opt[disabled]',z)); if(doneQ.length===all.length){ const sc=all.filter(z=>!$('.opt.wrong',z)).length; let s=$('.qz-score',box); if(!s){s=document.createElement('p'); s.className='mag-msg qz-score'; box.appendChild(s);} s.textContent='You scored '+sc+' out of '+all.length+'.'; } }
 }));});
// magnets
$$('.magnets').forEach(m=>{
  const pool=$('.mag-pool',m), board=$('.mag-board',m), msg=$('.mag-msg',m), sol=$('.mag-sol',m);
  const want=sol.textContent.split('\n').map(s=>s.trim());
  const orig=$$('.mag',pool);
  function hint(){ $('.mag-hint',board).hidden = $$('.mag',board).length>0; }
  m.addEventListener('click',e=>{const b=e.target.closest('.mag'); if(!b) return; (b.parentElement===pool?board:pool).appendChild(b); msg.textContent=''; hint();});
  $('.mag-reset',m).addEventListener('click',()=>{orig.forEach(b=>pool.appendChild(b)); msg.textContent=''; hint();});
  $('.mag-show',m).addEventListener('click',()=>{sol.hidden=!sol.hidden;});
  $('.mag-check',m).addEventListener('click',()=>{const got=$$('.mag',board).map(b=>b.textContent.trim());
     if(got.length<want.length){msg.className='mag-msg no'; msg.textContent='You still have '+(want.length-got.length)+' magnet(s) left in the pile.'; return;}
     const ok=got.every((g,i)=>g===want[i]); msg.className='mag-msg '+(ok?'ok':'no'); msg.textContent= ok?'It compiles! Every magnet is in the right place.':'Not yet. Something is out of order. Read it like the compiler would, top to bottom.';});
});
// cover IDE
const run=$('#runBtn'), out=$('#ideOut'), nm=$('#coverName');
function esc(s){return s.replace(/[&<>]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;'}[c]));}
function go(){ const name=nm.value; run.disabled=true; const lines=['<span class="dim">$ g++ hello.cpp -o hello</span>','<span class="dim">$ ./hello</span>',"What's your name? "+esc(name),'Hello, '+esc(name)+"! Let's learn C++."];
  if(!name) lines.push('<span class="dim">// You pressed Run with an empty box, so name holds an empty string.</span>');
  out.innerHTML=''; let i=0; const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
  (function step(){ if(i<lines.length){ out.innerHTML+=(i?'\n':'')+lines[i++]; setTimeout(step, reduce?0:380);} else run.disabled=false; })(); }
run.addEventListener('click',go); nm.addEventListener('keydown',e=>{if(e.key==='Enter'){e.preventDefault(); go();}});
// cover circuits
const cv=$('#circuit'), ctx=cv.getContext('2d'); let W,H,paths=[],pulses=[];
function rnd(a,b){return a+Math.random()*(b-a)}
function build(){ const dpr=window.devicePixelRatio||1; W=cv.clientWidth; H=cv.clientHeight; cv.width=W*dpr; cv.height=H*dpr; ctx.setTransform(dpr,0,0,dpr,0,0); paths=[];
  const n=Math.max(8,Math.floor(W/70));
  for(let k=0;k<n;k++){ let x=rnd(0,W), y=-5, pts=[[x,y]]; let len=rnd(H*.25,H*.85);
    y=rnd(H*.1,len*.5); pts.push([x,y]); const dx=rnd(-60,60); x+=dx; y+=Math.abs(dx); pts.push([x,y]); y=len; pts.push([x,y]); paths.push(pts); }
  pulses=paths.map((p,i)=>({p:i,t:Math.random()})); }
function seglen(p){let L=0; for(let i=1;i<p.length;i++) L+=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]); return L;}
function at(p,t){let L=seglen(p)*t; for(let i=1;i<p.length;i++){const s=Math.hypot(p[i][0]-p[i-1][0],p[i][1]-p[i-1][1]); if(L<=s){const r=L/s; return [p[i-1][0]+(p[i][0]-p[i-1][0])*r,p[i-1][1]+(p[i][1]-p[i-1][1])*r];} L-=s;} return p[p.length-1];}
function draw(){ ctx.clearRect(0,0,W,H); ctx.lineWidth=2; ctx.strokeStyle='rgba(255,255,255,.09)';
  paths.forEach(p=>{ctx.beginPath(); ctx.moveTo(p[0][0],p[0][1]); p.slice(1).forEach(q=>ctx.lineTo(q[0],q[1])); ctx.stroke(); const e=p[p.length-1]; ctx.beginPath(); ctx.arc(e[0],e[1],6,0,7); ctx.stroke();});
  pulses.forEach(u=>{const q=at(paths[u.p],u.t); ctx.fillStyle='rgba(247,147,30,.9)'; ctx.beginPath(); ctx.arc(q[0],q[1],3,0,7); ctx.fill();}); }
let last=0; const reduce=matchMedia('(prefers-reduced-motion: reduce)').matches;
function loop(ts){ if(!cover.hidden){ const dt=Math.min(50,ts-last); pulses.forEach(u=>{u.t+=dt/6000; if(u.t>1) u.t=0;}); draw(); } last=ts; requestAnimationFrame(loop); }
build(); draw(); if(!reduce) requestAnimationFrame(loop);
window.addEventListener('resize',()=>{build(); draw();});
})();
'''

def web(ctx, chapters):
    css = open(os.path.join(ROOT, 'style.css')).read()
    logo = b64(LOGO)
    toc = []
    arts = []
    n = len(chapters)
    slugs = [slug(num, meta, i) for i, (num, meta, h) in enumerate(chapters)]
    for i, (num, meta, h) in enumerate(chapters):
        s = slugs[i]
        kind = meta.get('kind', 'chapter')
        nlabel = num if num else ''
        toc.append(f'<li><a href="#{s}" data-slug="{s}"><span class="n">{nlabel}</span><span>{md_inline(meta["title"])}</span><span class="ck" aria-label="done">&#10003;</span></a></li>')
        secs = ctx.toc[i][3]
        sub = '<ul class="subtoc">' + ''.join(f'<li><a href="#{sid}">{md_inline(t)}</a></li>' for sid, t in secs) + '</ul>' if secs else ''
        prev = f'<a class="btn ghost" href="#{slugs[i-1]}">Previous</a>' if i > 0 else '<span></span>'
        nxt = f'<a class="btn" href="#{slugs[i+1]}">Next: {md_inline(chapters[i+1][1]["title"])}</a>' if i < n - 1 else '<span></span>'
        track = '1' if kind == 'chapter' else '0'
        donebtn = f'<button type="button" class="btn ghost done-btn" data-slug="{s}">Mark this chapter as done</button>' if track == '1' else ''
        # insert subtoc after opener
        h2 = h.replace('</header>', '</header>' + sub, 1)
        arts.append(f'<article class="chapter" data-slug="{s}" data-track="{track}" hidden>{h2}'
                    f'<nav class="chap-foot" aria-label="Chapter navigation">{prev}{donebtn}{nxt}</nav></article>')
    groups = []
    # group toc
    front = [t for t, (num, meta, h) in zip(toc, chapters) if meta.get('kind') == 'front']
    chs = [t for t, (num, meta, h) in zip(toc, chapters) if meta.get('kind', 'chapter') == 'chapter']
    apps = [t for t, (num, meta, h) in zip(toc, chapters) if meta.get('kind') == 'appendix']
    side = (f'<h5>Your progress</h5><div class="prog"><i id="progBar"></i></div><p class="prog-t" id="progTxt"></p>'
            f'<h5>Start here</h5><ul class="toc">{"".join(front)}</ul><h5>Chapters</h5><ul class="toc">{"".join(chs)}</ul>'
            + (f'<h5>Appendices</h5><ul class="toc">{"".join(apps)}</ul>' if apps else ''))
    cover = f'''<section class="cover" id="cover"><canvas id="circuit" aria-hidden="true"></canvas><div class="cover-in">
<div><p class="kicker">A brain-friendly handbook</p><h1>Hands-On <em>C++</em></h1>
<p class="sub">{SUB}. Written for beginners, and it keeps going until you can build real console applications on your own.</p>
<div class="cta"><a class="btn" href="#{slugs[0]}">Start reading</a><a class="btn ghost" href="#ch1">Jump to Chapter 1</a></div>
<div class="by"><img src="data:image/png;base64,{logo}" alt="Uditha Landekumbura logo"><div><b>{AUTHOR}</b><span>Author</span></div></div></div>
<div class="ide" role="group" aria-label="Try a C++ program"><div class="ide-bar"><i></i><i></i><i></i><span>hello.cpp</span></div>
<pre>{fix(hl_cpp(COVER_CODE))}</pre>
<div class="ide-in"><label for="coverName">Your program is waiting for input. Type your name and press Run.</label><input id="coverName" type="text" autocomplete="off" placeholder="Type your name" maxlength="40"><button type="button" id="runBtn">Run</button></div>
<div class="ide-out" id="ideOut" aria-live="polite"><span class="dim">Output appears here.</span></div></div>
</div></section>'''
    page = f'''<title>Hands-On C++</title>
<meta name="claude:viewport-fit-sides" content="cover">
<style>{fontface()}
{css}</style>
<header class="topbar"><button type="button" class="iconbtn menu-btn" id="menuBtn" aria-label="Open contents">Contents</button>
<a class="brand" href="#cover"><img class="logo-plate" src="data:image/png;base64,{logo}" alt=""><span>Hands-On C++</span></a><span class="sp"></span>
<button type="button" class="iconbtn" id="themeBtn">Dark mode</button></header>
{cover}
<div class="shell"><nav class="side" id="side" aria-label="Contents">{side}</nav>
<main class="main"><div class="page">{"".join(arts)}</div></main></div>
<footer class="sitefoot"><img class="logo-plate" src="data:image/png;base64,{logo}" alt="Uditha Landekumbura logo"><span>Hands-On C++ by {AUTHOR}. Share it with your classmates.</span></footer>
<script>{JS}</script>'''
    os.makedirs(os.path.join(REPO, 'dist'), exist_ok=True)
    p = os.path.join(REPO, 'dist', 'Hands-On_Cpp_Handbook.html')
    open(p, 'w').write(page)
    print('web ->', p, os.path.getsize(p) // 1024, 'KB')

def fix(h):
    return h

# ---------------------------------------------------------------- PDF
COVER_PDF = '''<!doctype html><html class="pdf"><head><meta charset="utf-8"><style>{ff}
@page{{size:A4; margin:0}}
html,body{{margin:0; padding:0}}
body{{width:210mm; height:297mm; position:relative; overflow:hidden; background:#FFFFFF; font-family:'Source Sans 3',sans-serif; color:#111}}
.top{{position:absolute; left:18mm; right:18mm; top:18mm; display:flex; justify-content:space-between; font-family:'Lexend'; font-size:9pt; letter-spacing:.2em; text-transform:uppercase; color:#555}}
.logo{{position:absolute; left:18mm; top:38mm; width:62mm}}
.title{{position:absolute; left:18mm; right:18mm; top:112mm}}
.k{{font-family:'Caveat'; font-size:26pt; color:#B35A00; margin:0}}
h1{{font-family:'Lexend'; font-weight:900; font-size:66pt; line-height:.95; margin:2mm 0 5mm; letter-spacing:-1.5pt}}
h1 em{{font-style:normal; color:#F7931E}}
.sub{{font-size:14pt; line-height:1.4; max-width:150mm; color:#333; margin:0}}
.code{{position:absolute; right:18mm; top:40mm; width:96mm; background:#111; color:#EEE; border-radius:4mm; padding:5mm 6mm; font-family:'JetBrains Mono'; font-size:8.6pt; line-height:1.55; transform:rotate(2.5deg); box-shadow:0 3mm 8mm rgba(0,0,0,.25)}}
.code .c-kw{{color:#FFA94D}}.code .c-ty{{color:#7CC7FF}}.code .c-str{{color:#A6E3A1}}.code .c-pre{{color:#CBA6F7}}.code .c-lib{{color:#F9E2AF}}.code .c-num{{color:#F5C2E7}}
.code pre{{margin:0; white-space:pre}}
.note{{position:absolute; right:22mm; top:112mm; font-family:'Caveat'; font-size:17pt; color:#B35A00; transform:rotate(-4deg)}}
.feat{{position:absolute; left:18mm; right:18mm; top:192mm; display:grid; grid-template-columns:repeat(3,1fr); gap:5mm}}
.feat div{{border:1.6pt solid #111; border-radius:3mm; padding:4mm}}
.feat b{{font-family:'Lexend'; display:block; font-size:11pt; margin-bottom:1mm}}
.feat span{{font-size:9.5pt; color:#444; line-height:1.35; display:block}}
.band{{position:absolute; left:0; right:0; bottom:0; height:62mm; background:#111; color:#fff}}
.band svg{{position:absolute; left:0; top:0; width:100%; height:100%}}
.by{{position:absolute; left:18mm; bottom:16mm; font-family:'Lexend'}}
.by small{{display:block; font-size:9pt; letter-spacing:.2em; text-transform:uppercase; color:#AAA; margin-bottom:2mm}}
.by b{{font-size:22pt; font-weight:700}}
.by b i{{font-style:normal; color:#F7931E}}
.ed{{position:absolute; right:18mm; bottom:18mm; font-family:'Lexend'; font-size:9pt; color:#AAA; text-align:right; letter-spacing:.1em; text-transform:uppercase}}
</style></head><body>
<div class="top"><span>Programming Fundamentals</span><span>C++17</span></div>
<img class="logo" src="data:image/png;base64,{logo}">
<div class="code"><pre>{code}</pre></div>
<div class="title"><p class="k">A brain-friendly handbook</p><h1>Hands-On<br><em>C++</em></h1>
<p class="sub">{sub}.</p></div>
<div class="feat"><div><b>Learn by doing</b><span>Nearly 200 tested code examples to type, run and break.</span></div>
<div><b>Think, then check</b><span>Puzzles, code magnets, quizzes and labs in every chapter.</span></div>
<div><b>Zero to projects</b><span>From your first cout to a complete shop management system.</span></div></div>
<div class="band"><svg viewBox="0 0 210 62" preserveAspectRatio="none"><g fill="none" stroke="#3A3A3F" stroke-width=".6">
<path d="M120 0v14l8 8h40l6 6v34"/><path d="M150 0v8l6 6h40v48"/><path d="M135 62V40l-6-6H98"/><circle cx="96" cy="34" r="2"/><path d="M190 0v4"/></g>
<rect x="168" y="44" width="42" height="18" fill="#F7931E"/><path d="M168 62 186 44h24v18z" fill="#F7931E"/></svg>
<div class="by"><small>Written by</small><b>Uditha <i>L</i>andekumbura</b></div><div class="ed">First edition</div></div>
</body></html>'''

def pdf(ctx, chapters):
    css = open(os.path.join(ROOT, 'style.css')).read()
    ff = fontface()
    logo = b64(LOGO)
    # cover
    cov = COVER_PDF.format(ff=ff, logo=logo, code=hl_cpp(COVER_CODE), sub=SUB)
    open(os.path.join(BUILD, 'cover.html'), 'w').write(cov)
    pages = json.load(open(os.path.join(BUILD, 'pages.json'))) if os.path.exists(os.path.join(BUILD, 'pages.json')) else {}
    def pg(key): return str(pages.get(key, '00'))
    # contents
    rows = []
    for i, (num, meta, h) in enumerate(chapters):
        kind = meta.get('kind', 'chapter')
        rows.append(f'<li><span class="n">{num}</span><span class="t">{md_inline(meta["title"])}</span><span class="tg"></span><span class="pg">{pg(f"MARK{i}")}</span></li>')
        if kind == 'chapter':
            for sid, t in ctx.toc[i][3]:
                rows.append(f'<li class="sub"><span class="t">{md_inline(t)}</span><span class="pg">{pg("S" + sid)}</span></li>')
    rows.append(f'<li><span class="n"></span><span class="t">Solutions to the exercises</span><span class="tg"></span><span class="pg">{pg("MARKSOL")}</span></li>')
    contents = f'<section class="frontpage" style="break-before:auto"><h1 style="font-size:26pt;margin:0 0 .4cm">Contents</h1><ul class="toc-p">{"".join(rows)}</ul></section>'
    body = []
    for i, (num, meta, h) in enumerate(chapters):
        # section markers for page lookup
        h = re.sub(r'<h2 id="([^"]+)">', lambda m: f'<h2 id="{m.group(1)}"><span class="marker">@@S{m.group(1)}@@</span>', h)
        body.append(f'<section class="chapter">{h}</section>')
    # solutions appendix
    sol = ['<section class="chapter"><header class="opener"><span class="marker">@@MARKSOL@@</span><h1>Solutions to the exercises</h1><p class="tagline">No peeking until you have tried!</p></header>']
    lastch = None
    for ch, lab, title, sh in ctx.solutions:
        if ch != lastch:
            chmeta = next(m for n_, m, _ in chapters if n_ == ch)
            sol.append(f'<h2>{"Chapter " + ch if ch.isdigit() else "Appendix " + ch}: {md_inline(chmeta["title"])}</h2>')
            lastch = ch
        sol.append(f'<div class="appx-sol"><h4>Exercise {lab} &middot; {md_inline(title)}</h4>{sh}</div>')
    sol.append('</section>')
    doc = (f'<!doctype html><html class="pdf"><head><meta charset="utf-8"><title>Hands-On C++</title><style>{ff}\n{css}\n'
           '@page{size:A4; margin:16mm 17mm 20mm 17mm}\n.marker{font-size:1px;color:transparent;position:static}</style></head><body>'
           f'{contents}{"".join(body)}{"".join(sol)}</body></html>')
    open(os.path.join(BUILD, 'body.html'), 'w').write(doc)
    # footer
    ls = logo_small()
    foot = (f'<div style="width:100%;padding:0 17mm;font-family:Helvetica,Arial,sans-serif;font-size:7.5pt;color:#555;display:flex;align-items:center;justify-content:space-between;-webkit-print-color-adjust:exact">'
            f'<span style="display:flex;align-items:center;gap:6px"><img src="data:image/png;base64,{ls}" style="height:20px;width:auto"><b style="color:#111;font-size:8pt">Uditha Landekumbura</b></span>'
            f'<span>Hands-On C++ &nbsp;<b style="display:inline-block;min-width:22px;text-align:center;background:#F7931E;color:#111;padding:2px 5px;border-radius:3px"><span class="pageNumber"></span></b></span></div>')
    open(os.path.join(BUILD, 'footer.html'), 'w').write(foot)
    print('pdf html written')

def write(mode, ctx, chapters):
    if mode == 'web': web(ctx, chapters)
    else: pdf(ctx, chapters)
