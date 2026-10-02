"""Generates assets/header-light.svg and assets/header-dark.svg.

Same palette as hilokeshrm.github.io: paper/ink plate, one accent, five domain colours.
Run from the repo root:  python tools/make_header.py
"""
import math
from pathlib import Path

W, H = 1200, 470

THEMES = {
    "light": dict(paper="#F4F3EF", ink="#141412", ink2="rgba(20,20,18,.62)", ink3="rgba(20,20,18,.40)",
                  line="rgba(20,20,18,.12)", line2="rgba(20,20,18,.24)", accent="#8B2E2E",
                  ai="#2F5D8A", vision="#C2553A", robot="#3E6B4A", iot="#B8892A", web="#8B2E2E"),
    "dark": dict(paper="#0A0A0A", ink="#F2F2ED", ink2="rgba(242,242,237,.64)", ink3="rgba(242,242,237,.40)",
                 line="rgba(242,242,237,.10)", line2="rgba(242,242,237,.24)", accent="#C4463F",
                 ai="#6F9FD0", vision="#E07A5F", robot="#7DB58C", iot="#E2B84A", web="#C4463F"),
}

SERIF = "Fraunces, 'Iowan Old Style', Georgia, 'Times New Roman', serif"
MONO = "'DM Mono', ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"

CX, CY = 905, 215


def ring(k, steps=180):
    """One closed contour: a wobbly ellipse that grows with k."""
    r = 16 + k * 19
    pts = []
    for i in range(steps):
        t = 2 * math.pi * i / steps
        m = (1 + 0.13 * math.sin(3 * t + k * 0.28) + 0.07 * math.sin(5 * t - k * 0.45)
             + 0.04 * math.cos(7 * t + k * 0.9))
        pts.append((CX + 1.38 * r * m * math.cos(t), CY + 0.92 * r * m * math.sin(t)))
    d = "M" + " L".join(f"{x:.1f},{y:.1f}" for x, y in pts) + " Z"
    return d


def point_on(k, t):
    r = 16 + k * 19
    m = (1 + 0.13 * math.sin(3 * t + k * 0.28) + 0.07 * math.sin(5 * t - k * 0.45)
         + 0.04 * math.cos(7 * t + k * 0.9))
    return CX + 1.38 * r * m * math.cos(t), CY + 0.92 * r * m * math.sin(t)


def build(c):
    o = []
    o.append(f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" '
             f'role="img" aria-label="Lokesh R M. I build intelligent machines and the software around them.">')
    o.append(f"""<style>
  .serif{{font-family:{SERIF}}} .mono{{font-family:{MONO};letter-spacing:.12em;text-transform:uppercase}}
  .c{{fill:none;stroke:{c['line2']};stroke-width:1;stroke-dasharray:1;stroke-dashoffset:1;animation:draw 2.4s cubic-bezier(.2,.6,.2,1) forwards}}
  .c.idx{{stroke:{c['ink3']};stroke-width:1.4}}
  @keyframes draw{{to{{stroke-dashoffset:0}}}}
  .fade{{opacity:0;animation:fade .9s ease forwards}}
  @keyframes fade{{to{{opacity:1}}}}
  .pulse{{animation:pulse 1.8s ease-in-out infinite;transform-origin:center;transform-box:fill-box}}
  @keyframes pulse{{0%,100%{{opacity:1;transform:scale(1)}}50%{{opacity:.35;transform:scale(.6)}}}}
  .caret{{animation:blink 1.1s steps(1) infinite}}
  @keyframes blink{{50%{{opacity:0}}}}
  @media (prefers-reduced-motion:reduce){{.c{{animation:none;stroke-dashoffset:0}}.fade{{animation:none;opacity:1}}.pulse,.caret{{animation:none}}}}
</style>""")
    o.append(f'<rect width="{W}" height="{H}" fill="{c["paper"]}"/>')
    o.append('<defs><clipPath id="plate"><rect x="24" y="56" width="1152" height="300"/></clipPath>'
             '<pattern id="grid" width="24" height="24" patternUnits="userSpaceOnUse">'
             f'<path d="M24 0H0V24" fill="none" stroke="{c["line"]}" stroke-width=".6"/></pattern></defs>')

    # plate frame + grid
    o.append(f'<rect x="24" y="56" width="1152" height="300" fill="url(#grid)" opacity=".55"/>')
    o.append(f'<rect x="24.5" y="24.5" width="1151" height="421" fill="none" stroke="{c["line2"]}"/>')
    o.append(f'<path d="M24 56.5H1176M24 356.5H1176" stroke="{c["line2"]}"/>')
    for x, y in [(24, 24), (1176, 24), (24, 446), (1176, 446)]:
        o.append(f'<path d="M{x-9} {y}H{x+9}M{x} {y-9}V{y+9}" stroke="{c["ink"]}" stroke-width="1.2"/>')

    # title block strip
    o.append(f'<text x="44" y="45" class="mono" font-size="11" fill="{c["ink2"]}">Plate 01 — github.com/hilokeshrm</text>')
    o.append(f'<text x="1156" y="45" class="mono" font-size="11" fill="{c["ink2"]}" text-anchor="end">'
             f'Bengaluru · 12.97° N 77.59° E · IST</text>')

    # contours
    o.append('<g clip-path="url(#plate)">')
    for k in range(1, 18):
        cls = "c idx" if k % 5 == 0 else "c"
        o.append(f'<path class="{cls}" pathLength="1" style="animation-delay:{0.05 * k:.2f}s" d="{ring(k)}"/>')
    o.append(f'<circle cx="{CX}" cy="{CY}" r="2.5" fill="{c["ink"]}"/>')
    # keep the name readable where contours run behind it
    o.append(f'<linearGradient id="veil" x1="0" x2="1"><stop offset="0" stop-color="{c["paper"]}" stop-opacity=".92"/>'
             f'<stop offset=".7" stop-color="{c["paper"]}" stop-opacity=".6"/>'
             f'<stop offset="1" stop-color="{c["paper"]}" stop-opacity="0"/></linearGradient>'
             f'<rect x="24" y="57" width="660" height="299" fill="url(#veil)"/>')
    o.append('</g>')

    # spec callouts pinned to contours
    callouts = [
        (6, -2.45, 655, 104, "80+ robots · one GPU", c["robot"], "start"),
        (9, -0.55, 1150, 92, "~60 ms voice loop", c["vision"], "end"),
        (8, 0.75, 1150, 330, "UK · IN clients", c["ai"], "end"),
    ]
    for i, (k, t, lx, ly, label, col, anchor) in enumerate(callouts):
        px, py = point_on(k, t)
        ex = lx + (-8 if anchor == "end" else 8) * 0
        d = 1.6 + i * 0.25
        o.append(f'<g class="fade" style="animation-delay:{d:.2f}s">'
                 f'<path d="M{px:.1f} {py:.1f}L{ex:.1f} {ly + 6}" stroke="{c["ink3"]}" stroke-width="1" fill="none"/>'
                 f'<circle cx="{px:.1f}" cy="{py:.1f}" r="4.5" fill="{c["paper"]}" stroke="{col}" stroke-width="2"/>'
                 f'<rect x="{lx - (len(label) * 8.6 + 20) if anchor == "end" else lx}" y="{ly - 12}" '
                 f'width="{len(label) * 8.6 + 20}" height="24" fill="{c["paper"]}" stroke="{c["line2"]}"/>'
                 f'<text x="{lx - 10 if anchor == "end" else lx + 10}" y="{ly + 4}" class="mono" font-size="11.5" '
                 f'fill="{c["ink"]}" text-anchor="{anchor}">{label}</text></g>')

    # left: status, name, line
    o.append(f'<g class="fade" style="animation-delay:.2s">'
             f'<rect x="56" y="92" width="232" height="26" rx="13" fill="{c["paper"]}" stroke="{c["line2"]}"/>'
             f'<circle class="pulse" cx="74" cy="105" r="4.5" fill="{c["robot"]}"/>'
             f'<text x="88" y="109" class="mono" font-size="11" fill="{c["ink"]}">Taking new projects</text></g>')
    o.append(f'<text x="52" y="210" class="serif fade" style="animation-delay:.35s" font-size="96" '
             f'letter-spacing="-2" fill="{c["ink"]}">Lokesh R M<tspan fill="{c["accent"]}">.</tspan></text>')
    o.append(f'<text x="56" y="262" class="serif fade" style="animation-delay:.55s" font-size="27" font-style="italic" '
             f'fill="{c["ink2"]}">I build intelligent machines</text>')
    o.append(f'<text x="56" y="298" class="serif fade" style="animation-delay:.65s" font-size="27" font-style="italic" '
             f'fill="{c["ink2"]}">and the software around them<tspan class="caret" fill="{c["accent"]}" font-style="normal">_</tspan></text>')
    o.append(f'<text x="56" y="336" class="mono fade" style="animation-delay:.8s" font-size="11" fill="{c["ink3"]}">'
             f'AI Engineer, Sirena Technologies  /  Founder, ANVE</text>')

    # domain index
    domains = [("01", "Agents & LLMs", c["ai"]), ("02", "Vision & voice", c["vision"]),
               ("03", "Robotics · ROS 2", c["robot"]), ("04", "IoT & edge", c["iot"]),
               ("05", "Full stack", c["web"])]
    col_w = 1152 / 5
    for i, (n, name, col) in enumerate(domains):
        x0 = 24 + i * col_w
        if i:
            o.append(f'<path d="M{x0:.1f} 356V446" stroke="{c["line2"]}"/>')
        o.append(f'<g class="fade" style="animation-delay:{1.0 + i * 0.12:.2f}s">'
                 f'<rect x="{x0 + 20:.1f}" y="378" width="28" height="4" fill="{col}"/>'
                 f'<text x="{x0 + 20:.1f}" y="404" class="mono" font-size="10.5" fill="{c["ink3"]}">{n}</text>'
                 f'<text x="{x0 + 20:.1f}" y="428" class="serif" font-size="19" fill="{c["ink"]}">{name.replace("&", "&amp;")}</text></g>')

    o.append("</svg>")
    return "\n".join(o)


if __name__ == "__main__":
    out = Path(__file__).resolve().parent.parent / "assets"
    out.mkdir(exist_ok=True)
    for name, c in THEMES.items():
        (out / f"header-{name}.svg").write_text(build(c), encoding="utf-8")
    print("wrote", *sorted(p.name for p in out.glob("header-*.svg")))
