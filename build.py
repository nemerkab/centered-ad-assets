#!/usr/bin/env python3
"""Render Centered Software static ad creative to PNG via headless Chrome.

Brand tokens lifted directly from centeredsoftware.com stylesheets.
"""
import subprocess, pathlib, shutil, sys

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / "build"
OUT = ROOT / "images"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BG = "#05050a"
SURFACE = "#0c0c13"
TEXT = "#ffffff"
MUTED = "#ffffff8c"
BORDER = "#ffffff1a"
ACCENT = "#10b981"

SIZES = {"1x1": (1080, 1080), "4x5": (1080, 1350)}

ADS = [
    {
        "slug": "zero-agency-drag",
        "kicker": "AI-NATIVE SOFTWARE AGENCY",
        "head": ["Zero", "agency", "drag."],
        "body": "No discovery phase. No account managers. Senior engineers shipping production software in weeks.",
    },
    {
        "slug": "senior-judgment",
        "kicker": "SENIOR-LED / AI-ACCELERATED",
        "head": ["Senior", "judgment.", "Machine", "speed."],
        "body": "AI writes code fast. It doesn't know what to build. We bring the judgment that decides.",
    },
    {
        "slug": "honest-call",
        "kicker": "FREE STRATEGY CALL",
        "head": ["We'll tell", "you if", "we're not", "a fit."],
        "body": "Most agencies say yes to everything. We'll show you the fastest path to production — or point you somewhere better.",
    },
    {
        "slug": "sentence-to-shipped",
        "kicker": "MVP LAUNCH SPRINTS",
        "head": ["From a", "sentence", "to shipped."],
        "body": "Your idea is one line today. In weeks it's a live product learning from real users.",
    },
]

TPL = """<!doctype html><html><head><meta charset="utf-8"><style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html,body {{ width:{w}px; height:{h}px; }}
body {{
  background:
    radial-gradient(circle at 12% 8%, #ffffff14, transparent 46%),
    radial-gradient(circle at 88% 28%, #ffffff0d, transparent 40%),
    radial-gradient(circle at 30% 88%, {accent}1a, transparent 42%),
    {bg};
  font-family: -apple-system, BlinkMacSystemFont, "SF Pro Display", system-ui, sans-serif;
  color:{text};
  display:flex; flex-direction:column;
  padding:{pad}px;
  position:relative; overflow:hidden;
}}
.frame {{
  position:absolute; inset:{inset}px;
  border:1px solid {border}; border-radius:24px; pointer-events:none;
}}
.kicker {{
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size:{kick}px; letter-spacing:0.18em; color:{accent};
  font-weight:600; margin-bottom:auto;
}}
h1 {{
  font-size:{hs}px; line-height:0.94; font-weight:900;
  letter-spacing:-0.035em; margin:0 0 {gap}px 0;
}}
h1 span {{ display:block; }}
h1 .dim {{ color:{muted}; }}
p {{
  font-size:{bs}px; line-height:1.45; color:{muted};
  font-weight:500; max-width:{bw}px;
}}
footer {{
  margin-top:{fgap}px; padding-top:{fpad}px; border-top:1px solid {border};
  display:flex; align-items:center; justify-content:space-between;
  font-family: ui-monospace, SFMono-Regular, Menlo, monospace;
  font-size:{fs}px; color:{muted}; letter-spacing:0.04em;
}}
.dot {{
  display:inline-block; width:{dot}px; height:{dot}px; border-radius:50%;
  background:{accent}; margin-right:{dotgap}px; vertical-align:middle;
  box-shadow:0 0 {glow}px {accent};
}}
.cta {{ color:{text}; font-weight:600; }}
</style></head><body>
<div class="frame"></div>
<div class="kicker">{kicker}</div>
<h1>{head}</h1>
<p>{body}</p>
<footer>
  <span><span class="dot"></span>centeredsoftware.com</span>
  <span class="cta">Apply &rarr;</span>
</footer>
</body></html>"""

# per-size typographic scale
SCALE = {
    "1x1": dict(pad=88, inset=40, kick=21, hs=118, gap=34, bs=29, bw=880,
                fgap=48, fpad=30, fs=21, dot=11, dotgap=13, glow=14),
    "4x5": dict(pad=92, inset=42, kick=22, hs=132, gap=40, bs=31, bw=890,
                fgap=64, fpad=32, fs=22, dot=12, dotgap=14, glow=16),
}


def head_html(lines):
    # last line dimmed for typographic rhythm
    out = []
    for i, ln in enumerate(lines):
        cls = ' class="dim"' if i == len(lines) - 1 and len(lines) > 2 else ""
        out.append(f"<span{cls}>{ln}</span>")
    return "".join(out)


def main():
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")
    for d in (HTML, OUT):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)

    jobs = []
    for ad in ADS:
        for key, (w, h) in SIZES.items():
            s = SCALE[key]
            html = TPL.format(
                w=w, h=h, bg=BG, text=TEXT, muted=MUTED, border=BORDER,
                accent=ACCENT, surface=SURFACE,
                kicker=ad["kicker"], head=head_html(ad["head"]), body=ad["body"],
                **s,
            )
            name = f"{ad['slug']}-{key}"
            p = HTML / f"{name}.html"
            p.write_text(html)
            jobs.append((name, p, w, h))

    for name, path, w, h in jobs:
        png = OUT / f"{name}.png"
        subprocess.run([
            CHROME, "--headless", "--disable-gpu", "--hide-scrollbars",
            "--force-device-scale-factor=1",
            f"--window-size={w},{h}",
            f"--screenshot={png}",
            path.as_uri(),
        ], check=True, capture_output=True)
        print(f"  {png.name}  {png.stat().st_size // 1024} KB")

    print(f"\n{len(jobs)} images -> {OUT}")


if __name__ == "__main__":
    main()
