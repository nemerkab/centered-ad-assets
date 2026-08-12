#!/usr/bin/env python3
"""Render /start/apply Meta static creatives to PNG via headless Chrome.

Brand tokens from centeredsoftware.com (dark monochrome + Inter).
"""
from __future__ import annotations

import pathlib
import shutil
import subprocess
import sys

ROOT = pathlib.Path(__file__).parent
HTML = ROOT / "html"
OUT = ROOT / "images"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

BG = "#05050a"
TEXT = "#ffffff"
MUTED = "rgba(255,255,255,0.55)"
BORDER = "rgba(255,255,255,0.10)"
SOFT = "rgba(255,255,255,0.08)"

SIZES = {"1x1": (1080, 1080), "4x5": (1080, 1350)}

# layout: "left" = editorial stack, "center" = pitch-style hero
ADS = [
    {
        "slug": "01-weeks-not-months",
        "layout": "center",
        "badge": "Free strategy call",
        "head": ["Ship production-ready", "software in weeks —", "not months."],
        "body": "Tell us about your project. We'll map the fastest path to a live product — or tell you if we're not a fit.",
        "cta": "Apply for a free strategy call →",
    },
    {
        "slug": "02-vibe-to-production",
        "layout": "left",
        "badge": "For founders who built it themselves",
        "head": ["Vibe-coded", "MVP.", "Production", "next."],
        "body": "You got early traction with Cursor, Replit, or Lovable. We'll harden it for real users — without throwing away your progress.",
        "cta": "Apply →",
    },
    {
        "slug": "03-free-strategy-call",
        "layout": "center",
        "badge": "No pressure. No pitch deck theater.",
        "head": ["Free strategy", "call. Real", "answers."],
        "body": "Talk with the person who'd actually lead your build — not a salesperson reading a script.",
        "cta": "Apply for a free strategy call →",
    },
    {
        "slug": "04-honest-fit",
        "layout": "left",
        "badge": "Free strategy call",
        "head": ["We'll tell", "you if", "we're not", "a fit."],
        "body": "Most agencies say yes to everything. We'll show you the fastest path to production — or point you somewhere better.",
        "cta": "Apply →",
    },
    {
        "slug": "05-senior-machine-speed",
        "layout": "left",
        "badge": "Senior-led / AI-accelerated",
        "head": ["Senior", "judgment.", "Machine", "speed."],
        "body": "AI writes code fast. It doesn't know what to build. We bring the judgment that decides — and ships production-ready software in weeks.",
        "cta": "Apply →",
    },
    {
        "slug": "06-idea-to-live",
        "layout": "center",
        "badge": "Client outcome",
        "head": ["Idea to live", "product in", "2–8 weeks."],
        "body": "Not a prototype stuck in staging. A deployed, user-ready product — scoped ruthlessly and built to last.",
        "cta": "Apply for a free strategy call →",
    },
    {
        "slug": "07-zero-drag",
        "layout": "left",
        "badge": "AI-native software agency",
        "head": ["Zero", "agency", "drag."],
        "body": "No status-meeting theater. No junior handoffs. Senior engineers shipping production software in weeks.",
        "cta": "Apply →",
    },
    {
        "slug": "08-come-with-problem",
        "layout": "center",
        "badge": "You don't need a perfect spec",
        "head": ["Come with", "your problem.", "Not a brief."],
        "body": "On a free strategy call we'll figure out what to build now vs later — then the fastest honest path to production.",
        "cta": "Apply for a free strategy call →",
    },
    {
        "slug": "09-one-team",
        "layout": "left",
        "badge": "Strategy · Design · Engineering",
        "head": ["One team.", "No vendor", "ping-pong."],
        "body": "Strategy, UI, and engineering together. No coordinating three vendors. No handoffs to juniors.",
        "cta": "Apply →",
    },
    {
        "slug": "10-launch-sprint",
        "layout": "center",
        "badge": "Launch Sprint",
        "head": ["Scoped. Built.", "Deployed", "in weeks."],
        "body": "MVP, internal tool, automation, or high-value milestone — then a clear post-launch roadmap if you want to keep shipping.",
        "cta": "Apply for a free strategy call →",
    },
    # --- Vibe-code takeover angles ---
    {
        "slug": "11-we-take-it-from-here",
        "layout": "center",
        "badge": "Vibe-coded → production-ready",
        "head": ["You built it.", "We'll take it", "from here."],
        "body": "Hand us the Cursor / Replit / Lovable MVP. Senior engineers harden it for real users — auth, infra, reliability — without a rewrite.",
        "cta": "Apply for a free strategy call →",
    },
    {
        "slug": "12-keep-what-works",
        "layout": "left",
        "badge": "No throwaway rebuilds",
        "head": ["Keep what", "works.", "Fix what", "won't."],
        "body": "We don't scrap your vibe-coded progress. We audit, harden, and ship a production foundation you can grow on.",
        "cta": "Apply →",
    },
    {
        "slug": "13-before-it-breaks",
        "layout": "center",
        "badge": "For founders with early users",
        "head": ["Harden it", "before real", "customers", "depend on it."],
        "body": "Tech debt, security gaps, fragile demos — we turn vibe-coded software into something that won't buckle under real traffic.",
        "cta": "Apply for a free strategy call →",
    },
    {
        "slug": "14-traction-needs-engineers",
        "layout": "left",
        "badge": "Early traction. Fragile code.",
        "head": ["Traction", "without", "engineering", "is a trap."],
        "body": "Users showed up. Your vibe-coded MVP is sweating. Bring in senior engineers to make it production-ready — and keep shipping.",
        "cta": "Apply →",
    },
    {
        "slug": "15-vibe-code-ceiling",
        "layout": "center",
        "badge": "Cursor · Replit · Lovable",
        "head": ["Vibe code", "got you here.", "Pros get you", "to production."],
        "body": "AI tools ship demos fast. Production needs judgment, infrastructure, and a team that owns the outcome. That's us.",
        "cta": "Apply for a free strategy call →",
    },
]

SCALE = {
    "1x1": dict(
        pad=72, inset=36, badge=22, hs=92, gap=28, bs=28, bw=860,
        fgap=40, fpad=28, logo=34, cta=24, pill_y=18, pill_x=28,
    ),
    "4x5": dict(
        pad=80, inset=40, badge=24, hs=104, gap=34, bs=30, bw=880,
        fgap=52, fpad=32, logo=36, cta=26, pill_y=20, pill_x=32,
    ),
}


def head_html(lines: list[str], layout: str) -> str:
    out = []
    for i, ln in enumerate(lines):
        # last line gets the brand gradient treatment
        if i == len(lines) - 1:
            out.append(f'<span class="grad">{ln}</span>')
        else:
            out.append(f"<span>{ln}</span>")
    return "".join(out)


def render_html(ad: dict, key: str, w: int, h: int) -> str:
    s = SCALE[key]
    layout = ad["layout"]
    align = "center" if layout == "center" else "flex-start"
    text_align = "center" if layout == "center" else "left"
    body_mx = "auto" if layout == "center" else "0"
    footer_justify = "center" if layout == "center" else "space-between"
    footer_gap = "28px" if layout == "center" else "0"

    # slightly tighter headline on longer lines for center layouts
    hs = s["hs"]
    if layout == "center" and max(len(x) for x in ad["head"]) > 18:
        hs = int(hs * 0.88)

    return f"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800;900&display=swap" rel="stylesheet">
<style>
* {{ margin:0; padding:0; box-sizing:border-box; }}
html, body {{ width:{w}px; height:{h}px; }}
body {{
  background:
    radial-gradient(ellipse 70% 55% at 50% -10%, rgba(255,255,255,0.10), transparent 55%),
    radial-gradient(circle at 88% 72%, rgba(255,255,255,0.04), transparent 38%),
    radial-gradient(circle at 8% 85%, rgba(16,185,129,0.08), transparent 36%),
    {BG};
  font-family: "Inter", ui-sans-serif, system-ui, -apple-system, sans-serif;
  color: {TEXT};
  display: flex;
  flex-direction: column;
  align-items: {align};
  justify-content: space-between;
  padding: {s['pad']}px;
  position: relative;
  overflow: hidden;
  -webkit-font-smoothing: antialiased;
}}
.dots {{
  position: absolute;
  inset: 0;
  background-image: radial-gradient(rgba(255,255,255,0.11) 1px, transparent 1px);
  background-size: 28px 28px;
  mask-image: radial-gradient(ellipse 70% 55% at 50% 20%, #000 10%, transparent 70%);
  -webkit-mask-image: radial-gradient(ellipse 70% 55% at 50% 20%, #000 10%, transparent 70%);
  pointer-events: none;
  opacity: 0.55;
}}
.frame {{
  position: absolute;
  inset: {s['inset']}px;
  border: 1px solid {BORDER};
  border-radius: 28px;
  pointer-events: none;
}}
.content {{
  position: relative;
  z-index: 1;
  width: 100%;
  display: flex;
  flex-direction: column;
  align-items: {align};
  text-align: {text_align};
  margin-top: auto;
  margin-bottom: auto;
}}
.badge {{
  display: inline-flex;
  align-items: center;
  gap: 12px;
  border: 1px solid {BORDER};
  background: {SOFT};
  color: {TEXT};
  font-size: {s['badge']}px;
  font-weight: 700;
  letter-spacing: 0.16em;
  text-transform: uppercase;
  padding: 12px 22px;
  border-radius: 999px;
  margin-bottom: {s['gap'] + 8}px;
}}
.badge .dot {{
  width: 10px; height: 10px; border-radius: 50%;
  background: {TEXT};
  box-shadow: 0 0 12px rgba(255,255,255,0.55);
  flex-shrink: 0;
}}
h1 {{
  font-size: {hs}px;
  line-height: 0.98;
  font-weight: 800;
  letter-spacing: -0.04em;
  margin: 0 0 {s['gap']}px 0;
}}
h1 span {{ display: block; }}
h1 .grad {{
  background: linear-gradient(135deg, #ffffff 0%, #a3a3a3 60%, #525252 100%);
  -webkit-background-clip: text;
  background-clip: text;
  color: transparent;
}}
p {{
  font-size: {s['bs']}px;
  line-height: 1.4;
  color: {MUTED};
  font-weight: 500;
  max-width: {s['bw']}px;
  margin: 0 {body_mx};
}}
.cta {{
  display: inline-flex;
  align-items: center;
  margin-top: {s['gap'] + 12}px;
  background: linear-gradient(135deg, #ffffff 0%, #e5e5e5 55%, #a3a3a3 100%);
  color: {BG};
  font-size: {s['cta']}px;
  font-weight: 700;
  letter-spacing: -0.01em;
  padding: {s['pill_y']}px {s['pill_x']}px;
  border-radius: 999px;
  box-shadow: 0 18px 50px rgba(0,0,0,0.45);
}}
footer {{
  position: relative;
  z-index: 1;
  width: 100%;
  margin-top: {s['fgap']}px;
  padding-top: {s['fpad']}px;
  border-top: 1px solid {BORDER};
  display: flex;
  align-items: center;
  justify-content: {footer_justify};
  gap: {footer_gap};
}}
.logo {{
  display: flex;
  flex-direction: column;
  align-items: {'center' if layout == 'center' else 'flex-start'};
  gap: 2px;
  line-height: 1;
}}
.logo .word {{
  font-size: {s['logo']}px;
  font-weight: 800;
  letter-spacing: -0.03em;
  color: {TEXT};
}}
.logo .sub {{
  font-size: {max(12, s['logo'] // 2 - 2)}px;
  font-weight: 600;
  letter-spacing: 0.22em;
  text-transform: uppercase;
  color: {MUTED};
}}
.url {{
  font-size: {max(18, s['cta'] - 4)}px;
  font-weight: 500;
  color: {MUTED};
  letter-spacing: 0.02em;
}}
.url strong {{ color: {TEXT}; font-weight: 600; }}
</style>
</head>
<body>
  <div class="dots"></div>
  <div class="frame"></div>
  <div class="content">
    <div class="badge"><span class="dot"></span>{ad['badge']}</div>
    <h1>{head_html(ad['head'], layout)}</h1>
    <p>{ad['body']}</p>
    <div class="cta">{ad['cta']}</div>
  </div>
  <footer>
    <div class="logo">
      <span class="word">centered</span>
      <span class="sub">Software</span>
    </div>
    {"<div class='url'><strong>/start/apply</strong></div>" if layout == "left" else ""}
  </footer>
</body>
</html>"""


def main() -> None:
    if not pathlib.Path(CHROME).exists():
        sys.exit(f"Chrome not found at {CHROME}")

    for d in (HTML, OUT):
        shutil.rmtree(d, ignore_errors=True)
        d.mkdir(parents=True)

    jobs = []
    for ad in ADS:
        for key, (w, h) in SIZES.items():
            name = f"{ad['slug']}-{key}"
            path = HTML / f"{name}.html"
            path.write_text(render_html(ad, key, w, h), encoding="utf-8")
            jobs.append((name, path, w, h))

    for name, path, w, h in jobs:
        png = OUT / f"{name}.png"
        subprocess.run(
            [
                CHROME,
                "--headless=new",
                "--disable-gpu",
                "--hide-scrollbars",
                "--force-device-scale-factor=1",
                f"--window-size={w},{h}",
                f"--screenshot={png}",
                path.as_uri(),
            ],
            check=True,
            capture_output=True,
        )
        print(f"  {png.name}  {png.stat().st_size // 1024} KB")

    print(f"\n{len(jobs)} images → {OUT}")


if __name__ == "__main__":
    main()
