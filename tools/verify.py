#!/usr/bin/env python3
"""Compile and run every C++ block collected by `build.py verify`.

Usage: python3 tools/verify.py [chapter]
"""
import json, os, re, subprocess, sys, tempfile, shutil
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))   # repository root
code = json.load(open(os.path.join(ROOT, 'build', 'code.json')))
W = os.path.join(ROOT, 'build', 'verify'); os.makedirs(W, exist_ok=True)
HDR = ('#include <iostream>\n#include <iomanip>\n#include <string>\n#include <cmath>\n#include <vector>\n'
       '#include <fstream>\n#include <sstream>\n#include <algorithm>\n#include <array>\n#include <cctype>\n#include <random>\n#include <climits>\n#include <limits>\nusing namespace std;\n')
only = sys.argv[1] if len(sys.argv) > 1 else None
groups = {}
fails = 0; stats = {'compiled': 0, 'ran': 0, 'skipped': 0, 'expected_error': 0}
for n, c in enumerate(code):
    if only and str(c['chapter']) != only: continue
    fl = c['flags']; src = c['code']
    if 'nocheck' in fl: stats['skipped'] += 1; continue
    grp = [f[6:] for f in fl if f.startswith('group=')]
    if grp:
        fname = [f[5:] for f in fl if f.startswith('file=')][0]
        groups.setdefault(grp[0], []).append((fname, c, n))
        continue
    full = re.search(r'\bint\s+main\s*\(', src) is not None
    if 'check' in fl: src = HDR + 'int main() {\n' + src + '\nreturn 0;\n}\n'
    elif 'fn' in fl: src = HDR + src + '\nint main() { return 0; }\n'
    elif not full: stats['skipped'] += 1; continue
    files = {}
    # multi-file support: flags file=name ; group=name compile together
    p = os.path.join(W, f'b{n}.cpp'); open(p, 'w').write(src)
    exe = os.path.join(W, f'b{n}')
    extra = ['-Wno-unused-variable', '-Wno-unused-but-set-variable'] if ('check' in fl or 'fn' in fl) else []
    r = subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', *extra, '-o', exe, p], capture_output=True, text=True)
    where = f"[ch {c['chapter']} block {n}]"
    if 'error' in fl:
        if r.returncode == 0 and 'warnerror' not in fl:
            # buggy programs may compile (logic bugs) - fine unless marked compileerror
            if 'compileerror' in fl:
                print(where, 'EXPECTED compile error but compiled'); fails += 1
        stats['expected_error'] += 1
        continue
    if r.returncode != 0:
        print(where, 'COMPILE FAIL\n', r.stderr[:1500], '\n', c['code'][:400]); fails += 1; continue
    if r.stderr.strip() and 'nowarn' not in fl:
        print(where, 'WARNING:', r.stderr.strip()[:600])
    stats['compiled'] += 1
    if c.get('run') and 'random' not in fl:
        want = c.get('want')
        if want is None:
            print(where, 'run flag but no output block'); fails += 1; continue
        inputs = re.findall(r'\[\[(.*?)\]\]', want)
        stdin = '\n'.join(inputs) + ('\n' if inputs else '')
        expect = re.sub(r'\[\[.*?\]\]\n?', '', want)
        cwd = os.path.join(W, f'run{n}'); shutil.rmtree(cwd, ignore_errors=True); os.makedirs(cwd, exist_ok=True)
        for fname, content in c.get('files', {}).items():
            if 'fresh' not in fl:
                open(os.path.join(cwd, fname), 'w').write(content)
        for fl2 in fl:
            if fl2.startswith('seedfile='):
                name, _, content = fl2[9:].partition(':')
                open(os.path.join(cwd, name), 'w').write(content.replace('\\n', '\n'))
        try:
            rr = subprocess.run([exe], input=stdin, capture_output=True, text=True, timeout=10, cwd=cwd)
        except subprocess.TimeoutExpired:
            print(where, 'TIMEOUT'); fails += 1; continue
        got = rr.stdout
        for fname, wantc in c.get('wantfiles', {}).items():
            fp = os.path.join(cwd, fname)
            gotc = open(fp).read() if os.path.exists(fp) else '<missing>'
            if gotc.rstrip() != wantc.rstrip():
                print(where, 'FILE MISMATCH', fname, '\n--- expected\n' + wantc + '\n--- got\n' + gotc); fails += 1
        if 'random' in fl:
            stats['ran'] += 1; continue
        if got.rstrip() != expect.rstrip():
            print(where, 'OUTPUT MISMATCH\n--- expected\n' + expect + '\n--- got\n' + got); fails += 1
        else:
            stats['ran'] += 1
for g, members in groups.items():
    d = os.path.join(W, 'grp_' + g); shutil.rmtree(d, ignore_errors=True); os.makedirs(d)
    for fname, c, n in members:
        open(os.path.join(d, fname), 'w').write(c['code'] + '\n')
    cpps = [m[0] for m in members if m[0].endswith('.cpp')]
    r = subprocess.run(['g++', '-std=c++17', '-Wall', '-Wextra', *cpps, '-o', 'app'], cwd=d, capture_output=True, text=True)
    if r.returncode != 0 or r.stderr.strip():
        print('[group', g, '] COMPILE', 'FAIL' if r.returncode else 'WARN', r.stderr[:2000]); fails += (r.returncode != 0)
        if r.returncode: continue
    stats['compiled'] += 1
    for fname, c, n in members:
        if not c.get('run'): continue
        for f2, content in c.get('files', {}).items():
            open(os.path.join(d, f2), 'w').write(content)
        want = c.get('want') or ''
        inputs = re.findall(r'\[\[(.*?)\]\]', want)
        stdin = '\n'.join(inputs) + '\n'
        expect = re.sub(r'\[\[.*?\]\]\n?', '', want)
        rr = subprocess.run(['./app'], input=stdin, capture_output=True, text=True, timeout=10, cwd=d)
        if rr.stdout.rstrip() != expect.rstrip():
            print('[group', g, '] OUTPUT MISMATCH\n--- expected\n' + expect + '\n--- got\n' + rr.stdout); fails += 1
        else:
            stats['ran'] += 1
        for fname2, wantc in c.get('wantfiles', {}).items():
            fp = os.path.join(d, fname2)
            gotc = open(fp).read() if os.path.exists(fp) else '<missing>'
            if gotc.rstrip() != wantc.rstrip():
                print('[group', g, '] FILE MISMATCH', fname2, '\n--- expected\n' + wantc + '\n--- got\n' + gotc); fails += 1
print(stats, 'FAILS:', fails)
sys.exit(1 if fails else 0)
