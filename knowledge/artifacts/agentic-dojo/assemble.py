#!/usr/bin/env python3
"""Inline chapters/chNN.html fragments into template.html at <!--__CHAPTERS__--> → index.html.
Usage: python3 assemble.py <output-dir>   (dir must contain template.html and chapters/)"""
import sys, re, pathlib
base = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.')
shell = (base / 'template.html').read_text(encoding='utf-8')
frags = []
for p in sorted((base / 'chapters').glob('ch*.html')):
    html = p.read_text(encoding='utf-8').strip()
    html = re.sub(r'^```[a-zA-Z]*\n', '', html); html = re.sub(r'\n```$', '', html)
    frags.append('\n' + html + '\n')
out = base / 'index.html'
out.write_text(shell.replace('<!--__CHAPTERS__-->', ''.join(frags)), encoding='utf-8')
print(f'WROTE {out}  ({len(frags)} sections inlined)')
