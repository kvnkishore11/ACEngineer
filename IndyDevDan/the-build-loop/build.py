#!/usr/bin/env python3
"""Fill the giving-back shell for THE BUILD LOOP, then inline the chapters."""
import re, pathlib

SKILL = pathlib.Path("/Users/kvnkishore/.claude/skills/giving-back/assets/template.html")
OUT = pathlib.Path(__file__).resolve().parent
s = SKILL.read_text(encoding="utf-8")

s = s.replace("{{TITLE}}", "The Build Loop")
s = s.replace("{{SUBTITLE}}", "IndyDevDan, reverse-engineered")
s = s.replace("{{COVER_KICKER}}", "A field guide · reconstructed from artifacts, not talks")
s = s.replace("{{FOOTER_LINE}}", "12 mining agents · 29 repos · 18 course codebases")
s = s.replace("{{COLOPHON}}",
              "Compiled by Fable from the IndyDevDan corpus — 29 cloned repos with git history, "
              "18 course codebases, 18 lesson transcripts, 52 committed specs. Command and agent "
              "counts are deduplicated by content hash — the raw file counts are inflated ~2x by .upstream/ mirrors. "
              "Every quote verbatim.")
s = s.replace('<div class="mark">G</div>', '<div class="mark">↻</div>')

TOC = '''<nav class="toc" id="toc">
    <a href="#ch00"><span class="n">00</span><span>Cover</span></a>
    <div class="railhint">Part I · What the artifacts show</div>
    <a href="#ch01"><span class="n">01</span><span>The evidence</span></a>
    <div class="railhint">Part II · The procedure</div>
    <a href="#ch02"><span class="n">02</span><span>Day one</span></a>
    <a href="#ch03"><span class="n">03</span><span>The feature loop</span></a>
    <a href="#ch04"><span class="n">04</span><span>When it fails</span></a>
    <a href="#ch05"><span class="n">05</span><span>Escalation</span></a>
    <div class="railhint">Part III · Out of the loop</div>
    <a href="#ch06"><span class="n">06</span><span>The ADW ladder</span></a>
    <a href="#ch07"><span class="n">07</span><span>Teams of agents</span></a>
    <div class="railhint">Part IV · A worked example</div>
    <a href="#ch08"><span class="n">08</span><span>Naming a startup</span></a>
    <a href="#ch09"><span class="n">09</span><span>What the run found</span></a>
    <div class="railhint">∞ · Send-off</div>
    <a href="#ch99"><span class="n">99</span><span>Build for the thousandth run</span></a>
  </nav>'''
s = re.sub(r'<nav class="toc" id="toc">.*?</nav>', TOC, s, flags=re.S)

COVER = '''<section class="chapter dark" id="ch00">
  <div class="wrap">
    <div class="kicker reveal">A field guide · reconstructed from artifacts, not talks</div>
    <h1 class="display reveal d1" style="max-width:15ch">Build the system that <em>builds the system.</em></h1>
    <p class="lede reveal d2" style="max-width:44ch;color:var(--on-dark-dim)">
      What IndyDevDan actually does when he ships a feature — recovered from commit history, source
      files and uncut video rather than from the parts he says out loud. Plus the whole method run
      once, end to end, on a real decision.
    </p>

    <div class="row reveal d3" style="margin-top:34px;gap:10px">
      <span class="pill clay">29 repos</span>
      <span class="pill">61 unique commands</span>
      <span class="pill">18 course codebases</span>
      <span class="pill">10 sections</span>
    </div>

    <div class="fig bare reveal d4" style="margin-top:46px;max-width:600px">
      <svg class="draw" viewBox="0 0 600 118" role="img" aria-label="Paper, planner, hard context break, builder, shipped">
        <rect x="4" y="44" width="74" height="34" rx="8" fill="none" stroke="var(--on-dark-dim)" stroke-width="1.5"/>
        <text x="41" y="65" text-anchor="middle" font-family="var(--mono)" font-size="10.5" fill="#efe7d8">paper</text>
        <path d="M78 61 H 128" stroke="var(--clay-2)" stroke-width="2" fill="none"/>
        <rect x="128" y="44" width="104" height="34" rx="8" fill="none" stroke="var(--blue)" stroke-width="2"/>
        <text x="180" y="65" text-anchor="middle" font-family="var(--mono)" font-size="10.5" fill="var(--on-dark-dim)">planner</text>
        <path d="M258 20 V 102" stroke="var(--clay-2)" stroke-width="2" stroke-dasharray="6 6" fill="none"/>
        <text x="258" y="14" text-anchor="middle" font-family="var(--mono)" font-size="9" fill="var(--on-dark-dim)">fresh agent</text>
        <path d="M232 61 H 250" stroke="var(--clay-2)" stroke-width="2" fill="none"/>
        <path d="M266 61 H 288" stroke="var(--clay-2)" stroke-width="2" fill="none"/>
        <rect x="288" y="44" width="104" height="34" rx="8" fill="none" stroke="var(--olive)" stroke-width="2"/>
        <text x="340" y="65" text-anchor="middle" font-family="var(--mono)" font-size="10.5" fill="var(--on-dark-dim)">builder</text>
        <path d="M392 61 H 442" stroke="var(--clay-2)" stroke-width="2" fill="none"/>
        <rect x="442" y="44" width="90" height="34" rx="8" fill="none" stroke="var(--amber)" stroke-width="2"/>
        <text x="487" y="65" text-anchor="middle" font-family="var(--mono)" font-size="10.5" fill="var(--on-dark-dim)">validate</text>
        <circle cx="562" cy="61" r="13" fill="none" stroke="var(--clay-2)" stroke-width="2"/>
        <path d="M556 61 l5 5 8 -10" stroke="var(--clay-2)" stroke-width="2" fill="none"/>
        <path d="M532 61 H 549" stroke="var(--clay-2)" stroke-width="2" fill="none"/>
      </svg>
    </div>

    <p class="small reveal d5" style="margin-top:40px;font-family:var(--mono);letter-spacing:.06em">
      Scroll, or press <kbd style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.2);color:#efe7d8">J</kbd>
      to begin &nbsp;↓
    </p>
  </div>
</section>'''
s = re.sub(r'<section class="chapter dark" id="ch00">.*?</section>', COVER, s, flags=re.S)

SENDOFF = '''<section class="chapter dark" id="ch99">
  <div class="wrap">
    <span class="chapnum reveal" style="color:var(--on-dark-dim)">— The Send-off</span>
    <div class="kicker reveal">where this leaves you</div>
    <h2 class="title reveal d1" style="max-width:22ch;color:#f6efe2">Build for the thousandth run — <em>after you've done the first ten by hand.</em></h2>
    <p class="lede reveal d2" style="max-width:44ch;color:var(--on-dark-dim)">
      The machinery in this guide is worth building. It is not worth building first. He says so himself,
      repeatedly, in the parts of the video most people skip.
    </p>

    <div class="grid grid-3 reveal" style="margin-top:18px">
      <div class="card glow accent"><span class="cnum">RECAP 01</span><p class="ctitle">Fresh agent, every step</p><p class="cbody">The one rule that survives every contradiction. You cannot debug a polluted window.</p></div>
      <div class="card glow blue"><span class="cnum">RECAP 02</span><p class="ctitle">Fix the system, not the output</p><p class="cbody">Attempts above one is a diagnosis, not a retry. Install the missing lever.</p></div>
      <div class="card glow olive"><span class="cnum">RECAP 03</span><p class="ctitle">Code disposes</p><p class="cbody">Settle mechanically what can be settled mechanically. Send only survivors to a body that argues.</p></div>
    </div>

    <div class="quote big reveal" style="margin:36px 0 8px">
      <p>I could have done all this with a single agent. I fully acknowledge that. This probably isn't the scale.</p>
      <span class="cite" style="display:block;margin-top:14px;color:var(--on-dark-dim)">— him, about his own multi-agent system</span>
    </div>

    <p class="prose reveal" style="max-width:70ch;color:var(--on-dark-dim)">
      He also says <em>"this arrangement of ADWs is completely arbitrary,"</em> and <em>"I haven't seen anyone
      doing zero-touch work yet,"</em> and <em>"many of the ideas I share with you here are experiments."</em>
      Take the loop. Leave the ceremony until it earns its place.
    </p>

    <p class="small reveal" style="margin-top:30px;color:var(--on-dark-dim)">
      Compiled by Fable from the IndyDevDan corpus — 29 cloned repos with git history, 18 course
      codebases, 18 lesson transcripts, 52 committed specs. Command and agent counts are deduplicated by
      content hash; raw file counts are inflated ~2&times; by <code>.upstream/</code> mirrors. Every quote verbatim.<br>
      <span style="font-family:var(--mono);letter-spacing:.06em">Press <kbd style="background:rgba(255,255,255,.06);border-color:rgba(255,255,255,.2);color:#efe7d8">K</kbd> to climb back up ↑</span>
    </p>
    <a class="jump reveal" href="#ch00" style="margin-top:26px">Back to the top &nbsp;↑</a>
  </div>
</section>'''
s = re.sub(r'<section class="chapter dark" id="ch99">.*?</section>', SENDOFF, s, flags=re.S)

(OUT / "template.html").write_text(s, encoding="utf-8")

frags = []
for p in sorted((OUT / "chapters").glob("ch*.html")):
    frags.append("\n" + p.read_text(encoding="utf-8").strip() + "\n")
(OUT / "index.html").write_text(s.replace("<!--__CHAPTERS__-->", "".join(frags)), encoding="utf-8")
print(f"WROTE {OUT/'index.html'} ({len(frags)} sections inlined)")
